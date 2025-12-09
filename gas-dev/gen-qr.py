import qrcode
import os
from urllib.parse import quote

# ================= 配置区域 =================

LIFF_ID = "2008626930-AddPwDy7" 

# 定义要生成的容器 ID 列表
CONTAINER_IDS = ["00001"]
# CONTAINER_IDS_1 = [f"2200{i}" for i in range(1, 10)]
# CONTAINER_IDS_2 = [   f"220{j}" for j in range(10,100)]
# CONTAINER_IDS_3 = [   f"22{k}" for k in range(100, 251)]

# CONTAINER_IDS = CONTAINER_IDS_1+CONTAINER_IDS_2+CONTAINER_IDS_3

# 图片保存的文件夹名称
OUTPUT_DIR = "return_qr_codes"

# ==========================================


def generate_liff_qr_codes():
    # 1. 检查 LIFF ID 是否填了
    if LIFF_ID == None:
        print("❌ 错误：请先在代码顶部填入正确的 LIFF ID！")
        return

    # 2. 创建输出目录
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    print(f"Start generating {len(CONTAINER_IDS)} QR codes...")
    print("-" * 30)

    count = 0
    for cid in CONTAINER_IDS:
        # 3. 构建 LIFF URL
        # 使用 quote 确保 ID 中的特殊字符（如空格）被安全编码
        safe_cid = quote(cid)
        # URL 结构：https://liff.line.me/{LIFF_ID}?id={容器ID}
        full_url = f"https://liff.line.me/{LIFF_ID}?id={safe_cid}"

        # 4. 创建 QR 码对象
        # error_correction=qrcode.constants.ERROR_CORRECT_H
        # 使用最高级别的容错率 (H - 30%)，这样即使二维码有点脏污或破损也能扫出来，适合实物粘贴。
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10, # 控制每个点的大小，越大图片越大
            border=4,    # 边框白边宽度
        )
        
        # 添加数据
        qr.add_data(full_url)
        qr.make(fit=True)

        # 创建图像
        img = qr.make_image(fill_color="black", back_color="white")

        # 5. 保存文件
        # 文件名 safe 一点，把原来的 ID 作为文件名
        filename = os.path.join(OUTPUT_DIR, f"{cid}.png")
        img.save(filename)

        count += 1
        print(f"[{count}/{len(CONTAINER_IDS)}] Generated: {filename}")
        print(f"   -> Link: {full_url}") # 调试时可以打开看链接对不对

    print("-" * 30)
    print(f"✅ Done! All {count} QR codes saved in '{OUTPUT_DIR}/' directory.")


if __name__ == "__main__":
    generate_liff_qr_codes()