class PortfolioImpl:
    def __init__(self):
        self.__securities = {'Stock': list()}
        self.__tickets = []

        self.__size = 0

    def printSecurities(self):
        for storage_type, securities_list in self.__securities.items():
            print("Storage type:", storage_type)
            for security in securities_list:
                print(security, security.getQuantity())
            print()

    def checkTicket(self, ticket):
        if ticket in self.__tickets:
            return True
        else:
            return False
    def allSecuritiesByKey(self, key):
        return self.__securities[key]

    def __addNewSecurityStorage(self, security_type):
        if security_type not in self.__securities:
            self.__securities[security_type] = list()
        else:
            print("Security storage already exists.")

    def calculateSize(self):
        sum_size = 0
        for storage_type, securities_list in self.__securities.items():
            for security in securities_list:
                sum_size += security.getQuantity()
        print("Amount of securities:", sum_size)
        return sum_size

    def addSecurity(self, security):
        security_type = security.getType()
        if security_type not in self.__securities:
            print("There is no such storage in portfolio!")
            print("Creating. . .")
            self.__addNewSecurityStorage(security_type)

        if security_type in self.__securities:
            sec_copy = security
            self.__securities[security_type].append(sec_copy)

    def buySecurity(self, security, quantity):
        security_type = security.getType()
        if security_type not in self.__securities:
            print("There is no such storage in portfolio!")
            print("Creating. . . ")
            self.__addNewSecurityStorage(security_type)

        if security_type in self.__securities:
            sec_copy = security
            if sec_copy.getTicket() in self.__tickets:
                for asset in self.__securities[security_type]:
                    if sec_copy.getTicket() == asset.getTicket():
                        asset.changeQuantity(quantity)
                        self.printSecurities()
                        return
            else:
                sec_copy.changeQuantity(quantity)
                self.__tickets.append(sec_copy.getTicket())
                self.__securities[security_type].append(sec_copy)
                return

    def removeSecurity(self, security):
        type = security.getType()
        self.__securities[type].remove(security)

    def weighting(self):
        self.__size = self.calculateSize()
        weights = {}

        for key in self.__securities.keys():
            for asset in self.__securities[key]:
                weights[asset.getTicket()] = asset.getQuantity() / self.__size * 100
            print(self.__size)
        return weights

    def getStock(self, ticket, type):
        for asset in self.__securities[type]:
            if asset.getTicket() == ticket:
                return asset

    def price(self):
        overall_price = 0.0
        for securities_list in self.__securities.values():
            for security in securities_list:
                overall_price += security.getPrice() * security.getQuantity()
        return overall_price

    def sellSecurity(self, ticket, type, change):
        for asset in self.__securities[type]:
            if asset.getTicket() == ticket:
                if change > asset.getQuantity() or change == asset.getQuantity():
                    self.removeSecurity(asset)
                    self.__tickets.remove(ticket)
                    self.printSecurities()
                else:
                    asset.changeQuantity(-change)
                    self.printSecurities()

    def getSecurities(self):
        return self.__securities
