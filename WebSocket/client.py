import asyncio
import websockets


async def main():

    # ユーザー名
    name = input("名前を入力してください：")

    # サーバーに接続
    async with websockets.connect(
        "ws://localhost:8765"
    ) as ws:
        role = await ws.recv()
        print("あなたはプレイヤー" + role + "です")
        print("サーバーに接続しました！")
        print("exit と入力すると終了します。")

        # 受信処理
        async def receive():

            async for message in ws:

                print("\n" + message)

        # 送信処理
        async def send():
            # while True:
            if role == "A":
                A_hand = input("あなたの出す手を選んでください　グー/チョキ/パー")
                await ws.send(
                    name + "は" + A_hand + "を出しました"
                )
            if role == "B":
                B_hand = input("あなたの出す手を選んでください　グー/チョキ/パー")
                await ws.send(
                    name + "は" + B_hand + "を出しました"
                )              
            # while True:
            #     message = await asyncio.to_thread(input, "")

            #     if message == "exit":
            #         await ws.close()
            #         break

            #     # メッセージ送信
            #     await ws.send(
            #         name + "：" + message
            #     )

        # 送信と受信を同時に実行
        await asyncio.gather(
            receive(),
            send()
        )


asyncio.run(main())