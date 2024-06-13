from compress import Compressor
from decompress import Decompressor
import os
import matplotlib.pyplot as plt
from PIL import Image


def process_images(directory):
    plots_directory = os.path.join(directory, 'plots')
    if not os.path.exists(plots_directory):
        os.makedirs(plots_directory)

    for filename in os.listdir(directory):
        if filename.endswith('.jpg') and 'decompressed_' not in filename:
            image_path = os.path.join(directory, filename)
            bin_path = os.path.join(directory, filename.split('.')[0] + '.bin')
            decompressed_path = os.path.join(directory, 'decompressed_' + filename)

            # Compress the image
            compressor = Compressor(image_path)
            compressor.compress(bin_path)

            # Decompress the image
            decompressor = Decompressor(bin_path)
            decompressor.decompress(decompressed_path)

            # Calculate file sizes and compression percentage
            original_size = os.path.getsize(image_path)
            compressed_size = os.path.getsize(bin_path)
            if original_size > 0:
                compression_percentage = 100 * (1 - (compressed_size / original_size))
            else:
                compression_percentage = 0

            # Display images side by side
            original_image = Image.open(image_path)
            decompressed_image = Image.open(decompressed_path)

            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            axes[0].imshow(original_image)
            axes[0].set_title('Original Image')
            axes[0].axis('off')

            axes[1].imshow(decompressed_image)
            axes[1].set_title('Decompressed Image')
            axes[1].axis('off')

            plt.suptitle(f'Processed {filename}\nCompression ratio: {compression_percentage:.2f}% reduction in size',
                         fontsize=16)

            # Save the plot
            plot_filename = f'comparison_{filename}.png'
            plot_path = os.path.join(plots_directory, plot_filename)
            fig.savefig(plot_path)
            plt.close(fig)

            print(f"Comparison plot saved to {plot_path}")
            print(f"Processed {filename}: Compressed to {bin_path} and decompressed to {decompressed_path}.")


process_images('data/')