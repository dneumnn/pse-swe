from dataclasses import dataclass, field

from product import Product

@dataclass
class Order:
    items: list[(Product, int)] = field(default_factory=lambda: [])
    status: str="open"

    def add_item(self, product: Product, quantity: int) -> None:
        self.items.append((product, quantity))

    def get_items(self) -> list[(Product, int)]:
        return self.items

    def total_price(self) -> float:
        total = 0
        for product, quantity in self.items:
            total += quantity * product.price
        return total



