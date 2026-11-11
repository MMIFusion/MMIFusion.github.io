# 多模态信息融合 · 学术主页

公众号「多模态信息融合」的学术资源主站。

主站地址：https://mmifusion.github.io/

数据资源：https://mmifusion.github.io/datasets.html

## 视觉与阅读体验

- 深色融合主题首屏，原创信息光轨与立体模块，支持三种主题切换。
- 正文以 16–18 px 为主，论文标题 18–20 px；Noto Sans SC 与 Space Grotesk 字体随网站本地托管。
- 文章分类卡片、三个研究方向入口、数据集真实样例图与研究工具入口。
- 滚动渐入、悬停反馈、阅读进度和回到顶部；可暂停动效并记住选择，默认遵循系统减弱动画设置。
- 无 JavaScript 时仍提供完整文章、主题阅读和资源链接。

## 已有功能

- 站内数据资源库：111 项资源、6 个方向、16 组任务，支持全文检索、分类、排序、完整档案、原图和条目分享。

- 公众号原始文章标题、日期与微信原文链接。
- 关键词、文章类型、研究方向、会议期刊组合筛选，排序和分页。
- 可分享筛选后的地址；按 `/` 聚焦搜索；手机导航。
- 九个四字栏目：论文阅读、数据资源、评估指标、融合团队、会议日历、投稿推荐、导师招生、配色模板、广告合作；放大导航字体并提供跟随选中的滑块。
- 北京时间实时日期、时钟和不蒜子网站访问次数（PV），数值载入时有动画。
- 公众号阅读 / 点赞 / 转发 / 在看 TOP 10，使用 Excel 的真实快照数据，可收藏和分享原文链接。
- 趣味投稿日历、可点击的好运祝福和本机投稿检查清单；与真实会议日期分开。
- 文章收藏保存在当前浏览器，可筛选“只看收藏”。
- 三场会议、六个节点：倒计时、时区切换、单条与整组 ICS 日历下载。
- EN / SD / SF 本地图片试算、三个合成示例、CSV 导出与 Python 实现。
- 两个融合团队、一个官方长期招募条目、三个会议期刊档案，可筛选并对比投稿方向。
- 四组可复制色板、SVG / JSON 下载、可编辑融合框架图与 Matplotlib 绘图脚本。
- 资源推荐表单生成可复制草稿与预填 GitHub Issue；不会自动发送或保存投稿。
- 无 JavaScript 时仍能阅读完整文章目录。
- 数据和页面分离，字体本地托管；核心阅读与工具无需第三方服务。访问次数单独使用不蒜子，故障时显示不可用，不伪造数字。

## 本地运行

构建使用 Python 3.10 或更新版本，无需安装依赖。指标单元检查需要 Node.js 18 或更新版本。下载的科学绘图 / 图片评估脚本另需各自声明的库。

```sh
python3 scripts/build.py
python3 scripts/check.py
node scripts/test_metrics.cjs
node scripts/test_community.cjs
python3 -m http.server 8765 --directory dist
```

打开 http://localhost:8765/ 。不要直接用 `file://` 打开，以免浏览器限制读取筛选数据。

## 发布到 GitHub Pages

1. 在 **MMIFusion** 账号下创建公开空仓库 `MMIFusion.github.io`。
2. 推送本项目到 `main`。
3. 使用 GitHub 用户主站自动启用的发布设置：Settings → Pages → Source 为 **Deploy from a branch**，分支 `main`，目录 `/ (root)`。
4. 每次构建后将生成页面一并推送到 `main`，GitHub Pages 会自动发布。`.nojekyll` 使站点直接按静态文件部署。

独立的 `Check website content` 工作流检查内容与生成文件一致性；发布由 GitHub 自带的 `pages build and deployment` 工作流完成。

仓库 SSH 地址：`git@github-mmif:MMIFusion/MMIFusion.github.io.git`。

## 更新内容

```sh
python3 scripts/import_articles.py '/path/to/微信文章导出.xlsx' --snapshot-date 2026-10-28
python3 scripts/import_stats.py '/path/to/微信文章导出.xlsx'
python3 scripts/build.py
python3 scripts/check.py
```

导入会重建文章目录，请使用包含全部待收录文章的完整导出表。原始表格保留在本机，不提交到公开仓库。经维护者明确要求，`import_stats.py` 只提取阅读、点赞、在看、转发四项计数，榜单标明快照日期；不发布其他运营字段。原表没有收藏数，本站收藏只存当前浏览器，不冒充公众号收藏统计。标题相同而微信文章标识不同的记录分别保留。微信链接使用 HTTPS，保留定位文章所需参数，移除会话和场景跟踪参数。

详细字段与维护流程见 [内容维护说明](docs/MAINTENANCE.md)；数据资源迁入记录、后续维护与链接约定见 [数据目录说明](docs/DATASETS.md)。

资源核对于 2026-11-11：投稿推荐收录 38 个会议期刊，按参考的 CCF 第七版分组，支持分类筛选与 2–3 项对比；2027 年会议日历收录 8 场相关 A 类会议、31 个已公布节点，未公布时间明确标注。官方来源及计算约定见 [来源说明](docs/SOURCES.md)，分类依据见 [投稿目录核对说明](docs/VENUES.md)。内容数据在 `data/portal.json`，新增条目后重新构建即可发布。

代码与文档：Copyright (c) 2026 公众号「多模态信息融合」。整理与维护：汐萌、囗〇。

原创代码采用 MIT License。原创 SVG 模板与色板采用 CC BY 4.0，使用时注明“多模态信息融合”。头像、文章及第三方内容的权利归各自权利人；代码许可不扩展到这些内容。
