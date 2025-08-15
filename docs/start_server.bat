@echo off
chcp 65001 >nul
echo ========================================
echo   启动AI发音训练器服务器
echo ========================================

set PROJECT_DIR=%~dp0ai-pronunciation-trainer
set VENV_DIR=%PROJECT_DIR%\venv

:: 检查项目目录
if not exist "%PROJECT_DIR%" (
    echo [!] 项目目录不存在: %PROJECT_DIR%
    echo     请先运行 windows_setup.bat 进行安装
    pause
    exit /b 1
)

:: 检查虚拟环境
if not exist "%VENV_DIR%" (
    echo [!] 虚拟环境不存在
    echo     请先运行 windows_setup.bat 进行安装
    pause
    exit /b 1
)

cd "%PROJECT_DIR%"

echo [+] 激活虚拟环境...
call "%VENV_DIR%\Scripts\activate.bat"

echo [+] 检查依赖...
python -c "import torch, flask, soundfile" 2>nul
if %errorLevel% neq 0 (
    echo [!] 依赖包缺失，请重新运行安装脚本
    pause
    exit /b 1
)

echo [+] 启动服务器...
echo.
echo ========================================
echo   服务器启动中...
echo   首次启动需要下载模型，请耐心等待
echo   服务器地址: http://localhost:3000
echo   按 Ctrl+C 停止服务器
echo ========================================
echo.

python webApp.py

echo.
echo [+] 服务器已停止
pause