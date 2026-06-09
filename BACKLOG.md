# KVoiceWalk Backlog

## 近期（现在～6月）— Local TTS Gateway ✅

在 kvoicewalk 中搭建 OpenAI 兼容 TTS 服务，复用现有 Kokoro 管线。

**状态：已完成（Sprint 1）**

## 中期（7～9月）— Kokoro 日语微调

对 Kokoro-82M 进行权重微调，提升日语合成质量。

| ID | 描述 | 优先级 | 状态 | 计划 |
|----|------|--------|------|------|
| FT-01 | **调研训练管线** — Kokoro 架构、训练代码、数据格式 | P1 | 待调研 | 暑期 |
| FT-02 | **构建日语数据集** — 文本 + 音频配对 | P1 | 待启动 | 暑期 |
| FT-03 | **微调实验** — 在 Mac 上跑通第一轮训练 | P1 | 待启动 | 暑期 |
| FT-04 | **评估/对比** — 微调前后日语合成质量对比 | P2 | 待启动 | 暑期 |
| FT-05 | **MPS/MLX 加速调研** — 评估 Apple Silicon GPU 对训练/推理的加速收益 | P2 | 待调研 | 暑期前 |

## 远期（未定）

| ID | 描述 | 优先级 | 状态 |
|----|------|--------|------|
| ZP-01 | **Zotero 9 TTS 插件** — 对接本地 Gateway，支持自定义音色和语言路由 | P3 | 待评估 |

## 踩坑记录

- PDF 转文本常含 Unicode 私用区（U+E000～U+F8FF）和代理项（U+D800～U+DFFF）字符，TTS 前必须过滤。已在 preprocessor.py 中实现 `_strip_unwanted()`。

## 已完成

- Sprint 1: Local TTS Gateway（4 commits, 5 ATTACK 风险修复）
