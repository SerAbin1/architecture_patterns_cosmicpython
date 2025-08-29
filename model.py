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
        self.available_qty = qty
        self._purchased_qty = qty
        self._allocations = set()

    def allocate(self, line: OrderLine):
        self.availability_qty -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.availability_qty >= line.qty
