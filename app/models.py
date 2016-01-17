# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, PickleType, DateTime, \
    ForeignKey, Table
# from app import db
from database import Base
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class Kana(Base):
    __tablename__ = 'kanas'
    id = Column(Integer, primary_key=True)
    hiragana = Column(String)
    katakana = Column(String)
    romaji = Column(String)
    pronunciation_id = Column(Integer, ForeignKey('pronunciations.id'))

    def __repr__(self):
        return '<Kana {0}>'.format(self.romaji)

    @staticmethod
    def insert_kanas(session):
        kanas = {
            'Seion': [
                ['あ', 'ア', 'a'], ['い', 'イ', 'i'], ['う', 'ウ', 'u'], ['え', 'エ', 'e'], ['お', 'オ', 'o'],
                ['か', 'カ', 'ka'], ['け', 'キ', 'ki'], ['く', 'ク', 'ku'], ['け', 'ケ', 'ke'], ['こ', 'コ', 'ko'],
                ['さ', 'サ', 'sa'], ['し', 'シ', 'shi'], ['す', 'ス', 'su'], ['せ', 'セ', 'se'], ['そ', 'ソ', 'so'],
                ['た', 'タ', 'ta'], ['ち', 'チ', 'chi'], ['つ', 'ツ', 'tsu'], ['て', 'テ', 'te'], ['と', 'ト', 'to'],
                ['な', 'ナ', 'na'], ['に', 'ニ', 'ni'], ['ぬ', 'ヌ', 'nu'], ['ね', 'ネ', 'ne'], ['の', 'ノ', 'no'],
                ['は', 'ハ', 'ha'], ['ひ', 'ヒ', 'hi'], ['ふ', 'フ', 'fu'], ['へ', 'ヘ', 'he'], ['ほ', 'ホ', 'ho'],
                ['ま', 'マ', 'ma'], ['み', 'ミ', 'mi'], ['む', 'ム', 'mu'], ['め', 'メ', 'me'], ['も', 'モ', 'mo'],
                ['や', 'ヤ', 'ya'], ['ゆ', 'ユ', 'yu'], ['よ', 'ヨ', 'yo'],
                ['ら', 'ラ', 'ra'], ['り', 'リ', 'ri'], ['る', 'ル', 'ru'], ['れ', 'レ', 're'], ['ろ', 'ロ', 'ro'],
                ['わ', 'ワ', 'wa'], ['を', 'ヲ', 'wo'],
                ['ん', 'ン', 'n']
            ],
            'Dakuon': [
                ['が', 'ガ', 'ga'], ['ぎ', 'ギ', 'gi'], ['ぐ', 'グ', 'gu'], ['げ', 'ゲ', 'ge'], ['ご', 'ゴ', 'go'],
                ['ざ', 'ザ', 'za'], ['じ', 'ジ', 'ji'], ['ず', 'ズ', 'zu'], ['ぜ', 'ゼ', 'ze'], ['ぞ', 'ゾ', 'zo'],
                ['だ', 'ダ', 'da'], ['ぢ', 'ヂ', 'di|ji'], ['づ', 'ヅ', 'du|zu'], ['で', 'デ', 'de'], ['ど', 'ド', 'do'],
                ['ば', 'バ', 'ba'], ['び', 'ビ', 'bi'], ['ぶ', 'ブ', 'bu'], ['べ', 'ベ', 'be'], ['ぼ', 'ボ', 'bo'],
            ],
            'Handakuon': [
                ['ぱ', 'パ', 'pa'], ['ぴ', 'ピ', 'pi'], ['ぷ', 'プ', 'pu'], ['ぺ', 'ペ', 'pe'], ['ぽ', 'ポ', 'po'],
            ],
            'Yoon-Seion': [
                ['きゃ', 'キャ', 'kya'], ['きゅ', 'キュ', 'kyu'], ['きょ', 'キョ', 'kyo'],
                ['しゃ', 'シャ', 'sha'], ['しゅ', 'シュ', 'shu'], ['しょ', 'ショ', 'sho'],
                ['ちゃ', 'チャ', 'cha'], ['ちゅ', 'チュ', 'chu'], ['ちょ', 'チョ', 'cho'],
                ['にゃ', 'ニャ', 'nya'], ['にゅ', 'ニュ', 'nyu'], ['にょ', 'ニョ', 'nyo'],
                ['ひゃ', 'ヒャ', 'hya'], ['ひゅ', 'ヒュ', 'hyu'], ['ひょ', 'ヒョ', 'hyo'],
                ['みゃ', 'ミャ', 'mya'], ['みゅ', 'ミュ', 'myu'], ['みょ', 'ミョ', 'myo'],
                ['りゃ', 'リャ', 'rya'], ['りゅ', 'リュ', 'ryu'], ['りょ', 'リョ', 'ryo'],
            ],
            'Yoon-Dakuon': [
                ['ぎゃ', 'ギャ', 'gya'], ['ぎゅ', 'ギュ', 'gyu'], ['ぎょ', 'ギョ', 'gyo'],
                ['じゃ', 'ジャ', 'ja'], ['じゅ', 'ジュ', 'ju'], ['じょ', 'ジョ', 'jo'],
                ['ぢゃ', 'ヂャ', 'dya|ja'], ['ぢゅ', 'ヂュ', 'dyu|ju'], ['ぢょ', 'ヂョ', 'dyo|jo'],
                ['びゃ', 'ビャ', 'bya'], ['びゅ', 'ビュ', 'byu'], ['びょ', 'ビョ', 'byo'],
            ],
            'Yoon-Handakuon': [
                ['ぴゃ', 'ピャ', 'pya'], ['ぴゅ', 'ピュ', 'pyu'], ['ぴょ', 'ピョ', 'pyo'],
            ]
        }
        for key, value in kanas.values():
            for k in value:
                kana = Kana.query.filter_by(hiragana=k[0]).first()
                if kana is None:
                    kana = Kana(hiragana=k[0])
                kana.katakana = k[1]
                kana.romaji = k[2]
                pronunciation = PronunciationOfKanamoji.query.filter_by(character=key).first()
                kana.pronunciation = pronunciation
                session.add(kana)
        session.commit()


class PronunciationOfKanamoji(Base):
    __tablename__ = 'pronunciations'
    id = Column(Integer, primary_key=True)
    character = Column(String)
    kanas = relationship('Kana', backref='pronunciation')

    @staticmethod
    def insert_pronunciations(session):
        pronunciations = [
            'Seion', 'Dakuon', 'Handakuon', 'Yoon-Seion', 'Yoon-Dakuon', 'Yoon-Handakuon'
        ]
        for p in pronunciations:
            pronunciation = PronunciationOfKanamoji.query.filter_by(character=p).first()
            if pronunciation is None:
                pronunciation = PronunciationOfKanamoji(character=p)
            session.add(pronunciation)
        session.commit()
