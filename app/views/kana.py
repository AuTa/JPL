# coding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, \
    jsonify, make_response
from app.models import Kana, PronunciationOfKanamoji, User, KanaTest
from app import db
from flask_nav.elements import Navbar, View
from app.forms import KanaForm
from datetime import timedelta
import time
import hashlib
import json
from copy import deepcopy
kana = Blueprint('kana', __name__)

kana_state = {
    'Seion': [
        [[True, True], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], None, [True, False], None, [True, False]],
        [[True, False], [True, False], [True, False], [True, False], [True, False]],
        [[True, False], None, None, None, [True, False]],
        [[True, False], None, None, None, None]
    ],
    'Dakuon': [
        [[False, False], [False, False], [False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False], [False, False], [False, False]],
    ],
    'Yoon-Seion': [
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
        [[False, False], [False, False], [False, False]],
    ]
}


@kana.route('/_ajax_state')
def ajax_state():
    col = request.args.get('col', 0, type=int)
    row = request.args.get('row', 0, type=int)
    character = request.args.get('character')
    hiragana = request.args.get('hiragana', type=int)
    session_id = request.cookies.get('session_id')
    with db.session as session:
        user = User.query(session).filter_by(session_id=session_id).first()
        kana = deepcopy(user.kana_state)
        print(kana[character][row])
        state = kana[character][row][col][hiragana]
        kana[character][row][col][hiragana] = not state
        print(user.kana_state[character][row])
        print( kana == user.kana_state)
        user.kana_state = kana
        user.username = time.time()
        session.add(user)
        session.commit()
    return jsonify()


@kana.route('/')
def index():
    kanas = {
        'Seion': [
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
        ],
        'Dakuon': [
            [['が', 'ガ', 'ga'], ['ぎ', 'ギ', 'gi'], ['ぐ', 'グ', 'gu'],
             ['げ', 'ゲ', 'ge'], ['ご', 'ゴ', 'go']],
            [['ざ', 'ザ', 'za'], ['じ', 'ジ', 'ji'], ['ず', 'ズ', 'zu'],
             ['ぜ', 'ゼ', 'ze'], ['ぞ', 'ゾ', 'zo']],
            [['だ', 'ダ', 'da'], ['ぢ', 'ヂ', 'di|ji'], ['づ', 'ヅ', 'du|zu'],
             ['で', 'デ', 'de'], ['ど', 'ド', 'do']],
            [['ば', 'バ', 'ba'], ['び', 'ビ', 'bi'], ['ぶ', 'ブ', 'bu'],
             ['べ', 'ベ', 'be'], ['ぼ', 'ボ', 'bo']],
        ],
        'Handakuon': [
            [['ぱ', 'パ', 'pa'], ['ぴ', 'ピ', 'pi'], ['ぷ', 'プ', 'pu'],
             ['ぺ', 'ペ', 'pe'], ['ぽ', 'ポ', 'po']]
        ],
        'Yoon-Seion': [
            [['きゃ', 'キャ', 'kya'], ['きゅ', 'キュ', 'kyu'], ['きょ', 'キョ', 'kyo']],
            [['しゃ', 'シャ', 'sha'], ['しゅ', 'シュ', 'shu'], ['しょ', 'ショ', 'sho']],
            [['ちゃ', 'チャ', 'cha'], ['ちゅ', 'チュ', 'chu'], ['ちょ', 'チョ', 'cho']],
            [['にゃ', 'ニャ', 'nya'], ['にゅ', 'ニュ', 'nyu'], ['にょ', 'ニョ', 'nyo']],
            [['ひゃ', 'ヒャ', 'hya'], ['ひゅ', 'ヒュ', 'hyu'], ['ひょ', 'ヒョ', 'hyo']],
            [['みゃ', 'ミャ', 'mya'], ['みゅ', 'ミュ', 'myu'], ['みょ', 'ミョ', 'myo']],
            [['りゃ', 'リャ', 'rya'], ['りゅ', 'リュ', 'ryu'], ['りょ', 'リョ', 'ryo']],
        ],
        'Yoon-Dakuon': [
            [['ぎゃ', 'ギャ', 'gya'], ['ぎゅ', 'ギュ', 'gyu'], ['ぎょ', 'ギョ', 'gyo']],
            [['じゃ', 'ジャ', 'ja'], ['じゅ', 'ジュ', 'ju'], ['じょ', 'ジョ', 'jo']],
            [['ぢゃ', 'ヂャ', 'dya|ja'], ['ぢゅ', 'ヂュ', 'dyu|ju'], ['ぢょ', 'ヂョ', 'dyo|jo']],
            [['びゃ', 'ビャ', 'bya'], ['びゅ', 'ビュ', 'byu'], ['びょ', 'ビョ', 'byo']],
        ],
        'Yoon-Handakuon': [
            [['ぴゃ', 'ピャ', 'pya'], ['ぴゅ', 'ピュ', 'pyu'], ['ぴょ', 'ピョ', 'pyo']],
        ]
    }
    session_id = request.cookies.get('session_id')
    global kana_state
    if session_id is not None:
        with db.session as session:
            user = User.query(session).filter_by(session_id=session_id).first()
            kana_state = user.kana_state
    resp = make_response(render_template('kana/kana.html', kanas=kanas, kana_state=kana_state))
    if session_id is None:
        user_agent = request.headers.get('User-Agent')
        user_agent_hash = hashlib.md5('{0}{1}'.format(user_agent, time.time()).encode('utf-8'))\
            .hexdigest()
        with db.session as session:
            user = User(session_id=user_agent_hash)
            session.add(user)
            session.commit()
        resp.set_cookie('session_id', user_agent_hash, max_age=timedelta(days=365))
    return resp


@kana.route('/test/', methods=['GET', 'POST'])
def test():
    form = KanaForm()
    if session.get('placeholder') is not None:
        if session.get('placeholder')[1] == 1:
            form.kanamoji.label.text = session.get('placeholder')[0]
            session['placeholder'][1] = 0
        else:
            form.kanamoji.label.text = 'Press Space Start'
            session['placeholder'][1] = 1
    if form.validate_on_submit():
        session['kanamoji'] = form.kanamoji.data
        session['render_time'] = form.render_time.data
        session['submit_time'] = form.submit_time.data
        session['placeholder'] = ['Input the Romaji', 1]
        return redirect(url_for('.test'))
    return render_template('kana/test.html',
                           form=form,
                           kanamoji=session.get('kanamoji'),
                           render_time = session.get('render_time'),
                           submit_time = session.get('submit_time'),
                           autofocus=session.get('placeholder')[1])
    
