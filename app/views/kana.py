# coding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, \
    jsonify
from app.models import Kana, PronunciationOfKanamoji
from app import db
from flask_nav.elements import Navbar, View
from app.forms import KanaForm

kana = Blueprint('kana', __name__)


# @kana.route('/test/_form_autofocus')
# def form_autofocus():
#     autofocus = session.get('placeholder')[1]
#     return jsonify(autofocus=autofocus)


@kana.route('/')
def index():
    kana = {
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
    return render_template('kana/kana.html', kana=kana)


@kana.route('/test', methods=['GET', 'POST'])
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
    
