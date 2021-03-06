# coding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, \
    jsonify, make_response
from app.models import Kana, PronunciationOfKanamoji, User, KanaTest
from app import db
from flask_nav.elements import Navbar, View
from app.forms import KanaForm
from datetime import timedelta, datetime
import time
import hashlib
import json
from copy import deepcopy
import random
from sqlalchemy import or_, and_

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
kanas = {
    'Seion': [
        [['あ', 'ア', 'a'], ['い', 'イ', 'i'], ['う', 'ウ', 'u'],
         ['え', 'エ', 'e'], ['お', 'オ', 'o']],
        [['か', 'カ', 'ka'], ['き', 'キ', 'ki'], ['く', 'ク', 'ku'],
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


def add_user(resp, db_session):
    user_agent = request.headers.get('User-Agent')
    user_agent_hash = hashlib.md5('{0}{1}'.format(user_agent, time.time()).encode('utf-8')) \
        .hexdigest()
    user = User(session_id=user_agent_hash)
    user.kana_state = [x[0] for y in kanas['Seion'] for x in y if x is not None]
    user.register_time = datetime.utcnow()
    db_session.add(user)
    db_session.commit()
    user_kana_state = user.kana_state
    resp.set_cookie('session_id', user_agent_hash, max_age=timedelta(days=365))
    session['kana_state'] = user_kana_state


kana = Blueprint('kana', __name__)


@kana.route('/')
def index():
    session_id = request.cookies.get('session_id')
    if session.get('kana_state') is None:
        session['kana_state'] = [x[0] for y in kanas['Seion'] for x in y if x is not None]
        session['default_state'] = True
    resp = make_response(
        render_template('kana/kana.html', kanas=kanas, kana_state=session.get('kana_state')))

    if session_id is not None:
        with db.session as db_session:
            user = User.query(db_session).filter_by(session_id=session_id).first()
            if user is None:
                return resp
            user_kana_state = user.kana_state
            if session.get('kana_state') != user_kana_state and session.get(
                    'dafault_state') == False:
                user.kana_state = session.get('kana_state')
                db_session.add(user)
                db_session.commit()

    return resp


@kana.route('/test/')
def test():
    session_id = request.cookies.get('session_id')
    form = KanaForm()
    prev_kana = '-'
    session['cur_kana'] = '-'
    session['next_kana'] = '-'
    session['result'] = [0, None, '', 0]

    if session_id is None:
        resp = make_response(render_template('kana/test.html',
                                             kanas=kanas,
                                             form=form,
                                             kana_state=session.get('kana_state'),
                                             display_kana=[prev_kana,
                                                           session.get('cur_kana'),
                                                           session.get('next_kana')],
                                             score=session.get('result')[0]))
        with db.session as db_session:
            add_user(resp, db_session)
        return resp
    else:
        with db.session as db_session:
            user = User.query(db_session).filter_by(session_id=session_id).first()
            if user is None:
                resp = make_response(render_template('kana/test.html',
                                                     kanas=kanas,
                                                     form=form,
                                                     kana_state=session.get('kana_state'),
                                                     display_kana=[prev_kana,
                                                                   session.get('cur_kana'),
                                                                   session.get('next_kana')],
                                                     score=session.get('result')[0]))
                add_user(resp, db_session)
                return resp
            session['result'][0] = user.score or 0
            user_kana_state = user.kana_state
            if session.get('kana_state') != user_kana_state and session.get(
                    'dafault_state') == False:
                user.kana_state = session.get('kana_state')
                db_session.add(user)
                db_session.commit()

    print(session.get('result')[0])

    return render_template('kana/test.html',
                           kanas=kanas,
                           form=form,
                           kana_state=session.get('kana_state'),
                           display_kana=[prev_kana,
                                         session.get('cur_kana'),
                                         session.get('next_kana')],
                           score=session.get('result')[0])


@kana.route('/_ajax_state', methods=['POST'])
def ajax_state():
    kana_state = session.get('kana_state')
    data = request.get_json()
    kanamoji = data['kanamoji']
    for i in kanamoji:
        if i is None:
            kanamoji.remove(i)
            for j in kanamoji:
                if j not in kana_state:
                    kana_state.append(j)
            break
        else:
            if i in kana_state:
                kana_state.remove(i)
            else:
                kana_state.append(i)
    session['default_state'] = False
    return jsonify()


@kana.route('/_ajax_test', methods=['POST'])
def ajax_test():
    session_id = request.cookies.get('session_id')
    kana_state = session.get('kana_state')
    data = request.get_json()
    kanamoji = data['kanamoji']
    next_kana_count = ''
    prev_romaji = session.get('romaji')

    if kanamoji == 'start':
        cur_kana = random.choice(kana_state)
        next_kana = random.choice(kana_state)
        prev_kana = session.get('cur_kana')
        session['cur_kana'] = cur_kana
        session['next_kana'] = next_kana

        with db.session as db_session:
            kana_model = Kana.query(db_session).filter(
                    or_(Kana.hiragana == cur_kana, Kana.katakana == cur_kana)).first()
            session['romaji'] = kana_model.romaji
    else:
        render_time = data['render_time']
        submit_time = data['submit_time']
        render_time = datetime.utcfromtimestamp(float(render_time) / 1000)
        submit_time = datetime.utcfromtimestamp(float(submit_time) / 1000)
        use_time = submit_time - render_time
        cur_kana = session.get('cur_kana')

        if kanamoji == prev_romaji:
            if session.get('result')[1] == True:
                session['result'][0] += 2
                session['result'][3] += 2
                session['result'][2] = '+2'
            else:
                session['result'][0] += 1
                session['result'][3] += 1
                session['result'][2] = '+1'
                session['result'][1] = True
        else:
            if session.get('result')[1] == False:
                session['result'][0] -= 2
                session['result'][3] -= 2
                session['result'][2] = '-2'
            else:
                session['result'][0] -= 1
                session['result'][3] -= 1
                session['result'][2] = '-1'
                session['result'][1] = False

        with db.session as db_session:
            user = User.query(db_session).filter_by(session_id=session_id).first()
            kana_model = Kana.query(db_session).filter(
                    or_(Kana.hiragana == cur_kana, Kana.katakana == cur_kana)).first()
            user.score = session.get('result')[0]
            kanatest = KanaTest(kanamoji=cur_kana)
            kanatest.use_time = use_time
            kanatest.submit_time = submit_time
            kanatest.enter_str = kanamoji
            kanatest.kana = kana_model
            kanatest.user = user
            kanatest.result = session.get('result')[1]
            db_session.add(user, kanatest)
            db_session.commit()

        cur_kana = session['next_kana']
        next_kana = random.choice(kana_state)
        prev_kana = session.get('cur_kana')
        session['cur_kana'] = cur_kana
        session['next_kana'] = next_kana
        with db.session as db_session:
            kana_model = Kana.query(db_session).filter(
                    or_(Kana.hiragana == cur_kana, Kana.katakana == cur_kana)).first()
            session['romaji'] = kana_model.romaji

            count_0 = db_session.query(KanaTest).join(KanaTest.user)\
                .filter(and_(User.session_id == session_id,
                             KanaTest.kanamoji == next_kana,
                             KanaTest.result == True)).count()
            count_1 = db_session.query(KanaTest).join(KanaTest.user)\
                .filter(and_(User.session_id == session_id,
                             KanaTest.kanamoji == next_kana,
                             KanaTest.result == False)).count()
            count_2 = db_session.query(KanaTest).join(KanaTest.user)\
                .filter(and_(User.session_id == session_id,
                             KanaTest.kanamoji == next_kana)).count()
            next_kana_count = '{0}/{1}/{2}'.format(count_0, count_1, count_2)

    return jsonify(display_kana=[prev_kana,
                                 session.get('cur_kana'),
                                 session.get('next_kana'), ],
                   result=session.get('result'),
                   romaji=prev_romaji,
                   next_kana_count=next_kana_count)
