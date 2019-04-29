from random import randint
from fighting import *

EnemyStatNames = ["XP","Grist","VG DROP","Vitality","Defense","Strength","Fortitude","Agility","Intell","AV","PA","EN","Damage Roll", "Name", "Guarding"]
PlayerStatNames = ["Static Damage","Effects","Gel Viscosity","Vitality","Defense","Strength","Fortitude","Agility","Intell","AV","PA","EN","Bonus Damage Roll", "Name", "Guarding"]

enemyCount = int(input("How many enemies are there?\n"))
playerCount = int(input("How many players are there?\n"))


#input enemies
Enemies = {}
for i in range(0, enemyCount):
    print("\nEnemy #{0}:".format(i+1))
    name = input("Name (unique str): ")
    Enemies[name] = {}
    for x in range(0, len(EnemyStatNames)):
        if not EnemyStatNames[x] in ["Damage Roll", "Bonus Damage Roll", "AV", "PA", "EN", "Name", "Guarding"]:
            Enemies[name][EnemyStatNames[x]] = int(input(EnemyStatNames[x] + " (int): "))
        elif EnemyStatNames[x] == "AV":
            Enemies[name][EnemyStatNames[x]] = Enemies[name]["Agility"] + 10
        elif EnemyStatNames[x] == "PA":
            Enemies[name][EnemyStatNames[x]] = Enemies[name]["Intell"] + 10
        elif EnemyStatNames[x] == "EN":
            Enemies[name][EnemyStatNames[x]] = True
        elif EnemyStatNames[x] == "Name":
            Enemies[name][EnemyStatNames[x]] = name
        elif EnemyStatNames[x] == "Guarding":
            Enemies[name][EnemyStatNames[x]] = "none"
        else:
            Enemies[name][EnemyStatNames[x]] = input(EnemyStatNames[x] + " (str): ")

#input players
Players = {}
for i in range(0, playerCount):
    print("\nPlayer #{0}:".format(i+1))
    name = input("Name (unique str): ")
    Players[name] = {}
    for x in range(0, len(PlayerStatNames)):
        if not PlayerStatNames[x] in ["Damage Roll", "Bonus Damage Roll", "AV", "PA", "EN", "Name", "Guarding"]:
            Players[name][PlayerStatNames[x]] = int(input(PlayerStatNames[x] + " (int): "))
        elif PlayerStatNames[x] == "AV":
            Players[name][PlayerStatNames[x]] = Players[name]["Agility"] + 10
        elif PlayerStatNames[x] == "PA":
            Players[name][PlayerStatNames[x]] = Players[name]["Intell"] + 10
        elif PlayerStatNames[x] == "EN":
            Players[name][PlayerStatNames[x]] = False
        elif PlayerStatNames[x] == "Name":
            Players[name][PlayerStatNames[x]] = name
        elif EnemyStatNames[x] == "Guarding":
            Players[name][PlayerStatNames[x]] = "none"
        else:
            Players[name][PlayerStatNames[x]] = input(PlayerStatNames[x] + " (str): ")

#ambush?
if input("\nAmbush? (y/n): ").lower() == "y":
    firstEnemy = list(Enemies.keys())[0]
    firstPlayer = list(Players.keys())[0]
    if int(input("Roll 1d20: ")) + Players[firstPlayer]["Agility"] >= Enemies[firstEnemy]["PA"]:
        print("Success!")
        Strife(Players[firstPlayer], Enemies[firstEnemy])
    else:
        print("Failure!")

#determine fighter order
print("\nRolling for turn order")
print("--------------------------")
Rolls = []
TurnOrder = []
EnemyNames = list(Enemies.keys())
PlayerNames = list(Players.keys())
for i in range(0, enemyCount):
    enemy = EnemyNames[i]
    roll = int(input(enemy + " roll 1d20: "))
    Rolls.append(roll + Enemies[enemy]["Agility"])
    TurnOrder.append(enemy)
for i in range(0, playerCount):
    player = PlayerNames[i]
    roll = int(input(player + " roll 1d20: "))
    Rolls.append(roll + Players[player]["Agility"])
    TurnOrder.append(player)
    if roll >= 20:
        print("TRUE SUCCESS!")
        Strife(Players[player], Enemies[list(Enemies.keys())[0]])

Unsorted = True
while Unsorted:
    Unsorted = False
    for i in range(0, len(Rolls)-1):
        if Rolls[i+1] > Rolls[i]:
            Unsorted = True
            Rolls.insert(i, Rolls[i+1])
            TurnOrder.insert(i, TurnOrder[i+1])
            Rolls.pop(i+2)
            TurnOrder.pop(i+2)
        elif Rolls[i+1] == Rolls[i]:
            Unsorted = True
            roll1 = 0
            roll2 = 0
            while roll1 == roll2:
                roll1 = int(input(TurnOrder[i] + " roll 1d20: "))
                roll2 = int(input(TurnOrder[i+1] + " roll 1d20: "))
            if roll1 > roll2:
                Rolls[i] = Rolls[i] + 1
            elif roll1 < roll2:
                Rolls[i+1] = Rolls[i+1] + 1

