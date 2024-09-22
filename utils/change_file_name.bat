@echo off
setlocal enabledelayedexpansion

:: Directory path (replace with your target directory)
set "target_dir=C:\Users\Wei\Desktop\bible-verse\static\images"

:: Change to the target directory
cd /d "%target_dir%"

:: Counter to track file numbering
set /a count=1

:: Loop through all files in the directory
for %%f in (*) do (
    :: Rename the file with an incrementing number and .jpg extension
    ren "%%f" "!count!.jpg"
    
    :: Increment the counter
    set /a count+=1
)

echo All files have been renamed to .jpg.
pause
