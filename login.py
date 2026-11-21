import json
import os
import random
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = "a"  # セッション用の暗号化キー

DATA_FILE = "sample.json"
save_data = {"user": []}

# データの読み込み関数
def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {}


# データの保存関数
def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


savedata = load_data()


# トップページ（ログイン画面）
@app.route("/")
def home():
  # すでにログイン済みの場合はマイページへ移動
  if "email" in session and session["email"] in savedata:
    return redirect(url_for("logined"))

  return """<h1>ログインしてください</h1>
              <form action="/login" method="POST">
                  <p>メール: <input type="email" name="email" required></p>
                  <p>パスワード: <input type="password" name="password" required></p>
                  <button type="submit">サインイン</button>
              </form>
              <p>アカウントがない場合: <a href="/signup">新規登録</a></p>"""


# 新規登録画面
@app.route("/signup")
def signup():
  return """<h1>新規登録してください</h1>
              <form action="/signup_touroku" method="POST">
                  <p>お名前: <input type="text" name="name" required></p>
                  <p>メール: <input type="email" name="email" required></p>
                  <p>パスワード: <input type="password" name="password" required></p>
                  <button type="submit">登録する</button>
              </form>
              <p>既にアカウントがある場合: <a href="/">サインイン</a></p>"""


# 新規登録の処理
@app.route("/signup_touroku", methods=["POST"])
def signup_touroku():
  name = request.form.get("name")
  email = request.form.get("email")
  password = request.form.get("password")

  # すでに同じメールアドレスが登録されている場合
  if email in savedata["user"]:
    return """<p>このメールアドレスは既に登録されています。</p>
                  <a href="/signup">戻る</a>"""

  # 初期所持金300円でユーザー登録
  savedata["user"].append({
      "email": email,
      "password": password,
      "name": name,
      "money": 300,
  })
  save_data(savedata)

  return redirect(url_for("home"))


# ログイン処理
@app.route("/login", methods=["POST"])
def login():
  email = request.form.get("email")
  password = request.form.get("password")
  for sd in savedata["user"]:
    if sd["email"] == email and sd["password"] == password:
        session["user_name"] = sd["name"]
    return redirect(url_for("logined"))
  else:
    return """<p>メールアドレスまたはパスワードが間違っています。</p>
                  <a href="/">ログイン画面に戻る</a>"""


# ログイン後のマイページ
@app.route("/logined")
def logined():
  # 未ログインの場合はトップページへ戻す
  if "user_name" not in session:
    return redirect(url_for("home"))

  name = session["user_name"]
  return f"""<h1>ようこそ、{user['name']}さん！</h1>
               <p>現在の所持金: <strong>{user['money']}円</strong></p>
               
               <hr>
               <h3>ミニゲーム（1回 100円）</h3>
               <form action="/game" method="POST">
                   <button type="submit">くじを引く（100円消費）</button>
               </form>
               <hr>
               
               <p><a href="/logout">ログアウト</a></p>"""


# randomを使ったくじ引き機能（所持金の増減と保存）
@app.route("/game", methods=["POST"])
def game():
  if "email" not in session or session["email"] not in savedata:
    return redirect(url_for("home"))

  email = session["email"]
  user = savedata[email]

  # 所持金が足りない場合
  if user["money"] < 100:
    return """<p>所持金が足りません！（100円必要です）</p>
                  <a href="/logined">マイページに戻る</a>"""

  # 100円消費してランダムに結果を決定
  user["money"] -= 100
  prize = random.choice([0, 50, 100, 300, 500])
  user["money"] += prize

  # 増減した所持金をファイルに保存
  save_data(savedata)

  return f"""<h2>結果: {prize}円 当たりました！</h2>
               <p>現在の所持金: {user['money']}円</p>
               <a href="/logined">マイページに戻る</a>"""


# ログアウト処理
@app.route("/logout")
def logout():
  session.pop("email", None)
  return redirect(url_for("home"))


if __name__ == "__main__":
  app.run(debug=True)
