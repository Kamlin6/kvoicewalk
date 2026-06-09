# Hammerspoon + Gateway 朗读

## 你需要做的

### 1. 安装 Hammerspoon

1. 打开 https://www.hammerspoon.org
2. 点 **Download** → 下载 dmg
3. 打开 dmg，把 **Hammerspoon** 拖到 **应用程序**

### 2. 部署配置

```bash
cd ~/dotfiles
stow -t ~ hammerspoon
```

### 3. 启用

打开 Hammerspoon → 菜单栏出现锤子图标 → 点图标 → **Enable**

### 4. 使用

```
在任意 App 选中文字 → ⌘C 复制 → ⌥⌘R
→ 自动合成并播放
```

### 测试

打开终端，手动试试脚本是否正常：

```bash
echo "Hello world" | pbcopy
~/user/kvoicewalk/bin/read-civilight-clipboard
```

Gateway 必须先启动：

```bash
cd ~/user/kvoicewalk
uv run python -m uvicorn utilities.server:app --host 127.0.0.1 --port 8880
```
