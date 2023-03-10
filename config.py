import os
from dotenv import load_dotenv

load_dotenv(override=False)  # do not overrise existing ones

class Config(object):
    Account = os.getenv("ACCOUNT")
    Password = os.getenv("PASSWORD")
    URL = os.getenv("URL")
