Set objFSO = CreateObject("Scripting.FileSystemObject")
strDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell -WindowStyle Hidden -Command ""Start-Process python -ArgumentList 'screen_tg.py' -WorkingDirectory '" & strDir & "' -Verb RunAs -WindowStyle Hidden""", 0, False
