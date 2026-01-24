from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ProductInput:
    title: str
    category: str
    description: str
    brand_tone: str
    promotion: Optional[str] = None
    target_audience: Optional[str] = None

@dataclass
class GeneratedCopy:
    captions: List[str]
    hashtags: List[str]
    ctas: List[str]
