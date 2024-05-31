if __name__ == "__main__":
    import os
    import logging
    import platform
    from pathlib import Path
    from file_renamer.cli import start_app

    tab = '   '  # 3 spaces
    home = os.path.expanduser('~')
    logs = Path(home + "/file-renamer.log")
    try:
        platform = platform.system()

        # Logs
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            filename=logs,
            filemode='w',
            level=logging.DEBUG
        )
    except Exception as err:
        print(f"Error: {err=}")
        print(f"Type:  {type(err)=}")
        raise
    else:
        logging.info('__main__.py')
        logging.info('%splatform: %s', tab, platform)

        params = {
            "tab": tab,
            "home": home,
            "logs": logs,
            "platform": platform,
            "app": None,
            "widget": None,
            "ui": None,
            "path": "",
            "base": "",
            "dir": "",
            "name": "",
            "ext": "",
            "id": "",
            "new": "",
            "current": "",
            "html_title": "",
            "html_body": ""
        }

        start_app(**params)
