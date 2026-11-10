# 内容维护说明

## 信息架构

| 页面 | 数据来源与用途 |
| --- | --- |
| 首页 | 文章总数、最新文章、八个栏目入口 |
| 论文阅读 | `data/articles.json` 全部文章 |
| 数据集 | 链接既有独立站，不复制它的数据 |
| 评估指标 | `评估与指标` 主题文章 |
| 融合团队 | `研究团队` 主题报道及 `community.json` 团队档案 |
| 会议时间 | `community.json` 官方日程 |
| 会议期刊推荐 | 投稿参考与论文速递 |
| 导师招生 | `community.json` 招生信息 |
| 配色模板 | 基础色板与公众号配色文章 |

## 文章

初始来源：`261028-多模态信息融合.xlsx`，工作表「微信文章导出」，第 2–240 行，共 239 条。

导入脚本只读取第一张工作表，要求 B 列为标题、C 列为标准文本发布时间（YYYY-MM-DD 开头）、F 列为微信链接，与本次导出格式一致。原始标题保留。`sourceRow` 供校对定位。发布日期按原表，不把文章日期当论文发表日期。

分类与主题由 `scripts/import_articles.py` 中规则辅助生成；可以修正规则后重导入，或直接修改 `data/articles.json`。重新导入会覆盖直接编辑，长期修正应改规则或为导入流程增设人工覆盖文件。会议期刊字段只从文章标题提取，不代表独立核验了录用状态。

同名文章只在链接一致时去重。不要只按标题去重，避免删除不同发布版本或不同内容。

## 站点设置

`data/site.json` 保存公众号链接、数据集独立站、交流微信、维护者与主站域名。不要填写未经确认的账号、二维码或邮箱。

## 扩展栏目

编辑 `data/community.json`。当前 `conferences`、`teams`、`opportunities` 为空，页面显示明确的待收录状态。

会议记录字段：`name`、`deadline`、`timezone`、`verifiedAt`、`source`。`deadline` 包含年份、日期与具体时间；`source` 应为官方说明。后续可扩展多种截止日期，而不是从文章年份推算截止日期。

团队记录字段：`name`、`institution`、`description`、`source`。`source` 使用团队/学校官方主页。涉及论文作者时保持完整名单与原始顺序。

招生记录字段：`institution`、`title`、`description`、`deadline`、`source`。过期后及时下架或在内容中明确标注，不能把历史招生当当前机会。

色板字段：`name`、`note`、`colors`（HEX 色值列表）。本站基础色板与论文配色文章分开标识。

## 构建与发布

页面模板：`scripts/build.py`；样式：`assets/style.css`；交互：`assets/app.js`。

输出目录 `dist/` 为可直接部署的静态站点。请修改源文件后重新构建，不要直接编辑输出。GitHub Actions 构建后发布该目录。

检查命令：`python3 scripts/check.py`。检查文章标识、微信 URL、文章完整性、所有站内文件/锚点、页面标题层级与外链安全属性。

更新内容后在浏览器检查受影响页面，至少查看手机和桌面宽度，验证搜索、分类、分页及外链目的地。

## Git 身份

使用 MMIFusion 身份：

```sh
git config user.name MMIFusion
git config user.email 276543646+MMIFusion@users.noreply.github.com
```

推送前确认 SSH 身份与仓库归属；不要使用其他 GitHub 账号。
