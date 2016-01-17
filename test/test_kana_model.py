#coding: utf-8

import unittest
from app.models import Kana, PronunciationOfKanamoji
from app import create_app
from database import init_db, db_drop, create_scoped_session
from flask import current_app


class KanaModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

        self.app_context = self.app.app_context()
        self.app_context.push()
        init_db('testing')
        self.session = create_scoped_session(config_name='testing')

    # def tearDown(self):
    #     self.session.remove()
    #
    #     self.app_context.pop()
    #     db_drop('testing')

    def test_pronun(self):
        PronunciationOfKanamoji.insert_pronunciations(self.session)
        pronun = PronunciationOfKanamoji.query.filter_by(character='Seion').first()
        self.assertTrue(pronun is not None)
