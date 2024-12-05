# Handy Scripts

This repository contains handy scripts and tools that can be used to improve your daily developer duties.

## Adding a script to a Windows system

You will need to add a new function to the `$PROFILE`. In order to test for the existance of the file, run this command:

```powershell
Test-Path $PROFILE
```

If you receive a `False` response, then run this command:

```powershell
New-Item -Path $PROFILE -ItemType File -Force
```

Now, open `$PROFILE` file using any editor:

```powershell
notepad $PROFILE
```

Add the function to the file:

```powershell
function gclean {
    python "{your_path}\handy-scripts\git\gclean.py" @args
}
```

## Adding a script to a Unix system

You will need to modify either the .bashrc or the .zshrc:

```bash
nano ~/.zshrc
```

Add an alias that calls the script:

```bash
alias gclean='python /{your_path}/handy-scripts/git/gclean.py'
```
