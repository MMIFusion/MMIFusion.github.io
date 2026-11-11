# 资源来源与计算约定

核对日期：2026-11-11。来源内容可能更新，请以各条目官方页面为准。本站条目是简要导航，未转载全文。站点信息架构参考 [LowLevelCV](https://lowlevelcv.com/) 的资源分类与日期导航；代码、页面布局及下载模板由本站独立实现。

## 官方日程

- [CVPR 2027 Call for Papers](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)：注册、论文、补充材料为 23:59 AoE（UTC−12）；也收录评审、作者回复与录用日期。教程和主会采用 [2027 Dates](https://cvpr.thecvf.com/Conferences/2027/Dates) 明列的 6 月 20–21 日、6 月 22–25 日，不采用其他汇总页的不同总会期。
- [ICCV 2027 Dates](https://iccv.thecvf.com/Conferences/2027/Dates)：教程 10 月 3–4 日、主会 10 月 5–7 日。首页正文另有 10 月 2–8 日总会期表述，页面已提示差异；未推测投稿截止。
- [ACM Multimedia 系列官网](https://www.acmmm.org/index.html)：只确认 2027 年香港举办，会期与投稿节点待公布。
- [ICLR 2027 Call for Papers](https://iclr.cc/Conferences/2027/CallForPapers)：摘要、论文、评审、作者讨论结束与最终结果日期；未明确时刻的节点不推定 23:59。[2027 Dates](https://iclr.cc/Conferences/2027/Dates) 列主会 4 月 26–28 日、研讨会 4 月 29–30 日。[Future Meetings](https://iclr.cc/Conferences/FutureMeetings) 列区域为北美西海岸，具体地点待公布。
- [ICML 2027 Dates](https://icml.cc/Conferences/2027/Dates)：教程 8 月 1 日，主会 8 月 2–4 日，研讨会 8 月 5–6 日。投稿节点待公布；征稿页当时尚无正文。
- [NeurIPS Future Meetings](https://neurips.cc/Conferences/FutureMeetings)：只列 2027 年欧洲举办，不估算会期或论文截止。
- [AAAI-27 主技术赛道征稿](https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/)：摘要 7 月 21 日、论文 7 月 28 日、补充材料 7 月 31 日（均为 2026 年 23:59 AoE）；作者反馈采用更新后的 10 月 24–31 日，不使用被划除的 10 月 19–25 日。终稿条目存在修订标记，暂不生成终稿节点。各专项赛道不混入主赛道日程。
- [ACL 2027 主会征稿](https://2027.aclweb.org/calls/main/)：最晚 ARR 投稿轮次为 2027 年 1 月 4 日 23:59 AoE；这不是 ACL commitment 截止，后者尚待公布。教程 8 月 17 日、研讨会 8 月 18–19 日、主会 8 月 20–22 日。

精确截止事件导出为 UTC。日期事件使用 ICS `VALUE=DATE`，结束日期不包含在事件内；它们保留官方日历日期，不等于把 AoE 转换成当地某个时刻。ICS 为下载时的静态快照，不是日历订阅。

## 团队、招生与投稿方向

团队目录现有 27 组团队与学者，按用户提供的压缩包及公开主页整理。原资料中的姓名与机构差异、访问限制和逐项入口见 [团队目录维护说明](TEAMS.md)。社区成员名称、顺序与激活展示状态来自用户明确要求。

- [马佳义官方主页](https://jiayi-ma.github.io/index.html)：武汉大学，图像匹配 / 配准、信息融合与视觉感知等研究方向。未据此推定当前招生名额。
- [刘日升 / VLOG 官方主页](https://rsliu.tech/)：大连理工大学，视觉、学习与优化。
- [刘日升的大连理工大学教师主页](https://faculty.dlut.edu.cn/rsliu/zh_CN/index.htm)：明确欢迎博士后、博士、硕士及本科生科研助理，并注明长期有效。本站只转述公开招募性质，具体批次和名额由申请者向团队确认。
- [IEEE TIP 官方范围](https://signalprocessingsociety.org/publications-resources/ieee-transactions-image-processing/about-transactions-image-processing)及[作者说明](https://signalprocessingsociety.org/publications-resources/information-authors)：用作期刊范围与指南入口；CVPR、ICLR 范围来自上述征稿页。

“选刊思路”是本站基于研究问题的编辑建议，不是官方承诺，也不表示录用概率。团队按收录顺序展示，不排名。

投稿推荐已扩充为 38 项，分类基于用户提供的第七版正式版 PDF；出版社、学会和会议官网用于范围及投稿入口核对。文件摘要、分类页码、关键版本差异和逐项官方入口记录在 [投稿目录核对说明](VENUES.md)。未收录的 Information Fusion 单列，不以 CCF 未收录推断期刊质量。

## 首页数据集

- [MSRS 原始项目](https://github.com/Linfeng-Tang/MSRS)
- [M3FD / TarDAL 原始项目](https://github.com/JinyuanLiu-CV/TarDAL)
- [RoadScene 原始项目](https://github.com/hanna-xu/RoadScene)

原数据资源目录已完整接入 [主站数据资源页](https://mmifusion.github.io/datasets.html)，保留团队作者、介绍、链接、下载说明和原图。初次导入记录及许可见 [数据目录说明](DATASETS.md)。本次整合未另行核验全部论文发表信息。

## 三个基础指标

[Evaluation for Image Fusion](https://github.com/Linfeng-Tang/Evaluation-for-Image-Fusion)作为完整评估工具箱入口。本站 EN / SD / SF 在线试算及 Python 代码是独立实现，不声称与任何论文或工具箱的所有预处理与数值完全一致。

- 8 位灰度：`floor(0.299 R + 0.587 G + 0.114 B + 0.5)`；透明度先与白底合成。
- EN：256 桶灰度直方图，以 2 为底，忽略零概率项。
- SD：总体标准差，分母 N。
- SF：分别计算横向、纵向有效相邻像素对的平方差均值，求和后开平方。无相邻像素的方向贡献为 0。
- 按原始解码尺寸计算；浏览器与 Pillow 解码及色彩管理可能产生细微差异。不要直接把演示结果与使用其他协议的论文数值混在一起。

解析测试：纯灰 EN / SD / SF 均为 0；2 × 2 黑白交错图 EN=1、SD=127.5、SF=255√2；256 级一行渐变 EN=8、SD=√5461.25、SF=1。指标增大不自动意味着融合质量提高。

## 下载模板

色板与双模态框架 SVG 为本站原创，CC BY 4.0；绘图与评估 Python 代码采用 MIT License。绘图脚本的数值和框架图仅为演示，需替换成自己的方法与实验。原公众号文章和头像不因模板许可而改变其权属。


## 视觉改版资源（2026-11-11）

- 字体：[Noto Sans SC](https://github.com/google/fonts/tree/main/ofl/notosanssc)、[Space Grotesk](https://github.com/google/fonts/tree/main/ofl/spacegrotesk)，使用官方文件制作网页字形子集，保留各自 SIL Open Font License。字体随本站分发，访问网站时不请求第三方字体服务。
- 数据集样例图沿用原数据资源目录：MSRS 对应 `46ac6691890dd24b.png`，M3FD 对应 `d93037bdb9110e73.png`，RoadScene 对应 `56ef0c4862636198.png`。源索引为 `MMIFusion/Datasets/docs/data/datasets.json`，与各自原始项目 / 数据档案关联。第三方示例图不包含在本站原创代码许可内。
- 融合光轨、立体模块、论文主题封面与工具插画为本站代码绘制。它们是概念表达，不展示算法性能或实验结论。
- 论文专题与方向计数直接从现有公众号索引计算，不新增未经核实的论文录用或性能声明。

## 社区功能（2026-11-11）

- 人气榜：用户提供的 `261028-多模态信息融合.xlsx`，工作表「微信文章导出」，标题 B2:B240，阅读 J2:J240、点赞 K2:K240、在看 N2:N240、转发 O2:O240；快照日期 2026-10-28。未提供收藏数，未使用赞赏或评论字段。使用稳定文章 ID 与原有微信链接对应，完整 XLSX 不公开。
- 网站访问次数：[不蒜子官方说明](https://busuanzi.ibruce.info/)提供 `busuanzi_value_site_pv`。接入脚本为 `https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js`，不是公众号文章阅读量，也不是独立访客数；从接入起累计，受第三方服务可用性影响。
- 日期采用浏览器 `Intl.DateTimeFormat`、`Asia/Shanghai` 时区。投稿日历是本站原创的科研趣味日签，不引用传统黄历，不代表科学预测或真实截止时间。
