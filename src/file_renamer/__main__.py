# Compilation mode, standalone everywhere, except on macOS there app bundle
# nuitka-project-if: {OS} in ("Windows", "Linux", "FreeBSD"):
#    nuitka-project: --onefile
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --standalone
#    nuitka-project: --macos-create-app-bundle
#
# Debugging options, controlled via environment variable at compile time.
# nuitka-project-if: os.getenv("DEBUG_COMPILATION", "no") == "yes"
#     nuitka-project: --enable-console
# nuitka-project-else:
#     nuitka-project: --disable-console

if __name__ == "__main__":
    # print ('__package__: ', __package__)
    # print ('__name__   : ', __name__)
    from src.file_renamer.cli import start_app

    start_app()
