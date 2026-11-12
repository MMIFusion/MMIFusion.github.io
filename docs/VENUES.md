# 投稿目录核对说明

核对日期：2026-11-12。共 183 项（109 本期刊、74 个会议）；页面位于 `venues.html`，原始维护数据为 `data/portal.json`。

## 分类依据

用户提供的 `第七版中国计算机学会推荐国际学术会议和期刊目录（正式版）.pdf`，72 页，封面标注 2026 年。文件 SHA-256：`271b630b576bf8a4f802e767f5694caded93680e22b3a19bef7902591c45c1d3`。PDF 不随网站公开分发，下表记录的页码均指文件页码；页面卡片不再展示页码行。

分类按该正式版文件，不混用旧版列表、影响因子或其他机构分类；[CCF 第七版发布说明](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-05/861526.shtml) 作为目录发布背景入口，不以公示稿替代所提供的正式版。

TMM、ICLR 为 A；IJCAI 为 B；PRCV 为 C。TGRS 在 PDF 中的简称写作 TGARS，按完整名称匹配，页面兼容两个简称检索。Information Fusion 未在该文件中收录，独立归为领域补充，不推测等级。

页面先按 A、B、C 展示，最后单列未收录补充项；同级按图像融合相关性组织，不声明同级内部权威排名。Proc. IEEE 的综述/教程取向、ACL 的语言导向、TGRS 和 TMI 的应用领域要求均在选刊建议中区分。

## 本轮筛选边界

从正式目录中的图形学与多媒体、人工智能、检索与数据挖掘、交叉应用，以及相关安全、交互条目筛选。共新增 145 项；A / B / C 分别 27 / 65 / 90 项，另有 1 项未收录补充。

- 直接方向：图像处理、视觉、计算成像、模式识别、多媒体、多模态学习。
- 方法方向：通用学习、统计推理、不确定性、模糊与进化优化；必须有相应方法或理论贡献。
- 应用方向：医学与遥感、机器人与工业、图文检索、文档与生物识别、图形与交互；必须满足领域任务要求。
- 不因“可以用到图像”就纳入纯网络协议、数据库事务、编程语言、密码学、商业管理等条目。纯语音、纯生物序列及无视觉关联的形式推理条目不作常规推荐。

这是对明确相关投稿方向的整理，不意味着所有条目都接受只有像素融合指标的论文。`scope` 概括公开研究领域；`fit` 是本站的条件性选刊判断，不是官方适配认证，也不承诺录用。研究方向可能交叉，一个条目可有多个 `focus`。

同一期刊跨领域重复出现时按完整名称去重：DKE（PDF 33 / 52 页）、IJIS（34 / 55 页）各保留一张卡片。会议与同名期刊、SIGGRAPH 会议轨道与 TOG 期刊轨道分别处理。常用简称和目录简称均可检索（TASE / TASAE、TRO / TR、TGRS / TGARS、MTA / MTAP、FITEE / EITEE）。

## 浏览与维护

`focus` 为七个投稿侧重，配合现有类型、CCF 和主题联合筛选。检索包含简称、全名、别名、主题、范围及选刊思路。分页发生在全部条目检索之后，每页 12 项；匹配数始终为全库结果。`page` URL 参数可恢复页码，`#venue-ID` 可定位跨页档案。对比选择跨页、跨筛选保留，上限 3 项；无 JavaScript 时保留完整静态目录。

本轮不改变会议日历范围，仍为已有 11 场 2027 A 类会议。KDD、SIGIR、WWW 投稿卡片连接已存在的日程；其他新增会议不虚构截止时间。引用 2026 官网的卡片明确标注年份。

## 来源可访问性

逐一请求新增官方入口，检查 HTTP 状态、最终域名和标题，并结合官网征稿/出版社范围页与目录核对。修复 CIKM 旧域名跳转无关网站、SGP/Eurographics 失效路径、ICANN 旧届跳转，替换 COLING、ICDAR、CVM、PG、ICDM、BigData 等入口。自动化读取遇到 ACM、Wiley、World Scientific、部分 IEEE 页面 403/418 限制时，不把限制当作停刊或链接失效；保留官方入口，范围采用公开期刊说明、学会页面或出版方索引能确认的层面，不声称已验证该站投稿系统。未对每个期刊作完整投稿政策审计。

