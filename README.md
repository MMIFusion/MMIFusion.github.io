# 多模态信息融合 · 学术主页

公众号「多模态信息融合」的学术资源主站。

主站地址：https://mmifusion.github.io/

数据集独立站：https://mmifusion.github.io/Datasets/

## 已有功能

- 公众号原始文章标题、日期与微信原文链接。
- 关键词、文章类型、研究方向、会议期刊组合筛选，排序和分页。
- 可分享筛选后的地址；按 `/` 聚焦搜索；手机导航。
- 八个栏目：论文阅读、数据集、评估指标、融合团队、会议时间、会议期刊推荐、导师招生、配色模板。
- 基础配色点击复制，公众号入口、交流微信与资源投稿链接。
- 无 JavaScript 时仍能阅读完整文章目录。
- 数据和页面分离，无第三方字体、追踪脚本或在线运行依赖。

## 本地运行

使用 Python 3.10 或更新版本，无需安装依赖。

```sh
python3 scripts/build.py
python3 scripts/check.py
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
python3 scripts/build.py
python3 scripts/check.py
```

导入会重建文章目录，请使用包含全部待收录文章的完整导出表。原始表格保留在本机，不要提交到公开仓库。导入只保留公开文章字段，不发布阅读、转发、赞赏等运营统计。标题相同而微信文章标识不同的记录分别保留。微信链接使用 HTTPS，保留定位文章所需参数，移除会话和场景跟踪参数。

详细字段与维护流程见 [内容维护说明](docs/MAINTENANCE.md)。

代码与文档：Copyright (c) 2026 公众号「多模态信息融合」。整理与维护：汐萌、囗〇。

原创代码采用 MIT License。头像、文章及第三方内容的权利归各自权利人；代码许可不扩展到这些内容。
