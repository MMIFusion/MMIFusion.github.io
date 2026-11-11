# 融合团队目录维护说明

本轮根据用户提供的团队资料，整理为 27 组团队与学者（20 组已有简介、7 组原为名单占位）。顺序沿用来源，不作排名。整理核对日期：2026-11-11。

## 来源与编辑规则

原始压缩包名称和 SHA-256 记录在 `data/portal.json` 的 `teamCollection`。原资料保留在用户本地，网站只收录简短研究介绍、成员线索和公开学术入口，不转载长篇履历或原始照片。学校、研究组与研究者个人主页用于交叉核对。

- `members` 表示关联展示的学者，不将同组所有人都写成负责人，也不推断固定隶属关系。
- 任职机构与既有研究团队分别表述；不将旧团队的所有成员随导师迁移到新机构。
- 不收录易过期的论文数、引用数、H 指数、行政职务或未经核实的招生名额。
- `verification` 为 `official`（主要信息经学校/本人页核对）、`conference`（会议官方介绍）或 `archive`（按所供资料整理，主页访问待核）。页面展示相应状态。
- `sourceLabel` 区分教师主页、团队入口与会议简介；`links` 保存补充学术入口。
- `cities` 支持多地区筛选；未知地区明确显示，不猜测。
- `aliases` 兼容原资料中的错字或旧机构搜索，页面显示规范姓名与核实后的机构。
- 保留已有 `jiayi-ma`、`vlog` 锚点及 `vlog-open` 招生关联，复制链接直达条目。

## 本轮关键校正

- 杨杨改为杨扬，徐函改为徐涵，均依学校主页；西北工业大学的徐爽写法保持不变。
- 赵子祥当前机构按个人主页列 ETH Zürich，西安交通大学作为博士培养单位写入展开说明。
- 朱鹏飞以东南大学展示个人机构，VISDRONE 实验室多单位共建信息独立说明。
- 王海鹏按 2026 IEEE ICUS 官方简介显示海军研究院；原资料的海军航空大学在备注中保留，地区待核。
- 何友为清华电子系双聘教授，并有深圳海洋工程研究院介绍；北京和深圳均可筛选。
- 李树涛任职机构与既有湖南大学团队分开呈现。
- 佛山大学李小松、黎熹来条目依据所供资料整理；教师页未完成访问核验，页面明确标注，不写作已核验。

## 社区成员与署名

`data/site.json` 的 `members` 控制“关于我们”的有序展示：汐萌、囗〇为已激活，木木彡、蓝白红为未激活席位。此状态仅为展示，不是账户或登录功能。

全站页脚统一使用公众号署名。只有 `datasets.html` 保留汐萌、囗〇的整理署名；数据资源原有寄语和版权说明保留。后续页面通过 `scripts/build.py` 的统一 footer 规则生成。

## 目录与核对入口

补充核对链接保存在 `data/portal.json` 的各条 `links` 字段中。七组原名单占位已按公开来源补充简介。

| 学者 | 机构 | 主入口 | 核对状态 |
|---|---|---|---|
| 马佳义, 唐霖峰 | 武汉大学 | [Source](https://jiayi-ma.github.io/index.html) | official |
| 刘日升, 刘晋源 | 大连理工大学 | [Source](https://rsliu.tech/) | official |
| 吴小俊, 李辉, 徐天阳 | 江南大学 | [Source](https://kjc.jiangnan.edu.cn/jgsz/wxj1.htm) | official |
| 刘羽 | 合肥工业大学 | [Source](https://yuliu316316.github.io/) | official |
| 胡清华, 曹兵 | 天津大学 | [Source](https://cic.tju.edu.cn/faculty/huqinghua/index.html) | official |
| 朱鹏飞 | 东南大学 | [Source](https://aiskyeye.com/) | official |
| 赵子祥 | ETH Zürich | [Source](https://zhaozixiang1228.github.io/) | official |
| 徐迈 | 北京航空航天大学 | [Source](https://shi.buaa.edu.cn/MaiXu/zh_CN/) | official |
| 祝闯 | 北京邮电大学 | [Source](https://github.com/bupt-ai-cz) | official |
| 岳裕丰 | 北京理工大学 | [Source](https://yfyue-bit.github.io/) | official |
| 李华锋, 张亚飞 | 昆明理工大学 | [Source](https://lhf12278.github.io/) | official |
| 杨扬 | 云南师范大学 | [Source](https://cic.ynnu.edu.cn/info/1056/1078.htm) | official |
| 李小松, 黎熹来 | 佛山大学 | [Source](https://www.fosu.edu.cn/spoe/yanjiu/ssds/gxgc/11653.html) | archive |
| 徐涵 | 东南大学 | [Source](https://automation.seu.edu.cn/xh/) | official |
| 徐爽 | 西北工业大学 | [Source](https://shuangxu96.github.io/) | official |
| 王泽宇 | 大连民族大学 | [Source](https://new.dlnu.edu.cn/comd/info/1235/1046.htm) | official |
| 姜智颖 | 大连海事大学 | [Source](https://ist.dlmu.edu.cn/info/1287/6828.htm) | official |
| 江俊君 | 哈尔滨工业大学 | [Source](https://homepage.hit.edu.cn/jiangjunjun) | official |
| 张星辰 | 英国埃克塞特大学 | [Source](https://xingchenzhang.github.io/) | official |
| 卢湖川 | 大连理工大学 | [Source](https://faculty.dlut.edu.cn/Huchuan_Lu/zh_CN/index.htm) | official |
| 邓良剑 | 电子科技大学 | [Source](https://yjsjy.uestc.edu.cn/gmis/jcsjgl/dsfc/dsgrjj/20071?yxsh=11) | official |
| 钱文华 | 云南大学 | [Source](https://www.ise.ynu.edu.cn/faculty/152/) | official |
| 赵文达 | 大连理工大学 | [Source](https://faculty.dlut.edu.cn/wdzhao/zh_CN/index.htm) | official |
| 李杏峰 | 西南科技大学 | [Source](https://lee-xingfeng.github.io/) | official |
| 王海鹏 | 海军研究院 | [Source](https://icus.c2.org.cn/uploads/admin/202604213007/69e6e23002bad.pdf) | conference |
| 何友 | 清华大学 | [Source](https://ioe.sigs.tsinghua.edu.cn/2022/0328/c4348a31571/page.psp) | official |
| 李树涛 | 长安大学 | [Source](https://www.chd.edu.cn/info/1059/1048.htm) | official |
