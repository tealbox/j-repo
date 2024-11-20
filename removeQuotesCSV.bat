@echo off
set "rootDir=C:\Path\To\Root\Directory"

for /f "tokens=*" %%f in ('dir /s /b /a-d "%rootDir%\*.csv"') do (
    (  
        for /f "usebackq delims=" %%l in ("%%f") do (
            set "line=%%l"
            setlocal enabledelayedexpansion
            set "line=!line:~1!" 
            if "!line:~-1!"=="\"" set "line=!line:~0,-1!"
            echo(!line!
            endlocal
        ) > "%%f.tmp"
        move /y "%%f.tmp" "%%f"
    )
)
