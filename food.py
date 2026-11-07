from flask import Flask,request

# Flaskアプリを作成
app = Flask(__name__)

# トップページにアクセスしたときの処理
@app.route("/")
def home():
    print("b")
    return """<h1>好きな食べ物を入力してください</h1>
              <form action="/tabemono" method="POST">
              <input type="text" id="food" name="food" placeholder="ラーメン">
              <button type="submit">送信する</button></form>"""

@app.route("/tabemono",methods=["POST"])
def tabemono():
    print("a")
    food = request.form.get('food')
    return f"あなたの好きな食べ物は{food}ですね"

app.run(debug=True, port=5000)
