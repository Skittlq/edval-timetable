@echo off
:: Check for admin rights
net session >nul 2>&1
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto getAdmin
) else ( goto gotAdmin )

:getAdmin
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
pushd "%CD%"
CD /D "%~dp0"

REM Check if the environment variable already exists
set "PATH_TO_ADD=C:\Program Files (x86)\Edval Timetable"
for %%i in ("%PATH:;=" "%") do if /I "%%~i"=="%PATH_TO_ADD%" (
    echo The path "%PATH_TO_ADD%" is already in the PATH.
    goto end
)

REM Add the new path to the system environment variables
set "NEW_PATH=%PATH_TO_ADD%;%PATH%"
setx /M PATH "%NEW_PATH%"

echo "C:\Program Files (x86)\Edval Timetable" has been added to the system PATH.

:end
exit /B