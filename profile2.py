from flask import Flask,request,render_template
import random
# Flaskアプリを作成
app = Flask(__name__)

# トップページにアクセスしたときの処理
@app.route("/")
def home():
    rmd = random.randint(1,6)
    return render_template("a.html",rmd = rmd)
@app.route("/profile",methods=["POST"])
def profile():
    name = request.form.get('name')
    age = request.form.get('age')
    return f"{name}さんは{age}さいです"

app.run(debug=True, port=5000)
