import random
import string
import re
from urllib.parse import urlparse
from datetime import datetime

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url):
    # Basic validation using urlparse
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False

def isoformat(dt):
    return dt.replace(microsecond=0).isoformat()