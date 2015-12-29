@echo off
git add .
if "%~1"=="" (git commit -am"update") else git commit -am"%1"
git push
