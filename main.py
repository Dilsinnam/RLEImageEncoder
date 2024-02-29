from console_gfx import ConsoleGfx
import os


def to_hex_string(data):
    return "".join(format(x, "02x") for x in data)


def count_runs(flat_data):
    runs = 1
    for i in range(1, len(flat_data)):
        if flat_data[i] != flat_data[i - 1]:
            runs += 1
    return runs


def encode_rle(flat_data):
    rle_data = []
    current_count = 1
    for i in range(1, len(flat_data)):
        if flat_data[i] == flat_data[i - 1]:
            current_count += 1
        else:
            rle_data.extend([current_count, flat_data[i - 1]])
            current_count = 1
    rle_data.extend([current_count, flat_data[-1]])
    return rle_data


def get_decoded_length(rle_data):
    return sum(rle_data[::2])


def decode_rle(rle_data):
    decoded_data = []
    for i in range(0, len(rle_data), 2):
        decoded_data.extend([rle_data[i + 1]] * rle_data[i])
    return decoded_data


def string_to_data(data_string):
    return [int(part, 16) for part in data_string.split(":")]


def string_to_hex_rle(hex_string):
    data = []
    for i in range(0, len(hex_string), 2):
        count = int(hex_string[i], 16)
        value = int(hex_string[i + 1], 16)
        data.extend([count, value])
    return data


def to_rle_string(rle_data):
    return ":".join(
        f"{rle_data[i]}{hex(rle_data[i + 1])[2:]}" for i in range(0, len(rle_data), 2)
    )


def string_to_rle(rle_string):
    parts = rle_string.split(":")
    return [int(parts[i][:-1]) for i in range(len(parts))], [
        int(parts[i][-1], 16) for i in range(len(parts))
    ]


import os


def main():
    print("Welcome to RLE image encoder!")
    print()
    data = None
    print("Displaying Spectrum Image:")
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
    print()

    while True:
        print("\nRLE Menu")
        print("--------")
        print("0. Exit")
        print("1. Load File")
        print("2. Load Test Image")
        print("3. Read RLE String")
        print("4. Read RLE Hex String")  # Added option
        print("5. Read Data Hex String")
        print("6. Display Image")
        print("7. Display RLE String")
        print("8. Display Hex RLE Data")
        print("9. Display Hex Flat Data")

        choice = input("Select a Menu Option: ")
        if choice == "0":
            print("Exiting program.")
            break

        if choice == "1":
            filename = input("Enter the filename from testfiles folder: ")
            dir_path = os.path.dirname(os.path.realpath(__file__))
            if not filename.startswith("testfiles/"):
                filename = os.path.join("testfiles", filename)
            full_path = os.path.join(dir_path, filename)
            try:
                data = ConsoleGfx.load_file(full_path)
            except FileNotFoundError:
                print("File not found.")

        elif choice == "2":
            data = ConsoleGfx.test_image
            print("Test image data loaded.")
        elif choice == "3":
            rle_string = input("Enter an RLE string to be decoded: ")
            data = string_to_data(rle_string)
        elif choice == "4":
            hex_string = input("Enter the hex string holding RLE data: ")
            data = string_to_data(hex_string)
        elif choice == "5":
            hex_rle_string = input("Enter the hex string holding RLE data: ")
            data = string_to_hex_rle(hex_rle_string)
        elif choice == "6":
            if data is not None:
                ConsoleGfx.display_image(data)
        elif choice == "7":
            rle_data = encode_rle(data)
            print("RLE hex values:", to_hex_string(rle_data))
        elif choice == "8":
            print("Flat hex values:", to_hex_string(data))
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
