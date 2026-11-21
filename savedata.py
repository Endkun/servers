import json
datas = {'users':[]}
filename = "output.json"
#一人ずつ登録
#1行目から4行目までのデータがファイルに入ってるものとして、ファイルを読み込んできて追加する
#->追加してまた保存する

#登録
new_email = input('登録するメール')
new_password = input('登録するパスワード')
new_name = input('登録する名前')
datas['users'].append({'email':new_email,'password':new_password,'name':new_name})
try:
    with open(filename, "r", encoding="utf-8") as f:
        data_dict = json.load(f)
except FileNotFoundError:
    data_dict = {"users": []}
data_dict["users"].extend(datas["users"])
print(f"{datas=} {data_dict=}")
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=2)