import os
from dotenv import load_dotenv

load_dotenv()
# print(os.getenv("GEMINI_API_KEY"))


def get_google_api_key():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # print(GEMINI_API_KEY)
    return GEMINI_API_KEY


def get_tavily_api_key():
    return os.getenv("TAVILY_API_KEY")


def get_kaggle_username():
    return os.getenv("KAGGLE_USERNAME")


def get_kaggle_api_key():
    return os.getenv("KAGGLE_API_KEY")
