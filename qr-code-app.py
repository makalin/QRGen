import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import cv2
import os
from datetime import datetime

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator & Scanner")
        self.root.geometry("800x600")
        
        # Create tabs
        self.tabControl = ttk.Notebook(root)
        self.generator_tab = ttk.Frame(self.tabControl)
        self.scanner_tab = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.generator_tab, text='Generate QR Code')
        self.tabControl.add(self.scanner_tab, text='Scan QR Code')
        self.tabControl.pack(expand=1, fill="both")
        
        self.setup_generator()
        self.setup_scanner()
        
    def setup_generator(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.generator_tab, text="Input", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Enter text or URL:").pack()
        self.text_input = ttk.Entry(input_frame, width=50)
        self.text_input.pack(pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(self.generator_tab, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(options_frame, text="QR Code Size:").pack()
        self.size_var = tk.StringVar(value="10")
        size_entry = ttk.Entry(options_frame, textvariable=self.size_var, width=10)
        size_entry.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.generator_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Generate QR Code", command=self.generate_qr).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save QR Code", command=self.save_qr).pack(side="left", padx=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self.generator_tab, text="Preview", padding=10)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()
        
        self.qr_image = None
        
    def setup_scanner(self):
        # Buttons frame
        button_frame = ttk.Frame(self.scanner_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Upload Image", command=self.upload_image).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Scan from Camera", command=self.scan_from_camera).pack(side="left", padx=5)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.scanner_tab, text="Scan Result", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(result_frame, height=5, width=50)
        self.result_text.pack(pady=5)
        
    def generate_qr(self):
        data = self.text_input.get()
        if not data:
            messagebox.showerror("Error", "Please enter text or URL")
            return
            
        try:
            size = int(self.size_var.get())
            qr = qrcode.QRCode(version=1, box_size=size, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            
            self.qr_image = qr.make_image(fill_color="black", back_color="white")
            self.display_qr()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid size value")
            
    def display_qr(self):
        if self.qr_image:
            # Convert PIL image to PhotoImage
            photo = ImageTk.PhotoImage(self.qr_image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
            
    def save_qr(self):
        if not self.qr_image:
            messagebox.showerror("Error", "Generate a QR code first")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            self.qr_image.save(filename)
            messagebox.showinfo("Success", "QR code saved successfully")
            
    def upload_image(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.scan_qr(filename)
            
    def scan_from_camera(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not access camera")
            return
            
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.imshow("Scan QR Code (Press 'q' to quit)", frame)
            
            # Try to decode QR code
            decoded_objects = decode(frame)
            if decoded_objects:
                cap.release()
                cv2.destroyAllWindows()
                
                # Display results
                self.result_text.delete(1.0, tk.END)
                for obj in decoded_objects:
                    self.result_text.insert(tk.END, obj.data.decode('utf-8') + '\n')
                return
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
    def scan_qr(self, image_path):
        try:
            image = Image.open(image_path)
            decoded_objects = decode(image)
            
            self.result_text.delete(1.0, tk.END)
            if decoded_objects:
                for obj in decoded_objects:
                    self.result_text.insert(tk.END, obj.data.decode('utf-8') + '\n')
            else:
                self.result_text.insert(tk.END, "No QR code found in the image")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error scanning image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
