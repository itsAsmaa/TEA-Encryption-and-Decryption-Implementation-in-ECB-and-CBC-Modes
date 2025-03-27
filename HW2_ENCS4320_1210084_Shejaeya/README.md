# TEA Image Encryption and Decryption using CBC and ECB

This project implements image encryption and decryption using the Tiny Encryption Algorithm (TEA) in both ECB and CBC modes. The code reads an image, encrypts it and then decrypts it ensuring the integrity of the original image.

## Features
- TEA Encryption and Decryption: encrypts and decrypts 64-bit blocks using a 128-bit key.
- Padding and Unpadding: ensures data is padded to a multiple of 8 bytes for encryption.
- ECB and CBC Modes: it supports encryption and decryption in both ECB and CBC modes.
- Image Handling: reads an image, converts it to grayscale, encrypts and decrypts it, and saves the processed images.

## Prerequisites
- Python 3.x
- Pillow library for image processing

You can install the Pillow library from the terminal using pip :
pip install Pillow


## How to Use

1. Run the script :
   python main.py
   
2. Follow the prompts:
   - Enter the key (in hexadecimal format).
   - Enter the IV (in hexadecimal format) for CBC mode.
   - Enter the path to the image file you want to encrypt.

## Code Overview

### TEA Encryption and Decryption Functions
- tea_encrypt(block, key): Encrypts a 64-bit block using a 128-bit key.
- tea_decrypt(block, key): Decrypts a 64-bit block using a 128-bit key.

### Padding and Unpadding Functions
- pad(data): Pads data to ensure its length is a multiple of 8 bytes.
- unpad(data): Removes padding from data.

### TEA Modes
- tea_ecb_encrypt(data, key): Encrypts data using TEA in ECB mode, leaving the first 10 blocks unencrypted.
- tea_ecb_decrypt(data, key): Decrypts data using TEA in ECB mode, leaving the first 10 blocks unencrypted.
- tea_cbc_encrypt(data, key, iv): Encrypts data using TEA in CBC mode, leaving the first 10 blocks unencrypted.
- tea_cbc_decrypt(data, key, iv): Decrypts data using TEA in CBC mode, leaving the first 10 blocks unencrypted.

### Image Handling Functions
- read_image(file_path): Reads and converts an image to grayscale.
- write_image(file_path, img): Saves an image to the specified path.
- image_to_bytes(img): Converts an image to a byte array.
- bytes_to_image(data, size): Converts a byte array back to an image.

### Main Function
1. Takes user inputs for the key, IV, and image path.
2. Reads and processes the image.
3. Encrypts and decrypts the image using both TEA-ECB and TEA-CBC modes.
4. Saves the resulting encrypted and decrypted images.

## Example input #######################################################################

Enter the 128-bit key (in hexadecimal): 9E3779B99E3779B99E3779B99E3779B9
Enter the 64-bit IV value (in hexadecimal for CBC mode): 9E3779B99E3779B9
Enter the path to the image: path/to/your/image.bmp
## #####################################################################################

The script will generate the following files:
- encrypted_ecb.bmp
- decrypted_ecb.bmp
- encrypted_cbc.bmp
- decrypted_cbc.bmp

These files will be saved in the same directory as the script .

## Notes
- Ensure the input image is in BMP format.
- The script leaves the first 10 blocks unencrypted for both ECB and CBC modes as specified.

