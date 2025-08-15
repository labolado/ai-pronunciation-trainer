@echo off
chcp 65001 >nul
echo ========================================
echo   停止AI发音训练器服务器
echo ========================================

echo [+] 正在查找并停止Python服务器进程...

:: 查找并终止webApp.py进程
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo table /nh ^| findstr webApp') do (
    echo [+] 找到进程ID: %%i
    taskkill /pid %%i /f
)

:: 备用方法：终止所有Python进程（谨慎使用）
:: taskkill /f /im python.exe

echo [+] 服务器进程已停止
pause