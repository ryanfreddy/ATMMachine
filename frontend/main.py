from QBASIC import QBASIC
import sys


if len(sys.argv) != 3:
    print("     Please specify the valid accounts list and transaction summary file\n      e.g. python3 main.py activeaccts.txt transsummary.txt")

    sys.exit()
else:
    app = QBASIC()
    app.initilizeQbasicTerminal(str(sys.argv[1]), str(sys.argv[2]))
