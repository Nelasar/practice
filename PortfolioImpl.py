class PortfolioImpl:
    def __init__(self):
        self.securities = {"Stock": list()}
        # self.securities["Stock"] = list()

    def printSecurities(self):
        for storage_type, securities_list in self.securities.items():
            print("Storage type:", storage_type)
            for security in securities_list:
                print(security)
            print()

    def addNewSecurityStorage(self, security_type):
        if security_type not in self.securities:
            self.securities[security_type] = list()
        else:
            print("Security storage already exists.")

    def size(self):
        sum_size = 0
        for storage_type, securities_list in self.securities.items():
            for security in securities_list:
                sum_size += security.getQuantity()
        print("Amount of securities:", sum_size)
        return sum_size

    def addSecurity(self, security):
        security_type = security.getType()
        if security_type in self.securities:
            self.securities[security_type].append(security)
        else:
            print("There is no such storage in portfolio!")

    def removeSecurity(self, security):
        self.securities['Stock'].remove(security)

    def weighting(self):
        size = self.size()
        weights = {}

        for asset in self.securities['Stock']:
            weights[asset.getTicket()] = asset.getQuantity() / size * 100
        print(size)
        return weights

    def getStock(self, ticket):
        for asset in self.securities['Stock']:
            if asset.getTicket() == ticket:
                return asset

    def price(self):
        overall_price = 0.0
        for securities_list in self.securities.values():
            for security in securities_list:
                overall_price += security.getPrice() * security.getQuantity()
        print("Overall price:", overall_price)
        return overall_price

    def getSecurities(self):
        return self.securities

    #@staticmethod
    #def new_instance():
    #    return PortfolioImpl()