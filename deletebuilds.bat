@echo off
REM we need to somehow make it so that Y is always typed regardless of user input so github action can run
echo y | del dist\main.exe
echo y | rmdir dist
echo y | del build\main\*
echo y | del build\main\*.*
echo y | del build\main\localpycs
echo y | rmdir build\main\localpycs
echo y | rmdir build\main
echo y | rmdir build
echo builds deleted!