不引用实时影响因子、分区、录用率、版面费、审稿速度或开放投稿状态。来源核对日期表示目录与公开资料整理时间，不表示征稿持续开放。来源访问证据保存在本地 QA 输出，网站不再显示 PDF 页码行。

## 条目与官方入口

| 条目 | 类型 | 分类 | PDF 页码 | 投稿侧重 | 官方入口 |
|---|---|---|---:|---|---|
| IEEE TPAMI | 期刊 | A | 51 | 图像与视觉、学习与推理 | [官方来源](https://www.computer.org/csdl/journal/tp/) |
| IJCV | 期刊 | A | 51 | 图像与视觉 | [官方来源](https://link.springer.com/journal/11263/aims-and-scope) |
| IEEE TIP | 期刊 | A | 44 | 图像与视觉 | [官方来源](https://signalprocessingsociety.org/publications-resources/ieee-transactions-image-processing/about-transactions-image-processing) |
| IEEE TMM | 期刊 | A | 44 | 多媒体融合 | [官方来源](https://signalprocessingsociety.org/publications-resources/ieee-transactions-multimedia) |
| AI | 期刊 | A | 51 | 学习与推理 | [官方来源](https://shop.elsevier.com/journals/artificial-intelligence/0004-3702) |
| Proc. IEEE | 期刊 | A | 67 | 机器人与工业、学习与推理 | [官方来源](https://proceedingsoftheieee.ieee.org/resources/preparing-your-regular-paper/) |
| CVPR | 会议 | A | 57 | 图像与视觉 | [官方来源](https://cvpr.thecvf.com/Conferences/2027/CallForPapers) |
| ICCV | 会议 | A | 57 | 图像与视觉 | [官方来源](https://iccv.thecvf.com/Conferences/2027) |
| ACM MM | 会议 | A | 47 | 多媒体融合 | [官方来源](https://www.acmmm.org/index.html) |
| NeurIPS | 会议 | A | 57 | 学习与推理 | [官方来源](https://neurips.cc/Conferences/2026/CallForPapers) |
| ICML | 会议 | A | 57 | 学习与推理 | [官方来源](https://icml.cc/Conferences/2027) |
| ICLR | 会议 | A | 57 | 学习与推理 | [官方来源](https://iclr.cc/Conferences/2027/CallForPapers) |
| AAAI | 会议 | A | 57 | 学习与推理 | [官方来源](https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/) |
| ACL | 会议 | A | 57 | 多媒体融合 | [官方来源](https://2027.aclweb.org/calls/main/) |
| JMLR | 期刊 | A | 51 | 学习与推理 | [官方来源](https://jmlr.org/author-info.html) |
| ACM TOG | 期刊 | A | 44 | 图形与交互 | [官方来源](https://dl.acm.org/journal/tog/about) |
| IEEE TVCG | 期刊 | A | 44 | 图形与交互 | [官方来源](https://www.computer.org/digital-library/journals/tg/cfp-ieee-transactions-on-visualization-computer-graphics) |
| ACM TOIS | 期刊 | A | 32 | 检索与挖掘 | [官方来源](https://dl.acm.org/journal/tois/about) |
| IEEE TKDE | 期刊 | A | 32 | 检索与挖掘 | [官方来源](https://www.computer.org/csdl/journal/tk) |
| IEEE TIFS | 期刊 | A | 17 | 图像与视觉 | [官方来源](https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security) |
| SCIS | 期刊 | A | 67 | 学习与推理、机器人与工业 | [官方来源](https://link.springer.com/journal/11432/aims-and-scope) |
| KDD | 会议 | A | 35 | 检索与挖掘 | [官方来源](https://kdd2027.kdd.org/research-track-call-for-papers/) |
| SIGIR | 会议 | A | 35 | 检索与挖掘 | [官方来源](https://sigir2027.org/pages/submit-tracks.html) |
| WWW | 会议 | A | 70 | 检索与挖掘、多媒体融合 | [官方来源](https://www2027.thewebconf.org/important-dates/) |
| SIGGRAPH | 会议 | A | 47 | 图形与交互 | [官方来源](https://s2026.siggraph.org/program/technical-papers/) |
| IEEE VR | 会议 | A | 47 | 图形与交互 | [官方来源](https://ieeevr.org/) |
| IEEE VIS | 会议 | A | 47 | 图形与交互 | [官方来源](https://ieeevis.org/year/2026/welcome/) |
| IEEE TCSVT | 期刊 | B | 45 | 图像与视觉 | [官方来源](https://ieee-cas.org/publication/tcsvt) |
| IEEE TNNLS | 期刊 | B | 52 | 学习与推理 | [官方来源](https://cis.ieee.org/publications/t-neural-networks-and-learning-systems) |
| Pattern Recognition | 期刊 | B | 53 | 图像与视觉 | [官方来源](https://shop.elsevier.com/journals/pattern-recognition/0031-3203) |
| Neural Networks | 期刊 | B | 53 | 学习与推理 | [官方来源](https://shop.elsevier.com/journals/neural-networks/0893-6080) |
| CVIU | 期刊 | B | 52 | 图像与视觉 | [官方来源](https://shop.elsevier.com/journals/computer-vision-and-image-understanding/1077-3142) |
| IEEE TGRS | 期刊 | B | 68 | 医学与遥感 | [官方来源](https://www.grss-ieee.org/publications/transactions-on-geoscience-remote-sensing/) |
| IEEE TMI | 期刊 | B | 68 | 医学与遥感 | [官方来源](https://ieeetmi.org/) |
| ECCV | 会议 | B | 58 | 图像与视觉 | [官方来源](https://eccv.ecva.net/Conferences/2026/CallForPapers) |
| IJCAI | 会议 | B | 58 | 学习与推理 | [官方来源](https://www.ijcai.org/) |
| ICASSP | 会议 | B | 48 | 图像与视觉、多媒体融合 | [官方来源](https://2027.ieeeicassp.org/call-for-papers/) |
| MICCAI | 会议 | B | 71 | 医学与遥感 | [官方来源](https://miccai.org/about-miccai/) |
| ACM TOMM | 期刊 | B | 45 | 多媒体融合 | [官方来源](https://dl.acm.org/journal/tomm/about) |
| SIIMS | 期刊 | B | 45 | 图像与视觉、学习与推理 | [官方来源](https://epubs.siam.org/journal/siims/editorial-policy) |
| Computational Visual Media | 期刊 | B | 45 | 图像与视觉、图形与交互 | [官方来源](https://www.sciopen.com/journal/2096-0433) |
| Computer Graphics Forum | 期刊 | B | 45 | 图形与交互 | [官方来源](https://www.eg.org/wp/eurographics-publications/cgf/) |
| IEEE TCYB | 期刊 | B | 52 | 学习与推理 | [官方来源](https://www.ieeesmc.org/publications/transactions-on-cybernetics/) |
| IEEE TFS | 期刊 | B | 52 | 学习与推理 | [官方来源](https://cis.ieee.org/publications/t-fuzzy-systems) |
| IJAR | 期刊 | B | 52 | 学习与推理 | [官方来源](https://shop.elsevier.com/journals/international-journal-of-approximate-reasoning/0888-613X) |
| Machine Learning | 期刊 | B | 53 | 学习与推理 | [官方来源](https://link.springer.com/journal/10994/aims-and-scope) |
| JAIR | 期刊 | B | 53 | 学习与推理 | [官方来源](https://www.jair.org/index.php/jair/about) |
| IEEE TAC | 期刊 | B | 52 | 多媒体融合 | [官方来源](https://www.computer.org/csdl/journal/ta) |
| ACM TAP | 期刊 | B | 52 | 图形与交互 | [官方来源](https://dl.acm.org/journal/tap/about) |
| IEEE TEC | 期刊 | B | 52 | 学习与推理 | [官方来源](https://cis.ieee.org/publications/t-evolutionary-computation) |
| ACM TKDD | 期刊 | B | 33 | 检索与挖掘 | [官方来源](https://dl.acm.org/journal/tkdd/about) |
| DMKD | 期刊 | B | 33 | 检索与挖掘 | [官方来源](https://link.springer.com/journal/10618/aims-and-scope) |
| Information Sciences | 期刊 | B | 33 | 学习与推理、检索与挖掘 | [官方来源](https://shop.elsevier.com/journals/information-sciences/0020-0255) |
| KAIS | 期刊 | B | 33 | 检索与挖掘 | [官方来源](https://link.springer.com/journal/10115/aims-and-scope) |
| IPM | 期刊 | B | 33 | 检索与挖掘 | [官方来源](https://shop.elsevier.com/journals/information-processing-and-management/0306-4573) |
| Advanced Engineering Informatics | 期刊 | B | 33 | 机器人与工业 | [官方来源](https://shop.elsevier.com/journals/advanced-engineering-informatics/1474-0346) |
| IEEE TASE | 期刊 | B | 68 | 机器人与工业 | [官方来源](https://www.ieee-ras.org/publications/t-ase) |
| IEEE TITS | 期刊 | B | 68 | 机器人与工业 | [官方来源](https://ieee-itss.org/pub/t-its/) |
| IEEE TRO | 期刊 | B | 68 | 机器人与工业 | [官方来源](https://www.ieee-ras.org/publications/t-ro) |
| JCST | 期刊 | B | 68 | 图像与视觉、学习与推理 | [官方来源](https://link.springer.com/journal/11390/aims-and-scope) |
| Frontiers of Computer Science | 期刊 | B | 68 | 图像与视觉、学习与推理 | [官方来源](https://link.springer.com/journal/11704/aims-and-scope) |
| IEEE TSMC: Systems | 期刊 | B | 62 | 机器人与工业、学习与推理 | [官方来源](https://www.ieeesmc.org/publications/transactions-on-smc-systems/) |
| Neural Computation | 期刊 | B | 53 | 学习与推理 | [官方来源](https://direct.mit.edu/neco) |
| GeoInformatica | 期刊 | B | 33 | 医学与遥感、检索与挖掘 | [官方来源](https://link.springer.com/journal/10707/aims-and-scope) |
| Data & Knowledge Engineering | 期刊 | B | 33 / 52 | 检索与挖掘 | [官方来源](https://shop.elsevier.com/journals/data-and-knowledge-engineering/0169-023X) |
| Evolutionary Computation | 期刊 | B | 52 | 学习与推理 | [官方来源](https://direct.mit.edu/evco) |
| IEEE TASLP | 期刊 | B | 52 | 多媒体融合 | [官方来源](https://signalprocessingsociety.org/publications-resources/ieee-transactions-audio-speech-and-language-processing) |
| TACL | 期刊 | B | 53 | 多媒体融合 | [官方来源](https://transacl.org/index.php/tacl/about) |
| IEEE THMS | 期刊 | B | 62 | 图形与交互、多媒体融合 | [官方来源](https://www.ieeesmc.org/publications/transactions-on-human-machine-systems/) |
| ACM ICMR | 会议 | B | 48 | 检索与挖掘、多媒体融合 | [官方来源](https://www.acmicmr.org/) |
| IEEE ICME | 会议 | B | 48 | 多媒体融合 | [官方来源](https://2027.ieeeicme.org/) |
| ECAI | 会议 | B | 58 | 学习与推理 | [官方来源](https://2026.ijcai.org/ijcai-ecai-2026-call-for-papers-main-track/) |
| UAI | 会议 | B | 58 | 学习与推理 | [官方来源](https://www.auai.org/) |
| ICRA | 会议 | B | 58 | 机器人与工业 | [官方来源](https://2027.ieee-icra.org/contribute/) |
| AAMAS | 会议 | B | 58 | 机器人与工业、学习与推理 | [官方来源](https://www.ifaamas.org/) |
| EMNLP | 会议 | B | 58 | 多媒体融合 | [官方来源](https://2026.emnlp.org/) |
| NAACL | 会议 | B | 58 | 多媒体融合 | [官方来源](https://naacl.org/) |
| COLING | 会议 | B | 58 | 多媒体融合 | [官方来源](https://2027.coling-iccl.org/calls/main_conference_papers/) |
| COLT | 会议 | B | 58 | 学习与推理 | [官方来源](https://www.learningtheory.org/) |
| CIKM | 会议 | B | 36 | 检索与挖掘 | [官方来源](https://cikm2026.diag.uniroma1.it/full-research-papers/) |
| WSDM | 会议 | B | 36 | 检索与挖掘 | [官方来源](https://www.wsdm-conference.org/) |
| IEEE ICDM | 会议 | B | 36 | 检索与挖掘 | [官方来源](https://icdm2026.neu.edu.cn/) |
| SDM | 会议 | B | 36 | 检索与挖掘 | [官方来源](https://www.siam.org/conferences-events/siam-conferences/sdm26/) |
| ECML-PKDD | 会议 | B | 36 | 学习与推理、检索与挖掘 | [官方来源](https://ecmlpkdd.org/) |
| RecSys | 会议 | B | 36 | 检索与挖掘 | [官方来源](https://recsys.acm.org/) |
| Eurographics | 会议 | B | 48 | 图形与交互 | [官方来源](https://eg2026.github.io/) |
| SGP | 会议 | B | 48 | 图形与交互 | [官方来源](https://sgp26.org/) |
| EGSR | 会议 | B | 48 | 图形与交互 | [官方来源](https://egsr2026.inria.fr/) |
| I3D | 会议 | B | 48 | 图形与交互 | [官方来源](https://i3dsymposium.org/) |
| ISMAR | 会议 | B | 48 | 图形与交互、机器人与工业 | [官方来源](https://ismar.org/) |
| Pacific Graphics | 会议 | B | 48 | 图形与交互 | [官方来源](https://pacificgraphics2026.github.io/) |
| DCC | 会议 | B | 48 | 图像与视觉 | [官方来源](https://datacompressionconference.org/) |
| Signal Processing | 期刊 | C | 46 | 图像与视觉 | [官方来源](https://shop.elsevier.com/journals/signal-processing/0165-1684) |
| Knowledge-Based Systems | 期刊 | C | 55 | 学习与推理 | [官方来源](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) |
| EAAI | 期刊 | C | 54 | 机器人与工业 | [官方来源](https://shop.elsevier.com/journals/engineering-applications-of-artificial-intelligence/0952-1976) |
| ESWA | 期刊 | C | 54 | 学习与推理、机器人与工业 | [官方来源](https://shop.elsevier.com/journals/expert-systems-with-applications/0957-4174) |
| Image and Vision Computing | 期刊 | C | 55 | 图像与视觉 | [官方来源](https://shop.elsevier.com/journals/image-and-vision-computing/0262-8856) |
| IET Image Processing | 期刊 | C | 46 | 图像与视觉 | [官方来源](https://ietresearch.onlinelibrary.wiley.com/journal/17519667) |
| IET Signal Processing | 期刊 | C | 54 | 图像与视觉 | [官方来源](https://ietresearch.onlinelibrary.wiley.com/page/journal/ietsp/homepage/productinformation.html) |
| IEEE GRSL | 期刊 | C | 69 | 医学与遥感 | [官方来源](https://www.grss-ieee.org/publications/geoscience-and-remote-sensing-letters/) |
| Medical Image Analysis | 期刊 | C | 69 | 医学与遥感 | [官方来源](https://shop.elsevier.com/journals/medical-image-analysis/1361-8415) |
| PRCV | 会议 | C | 49 | 图像与视觉 | [官方来源](https://www.prcv.cn/web/) |
| ACCV | 会议 | C | 59 | 图像与视觉 | [官方来源](https://accv2026.org/submissions/) |
| ICIP | 会议 | C | 49 | 图像与视觉 | [官方来源](https://signalprocessingsociety.org/our-story/news-updates/2026/11/ieee-signal-processing-society-announces-2027-summit-singapore) |
| IEEE SPL | 期刊 | C | 46 | 图像与视觉 | [官方来源](https://signalprocessingsociety.org/publications-resources/ieee-signal-processing-letters) |
| JVCIR | 期刊 | C | 46 | 图像与视觉 | [官方来源](https://shop.elsevier.com/journals/journal-of-visual-communication-and-image-representation/1047-3203) |
| Image Communication | 期刊 | C | 46 | 图像与视觉 | [官方来源](https://shop.elsevier.com/journals/signal-processing-image-communication/0923-5965) |
| Multimedia Systems | 期刊 | C | 46 | 多媒体融合 | [官方来源](https://link.springer.com/journal/530/aims-and-scope) |
| Multimedia Tools and Applications | 期刊 | C | 46 | 多媒体融合 | [官方来源](https://link.springer.com/journal/11042/aims-and-scope) |
| The Visual Computer | 期刊 | C | 46 | 图像与视觉、图形与交互 | [官方来源](https://link.springer.com/journal/371/aims-and-scope) |
| Computers & Graphics | 期刊 | C | 46 | 图形与交互 | [官方来源](https://shop.elsevier.com/journals/computers-and-graphics/0097-8493) |
| Visual Informatics | 期刊 | C | 46 | 图形与交互、图像与视觉 | [官方来源](https://www.sciencedirect.com/journal/visual-informatics) |
| Virtual Reality & Intelligent Hardware | 期刊 | C | 46 | 图形与交互、机器人与工业 | [官方来源](https://www.sciencedirect.com/journal/virtual-reality-and-intelligent-hardware) |
| IET Computer Vision | 期刊 | C | 54 | 图像与视觉 | [官方来源](https://ietresearch.onlinelibrary.wiley.com/journal/17519640) |
| Neurocomputing | 期刊 | C | 56 | 学习与推理、图像与视觉 | [官方来源](https://shop.elsevier.com/journals/neurocomputing/0925-2312) |
| Pattern Recognition Letters | 期刊 | C | 56 | 图像与视觉 | [官方来源](https://shop.elsevier.com/journals/pattern-recognition-letters/0167-8655) |
| Pattern Analysis and Applications | 期刊 | C | 56 | 图像与视觉、学习与推理 | [官方来源](https://link.springer.com/journal/10044/aims-and-scope) |
| Neural Computing and Applications | 期刊 | C | 55 | 学习与推理 | [官方来源](https://link.springer.com/journal/521/aims-and-scope) |
| Neural Processing Letters | 期刊 | C | 56 | 学习与推理 | [官方来源](https://link.springer.com/journal/11063/aims-and-scope) |
| Applied Intelligence | 期刊 | C | 54 | 学习与推理、机器人与工业 | [官方来源](https://link.springer.com/journal/10489/aims-and-scope) |
| Machine Vision and Applications | 期刊 | C | 55 | 图像与视觉、机器人与工业 | [官方来源](https://link.springer.com/journal/138/aims-and-scope) |
| International Journal of Intelligent Systems | 期刊 | C | 34 / 55 | 学习与推理 | [官方来源](https://onlinelibrary.wiley.com/journal/1098111x) |
| Fuzzy Sets and Systems | 期刊 | C | 54 | 学习与推理 | [官方来源](https://shop.elsevier.com/journals/fuzzy-sets-and-systems/0165-0114) |
| Soft Computing | 期刊 | C | 56 | 学习与推理 | [官方来源](https://link.springer.com/journal/500/aims-and-scope) |
| IJCIA | 期刊 | C | 55 | 学习与推理 | [官方来源](https://www.worldscientific.com/worldscinet/ijcia) |
| IJPRAI | 期刊 | C | 55 | 图像与视觉、学习与推理 | [官方来源](https://www.worldscientific.com/worldscinet/ijprai) |
| IJUFKS | 期刊 | C | 55 | 学习与推理 | [官方来源](https://www.worldscientific.com/worldscinet/ijufks) |
| IJDAR | 期刊 | C | 55 | 图像与视觉 | [官方来源](https://link.springer.com/journal/10032/aims-and-scope) |
| Intelligent Data Analysis | 期刊 | C | 55 | 检索与挖掘、学习与推理 | [官方来源](https://journals.sagepub.com/home/ida) |
| Artificial Intelligence in Medicine | 期刊 | C | 54 | 医学与遥感 | [官方来源](https://shop.elsevier.com/journals/artificial-intelligence-in-medicine/0933-3657) |
| IEEE JBHI | 期刊 | C | 69 | 医学与遥感 | [官方来源](https://www.embs.org/jbhi/) |
| Journal of Biomedical Informatics | 期刊 | C | 69 | 医学与遥感 | [官方来源](https://shop.elsevier.com/journals/journal-of-biomedical-informatics/1532-0464) |
| IEEE TII | 期刊 | C | 69 | 机器人与工业 | [官方来源](https://www.ieee-ies.org/pubs/transactions-on-industrial-informatics) |
| IEEE TBD | 期刊 | C | 69 | 检索与挖掘 | [官方来源](https://www.computer.org/csdl/journal/bd) |
| ACM TIST | 期刊 | C | 34 | 学习与推理、机器人与工业 | [官方来源](https://dl.acm.org/journal/tist/about) |
| ACM JATS | 期刊 | C | 56 | 机器人与工业 | [官方来源](https://dl.acm.org/journal/jats/about) |
| ACM TCPS | 期刊 | C | 69 | 机器人与工业 | [官方来源](https://dl.acm.org/journal/tcps/about) |
| ACM HEALTH | 期刊 | C | 69 | 医学与遥感 | [官方来源](https://dl.acm.org/journal/health/about) |
| IET Intelligent Transport Systems | 期刊 | C | 69 | 机器人与工业 | [官方来源](https://ietresearch.onlinelibrary.wiley.com/journal/17519578) |
| Computer Animation & Virtual Worlds | 期刊 | C | 46 | 图形与交互 | [官方来源](https://onlinelibrary.wiley.com/journal/1546427x) |
| Graphical Models | 期刊 | C | 46 | 图形与交互 | [官方来源](https://shop.elsevier.com/journals/graphical-models/1524-0703) |
| Computational Intelligence | 期刊 | C | 54 | 学习与推理 | [官方来源](https://onlinelibrary.wiley.com/journal/14678640) |
| Connection Science | 期刊 | C | 54 | 学习与推理 | [官方来源](https://www.tandfonline.com/journals/ccos20) |
| Expert Systems | 期刊 | C | 54 | 学习与推理、机器人与工业 | [官方来源](https://onlinelibrary.wiley.com/journal/14680394) |
| IJNS | 期刊 | C | 55 | 学习与推理、医学与遥感 | [官方来源](https://www.worldscientific.com/worldscinet/ijns) |
| JETAI | 期刊 | C | 55 | 学习与推理 | [官方来源](https://www.tandfonline.com/journals/teta20) |
| JIIS | 期刊 | C | 34 | 检索与挖掘、学习与推理 | [官方来源](https://link.springer.com/journal/10844/aims-and-scope) |
| IJGIS | 期刊 | C | 34 | 医学与遥感、检索与挖掘 | [官方来源](https://www.tandfonline.com/journals/tgis20) |
| ACM TELO | 期刊 | C | 56 | 学习与推理 | [官方来源](https://dl.acm.org/journal/telo/about) |
| ACM TORS | 期刊 | C | 34 | 检索与挖掘 | [官方来源](https://dl.acm.org/journal/tors/about) |
| ACM TIIS | 期刊 | C | 56 | 图形与交互、多媒体融合 | [官方来源](https://dl.acm.org/journal/tiis/about) |
| EITEE | 期刊 | C | 69 | 图像与视觉、机器人与工业 | [官方来源](https://www.academax.com/EITEE/home) |
| BMVC | 会议 | C | 59 | 图像与视觉 | [官方来源](https://bmvc2026.bmva.org/calls/call-for-papers/) |
| ICPR | 会议 | C | 60 | 图像与视觉 | [官方来源](https://icpr2026.org/) |
| 3DV | 会议 | C | 49 | 图像与视觉、图形与交互 | [官方来源](https://3dvconf.github.io/2027/call-for-papers/) |
| MMM | 会议 | C | 49 | 多媒体融合 | [官方来源](https://mmm2027.net/home) |
| ACM MM Asia | 会议 | C | 49 | 多媒体融合 | [官方来源](https://www.acmmmasia.org/) |
| CVM | 会议 | C | 49 | 图像与视觉、图形与交互 | [官方来源](https://iccvm.org/2026/index.htm) |
| ICIG | 会议 | C | 50 | 图像与视觉、图形与交互 | [官方来源](https://link.springer.com/conference/icig) |
| AISTATS | 会议 | C | 59 | 学习与推理 | [官方来源](https://virtual.aistats.org/Conferences/2027/CallForPapers) |
| ACML | 会议 | C | 59 | 学习与推理 | [官方来源](https://www.acml-conf.org/2026/calls/papers/) |
| ICANN | 会议 | C | 59 | 学习与推理 | [官方来源](https://e-nns.org/icann2026/) |
| IJCNN | 会议 | C | 60 | 学习与推理 | [官方来源](https://ijcnn.org/2027/authors/call-for-papers) |
| ICONIP | 会议 | C | 60 | 学习与推理 | [官方来源](https://iconip2026.org/call-for-papers) |
| PRICAI | 会议 | C | 60 | 学习与推理 | [官方来源](https://2026.pricai.org/calls/call-for-papers) |
| IROS | 会议 | C | 59 | 机器人与工业 | [官方来源](https://www.ieee-ras.org/conferences-workshops/financially-co-sponsored/iros/) |
| IJCB | 会议 | C | 60 | 图像与视觉 | [官方来源](https://ieee-biometrics.org/conferences/) |
| FG | 会议 | C | 59 | 图像与视觉、多媒体融合 | [官方来源](https://fg2026.ieee-biometrics.org/) |
| ICDAR | 会议 | C | 60 | 图像与视觉、多媒体融合 | [官方来源](https://icdar2027.org/call-for-papers) |
| PAKDD | 会议 | C | 37 | 检索与挖掘 | [官方来源](https://pakdd.org/) |
| ADMA | 会议 | C | 37 | 检索与挖掘 | [官方来源](https://adma2026.github.io/) |
| ECIR | 会议 | C | 37 | 检索与挖掘 | [官方来源](https://www.bcs.org/membership-and-registrations/member-communities/information-retrieval-specialist-group/conferences-and-events/) |
| ACM ICMI | 会议 | C | 66 | 多媒体融合、图形与交互 | [官方来源](https://icmi.acm.org/) |
| IEEE ICTAI | 会议 | C | 59 | 学习与推理、机器人与工业 | [官方来源](https://ictai.com/) |
| IEEE SMC | 会议 | C | 72 | 机器人与工业、学习与推理 | [官方来源](https://www.ieeesmc.org/conferences/) |
| ICIC | 会议 | C | 72 | 学习与推理、机器人与工业 | [官方来源](https://link.springer.com/conference/icic) |
| GECCO | 会议 | C | 59 | 学习与推理 | [官方来源](https://gecco-2026.sigevo.org/) |
| IEEE CEC | 会议 | C | 60 | 学习与推理 | [官方来源](https://cis.ieee.org/conferences/conference-calendar) |
| ALT | 会议 | C | 59 | 学习与推理 | [官方来源](https://algorithmiclearningtheory.org/) |
| ACM VRST | 会议 | C | 49 | 图形与交互 | [官方来源](https://vrst.acm.org/) |
| ACM SIGSPATIAL | 会议 | C | 72 | 医学与遥感、检索与挖掘 | [官方来源](https://www.sigspatial.org/) |
| IEEE BigData | 会议 | C | 72 | 检索与挖掘 | [官方来源](https://bigdataieee.org/BigData2026/calls/papers/) |
| Information Fusion | 期刊 | 未收录 | — | 图像与视觉、多媒体融合 | [官方来源](https://shop.elsevier.com/journals/information-fusion/1566-2535) |
