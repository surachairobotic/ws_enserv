@echo off
:: This script, run from a Windows (10) machine, finds a Raspberry Pi on local network

:: You can manually set subnet if needed
:: E.g.
::SET subnet=192.168.56
SET subnet=192.168.110

:: --- No need to edit below this line ---

SET raspIp=
SET myip=

:: Get IP for local PC
FOR /f "tokens=1-2 delims=:" %%a IN ('ipconfig^|find "IPv4"') DO SET myip=%%b
SET myip=%myip:~1%
echo IP for local PC: %myip%

:: Retrieve subnet if not manually set
IF "%subnet%" == "" (
    SETLOCAL EnableDelayedExpansion
    SET subnet=%myip%
    FOR /l %%a IN (1,1,31) DO IF NOT "!subnet:~-1!"=="." SET subnet=!subnet:~0,-1!
    SET subnet=!subnet:~0,-1!
    SETLOCAL DisableDelayedExpansion
)

:: Show subnet
echo Subnet: %subnet%
echo.

:: Loop through arp table entries and look for Raspberry Pis MAC addresses
echo Discovering network...
:: Ping all IPs in subnet from 1 to 254
FOR /L %%N IN (1,1,254) DO start /b ping -n 1 -w 200 %subnet%.%%N >nul
timeout 1 >nul
FOR /f "tokens=1" %%f  IN ('arp -a ^| findstr "28-cd-c1 b8-27-eb e4-5f-01 dc-26-32"') DO (
    IF NOT "%%f"=="" echo Found Raspberry Pi having IP %%f
)
echo.
pause