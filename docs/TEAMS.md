# 融合团队目录维护说明

根据用户提供的 27 组资料（20 组已有简介、7 组原为名单占位），拆分为 34 位研究者，一人一卡。前四位固定为马佳义、刘日升、吴小俊、刘羽；其余按学术资历、研究关联与同校归组形成编辑顺序，不作为量化声誉排名。整理核对日期：2026-11-11。

## 来源与编辑规则

原始压缩包名称和 SHA-256 记录在 `data/portal.json` 的 `teamCollection`。原资料保留在用户本地，网站只收录简短研究介绍、成员线索和公开学术入口，不转载长篇履历或原始照片。学校、研究组与研究者个人主页用于交叉核对。

- 每条 `members` 仅有一人，与 `name`、`lead` 一致。个人主页、Google Scholar、简介必须对应本人，不能沿用原分组中其他学者的资料。
- 任职机构与既有研究团队分别表述；不将旧团队的所有成员随导师迁移到新机构。
- 不收录易过期的论文数、引用数、H 指数、行政职务或未经核实的招生名额。
- `verification` 为 `official`（主要信息经学校/本人页核对）、`conference`（会议官方介绍）、`publication`（公开论文与作者项目）或 `archive`（按所供资料整理，主页访问待核）。页面展示相应状态。
- `sourceLabel` 区分教师主页、团队入口与会议简介；`links` 保存补充学术入口。
- `cities` 支持多地区筛选；未知地区明确显示，不猜测。
- `aliases` 兼容原资料中的错字或旧机构搜索，页面显示规范姓名与核实后的机构。
- 保留已有 `jiayi-ma`、`vlog` 锚点及 `vlog-open` 招生关联，复制链接直达条目。
- 展示顺序沿用既有编排：张星辰、赵子祥依次置于徐涵之前；末尾先列佛山地区（李小松、黎熹来），再列云南地区（李华锋、张亚飞、杨扬、钱文华）。其余研究者的相对顺序保持不变。

## 本轮关键校正

- 杨杨改为杨扬，徐函改为徐涵，均依学校主页；西北工业大学的徐爽写法保持不变。
- 赵子祥当前机构按个人主页列 ETH Zürich，西安交通大学作为博士培养单位写入展开说明。
- 朱鹏飞以东南大学展示个人机构，VISDRONE 实验室多单位共建信息独立说明。
- 王海鹏按 2026 IEEE ICUS 官方简介显示海军研究院；原资料的海军航空大学在备注中保留，地区待核。
- 何友为清华电子系双聘教授，并有深圳海洋工程研究院介绍；北京和深圳均可筛选。
- 李树涛任职机构与既有湖南大学团队分开呈现。
- 李小松的教师页未完成访问核验，明确标注。黎熹来独立以 UP-Fusion 作者仓库与公开论文建卡，机构依论文署名，不添加未经核实的职称。注意不能使用另一位同音学者“李曦来”的主页。
- 李辉与徐天阳均使用各自个人主页及各自 Google Scholar，不复用吴小俊的链接。李辉本人主页所链接的旧学校页面已失效，不加入目录。

## 社区成员与署名

`data/site.json` 的 `members` 控制“关于我们”的有序展示。`status` 为 `active` 或 `departed`；汐萌、囗〇保留当前状态，不显示额外说明，木木彡、蓝白红灰色展示“已退出”和“感谢参与”。此状态仅用于展示。

全站页脚（包括数据资源页）统一只使用公众号署名。数据资源正文原有整理寄语和来源说明保留。所有页面通过 `scripts/build.py` 的统一 footer 规则生成。

## 目录与核对入口

补充核对链接保存在 `data/portal.json` 的各条 `links` 字段中。七组原名单占位已按公开来源补充简介。

