# Sprint 1 — 验证 + 接入 macOS 右键朗读

## 1. 启动 Gateway

```bash
cd ~/user/kvoicewalk
uv run python -m uvicorn utilities.server:app --host 127.0.0.1 --port 8880
```

## 2. 创建 Automator 服务

1. 打开 **自动操作（Automator）**
2. 新建 → **服务（Service）**
3. 顶栏设置：**"服务收到选定的" `文本` "位于" `任何App`**
4. 左侧资源库搜索 **"运行Shell脚本"**，拖到右边
5. **"传递输入"** 选 **"作为 stdin"**
6. 脚本内容写：
   ```bash
   ~/user/kvoicewalk/bin/read-civilight
   ```
7. 保存为 **Read with Civilight**

## 3. 绑定快捷键

**系统设置 → 键盘 → 键盘快捷键 → 服务**
→ 在列表里找到 **"Read with Civilight"**
→ 双击右侧空白，按住 `⌥⌘R`

## 4. 使用

在任何App（Zotero、浏览器、编辑器等）选中一段文字 → 按 `⌥⌘R` → 自动播放合成语音。

## 5. 只想 Zotero 用？

在 Automator 顶栏把 `任何App` 改成 `Zotero` 即可。
