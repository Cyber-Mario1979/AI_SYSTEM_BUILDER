# AI_SYSTEM_BUILDER Setup Commands

## Verify environment

```powershell
python --version
where.exe python

Set-Location C:\
Set-Location .\AI_LAB
New-Item -ItemType Directory -Path .\AI_SYSTEM_BUILDER -Force | Out-Null
Set-Location .\AI_SYSTEM_BUILDER
py -3.14 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python --version
where.exe python
python -m pip install --upgrade pip
pip install pydantic
pip check
New-Item -ItemType Directory -Path .\asbp | Out-Null
New-Item -ItemType Directory -Path .\data\state -Force | Out-Null
New-Item -ItemType Directory -Path .\logs | Out-Null
New-Item -ItemType Directory -Path .\docs | Out-Null
New-Item -ItemType File -Path .\docs\DAY_01_NOTES.md -Force | Out-Null
code .
```
