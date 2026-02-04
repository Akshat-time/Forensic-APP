import base64
import io

def decode_base64_audio(base64_string):
    # Remove header if present (e.g., "data:audio/wav;base64,")
    if "," in base64_string:
        base64_string = base64_string.split(",", 1)[1]
    return io.BytesIO(base64.b64decode(base64_string))
