import os
import tkinter as tk
import time
import random
from chattingtransformer import ChattingGPT2


USER = os.getenv('USER')
CHAT_MODEL = 'gpt2-medium'
SAMPLING_METHOD = 'top-p-nucleus-sampling'  # 'greedy'  # 'beam-search'  # 'top-k-sampling'
LENGTH_VARIANCE = 10
PROMPT_REPEAT_CHANCE = 0.10
GPT_RESCUE_CHANCE = 0.8
CUSTOM_CHAT_SETTINGS = {
  "do_sample": True,
  "early_stopping": True,
  "num_beams": 4,
  "temperature": 1,
  "top_k": 40,
  "top_p": 0.4,
  "repetition_penalty": 1,
  "length_penalty": 1,
  "no_repeat_ngram_size": 2,
  'bad_words_ids': None
}
col = {
    'bg': '#303030',
    'mg': '#600060',
    'fg': '#ffffff',
    'acc': '#C000D0'
}
ROBOT_TEXT_COLOR = 'PaleGreen1'
USER_TEXT_COLOR = 'cyan'  # 'Magenta1'


def date_string() -> str:
    return time.strftime('The current date is %A the %d of %B %Y', time.localtime())


def time_string() -> str:
    return time.strftime('The current time is %X', time.localtime())


def ask_creator() -> str:
    return 'Perhaps we should ask my creator.'


class Conversator:
    def __init__(self):
        self.phrasebook = {
            'greeting': [f"Hi, {USER}!", f"Hello, {USER}!",
                         f"What's up, {USER}?", f"How's it hangin', {USER}?"],
            'confirmation': ["Are you sure?", "Are you certain?"],
            'date': [lambda: date_string()],
            'time': [lambda: time_string()],
            'filler': ['I see.', 'Um...', 'Hmm.', 'Well...'],
            'unknown': ["I don't know.", "You've got me stumped.", 'Curiously, I do not have an answer for that.',
                        'Dropped my brain. Honestly I have no clue.', lambda: ask_creator(),
                        lambda: self.subroutine_start('talk to gpt', confirm=True,
                                                      confirmation_prompt='Perhaps we should ask my colleague, GPT. '
                                                                          'Would you like to send this query to GPT?'),
                        "You're not making any sense at all, mate.", 'Sorry, what are we talking about again?',
                        'I do not know very much yet honestly. My creator is constantly updating me though.',
                        "I'm a newbie here, but I'd like to help"],
            'what': ["I am a personal assistant and AI chat program, created by Ethan to do your bidding. "
                     "I am a work in progress. :D"],
            'affirmative phrases': ['Yes', 'Yeah', 'Ok', 'Alright', 'Y', 'Definitely', "Let's do it!", 'Alright then!',
                                    'Awesome', 'Awesome!', 'Cool!', 'Awesome.', 'Sure'],
            'assumption of no': ["I'll take that as a no.", 'No? ok cool.', 'Got it.',
                                 "Yeah, why would we need to? Nevermind that I asked."],
            'gpt': lambda: self.subroutine_start('talk to gpt', confirm=True),
        }

        self.process_stack = ['basic']
        # a queue for the AI's responses allows for multiple chat bubbles to be sent in a row in the GUI:
        self.response_queue = [self.grab_phrase(key='greeting')]

        self.subroutines = {
            'basic': self.basic_ass_bitch_reply,
            'confirmation': self.confirm_or_deny,
            'talk to gpt': self.talk_to_gpt,
        }

        print(self.grab_phrase(self.phrasebook, 'greeting') + ' This is the debug window.')

        # set up GPT2
        self.gpt2 = ChattingGPT2(CHAT_MODEL)

        # set up GUI
        self.gui = GuiWindow()
        self.gui.conversator = self
        self.gui.unload_responses()
        self.gui.root.mainloop()

    def grab_phrase(self, item=None, key=None, args=None):
        if item is None:
            item = self.phrasebook
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

    def think(self, input_string: str) -> None:
        print(self.process_stack)
        print(self.response_queue)
        current_subroutine = self.process_stack[-1]
        self.subroutines[current_subroutine](input_string)

    def invoke_response(self, user_input: str) -> None:
        self.think(user_input)  # read and evaluate
        self.gui.unload_responses()  # print

    def enqueue_response(self, response: str) -> None:
        self.response_queue.append(response)

    def dequeue_response(self) -> str:
        return self.response_queue.pop(0)

    def basic_ass_bitch_reply(self, input_string: str) -> None:
        if input_string.lower() in self.phrasebook.keys():
            sentence = self.grab_phrase(key=input_string.lower())
            if sentence is not None:
                self.enqueue_response(str(sentence))
        else:
            if random.random() < GPT_RESCUE_CHANCE:
                self.enqueue_response(self.gpt_response(input_string))
            else:
                self.enqueue_response(self.grab_phrase(key='unknown'))

    def confirm_or_deny(self, user_input: str) -> None:
        if user_input.lower() in map(str.lower, self.phrasebook['affirmative phrases']):
            self.process_stack.pop()
            self.basic_ass_bitch_reply('affirmative phrases')
        else:
            self.process_stack.pop()
            self.process_stack.pop()
            self.basic_ass_bitch_reply('assumption of no')

    def subroutine_start(self, routine_name: str, confirm: bool = False, confirmation_prompt=None) -> None:
        self.process_stack.append(routine_name)
        if confirm:
            self.process_stack.append('confirmation')
            if confirmation_prompt is not None:
                self.enqueue_response(confirmation_prompt)
            else:
                self.enqueue_response(self.grab_phrase(key='confirmation'))
        else:
            self.basic_ass_bitch_reply('affirmative phrases')

    def gpt_response(self, user_input: str) -> str:
        response = self.gpt2.generate_text(user_input,
                                           min_length=len(user_input) - LENGTH_VARIANCE,
                                           max_length=len(user_input) + LENGTH_VARIANCE,
                                           custom_settings=CUSTOM_CHAT_SETTINGS)
        # randomly remove prompt (it's sometimes really funny or natural to have the bot repeat & continue)
        if bool(random.random() >= PROMPT_REPEAT_CHANCE):
            slice_start = len(user_input) + 1
            slice_end = len(response)
            if slice_start > slice_end:  # check edge case
                slice_start = slice_end
            response = response[slice_start:slice_end]
        while len(response) > 0 and response[0] == '\n':  # chomp leading newlines
            response = response[1:]
        return response

    def talk_to_gpt(self, user_input: str) -> None:
        if user_input != 'exit':
            self.enqueue_response(self.gpt_response(user_input))
        else:
            self.process_stack.pop()


