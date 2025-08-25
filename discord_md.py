import discord
import datetime

TOKEN = "MTQwNTA3NTA5MTY3ODY5NTQyNA.GQAUsT.G704z5N9KD4QM-AxxCuJPYIgmhzDGANP599bUE"
FILENAME = "C:\obsidian\storage\discord\link.md"
# ここに記録したいチャンネルのIDを指定してください（int型）
TARGET_CHANNEL_ID = 1403365203235831941  # 例: 123456789012345678

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')

    async def on_message(self, message):
        # Bot自身のメッセージは無視
        if message.author.bot:
            return

        # 特定のチャンネルのみ対象
        if message.channel.id != TARGET_CHANNEL_ID:
            return

        # 日本時間（UTC+9）で日時取得
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        now_str = now.strftime("%Y-%m-%d %H:%M")

        text = message.content

        with open(FILENAME, "a", encoding="utf-8") as f:
            f.write(f"{now_str}\n{text}\n")
            f.write(f"\n")
            f.write(f"***")
            f.write(f"\n")

        print(f"Saved message from {now_str}: {text}")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = MyClient(intents=intents)
client.run(TOKEN)
