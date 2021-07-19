from flask import Flask,g,request, Response, make_response,session, render_template
from datetime import datetime, date, timedelta
from flask.helpers import flash

from flask.templating import render_template

app = Flask(__name__)
app.debug = True
#app.jinja_env.trim_blocks = True

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

class Nav:
    def __init__(self, title, url = "#", children = []):
        self.title = title
        self.url = url
        self.children = children

@app.route('/tmpl3')
def tmpl3():
    py = Nav("파이썬", "https://search.naver.com", [])
    java = Nav("자바", "https://search.naver.com", [])
    prg = Nav("프로그래밍 언어", "https://search.naver.com", [py, java])
    jinja = Nav("Jinja", "https://search.naver.com", [])
    gc = Nav("Genshi, Cheetah", "https://search.naver.com", [])
    flask = Nav("플라스크", "https://search.naver.com", [jinja, gc])
    spr = Nav("스프링", "https://search.naver.com", [])
    ndjs = Nav("노드JS", "https://search.naver.com", [])
    webf = Nav("웹 프레임워크", "https://search.naver.com", [flask, spr, ndjs])
    my = Nav("나의 일상", "https://search.naver.com", [])
    issue = Nav("이슈 게시판", "https://search.naver.com", [])
    others = Nav("기타", "https://search.naver.com", [my, issue])
    return render_template('index.html', navs=[prg, webf, others])


@app.route('/tmpl')
def t():
    return render_template('index.html', title="Title")

@app.route('/wctest')
def wctest():
    return render_template('wctest.html', title="test")

@app.route('/wc', methods=["GET"])
def wc():
    key = request.args.get('key', type=str)
    val = request.args.get('val', type=str)
    res = Response("key:"+key+"val"+val)
    res.set_cookie(key, val)
    # session['Token'] = '123X'
    return make_response(res)

@app.route('/rc')
def rc():
    key = request.args.get('key')
    val = request.cookies.get(key)
    return "cookies[" + key + "] = " + val +"," + session.get('Token')

@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다!"

@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(),type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식:" + str(datestr)

@app.before_request
def before_request():
    print("before_request!!!")
    g.str = "한글"

@app.route("/gg")
def helloworld2():
    return "Hello flask world!" + getattr(g, 'str', '111')

@app.route("/")
def helloworld():
    return "Hello flask world!!!"

@app.route("/top100")
def top100():
    return render_template('application.html',title = "MAIN!!" )

@app.route("/login")
def login():
    return render_template('login.html', title="login")

@app.route("/loginInfo", methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        name = request.form['name']
        resp = make_response("LOGIN FINISHH")
        resp.set_cookie('userID', name)
        return resp