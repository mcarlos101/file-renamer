import logging
import inspect
from abc import ABC, abstractmethod
import file_renamer.html.rc_ui


class UI(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class WebUI(UI):

    def __init__(self, **fr):
        self.fr = fr
        self.html_top = self.top()
        self.html_body = self.fr['html_body'].strip()
        self.html_bottom = self.bottom()
        self.html_page = self.html_top + self.html_body + self.html_bottom

    def top(self):
        html_top = """<!doctype html>
<html lang="en" data-bs-theme='""" + self.fr['theme'] + """'>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>""" + self.fr['html_title'] + """</title>
        <link href='qrc:/css/bootstrap.min.css' rel="stylesheet">
    </head>
    <body>"""
        return html_top

    def bottom(self):
        html_bottom = """
    </body>
</html>"""
        return html_bottom

    def validate(self, value):
        pass
