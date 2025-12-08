import os
import qrcode
import urllib.parse

# BOT_BASIC_ID = os.getenv("BOT_BASIC_ID")
BOT_BASIC_ID = "@130cnftc"

CONTAINER_ID = input("Enter container ID: ")

# 3. 构造预填文字
text_message = f"borrow {CONTAINER_ID}"

# 4. URL 编码 (因为 URL 里不能有空格和中文，需要转义)
encoded_text = urllib.parse.quote(text_message)

# 5. 拼接最终 URL
# 格式: https://line.me/R/oaMessage/{bot_id}/?{text}
target_url = f"https://line.me/R/oaMessage/{BOT_BASIC_ID}/?{encoded_text}"

print(f"生成 URL: {target_url}")

# 6. 生成二维码
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(target_url)
qr.make(fit=True)

img = qr.make_image(fill='black', back_color='white')
img.save("bot_qr.png")
print("saved as bot_qr.png")
os.system("open bot_qr.png")