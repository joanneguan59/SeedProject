import os
import sys

filename = sys.argv[1]
logfile = filename.replace("gjf", "log")

#File Core Name
def fileNameEx(filename):
    index = filename.rfind(".gjf")
    fileN = filename[:index]
    return fileN
    print (fileN)

#Normal Termination Function
def NormalTermination(logfile):
    with open(logfile, "r")  as l:
        total = 0

        for i, line in enumerate(l):
            if "Normal termination" in line:
                total = total + 1
                print("'Normal termination' found in line:",i,)
        if total == 0:
            print ("No normal termination was found. Job did not terminate normally. Exiting program at step 1.")
            sys.exit()
        else:
            print("Total number of 'Normal termination' found:",total)
            print("Job normally terminated.")

#Single Point Energy Job
job = fileNameEx(filename)
print("\nRunning Step 1: Single Point Energy Job\n")
cmd = "g16 " + filename
os.system(cmd)
NormalTermination(logfile)
print("\nRunning Step 2: Stability Job\n")

#Stability Job
cmd = "g16 -ic=" + job + ".chk -y=" + job + "-2.chk -x='#p chkmethod chkbasis geom=allcheck guess=read Stable=opt' < /dev/null >& " + job + "-2.log"
os.system(cmd)
logfile = job + "-2.log"
NormalTermination(logfile)
with open((job+"-2.log"), "r")  as l:
     for i, line in enumerate(l):
        if "RHF -> UHF instability" in line:
            print("\nThe current closed-shell wavefunction is unstable. There is a lower energy open-shell wavefunction. \nWavefunction is unstable.")
        if "is stable" in line:
            print("The wavefunction is stable.")
print("\nRunning Step 3: Opt Freq Job\n")

#Opt Freq Job
cmd ="g16 -ic="+job+"-2.chk -y="+job+"-3.chk -x='#p chkmethod chkbasis geom=allcheck guess=read opt freq' < /dev/null >&"+job+"-3.log"
os.system(cmd)
logfile = job + "-3.log"
NormalTermination(logfile)
with open((job+"-3.log"), "r")  as l:
    total2 = 0
    for i, line in enumerate(l):
        if ("imaginary frequencies" in line) and total2 < 1:
            string = line
            total2 = 1
            print("\n'imaginary frequency' found in line:",i,)
            print(line[10:35], "found.", sep='')
print ("\nWorkflow manager has finished running. Exiting Program.")
exit()
