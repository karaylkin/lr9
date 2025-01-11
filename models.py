class User:
    def __init__(self, username, password, cashback_level=0, spending=0):
        self.username = username
        self.password = password
        self.cashback_level = cashback_level
        self.spending = spending


class BonusLevel:
    def __init__(self, name, threshold, cashback_percent):
        self.name = name
        self.threshold = threshold
        self.cashback_percent = cashback_percent
