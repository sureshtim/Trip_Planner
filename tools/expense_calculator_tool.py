from utils.expense_calculator import Calculator
from utils.currency_converter import CurrencyConverter
from typing import List, Dict
from langchain.tools import tool
import os
from dotenv import load_dotenv


class CalculatorTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.calculator = Calculator()
        self.currency_converter = CurrencyConverter(self.api_key)
        self.calculator_tool_list = self._setup_tools()

    def _format_currency_response(self, jpy_amount: float, label: str = "") -> str:
        """Format response with both JPY and USD amounts"""
        try:
            usd_amount = self.currency_converter.convert(jpy_amount, "JPY", "USD")
            return f"{label}¥{jpy_amount:,.0f} (${usd_amount:,.2f})"
        except Exception as e:
            # Fallback if conversion fails
            return f"{label}¥{jpy_amount:,.0f}"

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""

        @tool
        def estimate_total_hotel_cost(price_per_night: str, total_days: float) -> str:
            """Calculate total hotel cost with JPY and USD amounts"""
            try:
                price = float(price_per_night.replace("¥", "").replace(",", ""))
                total_jpy = self.calculator.multiply(price, total_days)
                return self._format_currency_response(total_jpy, "Total hotel cost: ")
            except ValueError:
                return f"Invalid price format: {price_per_night}"

        @tool
        def calculate_total_expense(costs: List[float]) -> str:
            """Calculate total expense of the trip with JPY and USD amounts"""
            total_jpy = self.calculator.calculate_total(*costs)
            return self._format_currency_response(total_jpy, "Total trip expense: ")

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> str:
            """Calculate daily expense budget with JPY and USD amounts"""
            daily_jpy = self.calculator.calculate_daily_budget(total_cost, days)
            return self._format_currency_response(daily_jpy, "Daily budget: ")

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget,
        ]
