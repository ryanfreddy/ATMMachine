import os
import time

class Test:

    testDirectory = "test_inputs_expected"

    expectedInputTests = {}
    expectedLogFiles = []
    expectedTransactionFiles = []
    expectedValidAccountsLists = []

    outputTests = {}
    testResults = {}

    # This functions reads the expected input files

    def readExpectedInputFiles(self):
        for subdir, dirs, files in os.walk(self.testDirectory):
            for file in files:
                commands = []
                if file == "expectedInputs.txt":
                    with open(os.path.join(subdir, file), 'r') as in_file:
                        for line in in_file:
                            line = line.replace('\n', '')
                            commands.append(line)
                    self.expectedInputTests[subdir] = commands
        return self.expectedInputTests

    # This function reads the expected output files

    def readExpectedOutputFiles(self):
        for subdir, dirs, files in os.walk(self.testDirectory):
            for file in files:
                log = []
                validAccounts = []
                transactionSummary = []
                if file == "expectedValidAccountsFile.txt":
                    with open(os.path.join(subdir, file), 'r') as in_file:
                        for line in in_file:
                            line = line.replace('\n', '')
                            validAccounts.append(line)
                    self.expectedValidAccountsLists.append(validAccounts)
                elif file == "expectedTransactionSummaryFile.txt":
                    with open(os.path.join(subdir, file), 'r') as in_file:
                        for line in in_file:
                            line = line.replace('\n', '')
                            transactionSummary.append(line)
                    self.expectedTransactionFiles.append(transactionSummary)
                elif file == "expectedLogFile.txt":
                    with open(os.path.join(subdir, file), 'r') as in_file:
                        for line in in_file:
                            line = line.replace('\n', '')
                            log.append(line)
                    self.expectedLogFiles.append(log)

    # This function validates the success of each test and writes it to an
    # output file as a report

    def validateTests(self):
        self.readExpectedOutputFiles()

        with open("test-report.txt", 'w') as resultsFile:
            resultsFile.write(time.strftime("%c") + '\n\n')
            for key, value in self.testResults:
                resultsFile.write(key + " : " + value + '\n')
