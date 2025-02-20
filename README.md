A price-time trading book is a data structure that contains all of the current bid and ask prices for a given asset. 
The bid prices should be ordered from biggest to lowest and the ask prices from lowest to biggest. 
If two orders have the same price, then the order made first should have priority.

Each order contains the following fields:

order ID
price
size
bid_or_ask
category

There are two categories of an order: Addition or Modification. An addition is when we add a new order, and a modification is when we modify a preexisting order. A modification can only change the size of a previous order,
it cannot change the price or the bid_or_ask field. Finally, when a modification with size = 0 appears, this is equivalent to erasing a previous order from the book. 