| 学者 | 机构 | 主入口 | 核对状态 |
|---|---|---|---|
| 马佳义 | 武汉大学 | [Source](https://jiayi-ma.github.io/index.html) | official |
| 刘日升 | 大连理工大学 | [Source](https://rsliu.tech/) | official |
| 吴小俊 | 江南大学 | [Source](https://kjc.jiangnan.edu.cn/jgsz/wxj1.htm) | official |
| 刘羽 | 合肥工业大学 | [Source](https://yuliu316316.github.io/) | official |
| 何友 | 清华大学 | [Source](https://ioe.sigs.tsinghua.edu.cn/2022/0328/c4348a31571/page.psp) | official |
| 李树涛 | 长安大学 | [Source](https://www.chd.edu.cn/info/1059/1048.htm) | official |
| 卢湖川 | 大连理工大学 | [Source](https://faculty.dlut.edu.cn/Huchuan_Lu/zh_CN/index.htm) | official |
| 刘晋源 | 大连理工大学 | [Source](https://faculty.dlut.edu.cn/liujinyuan1/zh_CN/index.htm) | official |
| 赵文达 | 大连理工大学 | [Source](https://faculty.dlut.edu.cn/wdzhao/zh_CN/index.htm) | official |
| 胡清华 | 天津大学 | [Source](https://cic.tju.edu.cn/faculty/huqinghua/index.html) | official |
| 曹兵 | 天津大学 | [Source](https://bcaosudo.github.io/) | official |
| 江俊君 | 哈尔滨工业大学 | [Source](https://homepage.hit.edu.cn/jiangjunjun) | official |
| 徐迈 | 北京航空航天大学 | [Source](https://shi.buaa.edu.cn/MaiXu/zh_CN/) | official |
| 朱鹏飞 | 东南大学 | [Source](https://aiskyeye.com/) | official |
| 张星辰 | 英国埃克塞特大学 | [Source](https://xingchenzhang.github.io/) | official |
| 赵子祥 | ETH Zürich | [Source](https://zhaozixiang1228.github.io/) | official |
| 徐涵 | 东南大学 | [Source](https://automation.seu.edu.cn/xh/) | official |
| 邓良剑 | 电子科技大学 | [Source](https://yjsjy.uestc.edu.cn/gmis/jcsjgl/dsfc/dsgrjj/20071?yxsh=11) | official |
| 李辉 | 江南大学 | [Source](https://hli1221.github.io/) | official |
| 徐天阳 | 江南大学 | [Source](https://xu-tianyang.github.io/) | official |
| 祝闯 | 北京邮电大学 | [Source](https://github.com/bupt-ai-cz) | official |
| 岳裕丰 | 北京理工大学 | [Source](https://yfyue-bit.github.io/) | official |
| 王海鹏 | 海军研究院 | [Source](https://icus.c2.org.cn/uploads/admin/202604213007/69e6e23002bad.pdf) | conference |
| 徐爽 | 西北工业大学 | [Source](https://shuangxu96.github.io/) | official |
| 李杏峰 | 西南科技大学 | [Source](https://lee-xingfeng.github.io/) | official |
| 唐霖峰 | 武汉大学 | [Source](https://linfeng-tang.github.io/zh/) | official |
| 王泽宇 | 大连民族大学 | [Source](https://new.dlnu.edu.cn/comd/info/1235/1046.htm) | official |
| 姜智颖 | 大连海事大学 | [Source](https://ist.dlmu.edu.cn/info/1287/6828.htm) | official |
| 李小松 | 佛山大学 | [Source](https://www.fosu.edu.cn/spoe/yanjiu/ssds/gxgc/11653.html) | archive |
| 黎熹来 | 佛山大学 | [Source](https://github.com/ixilai/UP-Fusion) | publication |
| 李华锋 | 昆明理工大学 | [Source](https://lhf12278.github.io/) | official |
| 张亚飞 | 昆明理工大学 | [Source](https://xzy.kmust.edu.cn/info/1127/3838.htm) | official |
| 杨扬 | 云南师范大学 | [Source](https://cic.ynnu.edu.cn/info/1056/1078.htm) | official |
| 钱文华 | 云南大学 | [Source](https://www.ise.ynu.edu.cn/faculty/152/) | official |
