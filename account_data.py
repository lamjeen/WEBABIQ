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
    
    def get_today_date(self):
        """Get formatted current date"""
        return datetime.now().strftime("%B %d, %Y")
    
    def get_income(self):
        """Calculate total income"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Income')
    
    def get_paid(self):
        """Calculate total paid amount"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Paid')
    
    def get_total_saving(self):
        """Calculate total savings"""
        return self.get_income() - self.get_paid()