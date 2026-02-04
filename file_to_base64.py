import sys
import base64
import os

def convert_to_base64(file_path, output_file=None):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"Reading '{file_path}'...")
    with open(file_path, "rb") as f:
        file_content = f.read()
        base64_string = base64.b64encode(file_content).decode("utf-8")

    if output_file:
        with open(output_file, "w") as out:
            out.write(base64_string)
        print(f"Success! Base64 string saved to '{output_file}'")
    else:
        print("\n--- Base64 Output (First 500 chars) ---")
        print(base64_string[:500] + "... (truncated)")
        print("\nTo save to a file, run use: python file_to_base64.py <input_file> <output_txt_file>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_to_base64.py <path_to_audio_file> [output_text_file]")
        print("Example: python file_to_base64.py sample.mp3 output.txt")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        convert_to_base64(input_path, output_path)
