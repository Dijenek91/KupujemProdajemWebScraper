"""
Represents a infromation touple for a car.
Example:
    Column Name: Price
    Data field: 1000 E
"""

class CarDataItem:
    def __init__(self, column_name, data_field):
        self.column_name = column_name
        self.data_field = data_field