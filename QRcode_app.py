import tkinter as tk
from tkinter import filedialog
import qrcode
import cv2
from PIL import Image, ImageTk

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code App")

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()
        
        self.btn_generate = tk.Button(root, text="Generate QR Code", command=self.generate_qr)
        self.btn_generate.pack(pady=10)

        self.btn_decode = tk.Button(root, text="Decode QR Code", command=self.decode_qr)
        self.btn_decode.pack(pady=10)

    def generate_qr(self):
        data = tk.simpledialog.askstring("QR Code Generator", "Enter data to encode:")
        if data:
            qr = qrcode.make(data)
            qr.show()

    def decode_qr(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = cv2.imread(file_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(gray)
            if data:
                tk.messagebox.showinfo("QR Code Decoded", f"The QR code contains:\n\n{data}")
            else:
                tk.messagebox.showinfo("QR Code Decoded", "No QR code found in the image.")

root = tk.Tk()
app = QRCodeApp(root)
root.mainloop()
