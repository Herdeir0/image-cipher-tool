# Image Cipher Tool
Encode and decode messages using a greyscale image as a key.

## Usage
Save your key image on the assets folder, then choose if you want to encode or decode a message.

### Encode
Via GUI:
Write your message on the input field and click "Encode", the coordinates will appear below.

On CLI:
python main.py encode "your message"

### Decode
Via GUI:
Paste the encrypted coordinates on the input field and click "Decode", and the secret message will appear below!

On CLI:
python main.py decode "your, coordinates; like, this; X, Y"