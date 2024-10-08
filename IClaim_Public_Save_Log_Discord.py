import discord
import pymssql

# Database connection details
server = "10.200.0.21"
user = "sa"
password = "gF5E8E8#02"
database = "IClaim"

# Connect to the database
conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor()

# SQL query
query = """
SELECT [DataSource]
      ,CONCAT([CountRow],' Row') AS [CountRow]
      ,[LastExtract]
  FROM [IClaim].[dbo].[ExtractLog]
  WHERE [DataSource] IN 
  ('dm_IClaimPublic_Transaction','dm_IClaimPublic_Accumulate_Approve_Amount')
"""
cursor.execute(query)
rows = cursor.fetchall()
conn.close()

# Format message content
message = "Name: IClaim Public\nJob: IClaim Public\nDatabase: IClaim\n"

for row in rows:
    data_source = row[0]  # [DataSource]
    count_row = row[1]    # [CountRow]
    etl_date = row[2]     # [LastExtract]
    message += f"\n{data_source}\nRow: {count_row}\nTime: {etl_date}\n"

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Token และ Channel ID (จาก Discord Developer Portal และจาก Server)
# DISCORD_TOKEN = "MTI5MzA0NDQyNzgyMDEwOTg0NQ.GNKxw4.oGajs-8sBJTfcwPQy47leGVKT5XGZKRFUaJBus"  # Replace with your Discord Bot token
DISCORD_TOKEN = " Replace Discord Bot token "
CHANNEL_ID = " Replace channel ID "
# CHANNEL_ID = 1293047160731992145  # Replace with your target channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)  # ส่งข้อความไปยัง Discord channel ที่ระบุ
    await bot.close()  # ปิดบอทหลังจากส่งข้อความสำเร็จ

bot.run(DISCORD_TOKEN)
