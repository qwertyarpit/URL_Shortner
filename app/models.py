from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class URLMapping:
    original_url: str
    short_code: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    click_count: int = 0

# In-memory store for short_code -> URLMapping
url_store = {}