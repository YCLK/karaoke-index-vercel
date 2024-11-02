from flask import Flask
from flask import render_template
from flask import request            #브라우저의 요청을 처리하기 위한 클래스
from flask import redirect            #인자로 전달된 주소(라우트) 호출
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)    #플라스크 객체(서버) 생성

app.config["MONGO_URI"] = "mongodb+srv://admin:1234@cluster0.e1str.mongodb.net/karaoke?"
mongo = PyMongo(app)     #mongo 변수를 통해 DB(myweb)에 접근 가능

@app.route("/")    #라우트는 데코레이터(@)와 함수를 활용하여 구현됨, "/"은 루트 경로
def index():
    index = mongo.db.karaoke
    kList = index.find()
    
    return render_template('index.html', kList=kList)
    #플라스크 서버 실행

@app.route("/add/")    #라우트는 데코레이터(@)와 함수를 활용하여 구현됨, "/"은 루트 경로
def add():
    return render_template('register.html')

@app.route("/manage/")    #라우트는 데코레이터(@)와 함수를 활용하여 구현됨, "/"은 루트 경로
def manage():
    index = mongo.db.karaoke
    kList = index.find()

    return render_template('manage.html', kList=kList)

@app.route("/karaoke", methods=["POST"])   #POST 요청 처리를 위해 필요한 속성
def karaoke():    
    title = request.form.get("title") 
    artist = request.form.get("artist") 
    karaoke1 = request.form.get("karaoke1") 
    number = request.form.get("number")
    categories = request.form.get("categories") 
    
    post = { "title" : title, "artist" : artist, "karaoke" : karaoke1, "number" : number, "categories" : categories }     #데이터베이스에 저장될 자료구조(딕셔너리)
    
    karaoke = mongo.db.karaoke     #todo는 컬렉션(테이블)의 이름
    karaoke.insert_one(post)
    
    return redirect('/')

@app.route("/delete/<idx>")    # 팬시(간편, clean) URL 형식
def delete(idx):
    karaoke = mongo.db.karaoke
    karaoke.delete_one({"_id":ObjectId(idx)}) 
    
    return redirect('/')

if __name__ == "__main__":    #파이썬의 엔트리 포인트(직접 실행된 파일에서만 True)
    app.run(debug=True)