Invoke-WebRequest "https://www.python.org/ftp/python/3.10.5/python-3.10.5-embed-amd64.zip" -OutFile .\python.zip
Expand-Archive -Path .\python.zip -DestinationPath .\python -Verbose 
$file = '.\python\python310._pth'
$find = '#import site'
$replace = 'import site'
(Get-Content $file).replace($find, $replace) | Set-Content $file
Invoke-WebRequest 'https://bootstrap.pypa.io/get-pip.py' -OutFile .\python\get-pip.py
cd .\python
./python.exe get-pip.py --no-warn-script-location
cd .\scripts
./pip.exe install requests --no-warn-script-location
./pip.exe install python-osc --no-warn-script-location
./pip.exe install configparser --no-warn-script-location
