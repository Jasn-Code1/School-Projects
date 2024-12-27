@if (@CodeSection == @Batch) @then
@echo off
    set SendKeys=CScript //nologo //E:JScript "%~F0"
    cls
    color 0a
    start https://youtu.be/xvFZjo5PgG0?si=BQgJX_F6ZIdLKOVi
    timeout /t 4
    %SendKeys% {"f"}
@end
var WshShell = WScript.CreateObject("WScript.Shell");
WshShell.SendKeys(WScript.Arguments(0));
