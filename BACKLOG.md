# KVoiceWalk Backlog

## 近期（现在～6月）— Local TTS Gateway

在 kvoicewalk 中搭建 OpenAI 兼容 TTS 服务，复用现有 Kokoro 管线。

| ID | 描述 | 优先级 | 状态 | 计划 |
|----|------|--------|------|------|
| GW-01 | **OpenAI 兼容端点** — FastAPI `POST /v1/audio/speech` | P1 | 待设计 | Sprint 1 |
| GW-02 | **TTS 后端抽象** — `TTSEngine` 接口 + `KokoroAdapter` | P1 | 待设计 | Sprint 1 |
| GW-03 | **`--serve` 模式** — `main.py` 支持 `--serve` 启动 uvicorn | P1 | 待设计 | Sprint 1 |
| GW-04 | **SpeechGenerator 参数化** — `lang_code` 从硬编码改为可配置 | P1 | 待设计 | Sprint 1 |
| GW-05 | **文本预处理器** — PDF 噪音清理，解耦自 TTS 后端 | P2 | 待设计 | Sprint 1 |

## 中期（7～9月）— Kokoro 日语微调

对 Kokoro-82M 进行权重微调，提升日语合成质量。

| ID | 描述 | 优先级 | 状态 | 计划 |
|----|------|--------|------|------|
| FT-01 | **调研训练管线** — Kokoro 架构、训练代码、数据格式 | P1 | 待调研 | 暑期 |
| FT-02 | **构建日语数据集** — 文本 + 音频配对 | P1 | 待启动 | 暑期 |
| FT-03 | **微调实验** — 在 Mac 上跑通第一轮训练 | P1 | 待启动 | 暑期 |
| FT-04 | **评估/对比** — 微调前后日语合成质量对比 | P2 | 待启动 | 暑期 |
| FT-05 | **MPS/MLX 加速调研** — 评估 Apple Silicon GPU 对训练/推理的加速收益，决定暑期是否切换 | P2 | 待调研 | 暑期前 |

## 已完成

（暂无）
