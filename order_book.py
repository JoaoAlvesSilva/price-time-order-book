from enum import Enum
from dataclasses import dataclass

class OrderType(Enum):
    Addition = 0
    Modification = 1

class BuySellType(Enum):
    Buy = 0
    Sell = 1

@dataclass
class Message:
    OrderID: int  
    category: OrderType  
    buy: BuySellType  
    size: int 
    price: float 

class Book:
    def __init__(self):
        self.bids = {}  # Dictionary to store buy orders {order_id: (price, size, timestamp)}
        self.asks = {}  # Dictionary to store sell orders {order_id: (price, size, timestamp)}
        self.timestamp = 0  # Timestamp to maintain order priority
    
    def update(self, msg: Message):
        self.timestamp += 1
        
        if msg.category == OrderType.Addition:
            order_dict = self.bids if msg.buy == BuySellType.Buy else self.asks
            order_dict[msg.OrderID] = (msg.price, msg.size, self.timestamp)
        
        elif msg.category == OrderType.Modification:
            order_dict = self.bids if msg.OrderID in self.bids else self.asks
            if msg.size == 0:
                if msg.OrderID in order_dict:
                    del order_dict[msg.OrderID]
            else:
                if msg.OrderID in order_dict:
                    price, _, timestamp = order_dict[msg.OrderID]
                    order_dict[msg.OrderID] = (price, msg.size, timestamp)
    
    def bid_price(self):
        if not self.bids:
            return None
        return max(self.bids.values(), key=lambda x: (x[0], -x[2]))[0]
    
    def ask_price(self):
        if not self.asks:
            return None
        return min(self.asks.values(), key=lambda x: (x[0], x[2]))[0]
    
    def bid_levels(self):
        levels = {}
        for price, size, _ in self.bids.values():
            levels[price] = levels.get(price, 0) + size
        return sorted(levels.items(), key=lambda x: -x[0])
    
    def ask_levels(self):
        levels = {}
        for price, size, _ in self.asks.values():
            levels[price] = levels.get(price, 0) + size
        return sorted(levels.items(), key=lambda x: x[0])
    
    def order_id_nth_order_price(self, order_id: int, n: int):
        price_orders = [oid for oid, (price, _, _) in self.bids.items() if price == self.bids.get(order_id, (None,))[0]]
        price_orders += [oid for oid, (price, _, _) in self.asks.items() if price == self.asks.get(order_id, (None,))[0]]
        price_orders.sort()
        return price_orders[n - 1] if 0 < n <= len(price_orders) else 0
    
    def size_of_order(self, order_id):
        if order_id in self.bids:
            return self.bids[order_id][1]
        if order_id in self.asks:
            return self.asks[order_id][1]
        return None

# Creating 10 instances of Message and running them in the book
book = Book()
messages = [
    Message(1, OrderType.Addition, BuySellType.Buy, 10, 100.0),
    Message(2, OrderType.Addition, BuySellType.Sell, 15, 101.0),
    Message(3, OrderType.Addition, BuySellType.Buy, 5, 99.5),
    Message(4, OrderType.Addition, BuySellType.Sell, 20, 102.0),
    Message(5, OrderType.Addition, BuySellType.Buy, 8, 100.0),
    Message(6, OrderType.Addition, BuySellType.Sell, 10, 101.0),
    Message(7, OrderType.Modification, BuySellType.Buy, 0, 100.0),
    Message(8, OrderType.Modification, BuySellType.Sell, 5, 101.0),
    Message(9, OrderType.Addition, BuySellType.Buy, 12, 99.5),
    Message(10, OrderType.Addition, BuySellType.Sell, 18, 102.5),
]

for msg in messages:
    book.update(msg)

print("Bid Price:", book.bid_price())
print("Ask Price:", book.ask_price())
print("Bid Levels:", book.bid_levels())
print("Ask Levels:", book.ask_levels())
print("Order ID nth Order Price (OrderID 1, nth 2):", book.order_id_nth_order_price(1, 2))
print("Size of Order (OrderID 3):", book.size_of_order(3))
        