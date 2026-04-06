@echo off
REM Gold Tier Integration Test Suite
REM Tests all Gold Tier features: Odoo, Facebook, Instagram, Twitter, CEO Briefing

echo ======================================================================
echo   GOLD TIER INTEGRATION TEST SUITE
echo ======================================================================
echo.

cd /d "%~dp0"

REM Check if vault path provided
if "%~1"=="" (
    set VAULT_PATH=..\AI_Employee_Vault
) else (
    set VAULT_PATH=%~1
)

echo Vault Path: %VAULT_PATH%
echo.

REM Test 1: Odoo MCP
echo ======================================================================
echo TEST 1: Odoo MCP Server
echo ======================================================================
echo.
if exist "odoo\scripts\test_odoo_mcp.py" (
    python odoo\scripts\test_odoo_mcp.py "%VAULT_PATH%"
) else (
    echo [SKIP] Odoo test script not found
)
echo.

REM Test 2: Facebook/Instagram MCP
echo ======================================================================
echo TEST 2: Facebook/Instagram MCP
echo ======================================================================
echo.
if exist "%VAULT_PATH%\scripts\test_facebook_mcp.py" (
    python "%VAULT_PATH%\scripts\test_facebook_mcp.py" "%VAULT_PATH%"
) else (
    echo [SKIP] Facebook test script not found
)
echo.

REM Test 3: CEO Briefing
echo ======================================================================
echo TEST 3: CEO Briefing Generation
echo ======================================================================
echo.
if exist "%VAULT_PATH%\scripts\ceo_briefing.py" (
    python "%VAULT_PATH%\scripts\ceo_briefing.py" "%VAULT_PATH%"
) else (
    echo [SKIP] CEO Briefing script not found
)
echo.

REM Test 4: Twitter MCP
echo ======================================================================
echo TEST 4: Twitter/X MCP
echo ======================================================================
echo.
if exist "%VAULT_PATH%\scripts\twitter_poster.py" (
    python "%VAULT_PATH%\scripts\twitter_poster.py" "%VAULT_PATH%" --tweet "Gold Tier Test Tweet - Testing Twitter Integration"
) else (
    echo [SKIP] Twitter poster script not found
)
echo.

REM Test 5: Audit Logger
echo ======================================================================
echo TEST 5: Audit Logger
echo ======================================================================
echo.
if exist "%VAULT_PATH%\scripts\audit_logger.py" (
    python "%VAULT_PATH%\scripts\audit_logger.py" "%VAULT_PATH%" --action test
) else (
    echo [SKIP] Audit Logger script not found
)
echo.

REM Test 6: Domain Router
echo ======================================================================
echo TEST 6: Domain Router
echo ======================================================================
echo.
if exist "%VAULT_PATH%\scripts\domain_router.py" (
    python "%VAULT_PATH%\scripts\domain_router.py" "%VAULT_PATH%"
) else (
    echo [SKIP] Domain Router script not found
)
echo.

REM Test 7: Ralph Wiggum Loop
echo ======================================================================
echo TEST 7: Ralph Wiggum Loop
echo ======================================================================
echo.
if exist "%VAULT_PATH%\scripts\ralph_wiggum.py" (
    python "%VAULT_PATH%\scripts\ralph_wiggum.py" "%VAULT_PATH%" "Test task completion"
) else (
    echo [SKIP] Ralph Wiggum script not found
)
echo.

REM Test 8: Watchdog
echo ======================================================================
echo TEST 8: Watchdog Process Monitor
echo ======================================================================
echo.
if exist "%VAULT_PATH%\scripts\watchdog.py" (
    echo [INFO] Watchdog script exists - manual testing required
    echo [INFO] Run: python "%VAULT_PATH%\scripts\watchdog.py" "%VAULT_PATH%"
) else (
    echo [SKIP] Watchdog script not found
)
echo.

echo ======================================================================
echo   TEST SUITE COMPLETE
echo ======================================================================
echo.
echo Next Steps:
echo 1. Review test results above
echo 2. Check AI_Employee_Vault/Briefings/ for CEO Briefing
echo 3. Check AI_Employee_Vault/Logs/ for audit logs
echo 4. Check AI_Employee_Vault/Domains/ for domain files
echo.
echo For Odoo testing:
echo   cd odoo
echo   docker-compose up -d
echo.
echo For Facebook testing:
echo   Create facebook_config.json with access tokens
echo.

pause
