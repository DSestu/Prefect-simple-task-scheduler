Dim WinScriptHost
Dim FSO
Dim ScriptPath

' Create objects
Set WinScriptHost = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where the VBS script is located
ScriptPath = FSO.GetParentFolderName(WScript.ScriptFullName)

' Run the batch file from the same directory
WinScriptHost.Run Chr(34) & ScriptPath & "\start_prefect.bat" & Chr(34), 0

' Clean up
Set WinScriptHost = Nothing
Set FSO = Nothing