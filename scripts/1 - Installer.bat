@REM This uses CX_Freeze to create an MSI installer file.
copy BuildInstaller.py ..\script\
mkdir ..\script\Resources\
copy ..\Resources ..\script\Resources
copy ..\pishock.cfg.example ..\script\
cd ..\script
BuildInstaller.py bdist_msi
del /q BuildInstaller.py
