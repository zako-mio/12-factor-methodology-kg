# 12factor.net 站点源码 (12factor.net Jekyll Site)

- ID: `tool-app-site`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 基础 basic

> 官方文档站自身即 Jekyll 应用，是 App 原则的参考实现

## 核心主张 (what)

- 12factor.net 官网是 Sinatra（web.rb）+ ERB 视图的 Ruby 应用，Jekyll 式 content/ 内容目录，部署在 Heroku
- Procfile 仅一行 `web: ruby web.rb -p $PORT`，web 进程经 web.rb 启动，端口来自 $PORT 环境变量（端口绑定原则）
- web.rb 实现 i18n 多语言（locales/*.yml）、/blog、/community、/sitemap.xml 动态生成、www→裸域 301 重定向、可选 PASSWORD 会话保护
- app.json 声明 Heroku 部署配置（stack=heroku-22），TOC 数组集中管理 12 因子章节顺序

## 为什么 (why)

- 官方站点吃自己的狗粮：Procfile 声明进程类型、$PORT 端口绑定、ENV 注入配置（PASSWORD/FORCE_SSL）都是 12-factor 原则的活教材
- 内容与渲染分离，12 因子条目以数据驱动而非硬编码在路由

## 如何实践 (how)

- Procfile 声明 web 进程，`ruby web.rb -p $PORT` 绑定 Heroku 注入的端口
- web.rb 用 Sinatra + ERB 渲染，i18n backend 加载 locales 实现多语言，locale 前缀路由分发
- PASSWORD env 开启时进入登录守卫，FORCE_SSL 时启用 Rack::SslEnforcer 强制 HTTPS
- TOC = %w(codebase dependencies config backing-services ... admin-processes) 即教义章节固定顺序

## 案例 (cases)

- 官方 12factor.net 生产部署：12 因子条目 + 博客 + 社区页 + 多语言 + 站点地图
- host 为 www.12factor.com 时 301 归一化到裸域，符合可寻址性规范

## 反模式/易错点

- 把章节内容硬编码进 web.rb 路由而非集中到 TOC/content 数据驱动
- 在代码里写死端口而非读取 $PORT，违反端口绑定原则
- 凭据写入配置/代码而非走 ENV（站内用 PASSWORD env 正示范避免此坑）

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-app-site → app-codebase | 依赖关联 | 站点是 App 原则的参考实现 |
| tool-app-site → app-build-run | 依赖关联 | Procfile 三阶段部署实践 |
