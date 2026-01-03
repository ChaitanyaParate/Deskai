import os
from llm.local import LocalLLM
from llm.openai_client import OpenAIClient
# ------------ Returns Local or Online LLM -------------------
def get_llm():
    # if os.getenv("DESKAI_USE_REMOTE_LLM") == "1":
    #     return OpenAIClient(api_key=os.environ["OPENAI_API_KEY"])
    return LocalLLM()
