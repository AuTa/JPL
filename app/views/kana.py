# coding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import Kana, PronunciationOfKanamoji
from app import db, nav
from flask_nav.elements import Navbar, View

kana = Blueprint('kana', __name__)


@nav.navigation()
def mynavbar():
    return Navbar(
        'JPL',
        View('Kana', 'kana.index')
    )


@kana.route('/')
def index():
    seion = [
        [['あ', 'ア', 'a'], ['い', 'イ', 'i'], ['う', 'ウ', 'u'],
        ['え', 'エ', 'e'], ['お', 'オ', 'o']],
        [['か', 'カ', 'ka'], ['け', 'キ', 'ki'], ['く', 'ク', 'ku'],
        ['け', 'ケ', 'ke'], ['こ', 'コ', 'ko']],
        [['さ', 'サ', 'sa'], ['し', 'シ', 'shi'], ['す', 'ス', 'su'],
        ['せ', 'セ', 'se'], ['そ', 'ソ', 'so']],
        [['た', 'タ', 'ta'], ['ち', 'チ', 'chi'], ['つ', 'ツ', 'tsu'],
        ['て', 'テ', 'te'], ['と', 'ト', 'to']],
        [['な', 'ナ', 'na'], ['に', 'ニ', 'ni'], ['ぬ', 'ヌ', 'nu'],
        ['ね', 'ネ', 'ne'], ['の', 'ノ', 'no']],
        [['は', 'ハ', 'ha'], ['ひ', 'ヒ', 'hi'], ['ふ', 'フ', 'fu'],
        ['へ', 'ヘ', 'he'], ['ほ', 'ホ', 'ho']],
        [['ま', 'マ', 'ma'], ['み', 'ミ', 'mi'], ['む', 'ム', 'mu'],
        ['め', 'メ', 'me'], ['も', 'モ', 'mo']],
        [['や', 'ヤ', 'ya'], None, ['ゆ', 'ユ', 'yu'], None, ['よ', 'ヨ', 'yo']],
        [['ら', 'ラ', 'ra'], ['り', 'リ', 'ri'], ['る', 'ル', 'ru'],
        ['れ', 'レ', 're'], ['ろ', 'ロ', 'ro']],
        [['わ', 'ワ', 'wa'], None, None, None, ['を', 'ヲ', 'wo']],
        [['ん', 'ン', 'n'], None, None, None, None]
    ]
    return render_template('kana.html', seion=seion)
