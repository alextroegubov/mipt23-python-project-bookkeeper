"""
Budget class
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Budget:
    """
    Budget.
    period -- period for budget
    category -- specify category
    budget -- money limit

    """
    period: str
    category: int
    budget: int
    pk: int = 0