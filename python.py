import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk
import barcode
from barcode.writer import ImageWriter
from tkinter import filedialog
import shutil

# =≈≠≡

# ======================
# 기본 설정
# ======================
root = ctk.CTk()
root.geometry("600x500")
root.title("QR / 바코드 생성기")
# ======================
# 폰트 설정
# ======================
FONT = ctk.CTkFont(family="맑은 고딕", size=14)
TITLE_FONT = ctk.CTkFont(family="맑은 고딕", size=18, weight="bold")
# ======================
# 다크모드 토글
# ======================
def toggle_mode():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

mode_toggle = ctk.CTkSwitch(root, text="다크/라이트 모드", command=toggle_mode, font=FONT)
mode_toggle.pack(pady=10, anchor="e", padx=10)

# ======================
# 탭 생성
# ======================
tabview = ctk.CTkTabview(root)
tabview.pack(expand=False, padx=10, pady=10)

tabview.add("QR코드")
tabview.add("바코드")

tab_qr = tabview.tab("QR코드")
tab_barcode = tabview.tab("바코드")

# ======================
# QR코드 영역
# ======================
title_qr = ctk.CTkLabel(tab_qr, text="QR코드 생성", font=TITLE_FONT)
title_qr.pack(pady=5)

entry_qr = ctk.CTkEntry(tab_qr, placeholder_text="https://example.com", font=FONT)
entry_qr.pack(pady=10)

label_qr = ctk.CTkLabel(tab_qr, text="", font=FONT)
label_qr.pack(pady=20)

current_qr = None

def make_qr():
    global current_qr
    link = entry_qr.get()

    if link.strip():
        qr_img = qrcode.make(link)
        img_tk = ImageTk.PhotoImage(qr_img)

        label_qr.configure(image=img_tk, text="")
        label_qr.image = img_tk

        current_qr = qr_img
    else:
        label_qr.configure(text="값을 입력하세요")

def save_qr():
    if current_qr:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 파일", "*.png")],
            title="QR코드 저장"
        )
        if file_path:
            current_qr.save(file_path)
            label_qr.configure(text="저장 완료!")
    else:
        label_qr.configure(text="먼저 QR 생성하세요")

btn_make_qr = ctk.CTkButton(tab_qr, text="QR 생성", command=make_qr, font=FONT)
btn_make_qr.pack(pady=5)

btn_save_qr = ctk.CTkButton(tab_qr, text="QR 저장", command=save_qr, font=FONT)
btn_save_qr.pack(pady=5)

# ======================
# 바코드 영역
# ======================
title_bar = ctk.CTkLabel(tab_barcode, text="바코드 생성", font=TITLE_FONT)
title_bar.pack(pady=5)

entry_barcode = ctk.CTkEntry(tab_barcode, placeholder_text="바코드 값 입력", font=FONT)
entry_barcode.pack(pady=10)

label_barcode = ctk.CTkLabel(tab_barcode, text="", font=FONT)
label_barcode.pack(pady=20)

current_barcode = None

def make_barcode():
    global current_barcode
    data = entry_barcode.get()

    if data.strip():
        code = barcode.get('code128', data, writer=ImageWriter())
        filename = code.save(f'barcode_{data}')

        barcode_img = Image.open(filename)
        barcode_tk = ImageTk.PhotoImage(barcode_img)

        label_barcode.configure(image=barcode_tk, text="")
        label_barcode.image = barcode_tk

        current_barcode = filename
    else:
        label_barcode.configure(text="값을 입력하세요")

def save_barcode():
    if current_barcode:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 파일", "*.png")],
            title="바코드 저장"
        )
        if file_path:
            shutil.copy(current_barcode, file_path)
            label_barcode.configure(text="저장 완료!")
    else:
        label_barcode.configure(text="먼저 바코드를 생성하세요")

btn_make_barcode = ctk.CTkButton(tab_barcode, text="바코드 생성", command=make_barcode, font=FONT)
btn_make_barcode.pack(pady=5)

btn_save_barcode = ctk.CTkButton(tab_barcode, text="바코드 저장", command=save_barcode, font=FONT)
btn_save_barcode.pack(pady=5)

# ======================
# 실행
# ======================
root.mainloop()
