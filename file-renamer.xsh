#!/usr/bin/env xonsh

$PYTHONPATH = "/data/fr/file-renamer/src"

def frvenv(args):
    """Detect platform & activate File Renamer virtual environment
    Call with frvenv("dev") or frvenv("test")
    """

    if $OPSYS == "Linux":
        # reset
        try:
            cd /data/fr/file-renamer
        except NotADirectoryError as err:
            print(f"Unexpected {err=}, {type(err)=}")
        else:
            if args == "test":
                venv = "test"
                print("test source")
                source-bash /data/fr/venv/test/bin/activate
            else:
                venv = "dev"
                print("dev source")
                source-bash /data/fr/venv/dev/bin/activate
            print('Virtual Environment Activated: ', venv)
    elif $OPSYS == "Windows":
        cls
        venv = "win-dev"
        if args == "test":
            venv = "win-test"
            Path("/data/fr/venv/win-test/Scripts/activate")
        else:
            Path("/data/fr/venv/win-dev/Scripts/activate")
            $env:PYTHONPATH = C:\\Users\\Me\\fr\\file-renamer\\src
        print('Virtual Environment Activated: ', venv)
    else:
        print("Platform not supported yet")

def frapp(arg):
    print("FILE RENAMER")
    print("1. Activate Dev VENV")
    print("2. Activate Test VENV")
    print("3. Run")
    print("4. Build Wheel")
    print("5. Build Linux Binary")
    print("6. Build Windows Binary")
    print("7. Uninstall File Renamer Wheel")
    print("8. Install File Renamer Wheel")
    print("9. PyPi Upload Wheel")
    print("10. Exit")
    print()

    option= str(input("Option: "))
    if len(option):
        if option == "1":
            frvenv("dev")
        elif option == "2":
            frvenv("test")
        elif option == "3":
            python -m file_renamer
        elif option == "4":
            if $OPSYS == "Linux":
                python -m build
            elif $OPSYS == "Windows":
                py -m build
        elif option == "5":
            python -m nuitka \
                --onefile \
                --output-filename=file-renamer \
                --output-dir=deploy \
                --include-data-dir=/data/fr/file-renamer/icons=icons \
                --linux-onefile-icon=/data/fr/file-renamer/icons/file-renamer.png \
                --enable-plugin=pyside6 \
                /data/fr/file-renamer/src/file_renamer/__main__.py
        elif option == "6":
            pyinstaller app-win.spec
        elif option == "7":
            pip uninstall -y PySide6 PySide6_Addons PySide6_Essentials shiboken6 Unidecode file-renamer
        elif option == "8":
            pip install dist/file_renamer-*.whl
        elif option == "9":
            if $OPSYS == "Linux":
                python -m twine upload dist/file_renamer-*
            elif $OPSYS == "Windows":
                py -m twine upload ".\\dist\\file_renamer-*"
        else:
            print("Exit")

frapp('1')