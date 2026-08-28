# 太长不看

[English](README.en.md)

**太长不看** 是一套面向 Agent 工具的可视化问答式项目共建流程。它的目标不是让某一个 Agent 写得更多，而是让所有对话式、IDE 式、终端式、仓库式 Agent 在动手实现前，先把项目边界、结构、流程、函数契约和实现范围说清楚。

这个仓库当前以 Codex skill 格式打包，但方法本身不绑定 Codex。任何能保留上下文、写入 Markdown 工件，并通过 HTML Markdown 渲染器预览 Mermaid、表格和安全 HTML 的 Agent 工具，都可以移植这套流程。

## 解决什么问题

| 常见问题 | 太长不看的做法 |
|---|---|
| 用户一句需求，Agent 直接写一大堆代码 | 先过四个决策阶段，再实现 |
| 用户刷完手机回来才发现架构不对 | 每阶段都有图表和显式裁决 |
| 项目结构、依赖、模块边界看不清 | 用系统边界图、目录树、依赖层级图呈现 |
| 函数职责和异常流程后期才暴露 | 先画泳道流程，再审函数声明 |
| 用户被迫读长篇回复 | 用“篇幅暴政”把信息压进图表、表格和编号项 |
| 用户强行要求“别问了，直接写” | 进入闪电战模式，用 3 个 yes/no 问题压缩决策 |
| 对话过长导致 Agent 忘记前文 | 每轮维护已锁定决策快照 |
| 用户找不到图表在哪里 | 图表只放 Markdown 工件，并统一通过 HTML 渲染器预览；聊天窗口给路径、URL、文件用途和下一步 |
| Agent 一上来就假设目标 | 开头先问用户是否已有目标描述，或让用户用一段话说明 |

## 四阶段流程

| 阶段 | 名称 | 主要产物 | 用户动作 |
|---|---|---|---|
| 1 | 域划分 | 系统边界与依赖图 | 保留、删除或延后依赖与最小功能 |
| 2 | 结构契约 | 项目目录树、CMake 依赖层级图 | 移动、拆分、合并、删除或确认模块 |
| 3 | 流程编排 | 泳道时序图、函数声明表 | 补分支、改签名、确认契约 |
| 4 | 实现裁决 | 函数实现清单表 | 标记 `AI`、`协作` 或 `人工` |

## 适配范围

| Agent 类型 | 使用方式 |
|---|---|
| 对话式 Agent | 输出图表、表格、契约和实现计划，让用户手动执行 |
| IDE Agent | 先完成四阶段裁决，再修改文件 |
| 终端 Agent | 先确认结构与命令边界，再生成、构建、测试 |
| 仓库型 Agent | 把目录树、依赖图、函数清单作为变更前置审查 |
| 不支持 Mermaid 的 Agent | 使用等价 HTML Markdown 渲染器；若仍无法渲染，则输出 Mermaid 源码和紧凑文本备选 |
| 非软件项目 | 将 target 替换为交付物，将编译替换为产出最终稿 |

## 语言栈适配

| 栈 | 结构契约映射 |
|---|---|
| C / C++ / CMake | `CMakeLists.txt`、target、`target_link_libraries` |
| Python | `pyproject.toml`、`setup.py`、包、模块、依赖区 |
| Rust | `Cargo.toml`、crate、feature、workspace |
| Go | `go.mod`、package、`cmd/`、`internal/` |
| Node.js / TypeScript | `package.json`、`tsconfig.json`、script、package |
| Java | Maven/Gradle、package、module、JUnit |
| 其他 | 使用通用模块图、目录树和流程图，省略 CMake 专属图 |
| 非软件领域 | 使用通用 `artifacts.md`，四阶段映射为部分、目录/分工、时间线、交付责任 |

## 核心规则

