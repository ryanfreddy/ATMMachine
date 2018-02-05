

class Session:

    # INITIALIZATION FUNCTION: Creates a session and defines whether your in machine or agen mode

    def __init__(self, operationMode, validAccountsPath, validTransPath, readAccounts):

        self.operationMode = operationMode  # Operation Mode is 1 for Agent and 0 for Machine
        self.transPath = validTransPath
        self.accountPath = validAccountsPath
        self.transactionSummary=[]
        self.readAccounts = readAccounts

        self.readValidAccounts()            # Read and store the valid accounts in the session for later use


    # PUBLIC CLASS VARIABLES: Store information that multiple methods use

    validAccounts = []          # Dictionary of valid accounts and account names
    transactionSummary = []     # Transaction summary file
    operationMode = None        # Mode of operation, defined from the __init__ method

    accountPath = None
    transPath = None
    readAccounts = True

    withdrawalLimit = 1000



    # CLASS METHODS: Functions that perform actions, or manipulate session data


    def readValidAccounts(self):
        if self.readAccounts == True:
            with open(self.accountPath, 'r') as in_file:
                for line in in_file:                           # Reads .txt file with valid accounts and stores them
                    line = line.replace("\n", "")
                    self.validAccounts.append(line)


    def createAccount(self, accountNumber, accountName):
        self.addToTransactionSummary("NEW", accountNumber, accountName, " ")


    def deleteAccount(self, accountNumber):
        self.addToTransactionSummary("DEL", accountNumber, " ", " ")


    def writeToValidAccounts(self):
        #file = open(self.accountPath,"w")
        #for accountNumber in self.validAccounts:                 # Function that actually manuipulates the .txt
        #file.write(account + "\n")
        #file.close()
        return self.validAccounts

    def writeToTransactionFile(self, saveLocation, sessionNumber):
        if saveLocation == None:
            file = open(self.transPath,"w")
            for transaction in self.transactionSummary:                 # Function that actually manuipulates the .txt
                file.write(transaction + "\n")
            file.close()
            return self.transactionSummary
        else:
            fileName = "/transactionsummary" + str(sessionNumber) + ".txt"
            file = open(saveLocation + fileName,"w")
            for transaction in self.transactionSummary:                 # Function that actually manuipulates the .txt
                file.write(transaction + "\n")
            file.close()
            return self.transactionSummary



    def depositMoney(self, account, amountInCents):
        amount = int(amountInCents) / 100
        if self.operationMode == 1:
            if amount > 999999.99:
                print("   Cannot deposit more than $999,999.99")
            else:
                self.addToTransactionSummary("DEP", account, amount, None)

            print("   Money has been successfully deposited")
        else:
            if amount > 1000:
                print("   Cannot deposit more than $1,000")
            else:
                self.addToTransactionSummary("DEP", account, amount, None)

            print("   Money has been successfully deposited")


    def withdrawMoney(self, account, amountInCents):
        amount = int(amountInCents) / 100
        if self.operationMode == 1:
            if amount > 999999.99:
                print("   Cannot withdraw more than $999,999.99")
            else:
                self.addToTransactionSummary("WDR", account, amount, None)

            print("   Money has been successfully withdrawn")
        else:
            if amount > 1000:
                print("   Cannot withdraw more than $1,000")
            else:
                if self.withdrawalLimit > 0:
                    self.addToTransactionSummary("WDR", account, amount, None)
                    self.withdrawalLimit = self.withdrawalLimit-amount

                    print("   Money has been successfully withdrawn")
                else:
                    print("   Session withdrawal limit has been reached")


    def transferMoney(self, toAccountNumber, fromAccountNumber, amountInCents):
        amount = int(amountInCents) / 100
        if self.operationMode == 1: # In Agent mode
            if amount > 999999.99:
                print("   Sorry you cannot transfer more than $999,999.99")
                return "transferFail(exceededMaxTransferAgentMode)"
            else:
                self.addToTransactionSummary("XFR", toAccountNumber, amount, fromAccountNumber)
                return "transferSuccess"
        else:
            if amount > 1000.00:
                print("   Sorry you cannot transfer more than $1000 at this time.")
                return "transferFail(exceededMaxTransferMachineMode)"
            else:
                self.addToTransactionSummary("XFR", toAccountNumber, amount, fromAccountNumber)
                return "transferSuccess"




    def addToTransactionSummary(self, transactionType, toAccount, amount, fromAccount):
        logLine = ""
        if transactionType == "XFR":
            logLine = transactionType + " " + toAccount + " " + str(amount) + " " + fromAccount + " ***"
        elif transactionType == "DEP" or transactionType == "WDR":
            logLine = transactionType + " " + toAccount + " " + str(amount) + " 0000000 ***"
        elif transactionType == "NEW":
            logLine = transactionType + " " + toAccount + " 0 0000000 " + amount #amount variable used as account name
        elif transactionType == "DEL":
            logLine = transactionType + " " + toAccount + " 0 0000000 ***"
        elif transactionType == "EOS":
            logLine = transactionType + " " + toAccount + " 0 0000000 ***"
        self.transactionSummary.append(logLine)
