# Sprint 1 — 验证 + 接入 macOS 服务

## 1. 启动 Gateway

```bash
cd ~/user/kvoicewalk
uv run python -m uvicorn utilities.server:app --host 127.0.0.1 --port 8880
```

## 2. 创建 Automator Service

1. 打开 **Automator** → 新建 → **Service**
2. 顶栏：**Service receives selected `text` in `any application`**
3. 左侧搜索 **Run Shell Script**，拖到右边
4. **Pass input:** `to stdin`
5. **Shell 内容:**
   ```bash
   ~/user/kvoicewalk/bin/read-civilight
   ```
6. 保存为 **Read with Civilight**

## 3. 绑定快捷键

**系统设置 → 键盘 → 键盘快捷键 → 服务**
→ 找到 **Read with Civilight**
→ 双击右侧，按下 `⌥⌘R`

## 4. 使用

选中任意文字 → 按 `⌥⌘R`

## 5. 浏览器里也能用

因为 Service 是系统级的，Safari/Chrome 里选中文字也能用同一个快捷键。如果希望只限 Zotero，在 Automator Service 顶栏的 `any application` 改成 `Zotero` 即可。
