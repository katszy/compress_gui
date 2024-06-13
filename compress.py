import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


class Compressor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = self.read_image()
        self.bitmap = None
        self.color_centers = None
        self.height = None
        self.width = None
        self.compressed_data = None

    def read_image(self):
        return np.array(Image.open(self.image_path), dtype=np.uint8)

    def generate_bitmap(self, n_clusters=2):
        """ Generate bitmap by clustering the image into colors using k-means and use labels directly. """
        h, w, d = self.image.shape
        image_array = self.image.reshape((h * w, d))

        # Use kmeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(image_array)
        labels = kmeans.labels_

        # Use labels as bitmap
        self.bitmap = labels.reshape((h, w)).astype(np.uint8)
        self.color_centers = kmeans.cluster_centers_.astype(np.uint8)
        self.height, self.width = h, w

    def rle(self):
        """Run-Length Encoding (compression) """
        flat_bitmap = self.bitmap.flatten()
        current_bit = flat_bitmap[0]
        count = 0
        compressed = bytearray()

        for bit in flat_bitmap:
            if bit == current_bit and count < 128:
                count += 1
            else:
                compressed.append((current_bit << 7) | (count - 1))
                current_bit = bit
                count = 1

        compressed.append((current_bit << 7) | (count - 1))
        self.compressed_data = compressed

    def save_file(self, filename):
        """ Save the compressed byte data to a file.
        Store color centers, height, and width in the header. """
        with open(filename, 'wb') as f:
            # Write the dimensions (4 bytes: 2 bytes for height and 2 for width)
            f.write(self.height.to_bytes(2, 'big'))
            f.write(self.width.to_bytes(2, 'big'))
            # Write each color center (6 bytes total for two RGB colors)
            for color in self.color_centers:
                f.write(color.tobytes())
            f.write(self.compressed_data)

    def compress(self, output_path):
        self.generate_bitmap()
        plt.imshow(self.bitmap, cmap='gray')
        plt.title('Bitmap Image')
        plt.axis('off')
        #plt.show()

        self.rle()
        self.save_file(output_path)

