if __name__ == "__main__":
    import os
    import logging
    import platform
    import inspect
    from pathlib import Path
    from file_renamer.cli import start_app

    tab = '   '  # 3 spaces
    home = os.path.expanduser('~')

    # Logs
    logfile = Path(home + "/file-renamer.log")
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=logfile,
        encoding='utf-8',
        filemode='w',
        level=logging.DEBUG
    )

    try:
        platform = platform.system()
    except Exception as err:
        print('See logs: ', logfile)
        logger.exception(err)
    else:
        logger.info(__file__)
        name = '__main__'
        logger.info(name)
        logger.info('platform: %s', platform)

        fr = {
            "home": home,
            "platform": platform,
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

        start_app(**fr)
