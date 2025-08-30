# order: order_reference
# order_ref: order_lines: sku, quantity
#
# Can buy batches of stock: ref, sku, quantity, eta (if shipping, oldest eta given pref)
# order_lines are allocated to batches, then sent to customer delivery address
# available_quantity -= x, the no of allocated stock to batch

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


# order has order_ref which uiquely identifies it
# but line doesnt
# whenever we have a business concept that has data but no identitiy,
# we often choose to represent it using the **Value Object** pattern
# Value Object is any domain object that is uniquely  identified by the data it holds;
# we make them immutable
@dataclass(frozen=True)
class OrderLine:
    orderId: str
    sku: str
    qty: int


# we use the term entity to describe a domain object that has a long-lived identity
# entities have identity equality, even if we change their values, they're still the same thing
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocations = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate:
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_qty(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_qty(self) -> int:
        return self._purchased_qty - self.allocated_qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_qty >= line.qty

    # special method to define the behaviour of the class for the equality operator
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    # https://docs.python.org/3/glossary.html#term-hashable
    # An object is hashable if it has a hash value which never changes during its lifetime (it needs a __hash__() method),
    # and can be compared to other objects (it needs an __eq__() method).
    # Hashable objects which compare equal must have the same hash value.
    # Hashability makes an object usable as a dictionary key and a set member, because these data structures use the hash value internally.
    def __hash__(self):
        return hash(self.reference)

    # to enable sorted on our list of batches in allocate function
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    batch = next(
        b   
        for b in sorted(batches)
        if b.can_allocate(line)
    )
    batch.allocate(line)
    return batch.reference
