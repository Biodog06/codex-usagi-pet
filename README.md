# Codex 乌萨奇桌宠

为 Codex Desktop 制作的非官方乌萨奇动态桌宠。整体采用暖黄色、深棕线条和粉色腮红，保留圆润脸型与小巧四肢，并加入追蝴蝶、身体互换和拍照搞怪等特别动作。

![乌萨奇桌宠动作总览](assets/contact-sheet.png)

## 主要特点

- 使用 Codex Desktop v2 桌宠格式
- 1536 × 2288 透明 WebP 精灵图
- 8 × 11 布局，共 88 个标准格位
- 包含待机、左右移动、挥手、跳跃、失败、等待、工作和检查状态
- 支持 16 个环视方向
- 正面、侧面和背面均保持圆润轮廓
- 动画始终使用暖黄色身体、深棕色线条和粉色腮红

## 特别动作

### 追蝴蝶

工作状态下，乌萨奇会发现黄色蝴蝶，转身追赶后再回到正面。

### 身体互换

`failed` 状态参考身体互换篇第 207—208 话。外形仍是乌萨奇，但会表现出吉伊卡哇胆怯、容易含泪的一面：先不安地站着，再把双手收向胸前，眼眶含泪，最后轻轻吸鼻子。

![乌萨奇身体里的吉伊卡哇](assets/failed-action.gif)

### 拍照搞怪

`review` 状态参考第 80 话拍照场景：先正面停顿，随后快速转身弯腰，再从两腿之间倒着探头。

![乌萨奇转身倒着探头](assets/review-action.gif)

### 草裙与夹子

草裙抱胸动作与连贯夹子动作的设计稿：

![草裙与夹子动作设计](assets/special-actions.png)

## 安装前准备

- 已安装支持自定义 v2 桌宠的 Codex Desktop
- 已安装 Git；也可以直接下载仓库 ZIP
- 安装过程不需要管理员权限

## macOS 安装

打开“终端”，执行下面的完整命令：

```bash
git clone https://github.com/Biodog06/codex-usagi-pet.git
cd codex-usagi-pet

pet_target="$HOME/.codex/pets/usagi"
mkdir -p "$pet_target"
cp ./pet.json ./spritesheet.webp "$pet_target/"
```

安装位置：

```text
~/.codex/pets/usagi
```

## Windows 安装

打开 PowerShell，执行下面的完整命令：

```powershell
git clone https://github.com/Biodog06/codex-usagi-pet.git
Set-Location .\codex-usagi-pet

$PetTarget = Join-Path $env:USERPROFILE ".codex\pets\usagi"
New-Item -ItemType Directory -Force -Path $PetTarget | Out-Null
Copy-Item -Path .\pet.json, .\spritesheet.webp -Destination $PetTarget -Force
```

安装位置：

```text
%USERPROFILE%\.codex\pets\usagi
```

## 不使用 Git 安装

1. 在 GitHub 仓库页面选择 **Code → Download ZIP**。
2. 解压 ZIP。
3. 将 `pet.json` 和 `spritesheet.webp` 一起复制到对应系统的 `usagi` 目录：

```text
macOS:   ~/.codex/pets/usagi
Windows: %USERPROFILE%\.codex\pets\usagi
```

目录中最终应包含：

```text
usagi/
├── pet.json
└── spritesheet.webp
```

## 在 Codex 中启用

安装文件后：

1. 重新打开 Codex Desktop；或在桌宠选择处先切换到其他桌宠。
2. 重新选择“乌萨奇”。
3. 如果仍显示旧动作，完全退出 Codex Desktop 后重新打开，以刷新贴图缓存。

## 更新

### macOS

在本仓库目录中执行：

```bash
git pull

pet_target="$HOME/.codex/pets/usagi"
mkdir -p "$pet_target"
cp ./pet.json ./spritesheet.webp "$pet_target/"
```

### Windows PowerShell

在本仓库目录中执行：

```powershell
git pull

$PetTarget = Join-Path $env:USERPROFILE ".codex\pets\usagi"
New-Item -ItemType Directory -Force -Path $PetTarget | Out-Null
Copy-Item -Path .\pet.json, .\spritesheet.webp -Destination $PetTarget -Force
```

更新后重新选择“乌萨奇”，或重启 Codex Desktop。

## 卸载

卸载只需要删除 `usagi` 桌宠目录。

macOS：

```bash
pet_target="$HOME/.codex/pets/usagi"
rm -rf "$pet_target"
```

Windows PowerShell：

```powershell
$PetTarget = Join-Path $env:USERPROFILE ".codex\pets\usagi"
Remove-Item -Path $PetTarget -Recurse -Force
```

删除后重新打开 Codex Desktop。

## 项目文件

```text
codex-usagi-pet/
├── README.md
├── pet.json
├── spritesheet.webp
└── assets/
    ├── contact-sheet.png
    ├── failed-action.gif
    ├── review-action.gif
    └── special-actions.png
```

| 文件 | 用途 |
| --- | --- |
| `pet.json` | 桌宠名称、说明、v2 版本及精灵图路径 |
| `spritesheet.webp` | 可直接安装的透明动画精灵图 |
| `assets/contact-sheet.png` | 全部动作及环视方向总览 |
| `assets/failed-action.gif` | 身体互换失败动作预览 |
| `assets/review-action.gif` | 拍照搞怪检查动作预览 |
| `assets/special-actions.png` | 草裙与夹子动作设计稿 |

## 格式信息

| 项目 | 数值 |
| --- | --- |
| 桌宠 ID | `usagi` |
| 格式版本 | `spriteVersionNumber: 2` |
| 图集尺寸 | 1536 × 2288 |
| 单格尺寸 | 192 × 208 |
| 图集布局 | 8 列 × 11 行 |
| 图像格式 | 透明 WebP |

## 版权说明

这是由 Biodog06 与 Codex 共同调整的非官方同人桌宠，仅供个人学习与非商业使用。

乌萨奇、吉伊卡哇及相关角色版权归原作者 Nagano 与相关权利方所有。本项目与官方无关，也未获得官方授权。
