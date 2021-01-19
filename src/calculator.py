import pandas as pd
from decimal import Decimal, ROUND_HALF_EVEN


class FinancialCalculator:
    

    TWO_CENTS = (Decimal("0.00"), ROUND_HALF_EVEN)
    FOR_PLACES = Decimal("0.0000")

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
        self.current_age = current_age
        self.goal_age = goal_age
        self.goal_monthly_withdraw = Decimal(goal_monthly_withdraw)
        self.initial_patrimony = Decimal(initial_patrimony)
        self.monthly_contribution = Decimal(monthly_contribution)
        self.current_interest = Decimal().from_float(current_interest/100).quantize(self.FOR_PLACES, ROUND_HALF_EVEN)
        self.future_interest = Decimal().from_float(future_interest/100).quantize(self.FOR_PLACES, ROUND_HALF_EVEN)
        self.max_age = max_age

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
    def monthly_yield_current(self):
        return self._convert_to_monthly_yield(self.current_interest)

    @property
    def monthly_yield_goal(self):
        return self._convert_to_monthly_yield(self.future_interest)

    @property
    def consumable_patrimony_value(self):
        return self.goal_monthly_withdraw * ((1 + self.monthly_yield_goal)**self.consumption_months - 1)/((1 + self.monthly_yield_goal)**self.consumption_months * self.monthly_yield_goal)

    @property
    def profitable_patrimony_value(self):
        return (self.goal_monthly_withdraw/self.monthly_yield_goal).quantize(*self.TWO_CENTS)
    
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
            last_month_value = year_plus_interest
        return growth_history


    def create_yearly_growth_table(self):
        pass

    def create_patrimony_consume_table(self):
        pass
    
    def create_yield_consume_table(self):
        pass

    @staticmethod
    def _convert_to_monthly_yield(anual_profitability):
        FIVE_PLACES = Decimal("0.000000")
        value = Decimal((1 + anual_profitability)**Decimal(1/12) - 1)
        return value.quantize(FIVE_PLACES, ROUND_HALF_EVEN)
    
    @staticmethod
    def _to_percent(value):
        return Decimal(value/100)