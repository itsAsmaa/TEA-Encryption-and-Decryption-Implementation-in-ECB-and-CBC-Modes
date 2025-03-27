import struct
from PIL import Image

# Constants
DELTA = 0x9E3779B9  # Constant value used in the TEA algorithm
NUM_ROUNDS = 32  # Number of rounds for the TEA algorithm

# TEA Encryption Function
def tea_encrypt(block, key):
    L, R = struct.unpack('>2L', block)  # Unpack the 64-bit block into two 32-bit halves
    sum_val = 0
    K = struct.unpack('>4L', key)  # Unpack the 128-bit key into four 32-bit parts

    for _ in range(NUM_ROUNDS):
        sum_val = (sum_val + DELTA) & 0xFFFFFFFF
        L = (L + (((R << 4) + K[0]) ^ (R + sum_val) ^ ((R >> 5) + K[1]))) & 0xFFFFFFFF
        R = (R + (((L << 4) + K[2]) ^ (L + sum_val) ^ ((L >> 5) + K[3]))) & 0xFFFFFFFF

    return struct.pack('>2L', L, R)  # Pack the encrypted halves back into a 64-bit block

# TEA Decryption Function
def tea_decrypt(block, key):
    L, R = struct.unpack('>2L', block)  # Unpack the 64-bit block into two 32-bit halves
    sum_val = (DELTA * NUM_ROUNDS) & 0xFFFFFFFF
    K = struct.unpack('>4L', key)  # Unpack the 128-bit key into four 32-bit parts

    for _ in range(NUM_ROUNDS):
        R = (R - (((L << 4) + K[2]) ^ (L + sum_val) ^ ((L >> 5) + K[3]))) & 0xFFFFFFFF
        L = (L - (((R << 4) + K[0]) ^ (R + sum_val) ^ ((R >> 5) + K[1]))) & 0xFFFFFFFF
        sum_val = (sum_val - DELTA) & 0xFFFFFFFF

    return struct.pack('>2L', L, R)  # Pack the decrypted halves back into a 64-bit block

# Function to pad the data to a multiple of 8 bytes
def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

# Function to unpad the data
def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# TEA-ECB Mode Encryption
def tea_ecb_encrypt(data, key):
    encrypted_data = bytearray()
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        if i < 8 * 10:  # Leave the first 10 blocks unencrypted
            encrypted_data.extend(block)
        else:
            encrypted_data.extend(tea_encrypt(block, key))
    return bytes(encrypted_data)

# TEA-ECB Mode Decryption
def tea_ecb_decrypt(data, key):
    decrypted_data = bytearray()
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        if i < 8 * 10:  # Leave the first 10 blocks unencrypted
            decrypted_data.extend(block)
        else:
            decrypted_data.extend(tea_decrypt(block, key))
    return bytes(decrypted_data)

# TEA-CBC Mode Encryption
def tea_cbc_encrypt(data, key, iv):
    encrypted_data = bytearray()
    previous_block = iv

    for i in range(0, len(data), 8):
        block = data[i:i+8]
        if i < 8 * 10:  # Leave the first 10 blocks unencrypted
            encrypted_data.extend(block)
            previous_block = block
        else:
            block = bytes(x ^ y for x, y in zip(block, previous_block))  # XOR with the previous block
            encrypted_block = tea_encrypt(block, key)
            encrypted_data.extend(encrypted_block)
            previous_block = encrypted_block

    return bytes(encrypted_data)

# TEA-CBC Mode Decryption
def tea_cbc_decrypt(data, key, iv):
    decrypted_data = bytearray()
    previous_block = iv

    for i in range(0, len(data), 8):
        block = data[i:i+8]
        if i < 8 * 10:  # Leave the first 10 blocks unencrypted
            decrypted_data.extend(block)
            previous_block = block
        else:
            decrypted_block = tea_decrypt(block, key)
            decrypted_block = bytes(x ^ y for x, y in zip(decrypted_block, previous_block))  # XOR with the previous block
            decrypted_data.extend(decrypted_block)
            previous_block = block

    return bytes(decrypted_data)

# Function to read image file
def read_image(file_path):
    img = Image.open(file_path).convert('L')  # Open the image and convert to grayscale
    return img

# Function to write image file
def write_image(file_path, img):
    img.save(file_path)  # Save the image to the specified path

# Convert image to byte array
def image_to_bytes(img):
    return img.tobytes()  # Convert image to bytes

# Convert byte array back to image
def bytes_to_image(data, size):
    return Image.frombytes('L', size, data)  # Convert bytes back to an image

# Main Function
def main():
    # User inputs
    key = input("Enter the key (in hexadecimal): ")
    iv = input("Enter the IV value (in hexadecimal for CBC mode): ")
    image_path = input("Enter the path to the image: ")

    # Remove 0x prefix if present
    if key.startswith('0x'):
        key = key[2:]
    if iv.startswith('0x'):
        iv = iv[2:]

    # Convert inputs to bytes
    key = bytes.fromhex(key)
    iv = bytes.fromhex(iv)

    # Read the image file
    img = read_image(image_path)
    img_size = img.size

    # Convert image to bytes
    image_data = image_to_bytes(img)

    # Pad the image data
    padded_data = pad(image_data)

    # Encrypt and decrypt using TEA-ECB
    encrypted_ecb = tea_ecb_encrypt(padded_data, key)
    decrypted_ecb = tea_ecb_decrypt(encrypted_ecb, key)
    decrypted_ecb = unpad(decrypted_ecb)

    # Convert back to images
    encrypted_ecb_img = bytes_to_image(encrypted_ecb, img_size)
    decrypted_ecb_img = bytes_to_image(decrypted_ecb, img_size)

    # Save encrypted and decrypted images
    write_image('encrypted_ecb.bmp', encrypted_ecb_img)
    write_image('decrypted_ecb.bmp', decrypted_ecb_img)

    # Encrypt and decrypt using TEA-CBC
    encrypted_cbc = tea_cbc_encrypt(padded_data, key, iv)
    decrypted_cbc = tea_cbc_decrypt(encrypted_cbc, key, iv)
    decrypted_cbc = unpad(decrypted_cbc)

    # Convert back to images
    encrypted_cbc_img = bytes_to_image(encrypted_cbc, img_size)
    decrypted_cbc_img = bytes_to_image(decrypted_cbc, img_size)

    # Save encrypted and decrypted images
    write_image('encrypted_cbc.bmp', encrypted_cbc_img)
    write_image('decrypted_cbc.bmp', decrypted_cbc_img)

    print("Encryption and decryption complete. Check the generated files.")

if __name__ == "__main__":
    main()