1. 每轮回复顶部固定显示进度条。
2. 运行时回复语言跟随用户语言。
3. 中文回复的核心叙述文字默认不超过 200 字。
4. 图表、表格和编号列表承担主要信息量。
5. 未经过边界、结构、流程、声明和实现范围裁决，Agent 不默认实现整个项目。
6. Agent 工具自带的计划、记忆、审批、执行权限都必须服从四阶段门禁。
7. 用户显式打断时进入闪电战模式，不强行阻拦。
8. 完成后输出终局交付清单，列明已实现、已验证和用户接手项。
9. 已锁定决策不可被隐式回滚；冲突请求必须先确认覆盖。
10. 任何图表或决策表必须写入 Markdown 预览工件，并统一通过 HTML Markdown 渲染器展示；CLI Agent 必须提供本地浏览器预览地址。
11. 新流程开头必须先确认用户是否已有目标描述；已有清晰目标时才直接进入阶段 1。
12. 必须一阶段一阶段推进；每轮只生成当前阶段产物，图表保持精炼，说明放在图下场景表或编号项中。
13. 已确认阶段必须迁移到 confirmed Markdown 归档；活动预览 Markdown 只保留正在裁决的阶段。
14. Agent 回复窗口只能是简短纯文字导航，不直接渲染图表、HTML 组件或 Markdown 表格。
15. 图表工件不限制为一个 Markdown 文件；可以按阶段拆分，只要回复窗口明确说明每个文件的用途，并指导用户打开哪个文件或 URL。
16. 单个预览 Markdown 只能包含 `1 张图 + 1 个不超过 6 行的表`，或 `无图 + 1 个任意行数的表`；多文件之间用带说明的超链接连接。
17. 预览 Markdown 可以使用兼容 Markdown 的原生 HTML 语法；进度条、状态快照、徽章和面板优先使用渲染器内置的 `.tlndr-*` class。

## 仓库结构

```text
too-long-not-read/
|-- SKILL.md
|-- README.md
|-- README.en.md
|-- agents/
|   `-- openai.yaml
|-- assets/
|   `-- markdown-renderer.html
|-- scripts/
|   `-- serve_markdown.py
`-- references/
    |-- artifacts.md
    |-- function-contracts.md
    |-- project-c-c++.md
    |-- project-go.md
    |-- project-java.md
    |-- project-node-typescript.md
    |-- project-python.md
    `-- project-rust.md
```

## 安装到 Codex

如果使用 Codex，可以将本仓库复制到 Codex skills 目录，并确保目标目录名为 `too-long-not-read`。

Windows PowerShell:

```powershell
Copy-Item -Recurse -Force . "$env:USERPROFILE\.codex\skills\too-long-not-read"
```

macOS / Linux:

```bash
mkdir -p ~/.codex/skills/too-long-not-read
cp -R ./* ~/.codex/skills/too-long-not-read/
```

## 移植到其他 Agent

将 [SKILL.md](SKILL.md) 作为主指令，将 `references/` 下的文件作为阶段参考资料。不同 Agent 工具的具体接入方式不同，但核心要求一致：

1. 每轮先显示进度。
2. 在 HTML 预览中先图表，后解释。
3. 先让用户裁决，再实现。
4. 函数先声明，后写实现。
5. 用户未确认的实现范围保持 `?`。
6. 图表和表格写入 Markdown 预览工件，并统一用 HTML Markdown 渲染器查看；阶段确认后迁移到 confirmed Markdown 归档。用 `scripts/serve_markdown.py` 启动 `assets/markdown-renderer.html` 静态页面，在本地端口预览完整 Markdown。
7. 可生成多个 Markdown 工件，例如 `.tlndr/stage-1-domain.md`、`.tlndr/current.md`、`.tlndr/confirmed-stage-1-domain.md`；聊天窗口必须简要说明每个文件的用途，并给出当前应查看的路径或 URL。
8. 单个预览 Markdown 的容量规则是：`1 张图 + 1 个不超过 6 行的表`，或 `无图 + 1 个任意行数的表`。跨文件关系用带说明的 Markdown 超链接连接。

本地预览示例：

```bash
python scripts/serve_markdown.py too-long-not-read-artifacts.md --port 8765
```

渲染器支持 GitHub Flavored Markdown、表格、任务列表、代码块、高亮、链接、图片、引用、经过安全清洗的原生 HTML，以及 Mermaid 图表源码渲染。页面内置 Light、Dark、Paper、Terminal 主题；工件推荐使用兼容 Markdown 的 HTML 语法和 `.tlndr-*` class 呈现进度条、状态快照、徽章和面板。

## 使用示例

```text
使用 too-long-not-read 流程帮我从零规划一个 CMake/C++ 项目，先用问答和图表确定边界、结构、流程和实现范围。
```

Codex 中也可以这样调用：

```text
Use $too-long-not-read to turn this project idea into a guided Q&A build plan with diagrams and implementation choices.
```

## 校验

在 Codex skill 格式下，可以运行：

```powershell
python -X utf8 C:\Users\<you>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

期望输出：

```text
Skill is valid!
```
