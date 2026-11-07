import socket

# 1. TCPソケットを作る
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. IPアドレスとポート番号を指定する
server.bind(("127.0.0.1", 8080))

# 3. 接続を待ち受ける
server.listen()

print("HTTPサーバー起動！")
print("http://127.0.0.1:8080/")

while True:
    # 4. ブラウザからの接続を受け付ける
    client, address = server.accept()

    try:
        # 5. HTTPリクエストを受信する
        request = client.recv(4096).decode("utf-8")

        print("----- リクエスト -----")
        print(request)

        # 6. HTMLの本文を作る
        body = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>自作HTTPサーバー</title>
</head>
<body>
    <h1>Hello World!</h1>
    <p>これはPythonで作ったHTTPサーバーです。</p>
</body>
</html>
"""

        # 7. HTMLをバイト列に変換する
        body_bytes = body.encode("utf-8")

        # 8. HTTPレスポンスを組み立てる
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8") + body_bytes

        # 9. ブラウザにレスポンスを送る
        client.sendall(response)

    finally:
        # 10. 接続を終了する
        client.close()