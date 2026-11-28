import base64

# ここにコピーしたsessionの値を貼り付ける
cookie_value = "eyJlbWFpbCI6ImFhQGV4YW1wbGUuY29tIn0.xxxx.yyyy"

# ドットで区切った最初の部分（データ本体）を取り出す
payload = cookie_value.split(".")[0]

# Base64のルールに合わせて文字数を4の倍数に調整（パディング）
payload += "=" * ((4 - len(payload) % 4) % 4)

# デコードして表示
decoded_data = base64.urlsafe_b64decode(payload).decode("utf-8")
print(decoded_data)
