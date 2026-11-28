import asyncio
import websockets

# 接続しているプレイヤーを管理
players = {}


async def handler(ws):

    # プレイヤーの割り当て
    if "A" not in players:
        players["A"] = ws
        role = "A"

    elif "B" not in players:
        players["B"] = ws
        role = "B"

    else:
        await ws.send("満員です")
        return

    # プレイヤー番号をクライアントに送信
    await ws.send(role)

    print(role + " が参加しました")

    try:
        async for message in ws:
            print(role + "から受信:", message)

    finally:
        # 切断したプレイヤーの枠を解放
        players.pop(role, None)
        print(role + " が退出しました")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("サーバー起動！")
        await asyncio.Future()


asyncio.run(main())