# Extra Loadout Slots — Sniper Trio

适用于《HITMAN World of Assassination／杀手：暗杀世界》的 Simple Mod Framework（SMF）Mod。基于 **grappigegovert** 的 [Extra Loadout Slots 2.1.0](https://www.nexusmods.com/hitman3/mods/724) 制作，保留额外物品栏、移除物品及 `P` 调整数量的功能，并让三把狙击手模式武器可以通过手提箱或大型机构藏匿点带入故事任务。

**首个发布版：2.1.2，已通过使用者实机验证。**

## 下载与功能

直接下载 [2.1.2 安装包](dist/Extra.Loadout.Slots.Sniper.Trio-2.1.2.zip)，通过 SMF 安装即可；仅使用 Mod 不需要 Python、开发工具或原版 Mod 安装包。

新增的物品分类叫 **“狙击模式”**，英文为 **“Sniper Assassin”**。其中包含：

| 来源地图 | 武器 | 简体中文菜单条目 |
| --- | --- | --- |
| Himmelstein | Sieger 300 Ghost／席格 300 幽灵 | Sieger 300 幽灵 [狙击模式·Himmelstein] |
| Hantu Port | Druzhina 34 ICA／ICA 亲卫兵 34 | ICA 亲卫兵 34 [狙击模式·Hantu Port] |
| Siberia／西伯利亚 | Druzhina 34 ICA Arctic／ICA 亲卫兵 34 北极型 | ICA 亲卫兵 34 北极型 [狙击模式·西伯利亚] |

三把枪引用游戏已有的狙击手模式版本，保留普通、穿墙和震荡弹匣及弹药切换功能。每个手提箱仍装一把枪；三把枪会同时出现在选择列表中，供你选择。原有“狙击枪”等分类继续保留，故事模式奖励枪的定义也不变。本改版没有新增无限弹药、满级精通或地图解锁功能。

## 首次安装

### 1. 准备游戏和 SMF

- 本次研究使用 Windows Steam 版，读取的游戏版本为 **3.280.0.0**。
- 从 [Simple Mod Framework 原版页面](https://www.nexusmods.com/hitman3/mods/200) 下载并按其说明完成安装、配置游戏路径。Mod 声明的最低框架版本为 **2.33.28**；本次构建部署验证使用 **2.33.42**。
- 本机示例游戏路径为 `D:\SteamLibrary\steamapps\common\HITMAN 3`。其他电脑请使用实际安装路径。
- 要通过手提箱带枪，需能在所选任务及起点使用手提箱；要通过机构藏匿点带枪，需选择已开放的大型藏匿点。本 Mod 不解锁手提箱、起点或藏匿点。

### 2. 安装改版并应用

1. 完全退出游戏，打开 SMF 的 Mod 管理器。
2. 若已经安装 **Extra Loadout Slots**，先禁用原版。本改版已经包含它的功能，两者不能同时启用。
3. 下载上面的 **2.1.2 ZIP**，使用 SMF 的导入功能导入安装包。请下载实际 ZIP 文件，不要将网页另存为 ZIP，也不要把整个仓库源码压缩包当作 Mod 导入。
4. 在列表中启用 **Extra Loadout Slots - Sniper Trio**，确认显示版本 **2.1.2**。
5. 点击 **Apply Mods**，等待部署成功后再启动游戏。只导入或勾选 Mod 尚未完成部署。

也可以手动解压 ZIP，把其中的 `Extra Loadout Slots - Sniper Trio` 文件夹放到 SMF 的 `Mods` 目录。正确结构如下，`manifest.json` 应直接位于 Mod 文件夹内：

```text
Simple Mod Framework/
└─ Mods/
   └─ Extra Loadout Slots - Sniper Trio/
      ├─ manifest.json
      ├─ README.zh-CN.md
      ├─ fileEdits/
      └─ newBlobs/
```

手动解压后仍需在 SMF 中启用并执行 **Apply Mods**。不要将此 ZIP 或源文件直接放入游戏的 `Runtime`／`Retail` 目录。

## 在游戏中使用

### 用手提箱带入故事任务

1. 进入故事任务的准备页面，选择允许携带装备的起点。
2. 在普通装备槽中选择一个手提箱，再打开该手提箱的**内容物选择**。
3. 在分类条切换到新增的 **“狙击模式”／“Sniper Assassin”**。请注意，这是独立分类；只查看原有“狙击枪”分类可能仍只看到以前的条目。
4. 从上述三把枪中选择一把，返回准备页面并开始任务。
5. 在任务中从手提箱取出枪，使用游戏的弹药切换操作切换弹药。本次使用者的键位是 **`Z`／`X`**；如已改键，请按自己的设置操作。

如果准备页保留了旧的装备状态，可以返回任务列表，再重新进入准备页面选择。

### 用机构藏匿点带入

选择任务中的**大型机构藏匿点**，在其物品列表中打开同一个“狙击模式”分类并选择武器。进入任务后，到对应藏匿点取枪。小型藏匿点不能容纳这些大型武器。

### 使用原版额外物品栏功能

在准备页面使用新增的空物品栏选择装备；已有额外槽位填入物品后，可以继续使用新增的空槽位。在额外物品栏上使用 `P` 调整数量，移除物品则按页面底部显示的操作提示执行。

新增狙击枪分类只面向手提箱内容物及大型藏匿点。手枪槽、普通小型装备选择和额外小型物品栏不会因此直接出现三把大型狙击枪。若要带枪，请按上面的手提箱或大型藏匿点流程操作。

## 常见问题

| 现象 | 检查方法 |
| --- | --- |
| 仍然只看到原来的席格 300 幽灵 | 确认打开的是新增“狙击模式”分类，而非原有“狙击枪”分类；再核对 SMF 中版本为 2.1.2 且已成功 Apply Mods。 |
| 找不到“狙击模式”分类 | 确认正在选择手提箱内容物或大型藏匿点物品；检查原版是否已禁用、本改版是否已成功部署。返回任务列表重新进入，必要时退出游戏后重新部署。 |
| SMF 提示与原版冲突 | 禁用原版 Extra Loadout Slots，仅启用本改版，再 Apply Mods。 |
| 找不到手提箱或大型藏匿点入口 | 检查已有解锁、当前任务和起点是否允许使用；本改版不负责开放这些入口。 |
| ICA 亲卫兵没有预期的特殊弹药 | 确认选的是新分类内带有地图标记的“狙击模式”版本；故事模式奖励版即使外观相同，也使用不同的武器配置。 |
| 另一个菜单 Mod 同时启用后异常 | 其他 Mod 可能改动相同的准备页／物品选择组件。暂时禁用相关 Mod 后重新 Apply Mods，检查是否仍能复现。 |

若仍有问题，记录游戏版本、SMF 版本、启用的 Mod、在线／离线模式、任务／起点及进入物品列表的路径，并保留部署错误日志。这些信息有助于区分安装、槽位限制和菜单兼容问题。

## 卸载或恢复原版

退出游戏，在 SMF 中禁用本改版并执行 **Apply Mods**。如需恢复原版 Extra Loadout Slots，禁用本改版后启用原版，再执行 **Apply Mods**；不要同时启用两者。

建议在任务结束后卸载，并重新选择装备。已携带特殊武器的任务存档在卸载后的恢复行为未单独测试。

## 原理与验证

原版 Extra Loadout Slots 扩展的是任务准备菜单；狙击枪的穿墙和震荡能力来自游戏中已有的狙击手模式武器。本改版在手提箱／大型藏匿点的物品选择组件中插入独立分类，用三把原生武器的 Repository ID 装备它们，并保留原作者的额外物品栏功能。

完整的资源引用链、开发阶段的失败过程与原因分析、最终实现及验证范围统一记录在 [研究结论与实现](docs/原理说明.md)。

发布前已完成游戏资源核对、165 个菜单表达式模拟用例、SMF 隔离部署与资源回读，并收到使用者正常工作的实机反馈。其他游戏平台、离线模式及其他菜单 Mod 的组合兼容性尚未逐项验证。

## 仓库结构与重新打包

```text
README.md                         首次安装与使用说明
mod/Extra Loadout Slots - Sniper Trio/
                                  完整 Mod 源文件，可供 SMF 使用
dist/                             当前 ZIP 安装包及 SHA-256
docs/原理说明.md                  资源证据、实现细节和研究结论
research/verification.json        静态校验及资源引用记录
research/SMF-validation.log       隔离部署日志
tools/build.py                    从 mod/ 生成安装包
tools/create_mod.py               从原版参考文件重建改版源文件
tools/verify.py                   资源与菜单表达式校验
tools/validate_smf.ps1             隔离 SMF 部署验证
```

### 只重新打包

安装 Python 3，在仓库根目录运行以下命令。`build.py` 仅使用 Python 标准库，不需要游戏、原版参考文件或额外 Python 依赖：

```powershell
python -X utf8 tools/build.py
```

脚本读取 `mod/Extra Loadout Slots - Sniper Trio/manifest.json` 的版本，检查 JSON 语法，并在 `dist/` 生成 ZIP 和 SHA-256 文件。改动根目录 README 后，如需同步安装包内说明，先执行：

```powershell
Copy-Item -LiteralPath README.md -Destination 'mod/Extra Loadout Slots - Sniper Trio/README.zh-CN.md'
python -X utf8 tools/build.py
```

安装包中的 `README.zh-CN.md` 是本文副本，其中的仓库文件相对链接以仓库根目录为准。校验下载包时，可比较下列两条命令输出的哈希（大小写不影响结果）：

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'dist/Extra.Loadout.Slots.Sniper.Trio-2.1.2.zip'
Get-Content -LiteralPath 'dist/Extra.Loadout.Slots.Sniper.Trio-2.1.2.zip.sha256'
```

### 重现完整研究验证

`create_mod.py` 需要原版 2.1.0 参考文件；`verify.py` 和 `validate_smf.ps1` 还需要从本机游戏提取的资源、元数据及相关工具。它们是本次研究的复现脚本，**不是只克隆仓库就能直接运行的完整测试环境**。查看脚本中的输入路径及 [原理说明](docs/原理说明.md) 后再准备数据。

`ref/`、大型游戏资源提取目录、工具可执行文件和 `build/` 验证产物已通过 `.gitignore` 排除。`validate_smf.ps1` 默认游戏路径为本文的本机示例，可以通过 `-GamePath` 指定其他路径。

隔离部署需要同时把 Runtime 和 Retail 指向工作区测试副本：本次核对的 SMF 即使设置 `outputToSeparateDirectory`，仍会清理配置的 Runtime 内的 patch200–300 文件，因此只启用该选项不足以隔离正式游戏。脚本已使用独立副本，具体依据见原理说明。

## 致谢与来源

**特别感谢 grappigegovert 创作并分享 Extra Loadout Slots。** 本改版直接建立在其额外物品栏、数量控制、删除操作和临时槽位处理的实现之上；原作者的工作让本次扩展成为可能。

- **原作者与原版 Mod：** [grappigegovert — Extra Loadout Slots（Nexus Mods #724）](https://www.nexusmods.com/hitman3/mods/724)，本改版基于版本 2.1.0。研究时原页面的权限说明允许署名后的修改和分发，后续再分发请同时遵守原页面的权限要求并保留署名。
- **前置框架：** 感谢 Atampy26 及贡献者开发 [Simple Mod Framework（Nexus Mods #200）](https://www.nexusmods.com/hitman3/mods/200)；部署行为参考 [SMF 官方源码](https://github.com/atampy25/simple-mod-framework)。本安装包不包含 SMF。
- **排查参考：** 感谢 [Peacock 项目](https://github.com/thepeacockproject/Peacock) 提供公开的菜单路由和模板实现。Peacock 是研究参考，不是本 Mod 的安装前置。
- **游戏资产：** 武器和弹药定义属于原游戏。本改版通过 ID 引用它们，安装包不附带完整游戏数据库、模型或材质，也不为原作者代码或游戏资产另行声明许可证。
