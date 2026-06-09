# ZoTTS 接入指南

## 启动服务

```bash
cd ~/user/kvoicewalk
uv run python -m uvicorn utilities.server:app --host 127.0.0.1 --port 8880
```

## ZoTTS 配置

待 ZoTTS Issue [#169](https://github.com/ImperialSquid/zotero-zotts/issues/169) 发布后：

1. 打开 Zotero → ZoTTS 设置
2. 填入自定义端点：
   - **API Base URL:** `http://127.0.0.1:8880`
   - **API Key:** （留空，本地服务无 auth）
3. 保存

## 验证连通

```bash
curl http://127.0.0.1:8880/v1/models
# → {"object":"list","data":[{"id":"kokoro",...}]}
```

## 可用音色

| 名称 | .pt 文件 | 语言 |
|------|---------|------|
| `af_bella` | af_bella.pt | English (US) |
| `af_heart` | af_heart.pt | English (US) |
| `civilight` | af_civilight.pt | English (US) - **你克隆的** |
| `am_adam` | am_adam.pt | English (US) |
| `bf_emma` | bf_emma.pt | English (UK) |
| `jf_alpha` | jf_alpha.pt | Japanese |

所有 `voices/` 目录中的 .pt 文件均可使用。

## ZoTTS 预期行为

向 `POST /v1/audio/speech` 发送：

```json
{
  "model": "kokoro",
  "input": "论文选段文本...",
  "voice": "civilight",
  "response_format": "wav"
}
```
