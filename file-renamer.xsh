#!/usr/bin/env xonsh

print($ARGS)
# print($ARG1)


def run():
    try:
        python -m file_renamer
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    else:
        pass

def build_wheel():
    try:
        if $OPSYS == "Linux":
            python -m build
        elif $OPSYS == "Windows":
            py -m build
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    else:
        pass

def build_binary():
    try:
        if $OPSYS == "Linux":
            python -m nuitka \
                --onefile \
                --output-filename=file-renamer \
                --output-dir=deploy \
                --include-data-dir=/data/fr/file-renamer/icons=icons \
                --enable-plugin=pyside6 \
                /data/fr/file-renamer/src/file_renamer/__main__.py
        elif $OPSYS == "Windows":
            python -m nuitka `
            --onefile `
            --output-filename=file-renamer `
            --output-dir=deploy `
            --include-data-dir=.\\Users\\Admin\\fr\\file-renamer\\icons=icons `
            --enable-plugin=pyside6 `
            /data/fr/file-renamer/src/file_renamer/__main__.py
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    else:
        pass

def uninstall_wheel():
    try:
        pip uninstall -y PySide6 PySide6_Addons PySide6_Essentials shiboken6 Unidecode file-renamer
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    else:
        pass

def install_wheel():
    try:
        pip install dist/file_renamer-*.whl
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    else:
        pass

def upload_pypi():
    if $OPSYS == "Linux":
        python -m twine upload dist/file_renamer-*
    elif $OPSYS == "Windows":
        py -m twine upload ".\\dist\\file_renamer-*"

def main():

    print('len: ', len($ARGS))
    if len($ARGS) > 1:
        if $ARG1 == "run":
            run()
        elif $ARG1 == "build_wheel":
            build_wheel()
        elif $ARG1 == "build_binary":
            build_binary()
        elif $ARG1 == "uninstall_wheel":
            uninstall_wheel()
        elif $ARG1 == "install_wheel":
            install_wheel()
        elif $ARG1 == "upload_pypi":
            upload_pypi()
        else:
            print('UNKNOWN $ARG1:',  $ARG1)
    else:
        print()
        print("FILE RENAMER")
        print("1. Run")
        print("2. Build Wheel")
        print("3. Build Binary")
        print("4. Uninstall File Renamer Wheel")
        print("5. Install File Renamer Wheel")
        print("6. PyPi Upload Wheel")
        print("7. Exit")
        print()

        option= str(input("Option: "))
        if len(option):
            if option == "1":
                run()
            elif option == "2":
                build_wheel()
            elif option == "3":
                build_binary()
            elif option == "4":
                uninstall_wheel()
            elif option == "5":
                install_wheel()
            elif option == "6":
                upload_pypi()
            else:
                print('Exit')

main()
