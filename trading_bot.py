from binance.client import Client
from binance.exceptions import BinanceAPIException
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import sys
from typing import Optional, Tuple

from config import settings
from logger import logger

class TradingBot:
    def __init__(self):
        self.client = Client(
            settings.BINANCE_API_KEY,
            settings.BINANCE_API_SECRET,
            testnet=settings.TESTNET
        )
        self.console = Console()
        
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if the trading symbol exists."""
        try:
            self.client.futures_exchange_info()
            return True
        except BinanceAPIException as e:
            logger.error(f"Invalid symbol {symbol}: {str(e)}")
            return False
            
    def validate_quantity(self, quantity: float) -> bool:
        """Validate if the quantity is valid."""
        return quantity > 0
        
    def validate_price(self, price: float) -> bool:
        """Validate if the price is valid."""
        return price > 0
        
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Optional[dict]:
        """Place a market order."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            logger.info(f"Market order placed: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error placing market order: {str(e)}")
            return None
            
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Optional[dict]:
        """Place a limit order."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logger.info(f"Limit order placed: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error placing limit order: {str(e)}")
            return None
            
    def get_order_status(self, symbol: str, order_id: int) -> Optional[dict]:
        """Get the status of an order."""
        try:
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            logger.info(f"Order status: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error getting order status: {str(e)}")
            return None
            
    def display_order(self, order: dict):
        """Display order details in a table."""
        table = Table(title="Order Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in order.items():
            table.add_row(str(key), str(value))
            
        self.console.print(table)
        
    def parse_command(self, command: str) -> Tuple[str, list]:
        """Parse the command line input."""
        parts = command.strip().split()
        if not parts:
            return "", []
        return parts[0].lower(), parts[1:]
        
    def run(self):
        """Run the trading bot."""
        self.console.print("[bold green]Welcome to the Trading Bot![/bold green]")
        self.console.print("Type 'help' for available commands or 'exit' to quit.")
        
        while True:
            try:
                command, args = self.parse_command(Prompt.ask("\nEnter command"))
                
                if command == "exit":
                    break
                elif command == "help":
                    self.console.print("""
Available commands:
- market <symbol> <side> <quantity>
- limit <symbol> <side> <quantity> <price>
- status <symbol> <order_id>
- help
- exit
                    """)
                elif command == "market":
                    if len(args) != 3:
                        self.console.print("[red]Invalid arguments. Usage: market <symbol> <side> <quantity>[/red]")
                        continue
                        
                    symbol, side, quantity = args
                    if not self.validate_symbol(symbol):
                        continue
                    if not self.validate_quantity(float(quantity)):
                        self.console.print("[red]Invalid quantity[/red]")
                        continue
                        
                    order = self.place_market_order(symbol, side, float(quantity))
                    if order:
                        self.display_order(order)
                        
                elif command == "limit":
                    if len(args) != 4:
                        self.console.print("[red]Invalid arguments. Usage: limit <symbol> <side> <quantity> <price>[/red]")
                        continue
                        
                    symbol, side, quantity, price = args
                    if not self.validate_symbol(symbol):
                        continue
                    if not self.validate_quantity(float(quantity)):
                        self.console.print("[red]Invalid quantity[/red]")
                        continue
                    if not self.validate_price(float(price)):
                        self.console.print("[red]Invalid price[/red]")
                        continue
                        
                    order = self.place_limit_order(symbol, side, float(quantity), float(price))
                    if order:
                        self.display_order(order)
                        
                elif command == "status":
                    if len(args) != 2:
                        self.console.print("[red]Invalid arguments. Usage: status <symbol> <order_id>[/red]")
                        continue
                        
                    symbol, order_id = args
                    if not self.validate_symbol(symbol):
                        continue
                        
                    order = self.get_order_status(symbol, int(order_id))
                    if order:
                        self.display_order(order)
                        
                else:
                    self.console.print("[red]Unknown command. Type 'help' for available commands.[/red]")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                
        self.console.print("[bold green]Thank you for using the Trading Bot![/bold green]")

if __name__ == "__main__":
    try:
        bot = TradingBot()
        bot.run()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1) 