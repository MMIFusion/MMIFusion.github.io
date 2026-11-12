# 2027 会议日历核对记录

核对日期：2026-11-12（北京时间）。11 场 A 类会议，61 个已公布节点；ECCV 为独立的届次说明，不计入会议数或 ICS。

分类沿用用户提供的第七版 CCF 正式版 PDF，文件信息见 [投稿目录核对说明](VENUES.md)。人工智能类 A 会位于 PDF 第 57 页；KDD / SIGIR 位于第 35 页，WWW 位于第 70 页。ECCV 在第 58 页 B 类。以上相关页已进行文字和页面图像核对。分类不等同于同领域声誉排名。

## 会议来源与本轮变化

| 会议 | 事实与来源 | 本轮处理 |
|---|---|---|
| CVPR | [征稿](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)、[日程](https://cvpr.thecvf.com/Conferences/2027/Dates) | 原有 8 个节点与官方一致，保留；精确投稿时间为 23:59 AoE。 |
| ICCV | [日程](https://iccv.thecvf.com/Conferences/2027/Dates) | 教程 / 研讨会 10 月 3–4 日，主会 10 月 5–7 日；投稿时间仍待公布。采用分段日程，不混用首页总会期。 |
| ACM MM | [系列官网](https://www.acmmm.org/index.html) | 2027 香港已确认，日期仍未公布，不使用往届日期。 |
| ICLR | [征稿](https://iclr.cc/Conferences/2027/CallForPapers)、[首页](https://iclr.cc/Conferences/2027)、[日程](https://iclr.cc/Conferences/2027/Dates) | 新增评审与 AC 讨论阶段 2026-11-19 至 12-16；举办地更新为美国加利福尼亚州。官网未明确城市，不补造具体城市。 |
| ICML | [日程](https://icml.cc/Conferences/2027/Dates)、[首页](https://icml.cc/Conferences/2027)、[待公布征稿正文](https://icml.cc/Conferences/2027/CallForPapers) | 新增投稿开放 / 建议完成账号注册 1 月 8 日、摘要 1 月 14 日、全文 1 月 22 日、首轮拒稿 2 月 23 日、最终通知 5 月 3 日、Expo 7 月 31 日。地点为巴西里约热内卢。仅写日期的节点继续按全天记录。 |
| NeurIPS | [Future Meetings](https://neurips.cc/Conferences/FutureMeetings) | 只确认欧洲，具体地点、会期和投稿节点仍待公布。 |
| AAAI | [主技术赛道](https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/) | 原有 7 个节点保留；终稿条目仍有修订标记，明确列入待确认事项。作者回复采用更新后的 10 月 24–31 日。 |
| ACL | [主会征稿](https://2027.aclweb.org/calls/main/) | 最晚 ARR 为 1 月 4 日 23:59 AoE，主会 8 月 20–22 日。commitment 与录用时间仍未公布。保留两阶段投稿说明。 |
| KDD | [研究赛道第一轮](https://kdd2027.kdd.org/research-track-call-for-papers/)、[会期](https://kdd2027.kdd.org/) | 新增 5 个节点。第一轮摘要 2026-07-19、全文 07-26，回复 09-29 至 10-13，通知 11-14；大会 2027-08-01 至 08-05，圣何塞。第二轮只见月份提及，无完整日期表，不推算。 |
| SIGIR | [投稿总览及时间规则](https://sigir2027.org/pages/submit-tracks.html)、[长文征稿](https://sigir2027.org/pages/submit-full.html)、[分段会期](https://sigir2027.org/) | 新增 8 个长文 / 会期节点。摘要 1 月 14 日、全文 1 月 21 日、录用 4 月 5 日、终稿和作者注册 4 月 30 日；教程 7 月 19 日、主会 20–22 日、研讨会 23 日，圣何塞。投稿总览明确 23:59 AoE。官网总会期有 18–24 / 19–24 差异，采用明确分段，不将 24 日 ICTIR 并作 SIGIR 主会。 |
| WWW | [时间表](https://www2027.thewebconf.org/important-dates/)、[研究赛道](https://www2027.thewebconf.org/research-track-papers/)、[会期](https://www2027.thewebconf.org/) | 新增 10 个节点，区分长文和短文。录用 2027-01-04、终稿 01-31；研讨会 / 教程 05-10 至 05-11，主会 05-12 至 05-14，都柏林。研究问题需明确与 Web 相关。 |
| ECCV | [官方双数年办会说明](https://eccv.ecva.net/) | 无 ECCV 2027；只提供届次说明卡和官方入口，不编造截止日期，也不把 B 类归为 A 类。 |

## 数据与交互约定

- 截止时间只在官方明确时刻、时区或当日结束时编码为精确截止；“当日结束”按分钟精度 23:59 AoE 展示。录用通知和日期范围按全天表示，不附加虚构时刻。
- ICML / ICLR 原文只列日期的投稿节点保留全天，界面、倒计时逻辑和 ICS 一致。
- 待公布节点不生成 ICS；ECCV 说明也不进入全部日历。会期 `endExclusive` 为最后一天的下一天。
- 重点维护主研究赛道与会期；其他专项、资源、演示等赛道使用明确说明和官网入口，不将不同赛道混为同一截止。
- 快捷导航位于筛选栏下方。主导航按用户顺序排列，名称规范为 ACM MM 和 NeurIPS；更多方向补充 ICML、ACL、KDD、SIGIR、WWW。
- 会议被筛选隐藏时，点击快捷入口会解除阻挡目标的筛选并聚焦详情。支持直接哈希链接、键盘和手机触屏；关闭动效时直接定位。
- `calendarVerifiedAt` 独立记录会议核对日，不将其他资源一并标为本轮复核。
