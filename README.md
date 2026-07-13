# 公司月度成本流向与净利润分析系统

按月录入 5 条产品线的收入与成本，自动核算盈利状况，并以 SVG「主水管流程图」直观呈现成本流向与净利润的形成。

> 单文件 Web 程序（`index.html`，无需构建），数据存于浏览器 `localStorage`，可导出 / 导入 JSON。

---

## 一、在线访问

已部署在 GitHub Pages，直接打开即可（无需安装）：

**https://caiclhy0806.github.io/cost-flow-analysis/**

---

## 二、本地预览

本地预览依赖本机运行的 `server.py`（监听 `127.0.0.1:8765`）。

### 方式 A：临时启动（仅当前终端 / 会话有效）
```bash
cd "Cost flow"
python3 server.py 8765
# 浏览器打开 http://127.0.0.1:8765/index.html
```
> 关掉终端 / 重启后进程会退出，需重新执行。

### 方式 B：注册为开机自启服务（推荐，一次配置永久常驻）
本仓库已在本机放置启动项文件 `~/Library/LaunchAgents/com.costflow.preview.plist`
（`RunAtLoad` + `KeepAlive`，登录自启、崩溃自动重启）。在本机**真实终端**执行一次：

```bash
launchctl load ~/Library/LaunchAgents/com.costflow.preview.plist
```
- 验证：`curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8765/index.html` → `200`
- 停止：`launchctl unload ~/Library/LaunchAgents/com.costflow.preview.plist`

> 若需自行重建该 plist（例如换机器），内容如下（请将两个路径改成你本机的实际路径）：
> ```xml
> <?xml version="1.0" encoding="UTF-8"?>
> <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
> <plist version="1.0">
> <dict>
>     <key>Label</key>
>     <string>com.costflow.preview</string>
>     <key>ProgramArguments</key>
>     <array>
>         <string>/path/to/python</string>
>         <string>/path/to/Cost flow/server.py</string>
>         <string>8765</string>
>     </array>
>     <key>RunAtLoad</key>
>     <true/>
>     <key>KeepAlive</key>
>     <true/>
> </dict>
> </plist>
> ```

---

## 三、使用说明

1. 顶部选择**月份**（首次进入会新建空白月份）。
2. 在「数据录入」区填写 5 条产品线的**营业收入**与**直接成本**；在「间接成本」区填写研发 / 销售 / 管理分摊基数；在「税款与现金流」区填写税率与现金流调整项。
3. 页面实时展示：
   - **盈利状况表**（逐线毛利润 / 税前净利润 / 净利润）
   - **三重视角**（账面净利 / 可用库存 / 经营现金流）
   - **成本流向流程图**（主水管=营业收入 → 分支扣直接 / 间接 / 税款 → 末端净利润 + 子池）
4. **发布到仓库**（仅本地 `127.0.0.1` 可用）：点击「☁️ 发布到仓库」会把当前数据写入 `data/costflow.json`；每日自动化任务会提交并推送到 GitHub，使线上站与仓库数据保持一致。

### 核算口径
- 毛利润 = 营业收入 − 直接成本
- 间接成本按**各产品线直接成本占比**分摊
- 税前净利润 = 毛利润 − 分摊间接成本
- 净利润 = 税前净利润 × (1 − 税率)（亏损月份不计提所得税，保守口径）
- 经营现金流 ≈ 净利润 + 折旧 − 应收账款增加 − 可用库存增加

---

## 四、目录结构

```
Cost flow/
├── index.html          # 核心单文件（录入 / 计算 / 表格 / SVG 流程图）
├── server.py           # 本地静态服务 + /api/publish 发布接口（端口 8765）
├── data/costflow.json  # 已发布数据（仓库与线上站一致）
├── .nojekyll           # 禁用 GitHub Pages 的 Jekyll 处理
├── 开发记录.md          # 完整开发过程与需求演变记录
└── README.md           # 本文件
```

---

## 五、部署与维护

- **建站**：GitHub Pages，发布 `main` 分支根目录，配 `.nojekyll`。
- **自动更新**：WorkBuddy 每日自动化（约 09:30）提交并推送 `data/costflow.json`。
- **凭证安全**：推送使用复用自其他仓库的 Personal Access Token，经 `git -c url...insteadOf` 传入，**不写入本仓库的 `.git/config`**。建议定期轮换该令牌。

---

*项目由 WorkBuddy 协助搭建与迭代。*
