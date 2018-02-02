@ECHO OFF

SET ROOT=C:\Program Files\Side Effects Software\Houdini 16.0.671

SET HTOA=C:/solidangle/MtoA/htoa-2.1.3_rcca6014_houdini-${HOUDINI_VERSION}

SET EXTENSIONS_PATH=D:\Extensions

SET PATH=%PATH%;%ROOT%\bin;%HTOA%\scripts\bin

SET HOUDINI_PATH=%EXTENSIONS_PATH%;%HTOA%;^&

houdinifx.exe