from __future__ import annotations

from dataclasses import dataclass

from .models import Portfolio, Side, TokenFillResult, TokenOrder


@dataclass(slots=True)
class TokenMarket:
    ticker: str
    creator: str
    base_reserve: float
    quote_reserve: float

    @property
    def price(self) -> float:
        if self.base_reserve <= 0:
            return 0.0
        return self.quote_reserve / self.base_reserve


class TokenVenue:
    def __init__(self) -> None:
        self.markets: dict[str, TokenMarket] = {}

    def launch_token(self, ticker: str, creator: str, initial_supply: int, seed_price: float) -> tuple[bool, str]:
        if ticker in self.markets:
            return False, "launch rejected: ticker already exists"
        if initial_supply <= 0 or seed_price <= 0:
            return False, "launch rejected: invalid supply/price"

        self.markets[ticker] = TokenMarket(
            ticker=ticker,
            creator=creator,
            base_reserve=float(initial_supply),
            quote_reserve=float(initial_supply) * seed_price,
        )
        return True, "launch market created"

    def process_order(self, order: TokenOrder, portfolio: Portfolio) -> TokenFillResult:
        market = self.markets.get(order.ticker)
        if market is None:
            return TokenFillResult(False, "token market missing")

        if order.quantity <= 0 or order.side is Side.HOLD:
            return TokenFillResult(True, "hold", 0.0, 0.0, market.price)

        k = market.base_reserve * market.quote_reserve
        if k <= 0:
            return TokenFillResult(False, "invalid market reserves")

        if order.side is Side.BUY:
            spend_quote = min(portfolio.cash, order.quantity * market.price)
            if spend_quote <= 0:
                return TokenFillResult(False, "buy rejected: no cash")
            new_quote = market.quote_reserve + spend_quote
            new_base = k / new_quote
            base_out = max(0.0, market.base_reserve - new_base)
            if base_out <= 0:
                return TokenFillResult(False, "buy rejected: no output")

            market.quote_reserve = new_quote
            market.base_reserve = new_base
            portfolio.cash -= spend_quote
            portfolio.token_inventory[order.ticker] = portfolio.token_inventory.get(order.ticker, 0.0) + base_out
            exec_price = spend_quote / base_out if base_out else market.price
            return TokenFillResult(True, "buy executed", base_out, -spend_quote, exec_price)

        # SELL path
        inventory = portfolio.token_inventory.get(order.ticker, 0.0)
        sell_qty = min(order.quantity, inventory)
        if sell_qty <= 0:
            return TokenFillResult(False, "sell rejected: no inventory")

        new_base = market.base_reserve + sell_qty
        new_quote = k / new_base
        quote_out = max(0.0, market.quote_reserve - new_quote)
        if quote_out <= 0:
            return TokenFillResult(False, "sell rejected: no output")

        market.base_reserve = new_base
        market.quote_reserve = new_quote
        portfolio.cash += quote_out
        portfolio.token_inventory[order.ticker] = inventory - sell_qty
        exec_price = quote_out / sell_qty if sell_qty else market.price
        return TokenFillResult(True, "sell executed", -sell_qty, quote_out, exec_price)

    def mark_to_market_value(self, portfolio: Portfolio) -> float:
        value = 0.0
        for ticker, qty in portfolio.token_inventory.items():
            market = self.markets.get(ticker)
            if market is None:
                continue
            value += qty * market.price
        return value
