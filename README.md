# 公司月度成本流向与净利润分析系统

按月录入 5 条产品线的收入与成本，自动核算盈利状况，并以 SVG「主水管流程图」直观呈现成本流向与净利润的形成。

> 单文件 Web 程序（`index.html`，无需构建），数据存于浏览器 `localStorage`，可导出 / 导入 JSON。

---

## 一、在线访问（推荐）

已部署在 GitHub Pages，直接打开即可（无需安装、无需本地服务器）：

**https://caiclhy0806.github.io/cost-flow-analysis/**

---

## 二、本地查看（无需本地服务器）

本程序是单文件静态页面，**查看时不需要任何本地服务进程**。两种离线方式任选：

### 方式 A：直接双击打开
双击仓库内的 `index.html`，浏览器以 `file://` 方式打开即可正常使用。
- 数据存在浏览器 `localStorage`，录入 / 计算 / 流程图全部可用。
- 唯一例外：从仓库载入「已发布数据」那一步在 `file://` 下会被浏览器拦截，但代码已 `catch` 静默处理，不影响本地录入与查看。

### 方式 B：用 GitHub Pages 线上站
见上方「一、在线访问」。

> 说明：早期版本曾依赖本机 `server.py` + `launchctl` 常驻来提供预览，现已废除——exchange-rate 项目即采用「纯静态 + GitHub Pages」模式，本程序照此简化，查看不再需要任何本地服务。

---

## 三、使用说明

1. 顶部选择**月份**（首次进入会新建空白月份）。
2. 在「数据录入」区填写 5 条产品线的**营业收入**与**直接成本**；在「间接成本」区填写研发 / 销售 / 管理分摊基数；在「税款与现金流」区填写税率与现金流调整项。
3. 页面实时展示：
   - **盈利状况表**（逐线毛利润 / 税前净利润 / 净利润）
   - **三重视角**（账面净利 / 可用库存 / 经营现金流）
   - **成本流向流程图**（主水管=营业收入 → 分支扣直接 / 间接 / 税款 → 末端净利润 + 子池）
4. **发布到仓库（一键云发布）**：在页面下方的「GitHub 令牌(PAT)」输入框填入你的 PAT（需 `repo` 权限）并点「记住」，之后点「☁️ 发布到仓库」即直接用 GitHub API 把数据写入仓库 `data/costflow.json` 并触发 Pages 重建——**无需本地服务器、无需域名**。令牌仅存本机浏览器 `localStorage`。

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
├── data/costflow.json  # 已发布数据（仓库与线上站一致；由「一键发布」经 GitHub API 写入）
├── .github/workflows/  # GitHub Actions：每日自动同步（替代原本地自动化）
├── .nojekyll           # 禁用 GitHub Pages 的 Jekyll 处理
├── 开发记录.md          # 完整开发过程与需求演变记录
└── README.md           # 本文件
```

---

## 五、部署与维护

- **建站**：GitHub Pages，发布 `main` 分支根目录，配 `.nojekyll`。
- **自动更新**：`.github/workflows/auto-update.yml`（参照 exchange-rate 项目的 GitHub Actions 模式），每天北京时间 9:30 在 GitHub 云端运行并提交；也可在 Actions 页面手动 `workflow_dispatch` 触发。运行不依赖本机开机或本地进程。
- **一键发布数据**：在页面填入 GitHub PAT 并点「☁️ 发布到仓库」，即经 GitHub Contents API 将 `data/costflow.json` 提交到仓库（无需本地服务/域名）。令牌仅存本机浏览器。GitHub Actions 每日同步仍会保持仓库时间戳新鲜。
- **凭证安全**：仓库推送使用 Personal Access Token，经 `git -c url...insteadOf` 传入，**不写入** 本仓库的 `.git/config`。建议定期轮换该令牌。

---

## 六、版本与回退（ver.001）

本项目在引入「一键云发布」改造前，已将当时这版纯静态程序归档为 **`ver.001`**，便于随时回退：

- **Git 标签**：`ver.001`（annotated tag，已推送到仓库）。回退到该版本全量代码：
  ```bash
  git checkout ver.001        # 切到该快照
  # 或仅恢复工作区文件（不切分支）：
  git checkout ver.001 -- .
  ```
- **物理副本**：`versions/ver.001/`（含 `index.html` / `README.md` / `开发记录.md` / `data/` / `.github/` / `.nojekyll`，与源文件逐字节一致）。直接双击 `versions/ver.001/index.html` 即可查看改造前的程序，无需 git。

> 命名约定：后续若继续迭代，建议沿用 `ver.002`、`ver.003`… 的编号（每次在改造前打一个 git tag + 复制一份 `versions/ver.NNN/` 副本），形成可追溯的版本线。

---

## 七、创建细粒度 PAT（用于一键发布）

「☁️ 发布到仓库」需要你自己的 GitHub 个人访问令牌（PAT）。**推荐使用细粒度令牌（Fine-grained）**，并只授权本仓库、仅 `Contents` 写权限，最小化风险。

### 步骤流程图

```mermaid
flowchart TD
  A[打开 GitHub Token 设置页] --> B[Generate new token → Fine-grained]
  B --> C[填写名称（如 cost-flow-publish）与有效期]
  C --> D[Repository access → Only select repositories → 勾 cost-flow-analysis]
  D --> E[Permissions → Repository → Contents → Read and write]
  E --> F[Generate token]
  F --> G[复制生成的 github_pat_xxx]
  G --> H[回到本程序，粘贴到「GitHub 令牌(PAT)」框 → 点「记住」]
  H --> I[点「☁️ 发布到仓库」一键写入仓库]
```

### 文字步骤

1. 打开 **https://github.com/settings/tokens?type=beta**（细粒度令牌页；旧版在 `/settings/tokens` 选 "Fine-grained token"）。
2. 点 **Generate new token** → **Fine-grained token**。
3. **Token name**：任取，如 `cost-flow-publish`。
4. **Expiration**：设一个合理的过期时间（如 90 天），到期即失效更安全。
5. **Repository access**：选 **Only select repositories**，勾选 **`caiclhy0806/cost-flow-analysis`**（不要选 All repositories）。
6. **Permissions → Repository permissions → Contents**：右侧下拉改为 **Read and write**（这是发布所需的唯一权限；其余保持 No access）。
7. 滚到最下点 **Generate token**，页面会显示一次性的 `github_pat_xxxxxxxx`，**立即复制保存**（离开后不可再见）。
8. 回到本程序页面，把令牌粘贴进「GitHub 令牌(PAT)」输入框，点 **「记住」**（仅存本机浏览器 `localStorage`）。
9. 之后点 **「☁️ 发布到仓库」** 即可一键把数据写入仓库并触发 Pages 重建。

> 安全提示：
> - 令牌仅存于你本机浏览器，不会进入代码或仓库；换设备/清缓存后需重新粘贴。
> - 不再需要时，在页面点 **「清除」** 抹掉本地令牌，并到 GitHub 令牌页 **Revoke** 作废。
> - 切勿把 `github_pat_xxx` 明文发给他人或提交到代码里。

---

*项目由 WorkBuddy 协助搭建与迭代。*
