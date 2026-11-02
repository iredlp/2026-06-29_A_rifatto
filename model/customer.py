from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Customer:
    CustomerId: int
    FirstName: str
    LastName: str
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str
    SupportRepId: int

    list_artisti: list = field(default_factory=list)
    fatturato: float=0

    def __hash__(self):
        return hash(self.  CustomerId)

    def __eq__(self, other):
        if isinstance(other, Customer):
            return self.  CustomerId == other.  CustomerId
        return False

    def __repr__(self):
        return (f"{self.FirstName, self.LastName}  ({self.State if self. State is not None else 'N/D'})")