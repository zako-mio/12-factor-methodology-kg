# 12factor.net 站点源码 (12factor.net Jekyll Site)

- ID: `tool-app-site`
- 类型: 工具
- 来源: 工具
- 分组: G-TOOLS · 辅助工具集
- 阶段: 基础 basic

> 官方文档站自身即 Jekyll 应用，是 App 原则的参考实现

## 核心主张 (what)

- 12factor.net 官网是 Sinatra（web.rb）+ ERB 视图的 Ruby 应用，部署在 Heroku（Readme.md）
- Procfile 仅一行 `web: ruby web.rb -p $PORT`，web 进程经 web.rb 启动，端口来自 $PORT 环境变量（Procfile）
- web.rb 实现 i18n 多语言（locales/*.yml）、/blog、/community、/sitemap.xml 动态生成、www→裸域 301 重定向、可选 PASSWORD 会话保护（web.rb）
- app.json 声明 Heroku 部署配置（stack=heroku-22）（app.json）
- TOC 数组集中管理 12 因子章节顺序：codebase→admin-processes（web.rb TOC）
- Gemfile 声明 sinatra/builder/thin/maruku/i18n/puma/rack-ssl-enforcer 等依赖（Gemfile）
- 12 因子条目以数据驱动渲染而非硬编码路由：/:factor 校验 TOC 后 ERB 渲染（web.rb）
- blog POSTS 白名单与 sitemap 由 MAIN_PATHS/TOC/POSTS × locales 动态生成（web.rb）

## 为什么 (why)

- 官方站点吃自己的狗粮：Procfile 声明进程类型、$PORT 端口绑定、ENV 注入配置（PASSWORD/FORCE_SSL）都是 12-factor 原则的活教材
- 内容与渲染分离：12 因子条目以 TOC 数据驱动，增删章节不改路由
- 展示端口绑定+进程声明的生产实践，作为读者可部署参考实现
- PASSWORD 会话保护示范凭据走 ENV 而非代码（web.rb）
- 为 12-factor 方法论提供多语言、可寻址、可审计的权威展示层

## 如何实践 (how)

- Procfile 声明 web 进程类型，`ruby web.rb -p $PORT` 绑定 Heroku 注入的端口（Procfile）
- web.rb 用 Sinatra + ERB 渲染，i18n backend 加载 locales 实现多语言，locale 前缀路由分发（web.rb before '/:locale/*'）
- PASSWORD env 开启时进入登录守卫，FORCE_SSL 时启用 Rack::SslEnforcer 强制 HTTPS（web.rb configure）
- TOC = %w(codebase dependencies config backing-services … admin-processes) 即教义章节固定顺序（web.rb）
- sitemap.xml 由 MAIN_PATHS/TOC/POSTS × I18n.available_locales 生成，含 hreflang 变体（web.rb sitemap 块）
- host 为 www.12factor.com 时 301 归一化到裸域，符合可寻址性规范（web.rb before 块）
- 本地 bundle install + heroku local:start 开发，PR 合并自动部署（Readme.md）

## 案例 (cases)

- 官方 12factor.net 生产部署：12 因子条目 + 博客 + 社区页 + 多语言 + 站点地图
- blog POSTS 白名单校验，未收录文章返回 404（web.rb POSTS + halt 404）
- 每 deploy 端口由 Heroku $PORT 环境注入，本地由 heroku local 提供（Procfile/Readme.md）
- alternate_links helper 生成 hreflang=x-default 与各语言 alternates（web.rb helpers）

## 反模式/易错点

- 把章节内容硬编码进 web.rb 路由而非集中到 TOC 数据驱动，增删章节需改代码
- 在代码里写死端口而非读取 $PORT，违反端口绑定原则
- 凭据写入配置/代码而非走 ENV（站内用 PASSWORD env 正示范避免此坑）
- 忽略 locale 前缀路由导致 i18n 页面 404（web.rb before '/:locale/*' 处理）
- 不把依赖声明进 Gemfile 导致新环境缺包（Gemfile 显式声明反例）

## 源码索引（实践参考）

- `08-source/app-deploy/web.rb` — 
- `08-source/app-deploy/Procfile` — 
- `08-source/app-deploy/app.json` — 
- `08-source/app-deploy/Gemfile` — 
- `08-source/app-deploy/Readme.md` — 
- `08-source/app-deploy/.github/dependabot.yml` — 
- `08-source/app-deploy/CONTRIBUTING.md` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| tool-app-site → app-codebase | 依赖关联 | 站点是 App 原则的参考实现 |
| tool-app-site → app-build-run | 依赖关联 | Procfile 三阶段部署实践 |
