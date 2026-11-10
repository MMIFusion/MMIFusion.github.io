# 内容维护说明

## 信息架构

| 页面 | 数据来源与用途 |
| --- | --- |
| 首页 | 文章总数、最新文章、八个栏目入口 |
| 论文阅读 | `data/articles.json` 全部文章 |
| 数据集 | 链接既有独立站，不复制它的数据 |
| 评估指标 | EN / SD / SF 试算及评估专题阅读 |
| 融合团队 | `portal.json` 官方团队档案 |
| 会议时间 | `portal.json` 官方日程、时区与 ICS |
| 会议期刊推荐 | `portal.json` 官方范围、整理建议与对比 |
| 导师招生 | `portal.json` 官方招募信息 |
| 配色模板 | `community.json` 色板、原创下载模板与公众号文章 |
| 推荐资源 | 本地生成草稿，由访客确认后前往 GitHub 提交 |

## 文章

初始来源：`261028-多模态信息融合.xlsx`，工作表「微信文章导出」，第 2–240 行，共 239 条。

导入脚本只读取第一张工作表，要求 B 列为标题、C 列为标准文本发布时间（YYYY-MM-DD 开头）、F 列为微信链接，与本次导出格式一致。原始标题保留。`sourceRow` 供校对定位。发布日期按原表，不把文章日期当论文发表日期。

分类与主题由 `scripts/import_articles.py` 中规则辅助生成；可以修正规则后重导入，或直接修改 `data/articles.json`。重新导入会覆盖直接编辑，长期修正应改规则或为导入流程增设人工覆盖文件。会议期刊字段只从文章标题提取，不代表独立核验了录用状态。

同名文章只在链接一致时去重。不要只按标题去重，避免删除不同发布版本或不同内容。

## 站点设置

`data/site.json` 保存公众号链接、数据集独立站、交流微信、维护者与主站域名。不要填写未经确认的账号、二维码或邮箱。

## 扩展栏目

编辑 `data/portal.json`。每个条目使用稳定唯一的 `id`，保留 `source` 官方链接。`verifiedAt` 记录最近一次整体核对日期；批量更新前应逐项核实来源，不要只改日期。

- `conferences`：每场会议包含 `events`。精确截止节点使用 `kind: deadline` 和带 UTC 偏移的 ISO `at`。AoE 用 `-12:00`，不能误写成 UTC。只公布日期时用 `kind: date`、`start` 和不包含在事件中的 `endExclusive`。例如 8 月 2–4 日的结束值为 8 月 5 日。`original` 保留原始日期 / 时区说明。构建自动生成单条及全部 `.ics`，不安排自动更新订阅。
- `teams`：学校、城市、负责人、研究标签与官方主页；`relatedQuery` 用于检索公众号文章，`opportunity` 可关联招募条目 ID。引用论文时保留完整作者与顺序。
- `opportunities`：`teamId` 关联团队、`types` 表示招募类别。长期招募必须有官方原文依据；限期招生请写明到期时间并及时更新 / 移除。当前 `expires` 为记录字段，不自动下架。
- `venues`：将官方 `scope` 与本站整理的 `fit` 建议分开；`guide` 指向作者指南，`articleVenue` 必须匹配现有文章分类，`calendar` 可关联会议 ID。未核实的信息不填影响因子或录用率。
- `datasets`：首页精选入口；详情和下载链接继续由独立站维护。不要复制数据文件。
- `metrics`：定义、公式、注意点；若改计算约定，须同步浏览器 `assets/metrics-core.js`、Python 下载脚本与分析样例测试。

`data/community.json` 只保存基础色板：`name`、`note`、`colors`（HEX）。构建生成 SVG / JSON 下载。框架 SVG 由 `scripts/portal.py` 生成，绘图与指标 Python 脚本直接在 `downloads/` 维护。

收藏仅存当前浏览器的 localStorage（键 `mmifusion-bookmarks-v1`），不跨设备同步。图片只在内存中计算，不上传、不持久保存。投稿表单只生成预览与 GitHub 链接，维护者在仓库 Issues 中审核后手动更新数据。

## 构建与发布

页面模板：`scripts/build.py`、`scripts/portal.py`；样式：`assets/style.css`、`assets/portal.css`；交互：`assets/app.js`、`assets/portal.js`；指标计算：`assets/metrics-core.js`。

构建输出 `dist/` 供本地预览，同时将生成的 HTML、robots.txt、sitemap.xml 和 `.nojekyll` 同步到仓库根目录，复用根目录的 `assets/` 与 `data/`。请修改源文件后重新构建，不要直接编辑生成页面。

GitHub Pages 沿用 `main / (root)` 的分支发布；GitHub 自带发布流程会在推送后部署。`Check website content` 仅做一致性检查，不另行部署，避免两套发布流程相互覆盖。`dist/` 为本地构建产物，不提交到仓库。

检查命令：`python3 scripts/check.py`、`node scripts/test_metrics.cjs`。检查文章标识、微信 URL、文章完整性、所有站内文件/锚点、页面标题层级与外链安全属性，并验证 ICS 的 UTC / 日期编码、资源关联及指标解析样例。

更新内容后在浏览器检查受影响页面，至少查看手机和桌面宽度，验证搜索、分类、分页、收藏、日历下载、时区切换、图片计算与导出、会议期刊对比、投稿预览及外链目的地。

## Git 身份

使用 MMIFusion 身份：

```sh
git config user.name MMIFusion
git config user.email 276543646+MMIFusion@users.noreply.github.com
```

推送前确认 SSH 身份与仓库归属；不要使用其他 GitHub 账号。
