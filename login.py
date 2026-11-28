import json
import os
import random
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = "a"

DATA_FILE = "sample.json"


# データの読み込み関数（ファイルがない場合は初期構造を返す）
def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {"user": []}


# データの保存関数
def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# メールアドレスからユーザー辞書を探す補助関数
def get_user_by_email(email):
  for user in savedata["user"]:
    if user["email"] == email:
      return user
  return None


savedata = load_data()


@app.route("/")
def home():
  if "email" in session and get_user_by_email(session["email"]):
    return redirect(url_for("logined"))

  return """<h1>ログインしてください</h1>
              <form action="/login" method="POST">
                  <p>メール: <input type="email" name="email" required></p>
                  <p>パスワード: <input type="password" name="password" required></p>
                  <button type="submit">サインイン</button>
              </form>
              <p>アカウントがない場合: <a href="/signup">新規登録</a></p>"""


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


@app.route("/signup_touroku", methods=["POST"])
def signup_touroku():
  name = request.form.get("name")
  email = request.form.get("email")
  password = request.form.get("password")

  # 重複チェック
  if get_user_by_email(email) is not None:
    return """<p>このメールアドレスは既に登録されています。</p>
                  <a href="/signup">戻る</a>"""

  savedata["user"].append({
      "email": email,
      "password": password,
      "name": name,
      "money": 300,
  })
  save_data(savedata)

  return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
  email = request.form.get("email")
  password = request.form.get("password")

  user = get_user_by_email(email)
  if user and user["password"] == password:
    session["email"] = user["email"]  # 一意なemailをセッションに保存
    return redirect(url_for("logined"))

  return """<p>メールアドレスまたはパスワードが間違っています。</p>
              <a href="/">ログイン画面に戻る</a>"""


@app.route("/logined")
def logined():
  if "email" not in session:
    return redirect(url_for("home"))

  user = get_user_by_email(session["email"])
  if not user:
    return redirect(url_for("home"))

  return f"""<h1>ようこそ、{user['name']}さん！</h1>
               <p>現在の所持金: <strong>{user['money']}円</strong></p>
               
               <hr>
               <h3>ミニゲーム（1回 100円）</h3>
               <form action="/game" method="POST">
                   <button type="submit">くじを引く（100円消費）</button>
               </form>
               <hr>
               
               <p><a href="/logout">ログアウト</a></p>"""


@app.route("/game", methods=["POST"])
def game():
  if "email" not in session:
    return redirect(url_for("home"))

  user = get_user_by_email(session["email"])
  if not user:
    return redirect(url_for("home"))

  if user["money"] < 100:
    return """<p>所持金が足りません！（100円必要です）</p>
                  <a href="/logined">マイページに戻る</a>"""

  user["money"] -= 100
  prize = random.choice([0, 50, 100, 300, 500])
  user["money"] += prize

  save_data(savedata)

  return f"""<h2>結果: {prize}円 当たりました！</h2>
               <p>現在の所持金: {user['money']}円</p>
               <a href="/logined">マイページに戻る</a>"""


@app.route("/logout")
def logout():
  session.pop("email", None)
  return redirect(url_for("home"))


if __name__ == "__main__":
  app.run(debug=True)
