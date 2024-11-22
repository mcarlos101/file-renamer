# File Renamer
Rename files using a GUI desktop app for Linux & Windows

## Locations

### Github
https://github.com/mcarlos101/file-renamer

### PyPi
1. https://pypi.org/project/io.github.mcarlos101.file-renamer/ (Latest)
1. https://pypi.org/project/file-renamer/ (Deprecated)

### Flathub
https://flathub.org/apps/io.github.mcarlos101.file-renamer (Coming Soon)

### Chocolatey
https://chocolatey.org (Coming Soon)

## Screenshots

### Fedora 41 KDE Plasma Light Theme
App
![file-renamer app](https://raw.githubusercontent.com/mcarlos101/file-renamer/refs/heads/main/screenshots/fedora-linux-41/light/01-file-renamer-app.png)

***

List Files
![List Files](https://raw.githubusercontent.com/mcarlos101/file-renamer/refs/heads/main/screenshots/fedora-linux-41/light/02-file-renamer-list-files.png)

***

Preview
![Preview](https://raw.githubusercontent.com/mcarlos101/file-renamer/refs/heads/main/screenshots/fedora-linux-41/light/03-file-renamer-preview.png)

***

Renamed
![Renamed](https://raw.githubusercontent.com/mcarlos101/file-renamer/refs/heads/main/screenshots/fedora-linux-41/light/04-file-renamer-renamed.png)

***

## Installation

###  Linux
1. [Flathub](https://flathub.org/apps/io.github.mcarlos101.file-renamer) (Coming Soon)

### Windows
1. [Chocolatey](https://chocolatey.org) (Coming Soon)

### Python Package Index - Cross Platform
1. [PyPi](https://pypi.org/project/io.github.mcarlos101.file-renamer/)

```bash
# Install Python3.11 or higher (Fedora Linux example)
sudo dnf install python3.13

# Create file-renamer folder in $HOME dir or anywhere
mkdir file-renamer

# Change directory
cd file-renamer

# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
python3 -m pip install -r pip/requirements.txt

# Install file-renamer
pip install io.github.mcarlos101.file-renamer

# Run
file-renamer
```
