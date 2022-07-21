@echo off
ping -n %1 %2 | findstr /i "TTL"
if "%errorlevel%"=="0" exit \b 0
if "%errorlevel%"=="1" exit \b 1
@echo on
