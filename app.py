
from flask import Flask, request

# Flaskアプリを作成
app = Flask(__name__)

# トップページにアクセスしたときの処理
@app.route("/")
def home():
    
    return """<h1>Hello,あなたの名前を教えてください</h1>
              <form action="/hello" method="POST">
              <input type="text" id="username" name="username" placeholder="山田太郎" required>
              <button type="submit">送信する</button>
              </form>

    """
    # 名前を聞きます     
    # 名前を/helloに送信します
@app.route("/hello", methods = ["POST"])
def hello():
    #名前を取ります
    #return "Hello",名前 します
    name = request.form.get('username')
    return f"Hello,{name}さん"

# サーバーを起動
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
