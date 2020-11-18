import os
import tkinter as tk
import time
import random


USER = os.getenv('USER')


def date_string() -> str:
    return time.strftime('The current date is %A the %d of %B %Y', time.localtime())


def time_string() -> str:
    return time.strftime('The current time is %X', time.localtime())


def ask_creator() -> str:
    return 'Perhaps we should ask my creator.'


phrasebook = {
    'greeting': [f"Hi, {USER}!", f"Hello, {USER}!",
                 f"What's up, {USER}?", f"How's it hangin', {USER}?"],
    'confirmation': ["Are you sure?", "Are you certain?"],
    'date': [lambda: date_string()],
    'time': [lambda: time_string()],
    'filler': ['I see.', 'Um...', 'Hmm.', 'Well...'],
    'unknown': ["I don't know.", "You've got me stumped.", 'Curiously, I do not have an answer for that.',
                'Dropped my brain. Honestly I have no clue.', lambda: ask_creator(),
                "You're not making any sense at all, mate.", 'Sorry, what are we talking about again?',
                'I do not know very much yet honestly. My creator is constantly updating me though.'],
}


class Conversator:
    def __init__(self):
        print(self.grab_phrase(phrasebook, 'greeting'))

    def grab_phrase(self, item=None, key=None, args=None) -> str:
        if item is None:
            item = phrasebook
        if key is not None:
            first_key = key_list = key
            if isinstance(key_list, list):
                first_key = key_list.pop(0)  # delete first key from key list and assign it to first_key
                if len(key_list) == 0:
                    key_list = None
            else:
                key_list = None
            return self.grab_phrase(item[first_key], key=key_list, args=args)
        if isinstance(item, list):
            return self.grab_phrase(item[random.randrange(len(item))], args=args)
        if isinstance(item, dict):
            return self.grab_phrase(item[random.choice(list(item.keys()))], args=args)
        if callable(item):
            if args is not None:
                return item(args)
            return item()
        return item

    def basic_ass_bitch_reply(self, input_string: str) -> str:
        if input_string in phrasebook.keys():
            return self.grab_phrase(phrasebook, input_string)
        else:
            return self.grab_phrase(phrasebook, 'unknown')


c = Conversator()


col = {
    'bg': '#303030',
    'mg': '#600060',
    'fg': '#ffffff',
    'acc': '#C000D0'
}


class GuiWindow:
    def __init__(self):
        self.robot_spoke_last = True

        self.root = tk.Tk()
        self.root.title('Assistant')
        self.icon = tk.PhotoImage(file='res/robot-small.png')
        self.root.iconphoto(True, self.icon)
        self.root.geometry('400x520')
        self.root.minsize(320, 320)

        self.main_menu = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.root)
        self.file_menu.add_command(label='New...')
        self.file_menu.add_command(label='Save As...')
        self.file_menu.add_command(label='Exit', command=self.root.destroy)
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_command(label='Edit')
        self.root.config(menu=self.main_menu)

        self.chat_area = tk.Text(self.root,
                                 bd=1, bg=col['bg'], fg=col['fg'],
                                 insertbackground=col['fg'],
                                 highlightcolor=col['acc'], selectbackground=col['acc'])
        self.chat_area.place(x=0, y=0, relwidth=1.0, relheight=0.8)

        self.message_area = tk.Text(self.root,
                                    bd=1, bg=col['bg'], fg=col['fg'],
                                    insertbackground=col['fg'],
                                    highlightcolor=col['acc'], selectbackground=col['acc'])
        self.message_area.place(x=0, rely=0.8, relwidth=0.75, relheight=0.2)

        self.send_button = tk.Button(self.root, text='Send', font=('Consolas', 12),
                                     command=self.user_send,
                                     bg=col['mg'], fg=col['fg'], activebackground=col['acc'])
        self.send_button.place(anchor='ne', relx=1.0, rely=0.8, relwidth=0.25, relheight=0.1)

        self.preconfigured_button = tk.Button(self.root, text='Preconfigs', font=('Consolas', 8),
                                              bg=col['mg'], fg=col['fg'], activebackground=col['acc'])
        self.preconfigured_button.place(anchor='ne', relx=1.0, rely=0.9, relwidth=0.25, relheight=0.1)

        self.output('\n' + c.grab_phrase(phrasebook, 'greeting'))

        self.root.mainloop()

    def user_send(self):
        message = self.message_area.get('1.0', 'end-1c')  # exclude the last character, which is a line feed
        self.message_area.delete('1.0', 'end')
        self.output(message, from_robot=False)
        self.invoke_response(message)

    def output(self, string: str, from_robot: bool = True):
        header_bit = ''
        if from_robot != self.robot_spoke_last:
            self.robot_spoke_last = from_robot
            if from_robot:
                header_bit = "\nassistant:\n"
            else:
                header_bit = '\n'+USER+':\n'
        self.chat_area.insert('end', header_bit+string+'\n')

    def invoke_response(self, user_input: str):
        self.output(c.basic_ass_bitch_reply(user_input))


if __name__ == '__main__':
    main_window = GuiWindow()
