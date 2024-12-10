import json
from tabulate import tabulate
from datetime import datetime

class Expense_track:
    def __init__(self,date,category,description,amount):
        self.date=date
        self.category=category
        self.description=description
        self.amount=amount
    def add_expense(self,amount):
        self.amount-=amount
        return self.amount
    def add_income(self,inc):
        self.amount+=inc
        return self.amount

    def get_data(self):
        return [self.date, self.category, self.description, self.amount]

    def to_dict(self):
        return {

            "date": self.date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount
        }
    @classmethod
    def from_dict(cls,data):
        return cls(data['date'],data['category'],data['description'],data['amount'])

def validate_date(date_str):
    try:
        return datetime.strptime(date_str,'%d-%m-%y')
    except ValueError:
        print("Please enter a valid date with DD-MM-YY format")
        return None
def validate_amount(amount_string):
    try:
        amount=float(amount_string)
        if amount<=0:
            print("Amount must be positive")
            return None
        return amount
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return None



def get_user_input():
    while True:
        date = input("Enter the Date (DD-MM-YY) :")
        valid_date = validate_date(date)
        if valid_date:
            break

    category=input("Enter Expense Category :")
    description=input("Enter Description :")
    while True:
        amount = input("Enter Amount: ")
        valid_amount=validate_amount(amount)
        if valid_amount is not None:
            break
    return Expense_track(valid_date.strftime('%d-%m-%y'), category, description, valid_amount)

def save_expense(expenses, filename='expenses.json'):
    with open(filename, 'w') as file:
        json.dump([expense.to_dict() for expense in expenses], file)
        print("Expenses saved successfully")

def load_expense(filename='expenses.json'):
    try:
        with open(filename, 'r') as file:
            expense_data = json.load(file)
            return [Expense_track.from_dict(data) for data in expense_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


expenses = load_expense()
loop="yes"
while(loop.lower()=="yes"):
    option = input(
        "Enter the option (1.Add_expense, 2.View, 3.Analyse, 4.Filter_category, 5.Filter_date): ")
    if option == "1":
        expense = get_user_input()
        expenses.append(expense)
        ch=input("If you want to save this entry, please type YES: ").lower()
        if ch=='yes':
            save_expense(expenses)
        else:
            print("This entry is not saved")

        loop=input("if you want to continue, please type YES, \notherwise type anything to exit:").lower()

    elif option == "2":
        heading = ['Date', 'Category', 'Description', 'Amount']
        data = [expense.get_data() for expense in expenses]
        view = tabulate(data, headers=heading, tablefmt="grid")
        print(view)
        loop=input("if you want to continue, please type YES, \notherwise type anything to exit:").lower()
    elif option == "3":
        total_expense = sum(expense.amount for expense in expenses)
        avg_expense = total_expense / len(expenses) if expenses else 0

        print(f'Total expense : {total_expense}')
        print(f'Average expense : {avg_expense}')

        highest_exp = max(expenses, key=lambda expense: expense.amount)
        lowest_exp = min(expenses, key=lambda expense: expense.amount)

        print(f'Highest expense is : {highest_exp.amount} for {highest_exp.description} on {highest_exp.date}')
        print(f'Lowest expense is : {lowest_exp.amount} for {lowest_exp.description} on {lowest_exp.date}')
        loop=input("if you want to continue, please type YES, \notherwise type anything to exit:").lower()
    elif option == "4":
        cat=input("Enter category to filter : ").lower()
        category_filter = cat
        filter_by_cat = [expense for expense in expenses if expense.category == category_filter]
        filtered_data = [expense.get_data() for expense in filter_by_cat]
        print(f'Expenses with category {category_filter} :')
        print(tabulate(filtered_data, headers=heading, tablefmt="grid"))
        loop=input("if you want to continue, please type YES, \notherwise type anything to exit:").lower()
    elif option == "5":
        while True:
            dt_fil = input("Enter the date to filter : ").strip()
            valid_date=validate_date(dt_fil)
            if valid_date:
                date_filter = valid_date.strftime('%d-%m-%y')
                filter_by_date = [expense for expense in expenses if expense.date == date_filter]
                dt_filtered_data = [expense.get_data() for expense in filter_by_date]
                print(f'Expenses on {date_filter} :')
                print(tabulate(dt_filtered_data, headers=heading, tablefmt="grid"))
                break
            else:
                print('\n')
        loop = input("If you want to continue, please type YES, \notherwise type anything to exit: ").lower()
    else:
        print("Invalid entry, Please enter a valid option number")
        loop=input("if you want to continue, please type YES, \notherwise type anything to exit:").lower()

























