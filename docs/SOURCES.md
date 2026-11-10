# 首批资源与计算约定

核对日期：2026-11-11。来源内容可能更新，请以各条目官方页面为准。本站条目是简要导航，未转载全文。站点信息架构参考 [LowLevelCV](https://lowlevelcv.com/) 的资源分类与日期导航；代码、页面布局及下载模板由本站独立实现。

## 官方日程

- [CVPR 2027 Call for Papers](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)：论文注册、论文提交、补充材料三个截止节点；原始时刻为 23:59 AoE（UTC−12）。[作者指南](https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines)。
- [ICLR 2027 Call for Papers](https://iclr.cc/Conferences/2027/CallForPapers)：作者讨论结束与最终结果通知；原文只有日期，本站不推定精确截止时刻。[作者指南](https://iclr.cc/Conferences/2027/AuthorGuidelines)。
- [ICML 2027 Dates](https://icml.cc/Conferences/2027/Dates)：主会 2027-08-02 至 2027-08-04。首批未填写该页尚未公布的投稿截止日期。

精确截止事件导出为 UTC。日期事件使用 ICS `VALUE=DATE`，结束日期不包含在事件内；它们保留官方日历日期，不等于把 AoE 转换成当地某个时刻。ICS 为下载时的静态快照，不是日历订阅。

## 团队、招生与投稿方向

- [马佳义官方主页](https://jiayi-ma.github.io/index.html)：武汉大学，图像匹配 / 配准、信息融合与视觉感知等研究方向。未据此推定当前招生名额。
- [刘日升 / VLOG 官方主页](https://rsliu.tech/)：大连理工大学，视觉、学习与优化。
- [刘日升的大连理工大学教师主页](https://faculty.dlut.edu.cn/rsliu/zh_CN/index.htm)：明确欢迎博士后、博士、硕士及本科生科研助理，并注明长期有效。本站只转述公开招募性质，具体批次和名额由申请者向团队确认。
- [IEEE TIP 官方范围](https://signalprocessingsociety.org/publications-resources/ieee-transactions-image-processing/about-transactions-image-processing)及[作者说明](https://signalprocessingsociety.org/publications-resources/information-authors)：用作期刊范围与指南入口；CVPR、ICLR 范围来自上述征稿页。

“选刊思路”是本站基于研究问题的编辑建议，不是官方承诺，也不表示录用概率。团队按收录顺序展示，不排名。

## 首页数据集

- [MSRS 原始项目](https://github.com/Linfeng-Tang/MSRS)
- [M3FD / TarDAL 原始项目](https://github.com/JinyuanLiu-CV/TarDAL)
- [RoadScene 原始项目](https://github.com/hanna-xu/RoadScene)

完整数据档案、作者与下载信息继续由 [数据集独立站](https://mmifusion.github.io/Datasets/) 维护，主站只提供入口。

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
- 数据集样例图沿用本站维护的数据集独立站目录：MSRS 对应 `46ac6691890dd24b.png`，M3FD 对应 `d93037bdb9110e73.png`，RoadScene 对应 `56ef0c4862636198.png`。源索引为 `MMIFusion/Datasets/docs/data/datasets.json`，与各自原始项目 / 数据档案关联。第三方示例图不包含在本站原创代码许可内。
- 融合光轨、立体模块、论文主题封面与工具插画为本站代码绘制。它们是概念表达，不展示算法性能或实验结论。
- 论文专题与方向计数直接从现有公众号索引计算，不新增未经核实的论文录用或性能声明。
