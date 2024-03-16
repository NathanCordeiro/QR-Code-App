import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import qrcode
import cv2
from PIL import Image, ImageTk
import pyperclip

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code App")

        # Configure background color
        self.root.configure(bg="#f0f0f0")

        # Create canvas
        self.canvas = tk.Canvas(root, width=600, height=0, bg="#ffffff")
        self.canvas.pack()

        # Configure button styles
        button_style = {
            "font": ("Arial", 14),
            "bg": "#007bff",  # Blue color
            "fg": "white",    # White text
            "activebackground": "#0056b3",  # Darker blue on click
            "activeforeground": "white",     # White text on click
            "bd": 0,  # Border width
            "highlightthickness": 0  # No highlight border
        }

        # Generate QR Code button
        self.btn_generate = tk.Button(root, text="Generate QR Code", command=self.generate_qr, **button_style)
        self.btn_generate.pack(pady=20, padx=40, fill=tk.X)

        # Decode QR Code button
        self.btn_decode = tk.Button(root, text="Decode QR Code", command=self.decode_qr, **button_style)
        self.btn_decode.pack(pady=20, padx=40, fill=tk.X)

    def generate_qr(self):
        data_entry_dialog = DataEntryDialog(self.root)
        data = data_entry_dialog.result
        if data:
            qr = qrcode.make(data)
            qr.show()

    def decode_qr(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            dialog = QRDecoderDialog(self.root, file_path)
            dialog.show_result()

    def show_result(self):
        self.focus_set()
        self.grab_set()
        self.wait_window()
            
class DataEntryDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Enter Data")
        self.dialog.configure(bg="#f0f0f0")

        # Add padding
        self.dialog.geometry("300x150")

        self.label = tk.Label(self.dialog, text="Enter data to encode:", font=("Arial", 14), bg="#f0f0f0")
        self.label.pack(pady=(20, 5))  # Adjust top and bottom padding

        self.entry = tk.Entry(self.dialog, font=("Arial", 12))
        self.entry.pack(pady=5)  # Adjust vertical padding

        self.btn_ok = tk.Button(self.dialog, text="OK", command=self.dialog_ok, font=("Arial", 12), bg="#007bff", fg="white")
        self.btn_ok.pack(pady=(10, 20))  # Adjust bottom padding

        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)

    def dialog_ok(self):
        self.result = self.entry.get()
        self.dialog.destroy()

class QRDecoderDialog(tk.Toplevel):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        self.title("QR Code Decoded")
        self.geometry("400x400")
        self.configure(bg="#ffffff")

        # Load and display the QR code image
        image = Image.open(file_path)
        image.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=photo, bg="#ffffff")
        label.image = photo
        label.pack(pady=10)

        # Decode the QR code
        decoded_data = self.decode_qr(file_path)

        # Display the decoded data
        if decoded_data:
            text = f"The QR code contains:\n\n{decoded_data}"
        else:
            text = "No QR code found in the image."
        result_label = tk.Label(self, text=text, bg="#ffffff", font=("Arial", 12))
        result_label.pack(pady=10)

        # Copy button
        copy_button = tk.Button(self, text="Copy", command=lambda: self.copy_to_clipboard(decoded_data), bg="#007bff", fg="white")
        copy_button.pack(pady=10)


    def decode_qr(self, file_path):
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(gray)
        return data

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        messagebox.showinfo("Copy Success", "Text copied to clipboard.")

    def show_result(self):
        self.focus_set()
        self.grab_set()
        self.wait_window()

root = tk.Tk()
app = QRCodeApp(root)
root.mainloop()

