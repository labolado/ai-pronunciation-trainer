# AI发音训练器 Windows部署指南

## 📋 系统要求
- Windows 10/11
- 至少4GB内存
- 2GB可用磁盘空间

## 🚀 一键安装步骤

### 1. 下载必需软件
在运行安装脚本前，请确保已安装：

**Python 3.8-3.12**
- 下载：https://www.python.org/downloads/windows/
- ⚠️ 安装时勾选"Add Python to PATH"

**Git (可选)**
- 下载：https://git-scm.com/download/win

### 2. 运行安装脚本
1. 将所有项目文件复制到一个文件夹
2. 右键点击 `windows_setup.bat`
3. 选择"以管理员身份运行"
4. 等待安装完成

### 3. 启动服务器
双击运行 `start_server.bat`

### 4. 开始使用
在浏览器中打开：http://localhost:3000

## 🛠️ 手动安装 (如果自动安装失败)

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 安装依赖
pip install flask flask-cors
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install soundfile ffmpeg-python epitran librosa transformers
pip install "numpy<2.0"

# 4. 启动服务器
python webApp.py
```

## 🔧 FFmpeg安装

### 方法1: Chocolatey (推荐)
```bash
# 安装Chocolatey
# 在PowerShell(管理员)中运行：
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装FFmpeg
choco install ffmpeg
```

### 方法2: 手动安装
1. 下载：https://www.gyan.dev/ffmpeg/builds/
2. 解压到 `C:\ffmpeg`
3. 添加 `C:\ffmpeg\bin` 到系统PATH环境变量

## ❓ 常见问题

**Q: Python命令不被识别？**
A: 重新安装Python时勾选"Add Python to PATH"

**Q: 权限错误？**
A: 以管理员身份运行脚本

**Q: 模型下载慢？**
A: 首次启动需要下载Whisper模型，请耐心等待

**Q: 录音无声？**
A: 检查浏览器麦克风权限设置

## 📱 使用说明

1. 点击右侧箭头按钮生成练习样本
2. 允许浏览器访问麦克风
3. 点击麦克风按钮开始录音
4. 再次点击结束录音
5. 查看发音评分和反馈

## 🔄 更新项目

重新运行 `windows_setup.bat` 即可更新到最新版本。

---
如有问题，请检查控制台输出的错误信息。