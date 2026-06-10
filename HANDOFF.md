# Handoff — 2026-06-09

## 会话总结
Sprint 2 — Gateway 多语言 TTS 路由 的 CODE + 验证 + 归档完成。PLAN→DESIGN→ATTACK→CODE 全流程，Lite 模式。随后进入 Blog 草稿编写阶段（note_obsidian），但 Blog 尚未完成。

### 交付
- **GPTSoVITSAdapter**（gptsovits_adapter.py）：httpx 客户端，线程安全，三个异常子类（GPTSoVITSUnavailable/NotFound/APIError）
- **voice_map.json** 重构：扁平→分层（kokoro + gpt-sovits 两级）
- **server.py** 路由：model 参数分发，双层错误处理（isinstance 配异常子类）
- **ATTACK 4 H 级修复**：sf.read 异常捕获、AAC 动态采样率、异常子类替代字符串匹配、空音频防护
- **GPT-SoVITS API launchd 自启**：com.civilight.gpt-sovits-api.plist，stow 管理
- **Blog 草稿**（note_obsidian/blog/theresa-in-mac/draft.md）：多轮迭代但未完成
- **Writing 草稿**（note_obsidian/writing/人的第一份脚本/draft.md）：已写入未经讨论

### 验证
- 日文 GPT-SoVITS（200, 137KB）、中文 GPT-SoVITS（200, 68KB）
- AAC 格式正常编码（H-02 修复确认）、错误路径 400/404/503 均正确
- Kokoro 回归测试通过
- GPT-SoVITS API launchd 加载正常

## 进度状态
Sprint 2 全部完成。Gateway + GPT-SoVITS API 双服务均 launchd 管理。Blog 草稿待继续打磨。

## 待办事项
1. 完成 Blog 草稿打磨（`note_obsidian/blog/theresa-in-mac/draft.md`）
2. 生成 Demo 音频，替换占位符
3. 发布到 WordPress

## 上下文快照
- 分支: main（kvoicewalk 项目）
- 工作区: Sprint 2 已归档
- Gateway: 127.0.0.1:8880，launchd 管理
- GPT-SoVITS API: 127.0.0.1:9880，launchd 管理
- 记忆已写入：2 条（双引擎分离架构、模型路由替代语言路由）
- worklog 已写入：3 条（feat 多语言路由、fix 4H 修复、chore launchd）

## 相关文件
- `utilities/gptsovits_adapter.py` — 新增
- `utilities/voice_map.json` — 重构
- `utilities/server.py` — 路由+错误处理
- `PIPELINE/ARCHIVE/Sprint2/` — Sprint 2 文档归档
- `~/dotfiles/launchd/Library/LaunchAgents/com.civilight.gpt-sovits-api.plist` — launchd

## 下一步建议
参考 `note_obsidian/HANDOFF.md` 了解 Blog/Writing 草稿的完整上下文。先和用户确认 Blog 面向谁、目的是什么，再推草稿。
