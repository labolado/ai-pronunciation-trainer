@echo off
chcp 65001 >nul
echo ========================================
echo   AI发音训练器 - 双服务器管理
echo ========================================

set PROJECT_DIR=%~dp0ai-pronunciation-trainer
set VENV_DIR=%PROJECT_DIR%\venv

if not exist "%PROJECT_DIR%" (
    echo [!] 项目目录不存在，请先运行 windows_setup.bat
    pause
    exit /b 1
)

cd "%PROJECT_DIR%"

echo [1] 启动Flask Web界面服务器 (端口3000)...
call "%VENV_DIR%\Scripts\activate.bat"
start "Flask服务器" cmd /k "python webApp.py"

timeout /t 3 >nul

echo [2] 启动FastAPI接口服务器 (端口8000)...
start "FastAPI服务器" cmd /k "python fastapi_server.py"

timeout /t 3 >nul

echo.
echo ========================================
echo   两个服务器都已启动！
echo ========================================
echo.
echo 🌐 Web界面 (用户使用):
echo     http://localhost:3000
echo     - 在线发音训练
echo     - 用户友好界面
echo.
echo 🔧 API接口 (开发者使用):
echo     http://localhost:8000/docs
echo     - RESTful API
echo     - 接口文档
echo     - 程序集成
echo.
echo 📊 服务状态:
echo     Flask:   http://localhost:3000
echo     FastAPI: http://localhost:8000/health
echo.
echo 💡 提示: 关闭命令行窗口将停止对应服务器
echo.
pause