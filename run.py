# coding: utf-8

import os
from app import create_app, db
from flask_script import Manager, Shell
from app.models import Kana, PronunciationOfKanamoji

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
db = db
kana = Kana
pok = PronunciationOfKanamoji
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, kana=kana, pok=pok)
manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    """
    Run the unit tests.
    :return:
    """
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

