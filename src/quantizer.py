from decimal import Decimal

class QuantizeCtx:
    """ For decimal values only.
    Create a context for decimal's quantize(decimal_places and rounding) and apply it with 'apply' method"""
    
    def __init__(self, decimal_places, rounding):
        self.decimal_places = decimal_places
        self.rounding = rounding
    
    def apply(self, value):
        """Apply the Decimal's quantize method to a value with the given initial params"""
        
        return value.quantize(Decimal(self.decimal_places), self.rounding)
