from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
import requests
from bs4 import BeautifulSoup
import json
from bson import json_util
import math
from bson import ObjectId

app = Flask(__name__, static_folder="templates/static")

client = MongoClient(
    "mongodb+srv://sparta:test@cluster0.p5xkuy6.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)
db = client.dbsparta


@app.route("/")
def home():
    return render_template("pages/login.html")


# 글 상세 페이지
@app.route("/detail")
def detail_page():
    return render_template("pages/detail.html")


# 회원 가입 페이지
@app.route("/join")
def join_page():
    return render_template("pages/join.html")


# 로그인 페이지
@app.route("/login")
def login_page():
    return render_template("pages/login.html")


# 메인 페이지 (글 목록 페이지)
@app.route("/main")
def main_page():
    return render_template("pages/main.html")


# 마이페이지
@app.route("/my")
def my_page():
    return render_template("pages/my.html")


# 글 작성 페이지
@app.route("/write")
def write_page():
    return render_template("pages/write.html")


#회원 가입
@app.route("/user/join", methods=["POST"])
def join():
    id_receive = request.form["id_give"]
    name_receive = request.form["name_give"]
    password_receive = request.form["password_give"]

    doc = {"id": id_receive, "name": name_receive, "password": password_receive}

    db.user.insert_one(doc)

    return jsonify({"msg": "가입 성공!"})


# 회원가입 아이디 중복 체크 조회
@app.route("/user/idcheck", methods=["POST"])
def idcheck():
    id_receive = request.form["id_give"]
    user = db.user.find_one({"id": id_receive}, {"_id": False})

    return jsonify({"result": user})


#유저 정보 조회
@app.route("/user", methods=["GET"])
def getUser():
    id = request.args.get("id", type=str)
    user = db.user.find_one({'userId' : id}, {'_id':False})

    return jsonify({'user': user})

#유저 정보 수정
@app.route("/user", methods=["PUT"])
def updateUser():
    id = request.form['userId']
    new_name = request.form['newusername']

    db.user.update_one({"userId": id}, {"$set":{"userName": new_name}})

    return jsonify({'msg': "유저 이름이 변경되었습니다."})

# 로그인
@app.route("/user/login", methods=["POST"])
def login():
    id_receive = request.form["id_give"]
    password_receive = request.form["password_give"]

    user = db.user.find_one({"id": id_receive})

    if user == None:
        result = 0
        id = None
    elif user["password"] != password_receive:
        result = 1
        id = None
    else:
        result = 2
        id = user["id"]

    return jsonify({"result": result, "id": id})

# 내가 작성할 글 조회
@app.route("/posts", methods=["GET"])
def getPost():
    id = request.args.get("id", type=str)
    startIndex = request.args.get("startIndex", type=int)
    element_size = 3

    print(id)
    print(startIndex)

    posts = list(db.posts.find({'userId' : id}).skip(startIndex).limit(element_size))

    return jsonify({'result': json.loads(json_util.dumps(posts))})

# 내가 작성한 글 개수 조회
@app.route("/posts/my/count", methods=["GET"])
def getPostPageCount():
    id = request.args.get("id", type=str)
    element_size = 3
    
    result = len(list(db.posts.find({"userId" : id})))

    return jsonify({'count': math.ceil(result/element_size)})   

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
    post_id = request.args.get("postId", type=str)
    result = db.posts.find_one({"_id" : ObjectId(post_id)}, {'_id': False})

    return jsonify({'result': result})


# 댓글 목록 조회
@app.route("/posts/comment", methods=["GET"])
def getPostComments():
    post_id = request.args.get("postId", type=str)
    all_comment = list(db.comment.find({"postId" : post_id}, {'_id': False}))

    return jsonify({'result': all_comment})

# 댓글 개수 조회
@app.route("/posts/comment/count", methods=["GET"])
def getPostCommentscount():
    post_id = request.args.get("postId", type=str)
    element_size = 3

    result = len(list(db.comment.find({"postId" : post_id})))

    return jsonify({'count': math.ceil(result/element_size)})


# 댓글 작성
@app.route("/posts/comment", methods=["POST"])
def writeComment():
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    user_id = request.form['userid_give']
    post_id = request.form['postid_give']

    comment_list = list(db.comment.find({}, {'_id': False}))
    count = len(comment_list) + 1
    doc = {
        'num':count,
        'comment' : comment_receive,
        'star':star_receive,
        'userId':user_id,
        'postId':post_id
    }
    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


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
    


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
