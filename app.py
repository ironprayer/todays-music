from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
import requests
from bs4 import BeautifulSoup
import json
from bson import json_util
import math

app = Flask(__name__, static_folder="templates/static")

client = MongoClient('mongodb+srv://sparta:test@cluster0.p5xkuy6.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

@app.route('/')
def home():
   return render_template('pages/login.html')

# 글 상세 페이지
@app.route('/detail')
def detail_page():
   return render_template('pages/detail.html')

# 회원 가입 페이지
@app.route('/join')
def join_page():
   return render_template('pages/join.html')

# 로그인 페이지
@app.route('/login')
def login_page():
   return render_template('pages/login.html')

# 메인 페이지 (글 목록 페이지)
@app.route('/main')
def main_page():
   return render_template('pages/main.html')

# 마이페이지
@app.route('/my')
def my_page():
   return render_template('pages/my.html')

# 글 작성 페이지
@app.route('/write')
def write_page():
   return render_template('pages/write.html')

# 회원 가입
@app.route("/user/join", methods=["POST"])
def join():
    name_receive = request.form['name_give']
    
    doc = {
        'name' : name_receive,
    }

    db.fan.insert_one(doc)

    return jsonify({'msg': '저장 완료'})

# 유저 정보 조회
@app.route("/user", methods=["GET"])
def getUser():
    ns = request.args.get("id", type=str) # 파라미터 받는 부분

    all_comments = list(db.fan.find({}, {'_id':False}))
    
    return jsonify({'result': all_comments})


# 로그인
@app.route("/user/login", methods=["POST"])
def login():
    pass


# 로그인
@app.route("/user", methods=["PUT"])
def updateUser():
    pass


# 내가 작성할 글 조회
@app.route("/posts", methods=["GET"])
def getPost():
    pass

# 내가 작성한 글 삭제
@app.route("/posts", methods=["DELETE"])
def deleteUser():
    pass

# 지역별 글 목록 조회
@app.route("/posts/region", methods=["GET"])
def getPostsWithRegion():
    regionName = request.args.get("regionName", type=str)
    startIndex = request.args.get("startIndex", type=int)
    element_size = 3
    if(regionName == "전체") :
        result = list(db.posts.find({}).skip(startIndex).limit(element_size))
    else :
        result = list(db.posts.find({"region" : regionName}).skip(startIndex).limit(element_size))

    return jsonify({'result': json.loads(json_util.dumps(result))})

# 지역별 글 개수 조회
@app.route("/posts/region/count", methods=["GET"])
def getPostPageCountWithRegion():
    regionName = request.args.get("regionName", type=str)
    element_size = 3
    if(regionName == "전체") :
        result = len(list(db.posts.find({})))
    else :
        result = len(list(db.posts.find({"region" : regionName})))

    return jsonify({'count': math.ceil(result/element_size)})    

# 글 상세 조회
@app.route("/posts/detail", methods=["GET"])
def getPostDetail():
    pass

# 댓글 목록 조회
@app.route("/posts/comment", methods=["GET"])
def getPostComments():
    pass

# 댓글 작성
@app.route("/posts/comment", methods=["POST"])
def writeComment():
    pass

# 지역별 날씨 조회
@app.route("/posts/weather", methods=["GET"])
def getRegionWeather():
    region = request.args.get("region", type=str)
    URL = "https://weather.naver.com/today/api/nation/20230608/now"
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(URL,headers=headers).json()

    region_dic = {
        "서울" : "서울",
        "경기" : "수원",
        "강원" : "춘천",
        "충남" : "대전",
        "충북" : "청주",
        "경북" : "안동",
        "경남" : "부산",
        "전북" : "전주",
        "전남" : "목포",
        "제주" : "제주"
    }
    weather_dic = {}

    for value in data.values() :
        weather_dic[value["regionName"]] = {
            "wetrTxt" : value["wetrTxt"],
            "tmp" : value["tmpr"]
        }

    return jsonify({'result': weather_dic[region_dic[region]]})

# 글 작성
@app.route("/posts", methods=["POST"])
def writePost():
    region_receive = request.form["region_give"]
    temp_icon_receive = request.form["temp_icon_give"]
    temp_receive = request.form["temp_give"]
    title_receive = request.form["title_give"]
    music_link_receive = request.form["music_link_give"]
    content_receive = request.form["content_give"]
    ogtitle = ''
    ogimage = '' 
    ogdesc = ''
    is_validation_music_link = True   

    try :
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(music_link_receive,headers=headers)
    except :
        is_validation_music_link = False
        music_link_receive = ''

    if is_validation_music_link :
        soup = BeautifulSoup(data.text, 'html.parser')

        ogtitle = soup.select_one('meta[property="og:title"]')['content']
        ogimage = soup.select_one('meta[property="og:image"]')['content']
        ogdesc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'region' : region_receive,
        'temp_icon': temp_icon_receive,
        'temp': temp_receive,
        'title': title_receive,
        'music_link': music_link_receive,
        'content': content_receive,
        'ogtitle': ogtitle,
        'ogimage': ogimage,
        'ogdesc': ogdesc
    }

    db.posts.insert_one(doc)

    return jsonify({'msg': '저장 완료'})
    

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
