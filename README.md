# [file-renamer](https://github.com/mcarlos101/file-renamer)

Rename files using a GUI desktop app for Linux, Windows & macOS. macOS not yet tested.

# Screenshots

Launch App
![file-renamer app](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/file-renamer-01-desktop-app.png)

***

List Files
![List Files](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/file-renamer-02-list-files.png)

***

Regular Expression Preview
![Regular Expression Preview](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/file-renamer-17-search-replace-regular-expression-preview.png)

***

Regular Expression Renamed
![Regular Expression Renamed](https://raw.githubusercontent.com/mcarlos101/file-renamer/main/screenshots/file-renamer-18-search-replace-regular-expression-renamed.png)

# [Installation](https://pypi.org/project/file-renamer/)

## Linux

### Create a virtual environment (venv)
```sh
# For example
python3 -m venv "${HOME}/venv/file-renamer"
```

### Activate venv
```sh
source "${HOME}/venv/file-renamer/bin/activate"
```

### Install via pip
```sh
pip install file-renamer
```

### Run
```sh
cd "${HOME}/venv/file-renamer/lib/python3.12/site-packages/file-renamer"
python widget.py
```
