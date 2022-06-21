"""
About Crazy 8's:
    • There are two reels, one on the left and one on the right
    • There are several symbols on each reel, one of which is an 8
    • The 8 symbol lands on the left reel 1 in 9 plays of the game (aka spins)
    • The 8 symbol lands on the right reel 1 in 10 plays
    • The reels spin independently of each other, and each play is independent from previous plays
    • Each play of the game spins both reels
    • Each reel has a large 8 above it, split into 8 segments
    • As the 8 symbol lands on the corresponding reel below it, one additional segment of the large 8
        lights up
    • Once both large 8s are fully lit (i.e. at least 8-8s have landed on each reel) a 50 credit bonus is
        paid and the game ends
    • If one reel’s large 8 is already fully lit, the game isn’t over yet (i.e. do NOT pay the 10 credit
        bonus on a spin that completes the game), and a new 8 lands on its corresponding reel, a 10
        credit bonus is paid
    • Each play of the game costs 1 credit

This program computes the expected number of tokens resulting from a player
    playing Crazy 8's until they win. It prompts the user for a number of trials (y) 
    and a number of turns per trial (x), and then runs Crazy 8's x times for each of y trials.

The Crazy 8's function c8() stores two quantities e1 (8's in the left spinner)
    and e2 (8's in the right), as well as a token count and a boolean var tracking
    whether the 10 credit bonus has been paid out. It then emulates continual
    spins until e1 == e2 == 8, at which points it returns the list [s,c] where
    "s" is the number of spins required and "c" is the number of credits remaining.
    I ended up not using "s" anywhere.

The main driver of the code is the mc(...) (for "MonteCarlo") function, which
    runs c8() for the specified number of trials (call it "n") and stores the output
    number of credits as it goes. Then, every time 1% of "n" is reached, an EV
    update is returned.

Built in to mc is a secondary option allowing the user to specify whether they
    want the entire result list + the EVs or _just_ the EVs. This choice is
    specified in the initial prompt and is implemented via an optional
    handwritten listprettyprint(...) function which splits the ginormous result
    list into smaller sublists of a specified length (default length = 10).
"""

import random
import numpy as np
import time

# Creating Roll Dice Function
def spin():
    left = random.randint(1,9)
    right = random.randint(1,10)

    return [left,right]

# Crazy 8's function
def c8():
    e1=0
    e2=0
    credits=0
    bonus = False
    spins = 0

    while e1 != 8 or e2 != 8:
        r1,r2 = spin()
        credits -= 1
        spins += 1

        if r1 == 8 and e1 < 8:
            e1 += 1

        if r2 == 8 and e2 < 8:
            e2 += 1
        
        if e1 == 8 and e2 == 8:
            credits += 50
            return [spins,credits]
        elif (e1 == 8 or e2 == 8) and bonus == False:
            credits += 10
            bonus = True

# Loop to compute + print the EV
def mc(num_simulations,show_values):
    values = []
    toprint = np.ceil(num_simulations/100) if num_simulations >= 100 else 1

    for i in range(1,num_simulations+1):
        values.insert(len(values),c8()[-1])

        if i % toprint == 0 or i == num_simulations:
            if show_values == False:
                print("Through", i, "rolls, EV=", np.mean(values))
                time.sleep(0.25) #Slow down the output so the user can digest it
            else: 
                print("Through", i, "rolls:")
                print("   Values=")
                listprettyprint(values,10)
                print("   Through", i, "rolls, EV=", np.mean(values))
                time.sleep(0.25) #Slow down the output so the user can digest it

    return values

# Find expected values
def expected_value(lists):
    ev = []

    for list in lists:
        ev.append(np.mean(list))
    
    return ev

# Pretty print function
def listprettyprint(list1,desiredlen):
    list2 = []
    oldstop = 0

    rem = len(list1) % desiredlen

    for i in range(1,len(list1)+1):
        if i == 0:
            list2.insert(1,list1[0:desiredlen])
            oldstop = desiredlen
        if i > 0 and i % desiredlen != 0:
            list2.insert(len(list2),list1[oldstop:i])
        elif i > 0 and i % desiredlen == 0:
            for j in range(1,desiredlen):
                list2.pop(-1)
            list2.insert(len(list2),list1[oldstop:i])
            oldstop = i

    if rem >= 2 and len(list2) >= 2:
        for i in range(0,rem-1):
            list2.pop(-2)

    for lists in list2:
        print("      ", lists)


# TODO: Put in edge-case testing that continues to prompt the user
#       until inputs are of the correct form; currently, this fails ungracefully
#       for non-expected input.

# Main function
if __name__ == "__main__":
    print("This program computes the expected number of tokens resulting from a player playing Crazy 8's until they win\n")
    time.sleep(1)

    trials = int(input("How many trials would you like to run? ").strip())
    vals = str(input("Would you like to show the full values array on output (Y or N)? ").strip())
    
    results = mc(trials,True) if vals.lower()=="y" else mc(trials,False)

    # list1=list(range(0,55))
    # listprettyprint(list1,13)