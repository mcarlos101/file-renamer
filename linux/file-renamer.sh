#!/usr/bin/env bash

file_renamer() {

    # Colors
    declare -r ESC="\u001B"     # Unicode
    declare -r BLD="${ESC}[1m"  # Bold or brighter
    declare -r DEF="${ESC}[0m"  # Default color and effects

    menu() {
        printf '\n'
        printf '%b\n' "${BLD}FILE RENAMER${DEF}"
        printf '%s\n' "1) Run Module"
        printf '%s\n' "2) Build Wheel"
        printf '%s\n' "3) Install Wheel"
        printf '%s\n' "4) Run Wheel"
        printf '%s\n' "5) Uninstall Wheel"
        printf '%s\n' "6) Build Linux Binary"
        printf '%s\n' "7) Run Linux Binary"
        printf '%s\n' "8) Exit"
        read -r -s -n 1 -p "Enter Number: " keypress
        printf '%s' "$keypress"
        printf '\n\n'

        case "$keypress" in
            1)
                run_module;;
            2)
                build_wheel;;
            3)
                install_wheel;;
            4)
                run_wheel;;
            5)
                uninstall_wheel;;
            6)
                build_linux_binary;;
            7)
                run_linux_binary;;
            8)
                printf '%s\n' "Exit"
                exit 0;;
            *)
                printf '%s\n' "Bye!"
                exit 0
        esac
    } # menu

    run_module() {
        # Run module file_renamer from venv dev
        PYTHONPATH=/data/fr/file-renamer/src \
        /data/fr/venv/nix/py3.12/dev/bin/python -m file_renamer
        menu
    }

    build_wheel() {
        python -m build
        menu
    }

    install_wheel() {
        pip install /data/fr/file-renamer/dist/file_renamer-*.whl
        menu
    }

    run_wheel() {
        file-renamer
        menu
    }

    uninstall_wheel() {
        pip uninstall -y PySide6 PySide6_Addons PySide6_Essentials shiboken6 \
        Unidecode file-renamer
        menu
    }

    build_linux_binary() {
        pyinstaller --clean /data/fr/file-renamer/spec/app-linux.spec
        menu
    }

    run_linux_binary() {
        /data/fr/file-renamer/dist/file-renamer
    }

    menu
} # file_renamer

file_renamer "$@"
exit 0
