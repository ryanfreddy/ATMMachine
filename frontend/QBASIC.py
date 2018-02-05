import sys
import os
from itertools import islice
import collections
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from frontend.session import Session
from frontend.test import Test

class QBASIC:

    # FUNCTION THAT LOGS IN USER

    log = []
    transactionSummaryCopy = []
    validAccountsCopy = []

    validAccountsPath = None
    tranactionSummaryPath = None

    def login(self, mode, validAccountsPath):
        if self.currentSession == None:
            input_var = mode

            readAccounts = True
            if self.validAccountsPath == None:
                self.validAccountsPath = validAccountsPath + "/validaccounts.txt"
                readAccounts = False

            if input_var == None:
                input_var = input("   Enter 'm' for machine mode and 'a' for agent mode: ")
            if input_var.lower() == "a":
                print("   You have started Agent mode")
                self.currentSession = Session(1, self.validAccountsPath, self.tranactionSummaryPath, readAccounts)
                self.log.append("agentModeSelected")
                self.log.append("loginSuccess")

            elif input_var.lower() == "m":
                print("   You have started machine mode")
                self.currentSession = Session(0, self.validAccountsPath, self.tranactionSummaryPath, readAccounts)
                self.log.append("machineModeSelected")
                self.log.append("loginSuccess")

            else:
                self.log.append("invalidModeSelection")
                self.log.append("loginFail")
                if mode == None:
                    self.login(None, None)

        else:
            self.log.append("loginFail")
            print("You have already logged in. You cannot log in again.\n")

    def logout(self, saveLocation, sessionNumber):
        if self.currentSession == None:
            self.log.append("logoutFail")
            print("   You are not logged in. You must be logged in to log out\n")
        else:
            self.log.append("logoutSuccess")
            print("   You are now logged out\n")
            self.currentSession.addToTransactionSummary("EOS", "0000000", "0", "0000000")
            if saveLocation == None:
                self.transactionSummaryCopy = self.currentSession.writeToTransactionFile(None, None)
            else:
                self.transactionSummaryCopy = self.currentSession.writeToTransactionFile(saveLocation, sessionNumber)
            self.currentSession = None



    # FUNCTION THAT LETS USER WITHDRAW FROM ACCOUNT

    def withdraw(self, accArg, amtArg):
        if self.currentSession == None:
            self.log.append("withdrawalFail")
            print("You are not logged in")
        else:
            account = accArg
            amount = amtArg
            if account == None and amount == None:
                account = input("   Account number: ")
                amount = input("   Amount (in cents): ")
            if len(account) != 7 or account.startswith('0') or not account.isdigit:
                print("   Error: Acct # must be 7 digits and cannot start with 0")
            if account in self.currentSession.validAccounts:
                self.currentSession.withdrawMoney(account, amount)
            else:
                print("   Error: This is account does not exist.")



    # FUNCTION THAT ALLOWS USER TO DEPOSIT MONEY

    def deposit(self, accArg, amtArg):
        if self.currentSession == None:
            self.log.append("depositFail")
            print("You are not logged in")
        else:
            account = accArg
            amount = amtArg
            if account == None and amount == None:
                account = input("   Account number: ")
            if len(account) != 7 or account.startswith('0') or not account.isdigit:
                print("   Error: Acct # must be 7 digits and cannot start with 0")
            if account in self.currentSession.validAccounts:
                amount = input("   Amount (in cents): ")
                self.currentSession.depositMoney(account, amount)
            else:
                print("   Error: This is account does not exist.")


    # FUCNTION THAT ALLOWS USER TO CREATE AN ACCOUNT

    def createacct(self, accountNumber, accountName):
        if self.currentSession != None:

            name = ""
            account = ""
            if accountNumber != None and accountName != None:
                account = accountNumber
                name = accountName
            else:
                account = input("   Enter account number: ")
                name = input("   Enter account name: ")

            if len(name) < 3 or len(name) > 30 or name[0] == " " or name[len(name)-1] == " ":
                self.log.append("createAccountFailure(InvalidAccountName)")
                print("   Create account failed")

            elif len(account) != 7 or account.startswith('0') or not account.isdigit():
                print("   Invalid account number")
                self.log.append("createAccountFailure(InvalidAccountNumber)")
            elif account in self.currentSession.validAccounts:
                print("   This account already exists")
                self.log.append("createAccountFailure(AccountAlreadyExists)")
            else:
                self.currentSession.createAccount(account,name)

                print("   Account created ")
        else:
            print("   You must be logged in to perform this action")



    # FUCNTION THAT ALLOWS USER TO CREATE AN ACCOUNT

    def deleteacct(self, accountNumber):

        if self.currentSession != None:

            account = ""
            if accountNumber != None:
                account = accountNumber
            else:
                account = input("   Enter account number: ")

            if len(account) != 7 or account.startswith('0') or not account.isdigit():
                print("   Invalid account number")
                self.log.append("deleteAccountFail(InvalidAccountNumber)")
            elif account in self.currentSession.validAccounts:
                print("   This account already exists")
                self.log.append("deleteAccountFailure(AccountAlreadyExists)")
            else:
                self.currentSession.deleteAccount(account)
                self.validAccountsCopy = self.currentSession.writeToValidAccounts()
                self.log.append("deleteAccountSuccess")
                print("   Account deleted ")
        else:
            print("   You must be logged in to perform this action")

    # FUCNTION THAT ALLOWS USER TO Transfer

    def transfer(self, toAccountNumber, fromAccountNumber, amount):

        if self.currentSession != None:

            toAccount = toAccountNumber
            fromAccount = fromAccountNumber
            transferAmount = amount

            if toAccountNumber == None:
                toAccount = input("   Account to transfer to: ")

            if fromAccountNumber == None:
                fromAccount = input("   Account to transfer from: ")

            if transferAmount == None:
                transferAmount = input("   Amount (in cents): ")

            if len(toAccount) != 7 or toAccount.startswith('0') or not toAccount.isdigit:
                print("     This is not a valid account number")
                self.log.append("transferFail(eitherAccountNumberNotValid)")
                return

            if len(fromAccount) != 7 or fromAccount.startswith('0') or not fromAccount.isdigit:
                print("     This is not a valid account number")
                self.log.append("transferFail(eitherAccountNumberNotValid)")
                return

            self.currentSession.transferMoney(toAccount, fromAccount, transferAmount)
        else:
            print("   Sorry you must be logged in to perform this action")
            self.log.append("transferFail(notLoggedIn)")

    # FUCNTION THAT ALLOWS USER TO QUIT THE QBASIC PROGRAM

    def quit(self):
        sys.exit()


    def test(self):
        test = Test()
        expectedInputTests = test.readExpectedInputFiles()
        test.readExpectedOutputFiles()
        testfile = open("testResults.txt","w")

        counter = 0
        for testName, commands in expectedInputTests.items():
            commandsLength = iter(range(len(commands)))
            for i in commandsLength:
                command = commands[i]
                if command == "login":
                    mode = commands[commands.index(command)+1]
                    self.consume(commandsLength, 1)
                    self.login(mode, None)
                elif command == "logout":
                    self.logout(None, None)
                elif command == "deposit":
                    accountNumber = commands[commands.index(command)+1]
                    amount = commands[commands.index(command)+2]
                    self.consume(commandsLength, 2)
                    self.deposit(accountNumber, amount)
                elif command == "withdraw":
                    accountNumber = commands[commands.index(command)+1]
                    amount = commands[commands.index(command)+2]
                    self.consume(commandsLength, 2)
                    self.withdraw(accountNumber, amount)
                elif command == "transfer":
                    toAccountNumber = commands[commands.index(command)+1]
                    fromAccountNumber = commands[commands.index(command)+2]
                    amount = commands[commands.index(command)+3]
                    self.consume(commandsLength, 3)
                    self.transfer(toAccountNumber, fromAccountNumber, amount)
                elif command == "createacct":
                    accountNumber = commands[commands.index(command)+1]
                    accountName = commands[commands.index(command)+2]
                    self.consume(commandsLength, 2)
                    self.createacct(accountNumber, accountName)
                elif command == "deleteacct":
                    accountNumber = commands[commands.index(command)+1]
                    self.consume(commandsLength, 1)
                    self.deleteacct(accountNumber)
                elif command == "backoffice":
                    self.runBackOffice()
                else:
                    print(command + " is not a valid command")
                    # Not a valid command
            if self.log == test.expectedLogFiles[counter]:
                print("Log passed")

                if self.transactionSummaryCopy == test.expectedTransactionFiles[counter]:
                    print("Transactions passed")
                    testfile.write(testName + ": Passed" + "\n")

                else:
                    testfile.write(testName + ": Failed (Transactions List File not correct)" + "\n")
            else:
                print("Log failed")
                print("Test Failed")
                print(self.log)

                testfile.write(testName + ": Failed (Log File not correct)" + "\n")

            counter += 1
            del self.log[:]


    def executeDailyScript(self, pathToDayFolder, commands, sessionNumber):

        counter = 0
        commandsLength = iter(range(len(commands)))
        for i in commandsLength:
            command = commands[i]
            if command == "login":
                mode = commands[commands.index(command) + 1]
                self.consume(commandsLength, 1)
                self.login(mode, pathToDayFolder)
            elif command == "logout":
                # here we need to pass in the location of the Day folder so that the transction summary file can be saved there
                self.logout(pathToDayFolder, sessionNumber)
            elif command == "deposit":
                accountNumber = commands[commands.index(command) + 1]
                amount = commands[commands.index(command) + 2]
                self.consume(commandsLength, 2)
                self.deposit(accountNumber, amount)
            elif command == "withdraw":
                accountNumber = commands[commands.index(command) + 1]
                amount = commands[commands.index(command) + 2]
                self.consume(commandsLength, 2)
                self.withdraw(accountNumber, amount)
            elif command == "transfer":
                toAccountNumber = commands[commands.index(command) + 1]
                fromAccountNumber = commands[commands.index(command) + 2]
                amount = commands[commands.index(command) + 3]
                self.consume(commandsLength, 3)
                self.transfer(toAccountNumber, fromAccountNumber, amount)
            elif command == "createacct":
                accountNumber = commands[commands.index(command) + 1]
                accountName = commands[commands.index(command) + 2]
                self.consume(commandsLength, 2)
                self.createacct(accountNumber, accountName)
            elif command == "deleteacct":
                accountNumber = commands[commands.index(command) + 1]
                self.consume(commandsLength, 1)
                self.deleteacct(accountNumber)
            elif command == "backoffice":
                self.runBackOffice()
            else:
                print(command + " is not a valid command")
                # Not a valid command




    def consume(self, iterator, n):
        if n is None:
            collections.deque(iterator, maxlen=0)
        else:
            next(islice(iterator, n, n), None)


    executedCommands = []   # Record of executed commands

    currentSession = None   # The current session that QBASIC is workin in

    # LOOKS FOR COMMAND AND CHECKS ITS VALIDITY

    def waitForCommand(self):
        input_var = input("qbasic ")
        self.executeCommand(input_var)
        self.waitForCommand()

    def executeCommand(self, command):
        if command == "login":
            self.login(None, None)
        elif command == "logout":
            self.logout(None, None)
        elif command == "deposit":
            self.deposit(None, None)
        elif command == "withdraw":
            self.withdraw(None, None)
        elif command == "transfer":
            self.transfer(None, None, None)
        elif command == "createacct":
            self.createacct(None, None)
        elif command == "deleteacct":
            self.deleteacct(None)
        elif command == "test":
            self.test()
        elif command == "quit":
            self.quit()
        else:
            print("   X This command is not recognised by qbasic X")

        self.waitForCommand()


    # STARTS THE TEXT ENTRY AND INITILIZES THE SYSTEM

    def initilizeQbasicTerminal(self, validAccounts, transPath):
        print("\n//////// WELCOME TO QBASIC TERMINAL ////////\n")
        self.validAccountsPath = validAccounts
        self.tranactionSummaryPath = transPath
        self.waitForCommand()
