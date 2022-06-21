"""
About "Blanks and Scatters":
    • There are 15 independent reels each of which consists of only two symbols, 
        namely a scatter symbol and a blank symbol.												
    • Each independent reel has a probability 0.2 of stopping at a scatter symbol.												
    • Once a reel stops at a scatter symbol, the scatter symbol will lock in place and the reel will stop spinning.												
    • The player is awarded 3 free spins initially.												
    • Each time one or more reels stop at a scatter symbol, the number of spin remaining is reset to 3.												
    • Game ends when all 15 reels have stopped at a scatter symbol or no spin remaining.												
    • For each locked scatter symbol, the player is awarded a credit award that is determined												
        by first selecting a weight table from Credit Tables and then a credit value based on the weights 
        from the selected table.																							
    
    Credit Tables	            Table 1             Table 2             Table 3
    Table	    Weight          Credit  Weight      Credit  Weight      Credit  Weight
    Table 1	    1000000         1       20          4	    20          10	    20
    Table 2	    185000          2       20          5	    15          12	    10
    Table 3 	105000          3	    10          8	    10          15	    10

This program computes the expected number of tokens resulting from a player
    playing "Blanks and Scatters" (B&S) until they win / run out of turns. 
    It prompts the user for a number of trials (y) and a number of turns per trial (x), 
    and then runs B&S x times for each of y trials.

The B&S function Play() stores a length-15 array, as well as a count on the number of spins
    remaining and a boolean var tracking whether to reset the number of spins. It then emulates 
    continual spins until one of the end conditions is met, at which point it returns the list 
    [pay,scatters,count].

The main driver of the code is the Sim(...) (for "Simulation") function, which
    runs Play() for the specified number of trials (call it "n") and stores the output
    [pay,scatters,count] as it goes.
"""

import random
import numpy as np
import time

##################################################################
### ANSI in different OSes
##################################################################
import os
os.system("")  # enables ansi escape characters in terminal

COLOR = {
    "blue": "\033[94m",
    "green": "\033[92m",
    "red": "\033[91m",
    "none": "\033[0m",
}

# Utility Functions (stuff Mathematica can already do)
def ConstantArray(elt,size):
    return [elt for x in range(size)]

# Get >= 1 random "scatter" and/or "blank" elements
def RandChoice(n):
    list=["scatter","scatter","blank","blank","blank","blank","blank","blank","blank","blank"]

    return(random.choices(list,k=n))

# Credit-related Things
def Credit():
    credittable = ConstantArray(1,1000)+ConstantArray(2,185)+ConstantArray(3,105)
    table1 = ConstantArray(1,20)+ConstantArray(2,20)+ConstantArray(3,10)
    table2 = ConstantArray(4,20)+ConstantArray(5,15)+ConstantArray(8,10)
    table3 = ConstantArray(10,20)+ConstantArray(12,10)+ConstantArray(15,10)

    creditno = random.choice(credittable)

    if creditno == 1:
        creditamt = random.choice(table1)
    elif creditno == 2:
        creditamt = random.choice(table2)
    else: creditamt = random.choice(table3)

    return(creditamt)

# One game play
def Play():
    spin = RandChoice(15)
    oldspin = spin
    numspins = 3
    scatter = False
    history = []
    count = 1


    while("blank" in spin and numspins > 0):
        for i in range(len(spin)):
            if oldspin[i]=="scatter":
                spin[i]=oldspin[i]
            else:
                spin[i]=RandChoice(1)[0] #...[0] is needed bc RandChoice(...) is always a list.

                if spin[i]=="scatter":
                    scatter = True

        history.append(spin)

        if scatter == True:
            numspins = 3
        else: numspins -= 1

        count += 1
        scatter = False

    final = history[-1]
    scatters = final.count("scatter")
    pay = scatters * Credit()

    return([pay,scatters,count])

# A multi-play simulation
def Sim(n):
    data = [Play() for x in range(n)]

    pay = [d[0] for d in data]
    scatters = [d[1] for d in data]
    count = [d[2] for d in data]
    

    return([np.mean(pay),np.mean(scatters),np.mean(count)])

if __name__ == "__main__":
    print("\tThis program computes a number of expected values relating to trials of the scatter/blank slot machine.") #computes the expected number of tokens resulting from a player playing Crazy 8's until they win\n")
    time.sleep(1.25)

    trials = int(input("\n\tHow many trials would you like to run? ").strip())
    sims = Sim(trials)

    print("\t" + "From " + str(trials) + " trials, [" + COLOR["blue"] + "avg pay" + COLOR["none"] + 
    ", " + COLOR["green"] + "# scatters" + COLOR["none"] + ", " + COLOR["red"] + "avg # turns" +
    COLOR["none"] + "] = [" + COLOR["blue"] + str(sims[0]) + COLOR["none"] + ", " + COLOR["green"] +
    str(sims[1]) + COLOR["none"] + ", " + COLOR["red"] + str(sims[2]) + COLOR["none"] + "].\n")