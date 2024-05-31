from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Cost(Enum):
    """
    Cost settings so that we can iteratively develop with low cost settings and release with higher cost settings
    """
    HIGH = 'HIGH'
    LOW = 'LOW'


@dataclass
class Brand:
    """
    Convenience wrapper around brand data
    """
    name: str
    market: str
    brand_identity: str
    brand_style: Optional[str] = None