import cv2
import numpy as np

# Function to convert data into binary format
def data_to_binary(data):
    if type(data) == str:
        p = ''.join([format(ord(i), '08b') for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b') for i in data]
    return p


# Function to hide data in the given image
def hide_data(img, data):
    data += "$$"  # '$$' represents the secret key
    d_index = 0
    b_data = data_to_binary(data)
    len_data = len(b_data)

    # Iterate over pixels in the image and update pixel values
    for value in img:
        for pix in value:
            r, g, b = data_to_binary(pix)
            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-  1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index])
                d_index += 1
            if d_index >= len_data:
                break
    return img


def encode():
    img_name = input("Enter image name: ")
    image = cv2.imread(img_name)
    data = input("Enter message: ")
    if len(data) == 0:
        raise ValueError("Empty data")
    enc_img = input("Enter encoded image name: ")
    enc_data = hide_data(image, data)
    enc_data = np.array(enc_data, dtype=np.uint8)  # Convert to uint8 data type
    cv2.imwrite(enc_img, enc_data)
    print("Image encoded successfully.")


# Function to find hidden data in the image
def find_data(img):
    bin_data = ""
    for value in img:
        for pix in value:
            r, g, b = data_to_binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$$":
            break
    return readable_data[:-2]


def decode():
    img_name = input("Enter image name: ")
    image = cv2.imread(img_name)
    msg = find_data(image)
    return msg


def steganography():
    while True:
        print("Image Steganography")
        print("1. Encode")
        print("2. Decode")
        print("0. Exit")

        choice = int(input("Enter your choice (0-2): "))
        if choice == 1:
            encode()
            print()
        elif choice == 2:
            decoded_message = decode()
            if decoded_message:
                print("Decoded message:")
                print(decoded_message)
            else:
                print("No hidden message found in the image.")
            print()
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")
            print()


# Run the steganography function
steganography()
