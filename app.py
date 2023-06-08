from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
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
    pass

# 글 상세 조회
@app.route("/posts/detail", methods=["GET"])
def getPostDetail():
    all_posts = list(db.posts.find({}, {'_id': False}))
    # all_posts = list(db.posts.find({})) # 전체 검색
    
    # id = str(all_data[0]["_id"]) # _id 문자로 변경
    # id_data = db.posts.find_one({"_id" : ObjectId(id)}) # 문자를 ObjectId로 변환해서 검색

    return jsonify({'result': all_posts})

# 댓글 목록 조회
@app.route("/posts/comment", methods=["GET"])
def getPostComments():
    all_comment = list(db.comment.find({}, {'_id': False}))

    return jsonify({'result': all_comment})

# 댓글 작성
@app.route("/posts/comment", methods=["POST"])
def writeComment():
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    comment_list = list(db.comment.find({}, {'_id': False}))
    count = len(comment_list) + 1
    doc = {
        'num':count,
        'comment' : comment_receive,
        'star':star_receive
    }
    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

# 지역별 날씨 조회
@app.route("/posts/weather", methods=["GET"])
def getRegionWeather():
    pass

# 글 작성
@app.route("/posts", methods=["POST"])
def writePost():
    pass

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
