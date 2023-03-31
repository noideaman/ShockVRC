# Download Python 3.10.5 embeddable zip
Invoke-WebRequest "https://www.python.org/ftp/python/3.10.5/python-3.10.5-embed-amd64.zip" -OutFile .\python.zip

# Extract the downloaded zip file
Expand-Archive -Path .\python.zip -DestinationPath .\python -Verbose

# Clean up the now unneeded zip file.
Remove-Item .\python.zip

# Modify the python310._pth file to enable 'site' module
$file = '.\python\python310._pth'
$find = '#import site'
$replace = 'import site'
(Get-Content $file).replace($find, $replace) | Set-Content $file

# Download get-pip.py
Invoke-WebRequest 'https://bootstrap.pypa.io/get-pip.py' -OutFile .\python\get-pip.py

# Change the current directory to .\python
Set-Location .\python

# Install pip
./python.exe get-pip.py --no-warn-script-location

# Change the current directory to .\scripts
Set-Location .\scripts

# Install required Python packages
./pip.exe install requests --no-warn-script-location
./pip.exe install python-osc --no-warn-script-location
./pip.exe install configparser --no-warn-script-location
./pip.exe install PyQt5 --no-warn-script-location
./pip.exe install PySimpleGUIQt --no-warn-script-location

# Change back to the root directory
Set-Location ..
