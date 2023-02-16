import os

USER = os.getenv('USER')
AI_NAME = 'Logan'
CHAT_MODEL = 'gpt2-medium'
MAX_GPT_PROMPT_CHARS = 1000
SAMPLING_METHOD = 'top-p-nucleus-sampling'  # 'greedy'  # 'beam-search'  # 'top-k-sampling'
LENGTH_VARIANCE = 20
PROMPT_REPEAT_CHANCE = 0.08
GPT_RESCUE_CHANCE = 0.95
CUSTOM_CHAT_SETTINGS = {
  "do_sample": True,
  "early_stopping": True,
  # "num_beams": 4,
  "temperature": 0.35,
  # "top_k": 80,
  "top_p": 1,
  # "repetition_penalty": 1,
  # "length_penalty": 1,
  # "no_repeat_ngram_size": 2,
  'bad_words_ids': None
}
ROBOT_TEXT_COLOR = 'PaleGreen1'
USER_TEXT_COLOR = 'cyan'  # 'Magenta1'
