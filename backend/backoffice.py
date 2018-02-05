

class BackOffice:

    log = []
    transactions = []
    masterAccountsFile = {}
    validAccounts = []

    newValidAccountsFile = ""
    newMasterAccountsFile = ""

    expectedTestLogPath = ""

    def __init__(self, oldMasterAccountsFileName, mergedTransactionSummaryFileName,
                validAccountsFileName, newMasterAccountsFile, newValidAccountsFile):
        self.clearVariables()
        self.readTransactionSummaryFile(mergedTransactionSummaryFileName)
        self.readMasterAccountsFile(oldMasterAccountsFileName)
        if validAccountsFileName != "":
            self.readValidAccountsFile(validAccountsFileName)
        self.newValidAccountsFile = newValidAccountsFile
        self.newMasterAccountsFile = newMasterAccountsFile

    def readTransactionSummaryFile(self, fileName):
        with open(fileName, 'r') as outFile:
            for line in outFile:
                items = []
                for item in line.split():
                    items.append(item)
                self.transactions.append(items)
            outFile.close()

    def readMasterAccountsFile(self, fileName):
        with open(fileName, 'r') as outFile:
            for line in outFile:
                items = []
                accountNumber = line.split()[0]
                for item in line.split():
                    if item != accountNumber:
                        items.append(item)
                self.masterAccountsFile[accountNumber] = items
            outFile.close()

    def readValidAccountsFile(self, fileName):
        with open(fileName, 'r') as outFile:
            for line in outFile:
                self.validAccounts.append(line)
            outFile.close()

    # processes the withdraw from a users account
    def withdraw(self, account, amount):
        currentBalance = float(self.masterAccountsFile[account][0])
        if amount > 0:      # confirms that the amount your withdrawing is not negative
            newBalance = currentBalance-amount
            if newBalance >= 0:     # checks that the new ballance of the account is not negative
                self.masterAccountsFile[account][0] = newBalance
                self.addToLog("withdrawalSuccess")
            else:
                self.addToLog("withdrawalFail(balanceLowerThanZero)")
        else:
            self.addToLog("withdrawalFail(amountLowerThanZero)")

    def deposit(self, account, amount):
        currentBalance = float(self.masterAccountsFile[account][0])
        if amount > 0:
            newBalance = currentBalance+amount
            if newBalance >= 0:
                self.masterAccountsFile[account][0] = newBalance
                self.addToLog("depositSuccess")
            else:
                self.addToLog("depositFail(balanceLowerThanZero)")
        else:
            self.addToLog("depositFail(amountLowerThanZero)")

    def transfer(self, toAccount, fromAccount, amount):
        currentBalance = float(self.masterAccountsFile[toAccount][0])
        currentFromBalance  = float(self.masterAccountsFile[fromAccount][0])
        newFromBalance = currentFromBalance-amount
        newToBalance = currentBalance+amount
        self.masterAccountsFile[toAccount][0] = newBalance
        self.masterAccountsFile[fromAccount][0] = newFromBalance

    def createAccount(self, account, accountName):
        if (account not in self.validAccounts) and (account not in self.masterAccountsFile.keys()):
            self.validAccounts.insert(0, account + '\n')
            self.masterAccountsFile[account] = [0, accountName]     # if statement checks to see if the account is valid
            self.addToLog("creationSuccess")
        else:
            self.addToLog("creationFailed(accountExists)") # if it already exists then the creation fails

    def deleteAccount(self, account, accountName):
        balance = self.masterAccountsFile[account][0]
        if balance == 0:
            if account in mylist and account in self.masterAccountsFile.keys():
                index = self.validAccounts.index(account)
                self.validAccounts.pop(index)
                del self.masterAccountsFile[account]
            else:
                self.addToLog("Account does not exist")
        else:
            self.addToLog("The balance of the account is not 0")

    def writeToNewMasterAccountsFile(self):
        with open(self.newMasterAccountsFile, 'w') as outFile:
            for accountNumber, array in self.masterAccountsFile.items():
                outFile.write(str(accountNumber) + ' ' + str(array[0]) + ' ' + array[1] + '\n')

    def writeToNewValidAccountsFile(self):
        with open(self.newValidAccountsFile, 'w') as outFile:
            for accountNumber in self.validAccounts:
                outFile.write(str(accountNumber))

    def addToLog(self, log):
        self.log.append(log)

    def clearVariables(self):
        self.log = []
        self.transactions = []
        self.validAccounts = []
        self.masterAccountsFile = {}


    # function that checks if a test met or did not meet the requirements
    def validateTests(self):
        with open(self.expectedTestLogPath, 'r') as outFile:
            expectedLog = []
            for line in outFile:
                line = line.replace('\n', '')
                expectedLog.append(line)
            outFile.close()

            if expectedLog == self.log:     # compares the local log to the test's expected output log.
                return "Passed"
            else:
                return "Failed"

    def applyTransactions(self):
        for transaction in self.transactions:   # executes each of the transactions in the input

            transactionCode = transaction[0]
            toAccount = transaction[1]
            amount = float(transaction[2])
            fromAccount = transaction[3]
            accountName = transaction[4]

            if transactionCode == "DEP":        # determines what the transaction is and executes the method
                self.deposit(toAccount, amount)
            elif transactionCode == "WDR":
                self.withdraw(toAccount, amount)
            elif transactionCode == "XFR":
                self.transfer(toAccount, fromAccount, amount)
            elif transactionCode == "NEW":
                self.createAccount(toAccount, accountName)
            elif transactionCode == "DEL":
                self.deleteAccount(toAccount, accountName)
            elif transactionCode == "EOS":
                self.writeToNewValidAccountsFile()
                self.writeToNewMasterAccountsFile()
            else:
                break

        if self.expectedTestLogPath != "":      # after all trasactions in a test are done, we check the validity
            return self.validateTests()
