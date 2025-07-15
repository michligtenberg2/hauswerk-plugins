**🌐 支持语言:** [Nederlands](../README.md) | [English](README_EN.md) | [Deutsch](README_DE.md) | [Français](README_FR.md) | [中文](README_ZH.md)

# 🧹 Hauswerk 插件（中文）

欢迎访问 **Hauswerk 插件库** — 这是 [Hauswerk](https://github.com/michligtenberg2/Hauswerk) 图形界面的官方插件仓库。

本仓库包含多个 `.zip` 格式的插件包，以及中央配置文件 `plugins.json`，由 Hauswerk 应用内置的「插件商店」使用。

---

## 📦 本仓库包含的插件

| 插件名称         | 描述                                   | 文件名            |
|------------------|----------------------------------------|-------------------|
| Collage          | 创建剪辑合成视频                         | `collage.zip`     |
| Clipper          | 从视频中随机剪出多个片段                 | `clipper.zip`     |
| Stretcher        | 降速视频（可选保留音轨）                 | `stretcher.zip`   |
| Concat           | 合并多个视频为一个文件                   | `concat.zip`      |
| Psychotisch      | 带 EBM 风格的混乱视觉特效                | `psychotisch.zip` |
| AudioFadeBPM     | 批量提取音频并添加淡入淡出                | `audiofadebpm.zip`|
| UIBuilder        | 可视化插件界面构建器                     | `uibuilder.zip`   |

每个插件至少包含：
- 一个带 `QWidget` 子类的 `.py` 文件
- 一个包含元数据的 `plugin.json`
- *(可选)* `.svg` 图标文件
- *(可选)* `preview.png` 插件预览图
- *(可选)* `tags` 标签，如 `["视频", "音频", "滤镜"]`

---

## 🔗 插件索引文件 `plugins.json`

示例格式：
```json
{
  "name": "Collage",
  "description": "Hauswerk 的拼贴插件",
  "zip_url": "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/collage.zip",
  "tags": ["视频", "合成"],
  "verified": true
}
```

Hauswerk 应用将该列表用于插件展示、搜索与安装。

---

## 🚧 贡献插件的方式

提供插件有两种方式：

```
╔════════════════════════════════════════════════════╗
║     📂 插件文件夹结构与审核流程                    ║
╠══════════════╦═════════════════════════════════════╣
║ /unofficial/ ║ 所有人可提交，无需审核              ║
║ /official/   ║ 需提交 PR，并由维护者审核            ║
╚══════════════╩═════════════════════════════════════╝
```

### ✅ 方式一：上传至 `/unofficial/`
- 上传 `.zip` 文件至 `/unofficial/`
- 系统将自动：
  - ✅ 验证是否包含有效 `plugin.json`
  - ✅ 添加至 `unofficial/plugins.json`
  - ✅ 读取标签和预览图
- **无需审核或 Pull Request**

### 🔐 方式二：成为官方插件
- 提交 Pull Request，内容包括：
  - 插件 `.zip` 文件放入 `/official/`
  - 在主 `plugins.json` 文件中添加条目
- 审核通过后，插件将标记为 `verified: true`

| 方法                    | 谁能使用？ | 是否展示在应用？         | 是否需审核？ |
|-------------------------|------------|----------------------------|----------------|
| 上传到 `/unofficial/`   | 所有人     | ✅ 通过非官方源展示         | ❌              |
| 提交至 `/official/`     | 贡献者     | ✅ 出现在官方插件商店       | ✅              |

ℹ️ `/unofficial/plugins.json` 会在每次更改后自动生成。

---

## 💡 支持多个插件源

Hauswerk 支持从多个地址加载插件列表：

```json
[
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/plugins.json",
  "https://yourdomain.com/plugins.json",
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/unofficial/plugins.json"
]
```

你可以设置自己私有的插件源供团队或用户使用。

---

## 🛠️ 创建你自己的插件

1. 创建插件文件夹，包含：
   - `yourplugin.py`
   - `plugin.json`
   - *(可选)* `icon.svg`
   - *(可选)* `preview.png`

2. 打包压缩：
```bash
zip -r yourplugin.zip yourplugin/
```

3. 上传至 `/unofficial/`
4. 插件将在应用中自动显示
5. 若想成为官方插件 → 提交 PR 至 `/official/`

---

## 🧹 `plugin.json` 示例
```json
{
  "name": "我的插件",
  "entry": "myplugin.py",
  "class": "MyPluginWidget",
  "icon": "icon.svg",
  "tags": ["视频", "滤镜"],
  "verified": false
}
```

---

## 🔄 自动验证与索引更新

此仓库使用 GitHub Actions 实现自动处理：
- 检查 `plugins.json` 格式是否正确
- 验证每个 `.zip` 是否包含合法的 `plugin.json`
- 每次上传时重建 `unofficial/plugins.json`
- 自动加入标签、预览图、标记状态
- 可选：每日自动刷新徽章或统计

详情见 `.github/workflows/validate_plugins.yml`

---

## 📢 联系方式与支持
如有问题、建议或合作，请访问 [github.com/michligtenberg2/Hauswerk](https://github.com/michligtenberg2/Hauswerk) 提交 issue。

---

祝你构建愉快！🛠️
