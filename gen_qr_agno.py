import os
import qrcode

# 新 LIFF ID
LIFF_URL = "https://liff.line.me/2008653079-30XW9WnJ" 
# LIFF_URL = os.getenv("LIFF_URL")
CONTAINER_ID = input("Input container ID")

# 这里的 ?id=... 是给刚才那个 JS 读取用的
target_url = f"{LIFF_URL}?id={CONTAINER_ID}"

print(f"生成 URL: {target_url}")

qr = qrcode.QRCode(box_size=10, border=5)
qr.add_data(target_url)
qr.make(fit=True)
img = qr.make_image()
img.save("silent_borrow_qr.png")