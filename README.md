# Personal assistant / chatbot with GUI

### A simple chatbot and personal assistant with a graphical interface.

Also has a GPT 2 language model subroutine for more human-like responses on top of my basic chatbot implementation

----------------


## dependencies:

This app depends on these python modules:
 * tkinter (may also require system packages to work)
 * nltk
 * chattingtransformer

An internet connection is required when the program is first run in order to download the gpt-2 language model and
punkt tokenizing library. This will take some time.

## installation instructions

### how to install dependencies on Debian-based Linux

assuming you have python3 and pip3 installed and working:
```bash
sudo apt install python3-tk
python3 -m pip install chattingtransformer nltk
```

### how to install dependencies on other POSIX systems

assuming you have python and pip installed and up to date:
```bash
python -m pip install chattingtransformer nltk tkinter
```

### Running the assistant

```bash
cd assistant  # or wherever the project directory is
python main.py  # or python3 main.py
```

## computational resource considerations:

The size of the model is configurable in the global variables, and has a huge impact on the amount of processing time
and RAM used to generate text. Available values are:

|   CHAT_MODEL   |  Parameters  |    Size     |
|----------------|--------------|-------------|
| 'gpt2'         |    134 M     |   548  MB   |
| 'gpt2-medium'  |    335 M     |   1.52 GB   |
| 'gpt2-large'   |    774 M     |   3.25 GB   |
| 'gpt2-xl'      |    1.5 B     |   6.43 GB   |
