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

kana = Blueprint('kana', __name__)


@kana.route('/_ajax_state', methods=['POST'])
def ajax_state():
    kana_state = session.get('kana_state')
    data = request.get_json()
    chara_row_col_hira = data['chara_row_col_hira']
    # print(chara_row_col_hira[1])
    # if chara_row_col_hira[0] is None:
    #     character = chara_row_col_hira[1]
    #     hiragana = int(chara_row_col_hira[2])
    #     for i in character:
    #         kana_state[i] = \
    #             [[x, z, hiragana] for x, y in enumerate(kanas[i]) for z in range(len(y))]
    for i in chara_row_col_hira:
        if i is None:
            character = chara_row_col_hira[1]
            hiragana = int(chara_row_col_hira[2])
            for j in character:
                kana_state[j] = \
                    [[x, z, hiragana] for x, y in enumerate(kanas[j]) for z in range(len(y))]
            break
        else:
            character = i[0]
            row_col_hira = i[1]
            if row_col_hira in kana_state[character]:
                kana_state[character].remove(row_col_hira)
            else:
                kana_state[character].append(row_col_hira)
    return jsonify()


@kana.route('/')
def index():

    kana_state = {
        'Seion': [[x, z, 0] for x, y in enumerate(kanas['Seion']) for z in range(len(y))],
        'Dakuon': [],
        'Handakuon': [],
        'Yoon-Seion': [],
        'Yoon-Dakuon': [],
        'Yoon-Handakuon': [],
    }
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        session['session_id'] = session_id
        with db.session as dbsession:
            user = User.query(dbsession).filter_by(session_id=session_id).first()
            user_kana_state = user.kana_state
            if session.get('kana_state') is not None:
                pass
            elif session.get('kana_state') != user_kana_state:
                print(session.get('kana_state'))
                print(user_kana_state)
                user.kana_state = session.get('kana_state')
                dbsession.add(user)
                dbsession.commit()
    resp = make_response(render_template('kana/kana.html', kanas=kanas, kana_state=session.get('kana_state')))
    if session_id is None:
        user_agent = request.headers.get('User-Agent')
        user_agent_hash = hashlib.md5('{0}{1}'.format(user_agent, time.time()).encode('utf-8')) \
            .hexdigest()
        with db.session as dbsession:
            user = User(session_id=user_agent_hash)
            user.kana_state = kana_state
            dbsession.add(user)
            dbsession.commit()
            user_kana_state = user.kana_state
        resp.set_cookie('session_id', user_agent_hash, max_age=timedelta(days=365))
        session['session_id'] = user_agent_hash
        session['kana_state'] = user_kana_state
    return resp


@kana.route('/test/', methods=['GET', 'POST'])
def test():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return redirect(url_for('.index'))

    form = KanaForm()

    if session.get('placeholder') is not None:
        if session.get('placeholder')[1] == 1:
            form.kanamoji.label.text = session.get('placeholder')[0]
            session['placeholder'][1] = 0
        else:
            form.kanamoji.label.text = 'Press Space Start'
            session['placeholder'][1] = 1

    kana_state = {}
    with db.session as dbsession:
        user = User.query(dbsession).filter_by(session_id=session_id).first()
        kana_state = user.kana_state

    if form.validate_on_submit():
        session['kanamoji'] = form.kanamoji.data
        session['render_time'] = form.render_time.data
        session['submit_time'] = form.submit_time.data
        session['placeholder'] = ['Input the Romaji', 1]
        return redirect(url_for('.test'))
    return render_template('kana/test.html',
                           form=form,
                           kanamoji=session.get('kanamoji'),
                           render_time=session.get('render_time'),
                           submit_time=session.get('submit_time'),
                           autofocus=session.get('placeholder')[1])
