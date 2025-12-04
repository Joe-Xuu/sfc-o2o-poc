import qrcode
import urllib.parse

# 1. 你的 Bot ID (在 Messaging API 页面的最上方，通常是以 @ 开头的，比如 @123abcde)
# 注意：一定要带 @ 符号
BOT_BASIC_ID = "@2008616144" 

CONTAINER_ID = "TEST-001"

# 3. 构造预填文字
# 我们约定格式为："borrow TEST-001"
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
import os
os.system("open bot_qr.png")