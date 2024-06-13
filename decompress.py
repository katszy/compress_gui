import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class Decompressor:
    def __init__(self, compressed_file_path):
        self.compressed_file_path = compressed_file_path
        self.color_centers = None
        self.compressed_data = None
        self.original_dims = None
        self.bitmap = None
        self.decompressed_image = None

    def read_compressed(self):
        """ Read the compressed file.
        Extract the header data with including color and dimensions. """

        with open(self.compressed_file_path, 'rb') as f:
            # Read the dimensions
            height = int.from_bytes(f.read(2), 'big')
            width = int.from_bytes(f.read(2), 'big')
            # Read the colors (6 bytes: 2 colors x 3 bytes each)
            color_centers = np.frombuffer(f.read(6), dtype=np.uint8).reshape(2, 3)
            # Read the rest of the data
            compressed_data = bytearray(f.read())
        self.color_centers, self.compressed_data, self.original_dims = color_centers, compressed_data, (height, width)

    def rle(self):
        """RLE decompression."""
        bitmap = []
        for byte in self.compressed_data:
            present_bit = byte >> 7
            count = (byte & 0x7F) + 1
            bitmap.extend([present_bit] * count)
        self.bitmap = np.array(bitmap, dtype=np.uint8)

    def reconstruct_image(self):
        h, w = self.original_dims
        image = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(h):
            for j in range(w):
                image[i, j] = self.color_centers[self.bitmap[i * w + j]]
        self.decompressed_image = image

    def save_decompressed(self, image_output_path):
        pass
        Image.fromarray(self.decompressed_image).save(image_output_path)
        #print(f"Decompressed image saved to {image_output_path}")

    def decompress(self, image_output_path):
        self.read_compressed()
        self.rle()
        self.reconstruct_image()

        plt.imshow(self.decompressed_image)
        plt.title('Decompressed Image')
        plt.axis('off')
        #plt.show()

        self.save_decompressed(image_output_path)