"""Module for managing account data and calculations"""
from datetime import datetime

class AccountData:
    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, amount: float, category: str):
        """Add a new transaction"""
        self.transactions.append({
            'amount': amount,
            'category': category,
            'date': datetime.now()
        })
    
    @property
    def today_date(self):
        """Get formatted current date"""
        return datetime.now().strftime("%B %d, %Y")
    
    @property
    def income(self):
        """Calculate total income"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Income')
    
    @property
    def paid(self):
        """Calculate total paid amount"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Paid')
    
    @property
    def total_saving(self):
        """Calculate total savings"""
        return self.income - self.paid