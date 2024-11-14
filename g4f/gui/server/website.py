from flask import render_template, redirect
from time import time
from os import urandom
import flask
from pathlib import Path

class Website:
    def __init__(self, app) -> None:
        self.app = app
        self.routes = {
            '/': {
                'function': lambda: redirect('/chat'),
                'methods': ['GET', 'POST']
            },
            '/chat/': {
                'function': self._index,
                'methods': ['GET', 'POST']
            },
            '/chat/<conversation_id>': {
                'function': self._chat,
                'methods': ['GET', 'POST']
            },
            '/assets/<folder>/<file>': {
                'function': self._assets,
                'methods': ['GET', 'POST']
            }
        }

    def _chat(self, conversation_id):
        if '-' not in conversation_id:
            return redirect('/chat')

        return render_template('index.html', chat_id = conversation_id)

    def _index(self):
        return render_template('index.html', chat_id = f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}')

    def _assets(self, folder: str, file: str):
        try:
            return flask.send_from_directory((p := Path(f"./../client/{folder}/{file}")).parent, p.name, as_attachment=False)
        except:
            return "File not found", 404
