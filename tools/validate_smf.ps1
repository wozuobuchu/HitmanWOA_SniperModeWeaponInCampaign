param(
    [string]$GamePath = 'D:\SteamLibrary\steamapps\common\HITMAN 3'
)
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$validationRoot = [IO.Path]::GetFullPath((Join-Path $workspace 'build\smf-validation'))
if (-not $validationRoot.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar)) {
    throw 'Validation directory must be inside the workspace.'
}
$sourceSmf = Join-Path $GamePath 'Simple Mod Framework'
$testSmf = Join-Path $validationRoot 'SMF'
$testRuntime = Join-Path $validationRoot 'Runtime'
$testRetail = Join-Path $validationRoot 'Retail'
$baseline = Join-Path $validationRoot 'baseline\chunk0'
foreach ($dir in @($testSmf, $testRuntime, $testRetail, $baseline, (Join-Path $validationRoot 'tmp'))) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# SMF removes existing patch200-300 even with outputToSeparateDirectory=true.
# Both runtimePath AND retailPath therefore point to workspace-only fixtures.
# Copy only the original resources needed by these patches, never link the live Runtime.
$inputs = @(
    'research\vanilla\chunk0\JSON\0040B1B857627936.JSON',
    'research\vanilla\chunk0patch2\JSON\00E2C98879D3238A.JSON',
    'research\vanilla\chunk0patch4\JSON\00595CD49B4ACA64.JSON',
    'research\extracted\chunk0patch4\JSON\007F1E69F079CD50.JSON',
    'research\vanilla\chunk0patch4\ORES\00858D45F5F9E3CA.ORES',
    'research\vanilla\chunk0patch4\LOCR\00F5817876E691F1.LOCR'
)
foreach ($relative in $inputs) {
    $source = Join-Path $workspace $relative
    Copy-Item -LiteralPath $source -Destination $baseline -Force
    Copy-Item -LiteralPath ($source + '.meta') -Destination $baseline -Force
}
Copy-Item -LiteralPath (Join-Path $sourceSmf 'Deploy.exe') -Destination $testSmf -Force
Copy-Item -LiteralPath (Join-Path $sourceSmf 'Third-Party') -Destination $testSmf -Recurse -Force
foreach ($file in @('cleanPackageDefinition.txt', 'cleanThumbs.dat', 'cleanMicrosoftThumbs.dat')) {
    Copy-Item -LiteralPath (Join-Path $sourceSmf $file) -Destination $testSmf -Force
}
Copy-Item -LiteralPath (Join-Path $sourceSmf 'cleanPackageDefinition.txt') -Destination (Join-Path $testRuntime 'packagedefinition.txt') -Force
Copy-Item -LiteralPath (Join-Path $GamePath 'Retail\HITMAN3.exe') -Destination $testRetail -Force
Copy-Item -LiteralPath (Join-Path $sourceSmf 'cleanThumbs.dat') -Destination (Join-Path $testRetail 'thumbs.dat') -Force
$mods = Join-Path $testSmf 'Mods'
New-Item -ItemType Directory -Force -Path $mods | Out-Null
$testMod = [IO.Path]::GetFullPath((Join-Path $mods 'Extra Loadout Slots - Sniper Trio'))
if (-not $testMod.StartsWith($validationRoot + [IO.Path]::DirectorySeparatorChar)) {
    throw 'Refusing to clean a validation mod outside the workspace fixture.'
}
if (Test-Path -LiteralPath $testMod) {
    if ((Get-Item -LiteralPath $testMod).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw 'Validation mod directory must not be a junction or symlink.'
    }
    Remove-Item -LiteralPath $testMod -Recurse -Force
}
Copy-Item -LiteralPath (Join-Path $workspace 'mod\Extra Loadout Slots - Sniper Trio') -Destination $mods -Recurse -Force
$config = @{
    runtimePath = $testRuntime
    retailPath = $testRetail
    skipIntro = $false
    outputToSeparateDirectory = $true
    loadOrder = @('enjoy.ExtraLoadoutSniperTrio')
    modOptions = @{}
    outputConfigToAppDataOnDeploy = $false
    developerMode = $false
    reportErrors = $false
}
$config | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath (Join-Path $testSmf 'config.json') -Encoding utf8NoBOM
$env:TEMP = Join-Path $validationRoot 'tmp'
$env:TMP = $env:TEMP
& (Join-Path $sourceSmf 'Third-Party\rpkg-cli.exe') -generate_rpkg_from $baseline -output_path $testRuntime *> (Join-Path $validationRoot 'baseline-generation.log')
if ($LASTEXITCODE -ne 0) { throw 'RPKG fixture generation failed.' }
Push-Location -LiteralPath $testSmf
try {
    & '.\Deploy.exe' --doNotPause --useConsoleLogging *> (Join-Path $validationRoot 'console.log')
    $deployExit = $LASTEXITCODE
} finally { Pop-Location }
Get-Content -LiteralPath (Join-Path $validationRoot 'console.log') -Tail 25
if ($deployExit -ne 0) { throw "SMF exited with $deployExit" }
if (-not (Test-Path -LiteralPath (Join-Path $testSmf 'Output\chunk0patch300.rpkg'))) {
    throw 'SMF did not create the validation RPKG.'
}
Write-Output "SMF output: $testSmf\Output"
$manifest = Get-Content -LiteralPath (Join-Path $testMod 'manifest.json') -Raw | ConvertFrom-Json
$roundtrip = Join-Path $workspace ('build\roundtrip-' + $manifest.version)
$rpkg = Join-Path $testSmf 'Third-Party\rpkg-cli.exe'
& $rpkg -extract_from_rpkg (Join-Path $testSmf 'Output\chunk0patch300.rpkg') -output_path $roundtrip *> (Join-Path $validationRoot 'roundtrip.log')
& (Join-Path $testSmf 'Third-Party\OREStool.exe') (Join-Path $roundtrip 'chunk0patch300\ORES\00858D45F5F9E3CA.ORES') *> (Join-Path $validationRoot 'ores-roundtrip.log')
& $rpkg -hash_meta_to_json (Join-Path $roundtrip 'chunk0patch300\LOCR\00F5817876E691F1.LOCR.meta') *> (Join-Path $validationRoot 'locr-meta.log')
& (Join-Path $testSmf 'Third-Party\HMLanguageTools.exe') convert H3 LOCR (Join-Path $roundtrip 'chunk0patch300\LOCR\00F5817876E691F1.LOCR') (Join-Path $roundtrip 'localisation.json') *> (Join-Path $validationRoot 'locr-roundtrip.log')
if ($LASTEXITCODE -ne 0) { throw 'Localisation roundtrip failed.' }
