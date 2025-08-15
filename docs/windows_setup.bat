@echo off
chcp 65001 >nul
echo ========================================
echo   AI发音训练器 Windows自动安装脚本
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [✓] 以管理员权限运行
) else (
    echo [!] 请以管理员身份运行此脚本
    pause
    exit /b 1
)

:: 设置项目目录
set PROJECT_DIR=%~dp0ai-pronunciation-trainer
set VENV_DIR=%PROJECT_DIR%\venv

echo [1] 检查Python环境...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 未找到Python，请先安装Python 3.8+
    echo     下载地址: https://www.python.org/downloads/windows/
    pause
    exit /b 1
) else (
    echo [✓] Python已安装
    python --version
)

echo.
echo [2] 检查Git环境...
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 未找到Git，请先安装Git
    echo     下载地址: https://git-scm.com/download/win
    pause
    exit /b 1
) else (
    echo [✓] Git已安装
)

echo.
echo [3] 检查/安装FFmpeg...
ffmpeg -version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 未找到FFmpeg，正在尝试安装...
    
    :: 检查Chocolatey
    choco -v >nul 2>&1
    if %errorLevel% neq 0 (
        echo [!] 未找到Chocolatey包管理器
        echo     请手动安装FFmpeg:
        echo     1. 下载: https://www.gyan.dev/ffmpeg/builds/
        echo     2. 解压到C:\ffmpeg
        echo     3. 添加C:\ffmpeg\bin到PATH环境变量
        pause
        exit /b 1
    ) else (
        echo [+] 使用Chocolatey安装FFmpeg...
        choco install ffmpeg -y
        if %errorLevel% neq 0 (
            echo [!] FFmpeg安装失败，请手动安装
            pause
            exit /b 1
        )
    )
) else (
    echo [✓] FFmpeg已安装
)

echo.
echo [4] 克隆项目代码...
if exist "%PROJECT_DIR%" (
    echo [+] 项目目录已存在，正在更新...
    cd "%PROJECT_DIR%"
    git pull
) else (
    echo [+] 正在克隆项目...
    :: 这里需要替换为实际的项目地址
    echo [!] 请将项目文件复制到当前目录下的ai-pronunciation-trainer文件夹
    echo     或者如果有Git仓库地址，请修改此脚本
    
    :: 创建项目目录结构
    mkdir "%PROJECT_DIR%"
    echo [!] 请确保项目文件已正确放置在: %PROJECT_DIR%
    pause
)

cd "%PROJECT_DIR%"

echo.
echo [5] 创建Python虚拟环境...
if exist "%VENV_DIR%" (
    echo [+] 虚拟环境已存在，跳过创建
) else (
    echo [+] 创建虚拟环境...
    python -m venv venv
    if %errorLevel% neq 0 (
        echo [!] 虚拟环境创建失败
        pause
        exit /b 1
    )
)

echo.
echo [6] 激活虚拟环境并安装依赖...
call "%VENV_DIR%\Scripts\activate.bat"

echo [+] 升级pip...
python -m pip install --upgrade pip

echo [+] 安装基础依赖...
pip install flask flask-cors

echo [+] 安装PyTorch (CPU版本)...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

echo [+] 安装音频处理库...
pip install soundfile ffmpeg-python

echo [+] 安装其他依赖...
pip install numpy scipy epitran librosa transformers

echo [+] 安装降级NumPy以确保兼容性...
pip install "numpy<2.0"

echo.
echo [7] 下载预训练模型...
echo [+] 启动应用时会自动下载Whisper模型，首次启动可能较慢...

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 使用方法:
echo 1. 运行 start_server.bat 启动服务器
echo 2. 在浏览器中打开 http://localhost:3000
echo 3. 开始您的发音练习之旅！
echo.
pause