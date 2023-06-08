from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__, static_folder="templates/static")

client = MongoClient(
    "mongodb+srv://sparta:test@cluster0.ihsomwt.mongodb.net/?retryWrites=true&w=majority",
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


# 회원 가입
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
    user = db.user.find_one({"id": id_receive},{"_id":False})

    return jsonify({"result": user})


# 유저 정보 조회
@app.route("/user", methods=["GET"])
def getUser():
    ns = request.args.get("id", type=str)  # 파라미터 받는 부분

    all_comments = list(db.user.find({}, {"_id": False}))

    return jsonify({"result": all_comments})


# 로그인
@app.route("/user/login", methods=["POST"])
def login():
    id_receive = request.form["id_give"]
    password_receive = request.form["password_give"]

    user = db.user.find_one({"id": id_receive})
    
    if user == None :
        result = 0
    elif user['password'] != password_receive :
        result = 1
    else :
        result = 2

    return jsonify({"result": result})


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
    pass


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
    pass


# 글 작성
@app.route("/posts", methods=["POST"])
def writePost():
    pass


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
