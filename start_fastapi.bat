@echo off
chcp 65001 >nul
echo ========================================
echo   启动AI发音训练器 FastAPI服务器
echo ========================================

set PROJECT_DIR=%~dp0
set VENV_DIR=%PROJECT_DIR%venv

:: 检查虚拟环境
if not exist "%VENV_DIR%" (
    echo [!] 虚拟环境不存在，请先运行 windows_setup.bat
    pause
    exit /b 1
)

cd "%PROJECT_DIR%"

echo [+] 激活虚拟环境...
call "%VENV_DIR%\Scripts\activate.bat"

echo [+] 安装FastAPI依赖...
pip install -r fastapi_requirements.txt

echo [+] 启动FastAPI服务器...
echo.
echo ========================================
echo   FastAPI服务器启动中...
echo   API文档: http://localhost:8000/docs
echo   交互式文档: http://localhost:8000/redoc
echo   健康检查: http://localhost:8000/health
echo   按 Ctrl+C 停止服务器
echo ========================================
echo.

python fastapi_server.py

echo.
echo [+] FastAPI服务器已停止
pause