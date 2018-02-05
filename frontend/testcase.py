

class TestCase:

    name = ""
    validAccountsFile = []
    transactionSummaryFile = []
    log = []
    commands = []

    def __init__(self, name, validAccountsFile, transactionSummaryFile, commands):
        self.name = name
        self.validAccountsFile = validAccountsFile
        self.transactionSummaryFile = transactionSummaryFile

    def __init__(self, name, validAccountsFile, transactionSummaryFile, log):
        self.name = name
        self.validAccountsFile = validAccountsFile
        self.transactionSummaryFile = transactionSummaryFile
