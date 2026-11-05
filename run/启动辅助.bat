@echo off
rem 修真辅助 v8.5 还原版启动器（需与 run/ 同级的 tools\py27\python.exe）
rem 控制台中文：按 GBK 输出（与代码页 936 一致，避免乱码）；本文件须保存为 GBK/ANSI 编码
cd /d %~dp0
chcp 936 >nul
title 修真辅助 v8.5
set QT_PLUGIN_PATH=%~dp0qt4_plugins
set PYTHONIOENCODING=gbk:replace
start "xiuzhen_helper" "..\tools\py27\python.exe" xbxxz_helper.py
