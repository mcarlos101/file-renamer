#!/usr/bin/env bash

file_renamer() {

    # Colors
    declare -r ESC="\u001B"     # Unicode
    declare -r BLD="${ESC}[1m"  # Bold or brighter
    declare -r DEF="${ESC}[0m"  # Default color and effects

    menu() {
        printf '\n'
        printf '%b\n' "${BLD}FILE RENAMER${DEF}"
        printf '%s\n' "1) Install Dev Mode"
        printf '%s\n' "2) Run Dev Mode"
        printf '%s\n' "3) Remove Dev Mode"
        printf '%s\n' "4) Build Wheel"
        printf '%s\n' "5) Install Wheel"
        printf '%s\n' "6) Run Wheel"
        printf '%s\n' "7) Remove Wheel"
        printf '%s\n' "8) Build Linux Binary"
        printf '%s\n' "9) Run Linux Binary"
        printf '%s\n' "10) Build Flatpak"
        printf '%s\n' "11) Install Flatpak"
        printf '%s\n' "12) Run Flatpak"
        printf '%s\n' "13) Manifest Check"
        printf '%s\n' "14) Repo Check"
        printf '%s\n' "15) Remove Flatpak"
        printf '%s\n' "16) Clean Up"
        printf '%s\n' "17) Exit"
        read -r -n 2 -p "Enter Number: " keypress
        printf '\n'

        case "$keypress" in
            1)
                install_dev_mode;;
            2)
                run_dev_mode;;
            3)
                remove_dev_mode;;
            4)
                build_wheel;;
            5)
                install_wheel;;
            6)
                run_wheel;;
            7)
                remove_wheel;;
            8)
                build_linux_binary;;
            9)
                run_linux_binary;;
            10)
                build_flatpak;;
            11)
                install_flatpak;;
            12)
                run_flatpak;;
            13)
                manifest_check;;
            14)
                repo_check;;
            15)
                remove_flatpak;;
            16)
                clean_up;;
            17)
                printf '%s\n' "Exit"
                exit 0;;
            *)
                printf '%s\n' "Bye!"
                exit 0
        esac
    } # menu

    install_dev_mode() {
        printf '%s\n' "Install Dev Mode"
        python3 -m pip install -e .
        menu
    }

    run_dev_mode() {
        printf '%s\n' "Run Dev Mode"
        python3 -m file_renamer
        menu
    }

    remove_dev_mode() {
        printf '%s\n' "Remove Dev Mode"
        pip uninstall io.github.mcarlos101.file-renamer -y
        menu
    }

    build_wheel() {
        printf '%s\n' "Build Wheel"
        python3 -m build
        menu
    }

    install_wheel() {
        printf '%s\n' "Install Wheel"
        pip install /data/fr/file-renamer/dist/io.github.mcarlos101.file_renamer-*.whl
        menu
    }

    run_wheel() {
        printf '%s\n' "Run Wheel"
        file-renamer
        menu
    }

    remove_wheel() {
        printf '%s\n' "Remove Wheel"
        pip uninstall io.github.mcarlos101.file-renamer -y
        menu
    }

    build_linux_binary() {
        printf '%s\n' "Build Linux Binary"
        pyinstaller --clean /data/fr/file-renamer/spec/app-linux.spec
        menu
    }

    run_linux_binary() {
        printf '%s\n' "Run Linux Binary"
        /data/fr/file-renamer/dist/file-renamer
        menu
    }

    build_flatpak() {
        printf '%s\n' "Build Flatpak"
        flatpak-builder --verbose --force-clean flatpak-build-dir io.github.mcarlos101.file-renamer.json
        menu
    }

    install_flatpak() {
        printf '%s\n' "Install Flatpak"
        flatpak run org.flatpak.Builder --force-clean --sandbox --user --install --install-deps-from=flathub --ccache --mirror-screenshots-url=https://dl.flathub.org/media/ --repo=repo builddir io.github.mcarlos101.file-renamer.json
        menu
    }

    run_flatpak() {
        printf '%s\n' "Run Flatpak"
        flatpak run io.github.mcarlos101.file-renamer
        menu
    }

    manifest_check() {
        printf '%s\n' "Manifest Check"
        flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest io.github.mcarlos101.file-renamer.json
        menu
    }

    repo_check() {
        printf '%s\n' "Repo Check"
        flatpak run --command=flatpak-builder-lint org.flatpak.Builder repo repo
        menu
    }

    remove_flatpak() {
        printf '%s\n' "Remove Flatpak"
        flatpak uninstall io.github.mcarlos101.file-renamer
        menu
    }

    clean_up() {
        printf '%s\n' "Clean Up"

        printf '%s\n' "Remove __pycache__"
        find /data/fr/file-renamer/src/file_renamer/ -type d -name "__pycache__" -exec rm -rfv {} +

        printf '%s\n' "Remove /data/fr/file-renamer/builddir"
        rm -frv /data/fr/file-renamer/builddir

        printf '%s\n' "Remove /data/fr/file-renamer/dist"
        rm -frv /data/fr/file-renamer/dist

        printf '%s\n' "Remove /data/fr/file-renamer/flatpak-build-dir"
        rm -frv /data/fr/file-renamer/flatpak-build-dir

        printf '%s\n' "Remove /data/fr/file-renamer/.flatpak-builder"
        rm -frv /data/fr/file-renamer/.flatpak-builder

        printf '%s\n' "Remove /data/fr/file-renamer/repo"
        rm -frv /data/fr/file-renamer/repo

        printf '%s\n' "Remove /data/fr/file-renamer/src/io.github.mcarlos101.file_renamer.egg-info"
        rm -frv /data/fr/file-renamer/src/io.github.mcarlos101.file_renamer.egg-info

        menu
    }

    menu
} # file_renamer

file_renamer "$@"
exit 0
