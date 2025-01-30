import os

from sosmart.model_testing_ui.config_formatters.default import format_role as format_role_default
from sosmart.model_testing_ui.config_formatters.sensory_stt_punctuation import format_role as format_role_sensory_stt_punctuation


OUTPUT_FOLDER = "data"


DEFAULT_CONFIG = {
    "formatter": format_role_sensory_stt_punctuation,
    "remove_punctuation": True,

    #Model output parameters that change token probabilities
    "temperature": 1, #default 0.8 - flattens token distribution making tokens with lower probability more likely to be chosen
    "top_p": 0.95, #default 0.95 - max cummulative probability of tokens considered
    "top_k": 40, #default 40 - max number of tokens considered
    "frequency_penalty": 0.0,#default 0, penalty for repeated tokens
    "repeat_penalty": 1,
    "presence_penalty": 0.0,#default 0, penalty for tokens that exist in the whole context
    "typical_p": 1.0,#¯\_(ツ)_/¯ https://www.reddit.com/r/LocalLLaMA/comments/153bnly/what_does_typical_p_actually_do/
    "mirostat_mode": 0,#default 0 - 0=disabled, 1=v1, 2=latest(recommended)
    "mirostat_tau": 1,#default 1 - cross-entropy (or surprise) value, higher value corresponds to more surprising or less predictable text
    "mirostat_eta": 0.1,#default 0.1 - https://www.reddit.com/r/LocalLLaMA/comments/16nh7x9/how_mirostat_works/
    "logit_bias": None,#default none - "lets you control whether the model is more or less likely to generate a specific word." https://www.vellum.ai/llm-parameters/logit-bias
}



if "config" not in os.environ:
    print("\n\nYou forgot to add a config\n\n")
    exit(0)

if "user" not in os.environ:
    print("\n\nYou forgot to add a user\n\n")
    exit(0)


config = os.environ["config"]
user = os.environ["user"]



config_map = {
    "default": {
        "name": "default",
        "formatter": format_role_default,
        "remove_punctuation": False,
      },
    "sensory_stt_punctuation": {
        "name": "sensory_stt_punctuation",
        "formatter": format_role_sensory_stt_punctuation,
        "remove_punctuation": True,
    },
}

if config not in config_map:
    print(f"Invalid config allowed values are {config_map.keys()}")
    exit(0)


def get_config():
    return {**DEFAULT_CONFIG, **config_map[config]}


def get_user():
    return user


if __name__ == "__main__":
    print(f"Allowed configs: {config_map.keys()}")


