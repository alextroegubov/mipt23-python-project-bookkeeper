"""
Budget class
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Budget:
    """
    Budget.
    period -- period for budget
    budget -- money limit
    """
    period: str
    limit: float = 0
    spent: float = 0
    pk: int = 0