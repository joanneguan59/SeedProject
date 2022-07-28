import sys 
print("Enter log file name: ")
logfile = input()
with open(logfile, 'r') as l:
    total = 0
    total2 = 0
    string = str()
    
    for i, line in enumerate(l):
        if "Normal termination" in line:
            total = total + 1
            print("\n'Normal termination' found in line:",i,)
      
        if ("imaginary frequencies" in line) and total2 < 1:
            string = line 
            total2 = 1
            print("\n'imaginary frequency' found in line:",i,)
            print(line[10:35], "found.", sep = '')
       
        if "RHF -> UHF instability" in line:
            print("The current closed-shell wavefunction is unstable. There is a lower energy open-shell wavefunction. \nWavefunction is unstable.")
        if "is stable" in line:
            print("The wavefunction is stable.")
        
    print("\nTotal number of 'Normal termination' found:",total)
  
    if total == 0:
        print("Not normally terminated.")
    else:
        print("Normally terminated.")
