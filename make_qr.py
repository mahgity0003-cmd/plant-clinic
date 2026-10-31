#!/usr/bin/env python3
"""
ساخت دوبارهٔ QR Code سایت (برای زمانی که دامنه تهیه کردید).

روش استفاده:
    pip install opencv-python numpy pillow
    python tools/make_qr.py https://your-domain.ir

اگر آدرسی وارد نکنید، لینک موقعیت کلینیک در نشان استفاده می‌شود.
خروجی: assets/clinic-location-qr.png
"""
import sys, os
import cv2, numpy as np
from PIL import Image

DEFAULT = "https://neshan.org/maps/profile/je6_qac_n"
url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT

enc = cv2.QRCodeEncoder.create()
mat = enc.encode(url)                      # تصویر خاکستری با حاشیهٔ کوچک
mat = (mat < 128)                          # True = مربع تیره
# حذف حاشیهٔ سفید داخلی
ys, xs = np.where(mat)
mat = mat[ys.min():ys.max()+1, xs.min():xs.max()+1]
# تبدیل به ماتریس ماژول‌ها (اندازهٔ هر ماژول = 1 پیکسل در خروجی cv2 نیست؛ پس نمونه‌برداری می‌کنیم)
h, w = mat.shape
# تشخیص اندازهٔ ماژول از اولین run
row = mat[0]
run = 1
while run < w and row[run] == row[0]:
    run += 1
mod = max(1, run // 7) if run >= 7 else 1
n = h // mod
modules = mat[mod//2::mod, mod//2::mod][:n, :n]

SCALE, QUIET = 20, 4
size = (n + 2*QUIET) * SCALE
img = np.full((size, size), 255, np.uint8)
for r in range(n):
    for c in range(n):
        if modules[r, c]:
            y, x = (r+QUIET)*SCALE, (c+QUIET)*SCALE
            img[y:y+SCALE, x:x+SCALE] = 0
out = os.path.join(os.path.dirname(__file__), "..", "assets", "clinic-location-qr.png")
Image.fromarray(img).save(out)

# بررسی قابلیت اسکن
res = cv2.QRCodeDetector().detectAndDecode(cv2.imread(out))[0]
print("ذخیره شد:", os.path.abspath(out))
print("خوانده‌شده از QR:", res)
print("وضعیت:", "✔ درست" if res == url else "✘ مشکل در خواندن")
