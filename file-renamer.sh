#!/usr/bin/env bash

file_renamer() {

	menu() {
	    printf '%b\n' "\u001B[1mFile Renamer\u001B[0m"
		printf '%s\n' "1. Run"
		printf '%s\n' "2. Build Linux Binary"
		printf '%s\n' "3. Build Wheel"
        printf '%s\n' "4. Uninstall File Renamer"
		printf '%s\n' "5. Install Wheel"
		printf '%s\n' "6. PyPi Upload Wheel"
		printf '%s\n' "7. Exit"
		read -r -s -n 1 -p "Enter Number: " keypress
		printf '%s' "$keypress"
		printf '\n\n'

		case "$keypress" in
			1)
			    run;;
			2)
				build_linux_binary;;
			3)
                build_whl;;
			4)
			    uninstall;;
			5)
				install_whl;;
			6)
			    pypi_upload_whl;;
			7)
				printf '%s\n' "Exit"
				exit 0;;
			*)
				printf '%s\n' "Bye"
				exit 0
		esac

	} # menu

	run() {
        PYTHONPATH=src python -m file_renamer
	}

	build_linux_binary() {
        python -m nuitka \
            --standalone \
            --output-filename=file-renamer \
            --output-dir=deploy \
            --include-data-dir=/data/fr/file-renamer/icons=icons \
            --include-data-dir=/data/fr/file-renamer/themes=themes \
            --enable-plugin=pyside6 \
            /data/fr/file-renamer/src/file_renamer/__main__.py
	}

	build_whl() {
        python -m build
	}

	uninstall() {
        pip uninstall -y PySide6 PySide6_Addons PySide6_Essentials shiboken6 Unidecode file-renamer
	}

    install_whl() {
        pip install dist/file_renamer-*.whl
    }

    pypi_upload_whl() {
        python -m twine upload dist/file_renamer-*
    }

    menu

}

reset
file_renamer

exit 0
