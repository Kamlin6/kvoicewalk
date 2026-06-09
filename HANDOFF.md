# Handoff — 2026-06-09

## 会话总结

本轮完成 **Sprint 1 Local TTS Gateway** 全流程（DESIGN → ATTACK → CODE → 验证 → 归档）。

### 核心成果

- **删除 kokoro-tts-server** — 确认是空壳项目（零 commit、无 remote），完全被 kvoicewalk 覆盖
- **Sprint 1 Gateway** — 在 kvoicewalk 中搭建 OpenAI 兼容 TTS 服务
  - `POST /v1/audio/speech`（wav/flac/opus/aac）
  - `GET /v1/models`
  - `TTSEngine` 抽象 + `KokoroAdapter`（线程安全）
  - 文本预处理器（引用标记、Unicode 垃圾清理）
  - 音色映射表（`civilight` → `af_civilight.pt`）
  - ATTACK 17 风险全修复（路径遍历、线程安全、OOM 防护等）
- **PIPELINE 初始化** — kvoicewalk 项目引入 lite 流水线
- **Hammerspoon 集成** — `⌥⌘R` 朗读 / `⌥⌘C` 停止，GNU Stow 管理 dotfiles
- **Backlog 更新** — 加入 FT（暑期微调）、ZP-01（Zotero 9 插件）、踩坑记录

### 关键决策

- Kokoro 仅适合英语，日语/中文用 GPT-SoVITS（暑期微调再议）
- Gateway 一期只做 Kokoro，二期 GPT-SoVITS adapter
- 本地自用服务，安全风险降级处理
- Sprint 阶段必须走 orchestrator

## 进度状态

Sprint 1 已完结。无活跃任务。

## 待办事项

| # | 描述 | 优先级 |
|---|------|--------|
| 1 | 暑期：Kokoro 日语微调（FT-01～FT-05） | 中 |
| 2 | 远期：Zotero 9 TTS 插件（ZP-01） | 低 |

## 上下文快照

- kvoicewalk 分支: `main`（ahead of origin/main）
- 最新 commit: `2517436` [macOS][fix] use PID-based temp filename
- 其他: dotfiles 仓库也有对应 commit（hammerspoon 配置）

## 相关文件

### kvoicewalk

| 文件 | 说明 |
|------|------|
| `utilities/tts_engine.py` | TTSEngine ABC + KokoroAdapter |
| `utilities/server.py` | FastAPI 端点 + 安全防护 |
| `utilities/preprocessor.py` | 文本预处理器 |
| `utilities/voice_map.json` | 音色映射表 |
| `bin/read-civilight-clipboard` | 朗读脚本 |
| `bin/stop-civilight` | 停止脚本 |
| `bin/SETUP.md` | 中文安装指南 |
| `PIPELINE/STATUS.md` | Sprint 状态 |
| `PIPELINE/DESIGN/DESIGN-001_Gateway.md` | 设计方案 |
| `PIPELINE/DESIGN/USER_STORIES.md` | 用户故事 |
| `PIPELINE/DESIGN/DIAGRAM-001_*.puml` | UML 类图 |
| `PIPELINE/DESIGN/DIAGRAM-002_*.puml` | 流程图 |
| `PIPELINE/ATTACK/ATTACK-001_Gateway.md` | 安全审查 |
| `PIPELINE/TEST-PLAN.md` | 测试方案 |
| `BACKLOG.md` | 项目待办 |

### dotfiles

| 文件 | 说明 |
|------|------|
| `hammerspoon/.hammerspoon/init.lua` | Hammerspoon 快捷键配置 |

## 下一步建议

1. 如要继续，可以从 BACKLOG 中选择暑期 FT Sprint 开始调研
2. 如需做 Zotero 9 插件，需学习 Zotero 插件开发（TypeScript + plugin API）