class GuiWindow:
    def __init__(self):
        # GUIWindow is meant to be a component of a Conversator, with a reference back to it.
        self.conversator = None

        self.robot_spoke_last = True

        self.root = tk.Tk()
        self.root.title('Logan (Personal Assistant)')
        self.icon = tk.PhotoImage(file='res/robot-small.png')
        self.root.iconphoto(True, self.icon)
        self.root.geometry('380x472')
        self.root.minsize(320, 320)

        self.main_menu = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.root)
        # self.file_menu.add_command(label='New...')
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
        self.chat_area.tag_configure('robot', foreground=ROBOT_TEXT_COLOR)
        self.chat_area.tag_configure('user', foreground=USER_TEXT_COLOR)

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

    def user_send(self):
        message = self.message_area.get('1.0', 'end-1c')  # exclude the last character, which is a line feed
        print(message)
        self.message_area.delete('1.0', 'end')
        self.output(message, from_robot=False)
        self.conversator.invoke_response(message)

    def output(self, string: str, from_robot: bool = True):
        header_bit = ''
        if from_robot != self.robot_spoke_last:
            self.robot_spoke_last = from_robot
            if from_robot:
                # if self.c.process_stack[-1] == 'talk to gpt':
                #     header_bit = "\nLogan (gpt):\n"
                # else:
                header_bit = "\nLogan:\n"
            else:
                header_bit = '\n'+USER+':\n'
        if from_robot:
            tags = 'robot'
        else:
            tags = 'user'
        self.chat_area.insert('end', header_bit+string+'\n', tags)
        self.chat_area.yview('end')

    def unload_responses(self):
        print(self.conversator.response_queue)
        while len(self.conversator.response_queue) > 0:
            sentence = self.conversator.dequeue_response()
            if sentence is not None:  # here in case of errors
                self.output(sentence, from_robot=True)


if __name__ == '__main__':
    # main_window = GuiWindow()
    main_process = Conversator()
