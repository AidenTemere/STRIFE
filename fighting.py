def Strife(attacker, recipient):
    choice = 0
    while not (choice >= 1 and choice <= 5):
        try:
            choice = int(input("\n1-ASSAIL\n2-AGGREIVE\n3-ABJURE\n4-ABSCOND\n5-NOTHING\n"))
        except:
            print("What do you mean?")

    #return either "alive", "absconded", or "dead"
    if choice == 1:
        Assail(attacker, recipient)
    elif choice == 2:
        Aggreive(attacker, recipient)
    elif choice == 3:
        Abjure(attacker, recipient)
    elif choice == 4:
        if Abscond(attacker, recipient):
            return "absconded"
    if recipient["Vitality"] <= 0:
        recipient["Vitality"] = 0
        return "dead"
    return "alive"


def Assail(attacker, recipient):
    if DetermineStrikingRoll(recipient["Guarding"], recipient["Agility"], recipient["Strength"], recipient["Fortitude"], recipient["AV"], True):
        print("Success!")
        CRT = input("TRUE SUCCESS? (y/n): ").lower() == "y"
        if attacker["EN"]:
            DMG = int(input("Roll " + attacker["Damage Roll"] + " for DAMAGE: "))
            ATK = (1+CRT)*DMG - recipient["Defense"]
        else:
            BD = int(input("Roll " + attacker["Bonus Damage Roll"] + " for BONUS DAMAGE: "))
            ATK = (1+CRT)*(BD + attacker["Static Damage"] + attacker["Effects"]) - recipient["Defense"]

        recipient["Vitality"] = recipient["Vitality"] - ATK
        print("{0} ASSAILS {1} for {2} DAMAGE, leaving {1} with {3} VITALITY\n".format(attacker["Name"], recipient["Name"], ATK, recipient["Vitality"]))
    else:
        print("Failure: {0} missed {1}\n".format(attacker["Name"], recipient["Name"]))


def Aggreive(attacker, recipient):
    subact = input("Subaction before or after? (b/a): ")
    if subact == "b":
        SubAction(attacker)

    if DetermineStrikingRoll(recipient["Guarding"], recipient["Agility"], recipient["Strength"], recipient["Fortitude"], recipient["AV"], False):
        print("Success!")
        CRT = input("TRUE SUCCESS? (y/n): ").lower() == "y"
        if attacker["EN"]:
            DMG = int(input("Roll " + attacker["Damage Roll"] + " for DAMAGE: "))
            ATK = (1+CRT)*DMG - recipient["Defense"]
        else:
            ATK = (1+CRT)*(attacker["Static Damage"] + attacker["Effects"]) - recipient["Defense"]

        recipient["Vitality"] = recipient["Vitality"] - ATK
        print("{0} AGGREIVES {1} for {2} DAMAGE, leaving {1} with {3} VITALITY\n".format(attacker["Name"], recipient["Name"], ATK, recipient["Vitality"]))
    else:
        print("Failure: {0} missed {1}\n".format(attacker["Name"], recipient["Name"]))

    if subact == "a":
        SubAction(attacker)

def SubAction(attacker):
    choice = int(input("\n1-Switch Weapon\n2-Add Vitality\n3-Guard\n4-Other Action\n"))
    if choice == 1:
        print("\nCurrent SD: {0}".format(attacker["Static Damage"]))
        attacker["Static Damage"] = int(input("New SD (int): "))
        print("Current BD: {0}".format(attacker["Bonus Damage Roll"]))
        attacker["Bonus Damage Roll"] = input("New BD (str): ")
        print("Current Effects: {0}".format(attacker["Effects"]))
        attacker["Effects"] = int(input("New Effects (int): "))
    elif choice == 2:
        vit = int(input("How much Vitality?: "))
        attacker["Vitality"] = attacker["Vitality"] + vit
        if attacker["Vitality"] > attacker["Gel Viscosity"]:
            attacker["Vitality"] = attacker["Gel Viscosity"]
        print("Vitality now at {0}".format(attacker["Vitality"]))
    elif choice == 3:
        attacker["Guarding"] = "guarding"
        print("{0} guarding until next round".format(attacker["Name"]))
    elif choice == 4:
        print("Roll unfavourable for this action.")

def DetermineStrikingRoll(guarding, agility, strength, fortitude, AV, striking):
    favor = 0
    if input("Opponent PRONE or RESTRAINED? (y/n): ").lower() == "y":
        favor += 1
    if guarding == "guarding":
        favor -= 1

    if striking:
        strk = "+ STRIKING"
    else:
        strk = ""
    if favor < 0:
        fvr = " unfavourable"
    elif favor == 0:
        fvr = ""
    else:
        fvr = " favourable"
    question = "Fighter roll 1d20 " + strk + fvr + ": "
    roll = int(input(question))

    if guarding == "none" or guarding == "guarding":
        return roll >= AV
    elif guarding == "blocking":
        counter = fortitude
    elif guarding == "dodging":
        counter = agility
    elif guarding == "parrying":
        counter = strength
    return roll >= int(input("Opponent roll 1d20 favourable: ")) + counter


def Abjure(attacker, recipient):
    subact = input("Subaction before or after? (b/a): ")
    if subact == "b":
        SubAction(attacker)

    choice = int(input("\n1-Block (FOR)\n2-Dodge (AGL)\n3-Parry (STR)\n"))
    if choice == 1:
        attacker["Guarding"] = "blocking"
    elif choice == 2:
        attacker["Guarding"] = "dodging"
    elif choice == 3:
        attacker["Guarding"] = "parrying"
    print("{0} {1} until next round\n".format(attacker["Name"], attacker["Guarding"]))

    if subact == "a":
        SubAction(attacker)


def Abscond(attacker, recipient):
    SubAction(attacker)
    abscondChallenge = int(input("Roll 2d20 k1: ")) + attacker["Agility"]
    STRK = int(input("Roll 2 1d20 (Keep lowest): "))
    if(abscondChallenge > STRK):
        print("Success! {0} absconded\n".format(attacker["Name"]))
        return True

    if recipient["EN"]:
        ATK = int(input("Roll " + recipient["Damage Roll"] + " for DAMAGE: ")) - attacker["Defense"]
    else:
        ATK = recipient["Static Damage"] + recipient["Effects"] - attacker["Defense"]
    attacker["Vitality"] = attacker["Vitality"] - ATK
    print("Failure! {0} attacks {1} for {2} DAMAGE, leaving {1} with {3} VITALITY\n".format(recipient["Name"], attacker["Name"], ATK, attacker["Vitality"]))
    return False
