from flask import Flask, request, make_response, redirect, url_for

app = Flask(__name__)

# グローバル変数のリスト（今回はCookieで管理するため使用しませんがエラー回避のため残しています）
data = []

@app.route("/")
def home():
    # 1. ブラウザからCookie（名前、年齢、課金状態）を読み込む
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    charged = request.cookies.get('charged')

    # すでにCookieにデータが保存されている場合は、入力画面を出さずに直接プロフィールへリダイレクト
    if name and age and charged:
        return redirect(url_for('profile_get'))

    # Cookieがない場合は通常通りフォームを表示
    return """<h1>名前と年齢はなんですか</h1>
              <form action="/profile" method="POST">
              <input type="text" id="name" name="name" placeholder="山田太郎" required>
              <input type="text" id="age" name="age" placeholder="20" required>
              <h1>課金しますか</h1>
              <label><input type="radio" name="charge" value="Yes"> はい</label>
              <label><input type="radio" name="charge" value="No"> いいえ</label>
              <button type="submit">送信する</button></form>"""

@app.route("/profile", methods=["POST"])
def profile():
    name = request.form.get('name')
    age = request.form.get('age')
    charged = request.form.get('charge')

    # 表示するメッセージを判定
    if charged == "Yes":
        msg = f"{name}さんは{age}さいです。 課金しています。"
    elif charged == "No":
        msg = f"{name}さんは{age}さいです。 課金していません。"
    else:
        msg = f"{name}さんは{age}さいです。 選択されていません。"

    # 2. レンスポンスオブジェクトを作成し、Cookieをセットする
    response = make_response(f"{msg}<br><br><a href='/clear'>Cookieを削除してやり直す</a>")
    
    # max_age=60*60*24 で1日間保存（必要に応じて変更してください）
    response.set_cookie('name', name, max_age=60*60*24)
    response.set_cookie('age', age, max_age=60*60*24)
    response.set_cookie('charged', charged or 'None', max_age=60*60*24)
    
    return response

# 3. Cookieを持っている状態で直接アクセス、またはリダイレクトされた時の表示用
@app.route("/profile", methods=["GET"])
def profile_get():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    charged = request.cookies.get('charged')

    if charged == "Yes":
        msg = f"{name}さんは{age}さいです。 課金しています。（Cookieから読込）"
    elif charged == "No":
        msg = f"{name}さんは{age}さいです。 課金していません。（Cookieから読込）"
    else:
        msg = f"{name}さんは{age}さいです。 選択されていません。（Cookieから読込）"

    return f"{msg}<br><br><a href='/clear'>Cookieを削除してやり直す</a>"

# 4. テストしやすくするためにCookieを削除するルートを追加
@app.route("/clear")
def clear_cookie():
    response = make_response("Cookieを削除しました。<br><a href='/'>トップへ戻る</a>")
    response.set_cookie('name', '', max_age=0)
    response.set_cookie('age', '', max_age=0)
    response.set_cookie('charged', '', max_age=0)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)
