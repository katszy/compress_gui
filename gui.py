import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from compress import Compressor
from decompress import Decompressor


class MyGUI:
    def __init__(self):
        self.decompressed_path = None
        self.bin_path = None
        self.file_name = None
        self.original_photo = None
        self.dec_photo = None

        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("RLE image compression")

        self.choose_file_button = tk.Button(self.root, text="Choose file", command=self.choose_file)
        self.choose_file_button.pack(padx=10, pady=10)

        self.file_label = tk.Label(self.root, text="No file chosen")
        self.file_label.pack(padx=10, pady=10)

        self.compressed_file_label = tk.Label(self.root, text="")
        self.compressed_file_label.pack(padx=10, pady=10)

        self.ratio_label = tk.Label(self.root, text="")
        self.ratio_label.pack(padx=10, pady=10)

        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(padx=10, pady=10)

        self.original_image_label = tk.Label(self.image_frame)
        self.original_image_label.pack(side="left", padx=10, pady=10)

        self.dec_image_label = tk.Label(self.image_frame)
        self.dec_image_label.pack(side="right", padx=10, pady=10)

        self.compress_button = tk.Button(self.root, text="Compress", command=self.compress)
        self.compress_button.pack(padx=10, pady=10)

        self.decompress_button = tk.Button(self.root, text="Decompress", command=self.decompress)
        self.decompress_button.pack(padx=10, pady=10)

        self.root.mainloop()

    def choose_file(self):
        self.file_name = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if self.file_name:
            self.file_label.config(text=self.file_name)
            self.reset_image_frame()
            self.display_image(self.file_name, original=True)

    def compress(self):
        self.bin_path = os.path.join(self.file_name.split('.')[0] + '.bin')
        print(f"saving file to {self.bin_path}")
        compressor = Compressor(self.file_name)
        compressor.compress(self.bin_path)
        self.compressed_file_label.config(text=f"File saved to {self.bin_path}")

    def decompress(self):
        self.decompressed_path = os.path.join(self.file_name.split('.')[0] + '_decompressed.jpg')
        print(self.decompressed_path)

        # Decompress the image
        decompressor = Decompressor(self.bin_path)
        decompressor.decompress(self.decompressed_path)

        # Display image
        self.display_image(self.decompressed_path, original=False)

        # Display compression ratio
        original_size = os.path.getsize(self.file_name)
        compressed_size = os.path.getsize(self.bin_path)
        compression_percentage = 0
        if original_size > 0:
            compression_percentage = 100 * (1 - (compressed_size / original_size))
        print(compression_percentage)
        self.ratio_label.config(text=f"reduction in size: {compression_percentage:2f}%")



    def resize_image(self, image, max_size):
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        if original_width > original_height:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)
        image = image.resize((new_width, new_height))
        return image

    def display_image(self, path, original):
        image = Image.open(path)
        image = self.resize_image(image, 200)
        photo = ImageTk.PhotoImage(image)

        if original:
            self.original_photo = photo
            self.original_image_label.config(image=self.original_photo)
            self.original_image_label.image = self.original_photo
        else:
            self.dec_photo = photo
            self.dec_image_label.config(image=self.dec_photo)
            self.dec_image_label.image = self.dec_photo

    def reset_image_frame(self):
        self.original_image_label.config(image='')
        self.dec_image_label.config(image='')
        self.original_photo = None
        self.dec_photo = None
        self.decompressed_path = None
        self.bin_path = None

# Instantiate the GUI
app = MyGUI()
