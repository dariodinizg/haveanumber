import pandas as pd
from decimal import Decimal, ROUND_05UP, ROUND_CEILING, ROUND_DOWN, ROUND_FLOOR, ROUND_HALF_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_UP

from .quantizer import QuantizeCtx

class FinancialCalculator:
    
    to_7places = QuantizeCtx(Decimal("0.0000000"), ROUND_HALF_DOWN).apply
    to_2places = QuantizeCtx(Decimal("0.00"), ROUND_HALF_EVEN).apply
    # TWO_CENTS = (Decimal("0.00"), ROUND_UP)
    # FOR_PLACES = Decimal("0.0000")

    def __init__(
            self, 
            current_age, 
            goal_age, 
            goal_monthly_withdraw, 
            initial_patrimony, 
            monthly_contribution, 
            current_interest, 
            future_interest, 
            max_age
        ):
        self.current_age = int(current_age)
        self.goal_age = int(goal_age)
        self.goal_monthly_withdraw = Decimal(f"{goal_monthly_withdraw}")
        self.initial_patrimony = Decimal(f"{initial_patrimony}")
        self.monthly_contribution = Decimal(f"{monthly_contribution}")
        self.input_current_interest = current_interest
        self.input_future_interest = future_interest
        self.max_age = int(max_age)

    
    @property
    def decimal_current_yield(self):
        return self._to_percent(self._to_decimal(self.input_current_interest))
    
    @property
    def decimal_future_yield(self):
        return self._to_percent((self._to_decimal(self.input_future_interest)))

    @property
    def monthly_yield_current(self):
        return self._convert_to_monthly_interest(self.decimal_current_yield)

    @property
    def monthly_yield_goal(self):
        return self._convert_to_monthly_interest(self.decimal_future_yield)
   
    @property
    def contribution_years(self):
        return self.goal_age - self.current_age

    @property
    def contribution_months(self):
        return self.contribution_years * 12

    @property
    def consumption_months(self):
        return (self.max_age - self.goal_age) * 12
    
    @property
    def consumable_patrimony_value(self):
        return self.present_value(self.goal_monthly_withdraw, self.monthly_yield_goal, self.consumption_months)

    @property
    def infinity_patrimony_value(self):
        return self.to_2places((self.goal_monthly_withdraw/self.monthly_yield_goal))
    
    def create_monthly_growth_history(self):
        last_month_value = self.initial_patrimony
        growth_history = [last_month_value]
        for i in range(0, self.contribution_months + 1):
            month_plus_interest = (last_month_value * (1 + self.monthly_yield_current)) + self.monthly_contribution
            month_plus_interest.quantize(*self.TWO_CENTS)
            growth_history.append(month_plus_interest)
            last_month_value = month_plus_interest
        return growth_history

    def create_anual_growth_history(self):
        last_year_value = self.initial_patrimony
        growth_history = [last_year_value]
        for i in range(0, self.contribution_years + 1):
            year_plus_interest = (last_year_value * (1 + self.current_interest)) + (self.monthly_contribution * 12)
            year_plus_interest.quantize(*self.TWO_CENTS)
            growth_history.append(year_plus_interest)
            # last_month_value = year_plus_interest
        return growth_history

    def create_consumable_history(self):
        last_month = self.consumable_patrimony_value
        history = [last_month]
        for month in range(self.consumption_months):
            current_month = last_month * (Decimal())
            pass
        
    def create_patrimony_consume_table(self):
        pass
    
    def create_yield_consume_table(self):
        pass

    @staticmethod
    def present_value(payment, interest, period, is_postecipate = True):
        """payment * (((1 + interest)**period) - 1)/(((1 + interest)**(period-1)) * interest)"""

        interest = Decimal(str(interest))
        period = Decimal(str(period))
        payment = Decimal(str(payment))
        dividend_a = Decimal("1") + interest
        dividend_b = (dividend_a ** period).quantize(Decimal("0.00000000"), ROUND_FLOOR)
        dividend_total = dividend_b - Decimal("1")
        
        if is_postecipate:
            divisor_total = (dividend_b * interest).quantize(Decimal("0.0000000000"), ROUND_FLOOR)
        else:
            divisor_a = (dividend_a ** (period - Decimal("1")))
            divisor_total = (divisor_a * interest)

        division_result = (dividend_total / divisor_total).quantize(Decimal("0.00000"), ROUND_FLOOR)
        result = payment * division_result

        return result.quantize(Decimal("0.00"))

    @staticmethod
    def payment_value(future_value, interest, period):
        if type(interest) == float:
            interest = Decimal.from_float(interest)
        result = Decimal(future_value) * ( interest / ((1 + interest)**period - 1))
        return result.quantize(Decimal("0.00"))

    @staticmethod
    def future_value(monthly_contribution, interest, period):
        return monthly_contribution*(((1 + interest)**period) - 1)/interest 
    
    def _convert_to_monthly_interest(self,anual_interest):
        result = ((Decimal("1") + anual_interest)**(Decimal("1")/Decimal("12"))) - 1
        return self.to_7places(result)
    
    def _to_decimal(self,value):
        value = str(value)
        if ',' in value:
            value = value.replace(',', '.')
        return self.to_7places(Decimal(value))

    @staticmethod
    def _to_percent(value):
        return Decimal(value/Decimal("100"))