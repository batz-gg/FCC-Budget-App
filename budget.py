class Category:
  def __init__(self, category):
    self.name = category
    self.ledger = []

  def __str__(self):
    display = []
    display.append(self.name.center(30, "*")) # Title
    for item in self.ledger:
      description = item["description"][:23].ljust(23)
      amount = item["amount"]
      display.append(description + f"{amount:.2f}".rjust(7))
    display.append(f"Total: {self.get_balance():.2f}")
    return "\n".join(display)

  def deposit(self, amount, description=""):
    deposit = {"amount": amount, "description": description}
    self.ledger.append(deposit)
    return deposit

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      withdraw = {"amount": amount * - 1, "description": description}
      self.ledger.append(withdraw)
      return True
    else:
      return False

  def get_balance(self):
    balance = 0
    for item in self.ledger:
      balance += item["amount"]
    return balance

  def transfer(self, amount, destination_category):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {destination_category.name}")
      destination_category.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False

  def check_funds(self, amount):
    funds = 0
    for item in self.ledger:
      funds += item["amount"]
    return False if amount > funds else True


def create_spend_chart(categories_list):
  total_spend = 0
  categories_spend = []

  # -The percentage spent should be calculated only with withdrawals and not with deposits.
  # this for loop calculates each category spend and total spend.
  for category in categories_list:
    spent = 0
    for item in category.ledger:
      if item["amount"] < 0 and "Transfer" not in item["description"]:
        spent += item["amount"]
    total_spend += spent
    categories_spend.append({"name": category.name, "spent": spent})
  
  # -The height of each bar should be rounded down to the nearest 10.
  # this for loop calculates each category spend percentage and rounded it down to the nearest 10.
  for category in categories_spend:
    percentage = (category["spent"] * 100) / total_spend
    category["percentage"] = int(percentage - (percentage % 10))

  # -There should be a title at the top that says "Percentage spent by category".
  display_rows = []
  display_rows.append("Percentage spent by category")

  # -Down the left side of the chart should be labels 0 - 100.
  # -The "bars" in the bar chart should be made out of the "o" character. 
  for percent in range(100, -1 ,-10):
    row = str(percent).rjust(3) + "|"
    for category in categories_spend:
      if category["percentage"] >= percent:
        row += "o".center(3)
      else:
        row += " " * 3
    row += " "
    display_rows.append(row)
  
  # -The horizontal line below the bars should go two spaces past the final bar.
  display_rows.append((" ".rjust(4)) + "---" * len(categories_spend) + "-")
  
  # -Each category name should be vertacally below the bar.
  tags_length = max([len(category["name"]) for category in categories_spend])
  for i in range(tags_length):
    row = " " * 4
    for category in categories_spend:
      if i < len(category["name"]):
        row += category["name"][i].center(3)
      else:
        row += " " * 3
    row += " "
    display_rows.append(row)

  # join the rows and return the value as a string
  display = "\n".join(display_rows)
  return display