from enum import Enum

class Cost(Enum):
    """
    Cost settings so that we can iteratively develop with low cost settings and release with higher cost settings
    """
    HIGH = 'HIGH'
    LOW = 'LOW'