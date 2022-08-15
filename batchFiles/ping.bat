@echo off

set exitCode=0
set "tempFile=%temp%\%~nx0.%random%.tmp"

ping.exe -n %1 %2 > %tempFile%

findstr /m "find" %tempFile%
if %errorlevel%==0 (
    set exitCode=2
)
findstr /m "TTL" %tempFile%
if %errorlevel%==0 (
    set exitCode=1
)
exit %exitCode%
