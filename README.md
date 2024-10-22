# File Renamer
Rename files using a GUI desktop app for Linux, Windows & macOS. macOS not yet tested.

1. [Github](https://github.com/mcarlos101/file-renamer)
1. [PyPi](https://pypi.org/project/file-renamer/)

## Screenshots

### Fedora Linux 40 Light Theme
App
![file-renamer app](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/fedora-linux-40/light/file-renamer-light-01-app-fedora-linux-40.png)

***

List Files
![List Files](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/fedora-linux-40/light/file-renamer-light-02-list-files-fedora-linux-40.png)
***

Preview
![Preview](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/fedora-linux-40/light/file-renamer-light-03-preview-fedora-linux-40.png)

***

Renamed
![Renamed](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/fedora-linux-40/light/file-renamer-light-04-renamed-fedora-linux-40.png)

***

### Windows 11 Dark Theme
App
![file-renamer app](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/windows-11/dark/file-renamer-dark-01-app-windows-11.png)

***

List Files
![List Files](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/windows-11/dark/file-renamer-dark-02-list-files-windows-11.png)
***

Preview
![Preview](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/windows-11/dark/file-renamer-dark-03-preview-windows-11.png)

***

Renamed
![Renamed](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/windows-11/dark/file-renamer-dark-04-renamed-windows-11.png)

***


## Installation

###  Linux
1. Download latest [release](https://github.com/mcarlos101/file-renamer/releases)
1. Unzip file & change into dir
1. Right-click on file-renamer & launch app or run shell command `./file-renamer`

### Windows
1. Download latest [release](https://github.com/mcarlos101/file-renamer/releases)
1. Unzip file & change into dir
1. Right-click on file-renamer.exe & launch app

###  pip
Install from [PyPi](https://pypi.org/project/file-renamer/)
```bash
# Install Python3.12 on Fedora Linux 40
sudo dnf install python3.12

# Create file-renamer folder in $HOME dir or anywhere
mkdir file-renamer

# Change directory
cd file-renamer

# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install file-renamer
pip install file-renamer

# Run
file-renamer
```

1. Tested on Fedora Linux Workstation 40, Windows 11 & Ubuntu 24.04.1 LTS
1. macOS and other operating systems not tested (may the gods be with you!)
1. See [Installing Packages](https://packaging.python.org/en/latest/tutorials/installing-packages/) for more info on other operating systems.


