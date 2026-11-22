@echo off
del dist\main.exe
rmdir dist
del build\main\*
del build\main\*.*
del build\main\localpycs
rmdir build\main\localpycs
rmdir build\main
rmdir build
echo builds deleted!