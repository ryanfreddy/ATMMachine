import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from frontend import *
from backend import *

def runDailyScript(dayNumber):

    pathToDayFolder = ""
    sessionCounter = 0
    last_file=0


    pathToDayFolder = "Day" + str(dayNumber)

    # This ensures that each input file is executed in order

    for subdir, dirs, files in os.walk(pathToDayFolder):
        for file in files:
            if "inputs" in file:
                if int(file[7])>last_file:
                    last_file=int(file[7])
    last_file+=1

    # Read each session inputs and create a frontend instance so that
    # each session can be executed

    for file_num in range(1,last_file):
        currentCommands = []
        sessionCounter += 1
        with open(os.path.join(pathToDayFolder, "session" + str(file_num) + "-inputs.txt"), 'r') as in_file:
            for line in in_file:
                line = line.replace("\n", "")
                currentCommands.append(line)
        in_file.close()

        frontEnd = QBASIC.QBASIC()     # iniltilizes new instace of the front end for each session
        currentPath = os.path.abspath(pathToDayFolder)
        frontEnd.executeDailyScript(currentPath, currentCommands, sessionCounter)

        print("Finished running a total of {0} sessions".format(sessionCounter))

    # Get all commands from each generated transaction summary file

    commands = []
    for file_num in range(1,last_file):
        with open(os.path.join(pathToDayFolder, "transactionsummary" + str(file_num) + ".txt"), 'r') as in_file:
            for line in in_file:
                if "EOS" not in line:
                    commands.append(line)
        in_file.close()

    commands.append("EOS 0000000 0 0000000 ***")

    # Create merged transaction summary file

    with open(os.path.join(pathToDayFolder, "mergedtransactionsummary.txt"), 'w') as out_file:
        for command in commands:
            out_file.write(command)
    out_file.close()
    commands.clear()

    # Build paths to relevant files

    currentPath = os.path.abspath(pathToDayFolder)
    mergedTransactionSummary = currentPath + "/mergedtransactionsummary.txt"
    newValidAccountsFile = currentPath + "/newvalidaccounts.txt"
    oldMasterAccountsFile = currentPath + "/oldmasteraccounts.txt"
    newMasterAccountsFile = currentPath + "/newmasteraccounts.txt"
    oldValidAccountsFile = ""

    # If its not the first day, reference previous days master newValidAccountsFile
    # and newValidAccountsFile

    if dayNumber != 1:
        pathToDayFolder = "Day" + str(dayNumber-1)
        currentPath = os.path.abspath(pathToDayFolder)
        oldMasterAccountsFile = currentPath + "/newmasteraccounts.txt"
        oldValidAccountsFile = currentPath + "/newvalidaccounts.txt"

    # Create backend instance and run it

    backEnd = backoffice.BackOffice(oldMasterAccountsFile, mergedTransactionSummary,
                oldValidAccountsFile, newMasterAccountsFile, newValidAccountsFile)
    backEnd.applyTransactions()

runDailyScript(1)
