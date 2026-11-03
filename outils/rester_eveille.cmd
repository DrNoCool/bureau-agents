@echo off
title Rester eveille
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0rester_eveille.ps1" %*
pause
