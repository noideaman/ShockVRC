#Installer using cx_freeze stable(6.15.x), and python 3.11 (3.12 should be supported in cx_freeze 6.16.x)
from cx_Freeze import setup, Executable
#Update version numbers on new releases.

# Dependencies are automatically detected.
build_options = {'packages': [], 'excludes': [], "include_files" : ["pishock.cfg.example"]}


base = 'console'

# Create EXE and 2 shortcuts
executables = [
    #Desktop ShortCut
    Executable('pishockasync.py', 
    base=base,
    shortcut_name="ShockOSC",
    shortcut_dir="DesktopFolder",
    icon="Resources\VRChatpishock.ico",
    ),
    #StartMenu ShortCut
    Executable('pishockasync.py', 
    base=base,
    shortcut_name="ShockOSC",
    shortcut_dir="MyProgramMenu",
    icon="Resources\VRChatpishock.ico",
    ),
]

# Not 100% sure what this is for, and idk if anything will break removing it
directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

#Data to show in win32_programs?
msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", "v0.7", None, "VRChat OSC tool to control pishock shock collars", "IconId", None),
    ],
    "Icon": [
        ("IconId", "Resources\VRChatpishock.ico"),
    ],
}

#Values for the MSI installer file.
bdist_msi_options = {
    #we dont need the exe callable via cmd without the fullpath
    "add_to_path": False,
    "data": msi_data,
    #dont change  this, this tells windows what version to remove when performing an upgrade
    "upgrade_code": "{2787f9ec-f25c-46ee-bf9b-6d4983747575}",
    #this changes the icon in Add/Remove programs, sadly not the MSI it'self
    "install_icon":  "Resources\VRChatpishock.ico",
    #update the details tab in the MSI properties, these are the only values alloted
    "summary_data": {
        "author": "Various Authors",
        "comments": "https://github.com/noideaman/ShockOSC/releases",
        "keywords": "VRChat, OSC, shock, pishock",
    },
}

# Setting for the EXE, and options for python setup.py <options>
setup(name='ShockOSC',
      version = 'v0.7',
      description = 'VRChat OSC tool to move the player in the direction of a stretched Physbone',
      license = "GPL-2.0",
      options = {
      'build_exe': build_options,
      'bdist_msi': bdist_msi_options,
      },
      executables = executables)
