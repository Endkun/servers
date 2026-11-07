from flask import Flask,request,redirect,url_for,make_response

# Flaskアプリを作成
app = Flask(__name__)

# トップページにアクセスしたときの処理
savedata = {}

@app.route("/")
def home():
    print("b")
    return """<h1>ログインしてください</h1>
              <form action="/login" method="POST">
              <p>メール: <input type="text" id="email" name="email" required></p>
              <p>パスワード: <input type="text" id="password" name="password" required></p>
              <button type="submit">サインイン</button></form>
              <p>アカウントがない場合: <a href="/signup" class="button-link">登録</a></p>"""

@app.route("/signup")
def signup():
    return """<h1>登録してください</h1>
              <form action="/signup_touroku" method="POST">
              <p>お名前: <input type="text" id="name" name="name" required></p>
              <p>メール: <input type="text" id="email" name="email" required></p>
              <p>パスワード: <input type="text" id="password" name="password" required></p>
              <button type="submit">登録する</button></form>
              <p>既にアカウントがある場合: <a href="/">サインイン</a></p>"""

@app.route("/signup_touroku",methods=["POST"])
def signup_touroku():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    savedata[email] = {"password":password,"name":name}
    return redirect(url_for('home'))

@app.route("/login",methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    print(email,password,name)
    #{"a@example.com":{"password":password,"name":name}}
    if email in savedata and savedata[email]["password"] == password:
        return redirect(url_for('logined'))
    else:
        return redirect(url_for("home"))

@app.route("/logined")
def logined():
    name = request.form.get('name')
    return f"hello {name}"

app.run(debug=True, port=5000)
