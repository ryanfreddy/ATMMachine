from backoffice import BackOffice
import sys
import os

if (len(sys.argv) != 4) and (len(sys.argv) != 2):  # gets the command line arguments, location of merged transaction summary file, master accounts file and valid accounts file
    print("     Please specify the merged transaction summary file, master accounts file and valid accounts file\n      e.g. python3 main.py masteraccountsfile.txt mergedtransactionsummary.txt validaccounts.txt\n Or to test it, use python3 main.py test")
    sys.exit()
else:
    if str(sys.argv[1]) == "test":
        backendInputTests = {}
        for subdir, dirs, files in os.walk("backend_tests"): # for each of the test folders we want to get the inputs andexpectewd outputs
            for file in files:
                if "input" in file:
                    backendInputTests[subdir] = [subdir, file]
        with open("backOfficeTestReport.txt", 'w') as resultsFile:  # for ewach test we want to write the result to the report
            for test, paths in backendInputTests.items():
                transactionSummaryFilePath = os.path.join(paths[0], paths[1])
                backOffice = BackOffice("backend_tests/testmasteraccounts.txt", transactionSummaryFilePath, "backend_tests/testvalidaccounts.txt", paths[0] + "/newmasteraccounts.txt",  paths[0] + "/newvalidaccounts.txt")
                backOffice.expectedTestLogPath = paths[0] + "/expectedLog.txt"
                result = backOffice.applyTransactions()   # calling function that loops through all of the transactions
                print(paths[0] + " " + result)
                resultsFile.write(paths[0] + " " + result + '\n')
    else:
        backend = BackOffice(str(sys.argv[1]), str(sys.argv[2]),
                    str(sys.argv[3]), "newmasteraccountsfile.txt", "newvalidaccountsfile.txt")
        backend.applyTransactions()
