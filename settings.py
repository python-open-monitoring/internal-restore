import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG") == "1"
AMQP_URI = os.getenv("AMQP_URI")
DATABASE_URI = os.getenv("DATABASE_URI")
CACHE_URI = os.getenv("CACHE_URI")