XP = 0
Grist = 0
abscondedPL = 0
deadPL = 0
abscondedEN = 0
deadEN = 0
battleOver = False
while not battleOver:
    for i in range(0, len(TurnOrder)):
        try:
            fighterName = TurnOrder[i]
        except:
            break
        print("\n{0}'s turn!".format(fighterName))
        print("---------------")
        print(", ".join(TurnOrder))
        opponentName = input("Who will " + fighterName + " fight?: ")
        try:
            fighter = Players[fighterName]
        except:
            fighter = Enemies[fighterName]
        try:
            opponent = Enemies[opponentName]
        except:
            opponent = Players[opponentName]

        opponentState = Strife(fighter, opponent)
        if opponentState == "dead":
            if opponent["EN"]:
                XP += opponent["XP"]
                Grist += opponent["Grist"]
                Gel = randint(0, opponent["VG DROP"])
                fighter["Vitality"] = fighter["Vitality"] + Gel
                deadEN += 1
                if fighter["Vitality"] > fighter["Gel Viscosity"]:
                    fighter["Vitality"] = fighter["Gel Viscosity"]
                print("{0} perished, dropping {1} XP, {2} GRIST, and {3} VITALITY GEL\nrestoring {4}'s VITALITY to {5}\n".format(opponentName, XP, Grist, Gel, fighterName, fighter["Vitality"]))
            else:
                deadPL += 1
                print("{0} perished".format(opponentName))
            TurnOrder.remove(opponentName)
        #NOTE FIGHTER has absconded, NOT OPPONENT
        elif opponentState == "absconded":
            if fighter["EN"]:
                abscondedEN += 1
            else:
                abscondedPL += 1
            TurnOrder.remove(fighterName)


        if input("Special edit? (y/n): ").lower() == "y":
            editing = True
            while editing:
                choice = int(input("\n1-Player Values\n2-Enemy Values\n3-Remove Fighter\n4-End Battle\n5-Finish editing\n"))
                if choice == 1:
                    print("\n" + ", ".join(list(Players.keys())))
                    player = input("Choose a player: ")
                    moreStats = True
                    while moreStats:
                        print("\n" + ", ".join(PlayerStatNames))
                        stat = input("Choose a stat: ")
                        print("\nCurrent value: {0}".format(Players[player][stat]))
                        newVal = input("What would you like to change it to?: ")
                        if isinstance(Players[player][stat], int):
                            Players[player][stat] = int(newVal)
                        else:
                            Players[player][stat] = newVal
                        moreStats = input("More stats? (y/n): ").lower() == "y"
                elif choice == 2:
                    print("\n" + ", ".join(list(Enemies.keys())))
                    enemy = input("Choose an enemy: ")
                    moreStats = True
                    while moreStats:
                        print("\n" + ", ".join(EnemyStatNames))
                        stat = input("Choose a stat: ")
                        print("\nCurrent value: {0}".format(Enemies[enemy][stat]))
                        newVal = input("What would you like to change it to?: ")
                        if isinstance(Enemies[enemy][stat], int):
                            Enemies[enemy][stat] = int(newVal)
                        else:
                            Enemies[enemy][stat] = newVal
                        moreStats = input("More stats? (y/n): ").lower() == "y"
                elif choice == 3:
                    print("\n" + ", ".join(TurnOrder))
                    TurnOrder.remove(input("Choose a fighter to remove: "))
                elif choice == 4:
                    deadEN = enemyCount
                elif choice == 5:
                    editing = False

        #Remove all fighters at 0 Vit
        for fighter in TurnOrder:
            try:
                if Players[fighter]["Vitality"] <= 0:
                    TurnOrder.remove(fighter)
            except:
                if Enemies[fighter]["Vitality"] <= 0:
                    TurnOrder.remove(fighter)

        #Check if all enemies/players gone
        if deadEN + abscondedEN >= enemyCount or deadPL + abscondedPL >= playerCount:
            battleOver = True
            break

    for name in TurnOrder:
        try:
            Players[name]["Guarding"] = "none"
        except:
            Enemies[name]["Guarding"] = "none"


print("\nBATTLE is OVER")
print("----------------------")
if abscondedPL + deadPL >= playerCount:
    print("NO LOOT: all players died or absconded!")
else:
    print("LOOT:\nXP: {0}\tGrist: {1}".format(XP, Grist))

print("----------------------")
print("VITALITY:")
print("\nPLAYERS:")
for player in list(Players.keys()):
    print("{0}: {1}".format(player, Players[player]["Vitality"]))
print("\nENEMIES:")
for enemy in list(Enemies.keys()):
    print("{0}: {1}".format(enemy, Enemies[enemy]["Vitality"]))

input()
