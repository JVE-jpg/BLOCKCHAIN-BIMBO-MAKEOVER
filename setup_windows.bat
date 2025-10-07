@echo off
echo ========================================
echo Blockchain Bimbo Makeover - Setup Script
echo ========================================
echo NOTE: This script is for Windows only.
echo macOS/Linux users: Run ./setup.sh
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python 3 not found. Please install Python 3.8 or higher.
    echo.
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo.
echo Python found
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Try manually:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo Dependencies installed
echo.

REM Create .env if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo .env file created
    echo.
    echo ========================================
    echo IMPORTANT: Edit the .env file now
    echo ========================================
    echo.
    echo Required variables:
    echo   * ETH_PRIVATE_KEY        ^(66 chars, starts with 0x^)
    echo   * ZORA_CONTRACT_ADDRESS  ^(42 chars, starts with 0x^)
    echo   * WATCH_FOLDERS          ^(absolute paths^)
    echo.
    echo Opening .env file in Notepad...
    timeout /t 2 /nobreak >nul
    notepad .env
) else (
    echo .env file already exists
    echo.
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Make sure you edited .env with your configuration
echo    ^(If not, run: notepad .env^)
echo.
echo 2. Fund your wallet:
echo    * USDC/ETH for Arweave uploads
echo    * ETH on ZORA chain ^(bridge at: bridge.zora.energy^)
echo.
echo 3. Run the application:
echo    python blockchain_bimbo.py
echo.
echo The script will validate your config and show clear errors
echo if anything is missing or incorrect.
echo.
pause

