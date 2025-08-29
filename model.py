# order: order_reference
# order_ref: order_lines: sku, quantity
#
# Can buy batches of stock: ref, sku, quantity, eta (if shipping, oldest eta given pref)
# order_lines are allocated to batches, then sent to customer delivery address
# available_quantity -= x, the no of allocated stock to batch

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    orderId: str
    sku: str
    qty: int


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

    def deallocation(self, line: OrderLine):
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
