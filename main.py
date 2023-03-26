import random

import player
import enemy
import weapon
import statSpell
import randomWordGenerator

#These next 2 functions are in charge of custom character creator (I made these scripts long ago so the program may not look pretty)
#This one is to ask the user what stat to change
def customCharacter():
    print("Use a total of 20 points distibuted around your charcter")
    global points
    global health
    global attack
    global defence
    global speed
    global mana
    points = 20
    health = 1
    attack = 1
    defence = 1
    speed = 1
    mana = 1
    print("Health: "+str(health))
    print("Attack: "+str(attack))
    print("Defence: "+str(defence))
    print("Speed: "+str(speed))
    print("Mana: "+str(mana))
    print("Remaining points: "+str(points))
    while points != 0:
        chooseStat = input("Select a stat to change ")
        chooseStat = chooseStat.lower()
        if not chooseStat == "health" and not chooseStat == "defence" and not chooseStat == "attack" and not chooseStat == "speed" and not chooseStat == "mana":
            print("Not a stat")
            continue
        else:
            statChange(chooseStat)
            print("Health: "+str(health))
            print("Attack: "+str(attack))
            print("Defence: "+str(defence))
            print("Speed: "+str(speed))
            print("Mana: "+str(mana))
            print("Remaining points: "+str(points))
    return health, attack, defence, speed, mana

#For custom character: This adds to a stat 
def statChange(stat):
    global points
    global health
    global attack
    global defence
    global speed
    global mana
    while True:
        userInput = input("How many points will you use for "+ stat+"? ")
        try:
            userInput = int(userInput)
            break
        except:
            print("Not a number")
    if userInput > points:
        print("not enough points")
    else:
        if stat == "health":
            health += userInput
            points -= userInput
        elif stat == "defence":
            defence += userInput
            points -= userInput
        elif stat == "attack":
            attack += userInput
            points -= userInput
        elif stat == "speed":
            speed += userInput
            points -= userInput
        elif stat == "mana":
            mana += userInput
            points -= userInput
#This will be called everytime the player meets an enemy 
def mainCombatLoop(user,monster):
    print("==========BATTLE START==========")
    running = True
    originalLevel = user.getLvl()
    originalAttack = user.getAttack()
    originalDefence = user.getDefence()
    originalSpeed = user.getSpeed()
    #These stats may be altered in battle. I want the stats to go back to original values after fight is done
    inBattle = True
    while inBattle:
        print("----------------------------------------------------------")
        print("1:ATTACK 2:MAGIC 3:DEFEND 4:SWITCH GEAR 5:CHECK X:RUN AWAY")
        print("----------------------------------------------------------")
        defender = False
        print(monster.getName()+" Health: "+str(monster.getCurrentHealth())+"/"+str(monster.getMaxHealth()))
        print(user.getName()+" Health: "+str(user.getCurrentHealth())+"/"+str(user.getMaxHealth()))
        print(user.getName()+" Mana: "+str(user.getCurrentMana())+"/"+str(user.getMana()))
        action = input("What will you do? ")
        print("\n")
        if action == "1":
            user.battle(monster)
        elif action == "2":
            user.useStatSpell(monster)
        elif action == "3":
            print("You prepare yourself for a hit!")
            print("Your defence and speed went up for the next hit!")
            defender = True
        elif action == "4":
            user.inven()
            continue
        elif action == "5":
            monster.showStats()
            user.showStats()
            user.showEquipted()
            continue
        elif action.lower() == "x":
            run = user.canRunAway(monster)
            if run:
                print("You ran away from the battle.")
                inBattle = False
                break
            else:
                print("You failed to get away!")
        #Checks if monster is dead
        if monster.getCurrentHealth() <= 0:
            print("You defeated the "+monster.getName())
            print("You gained "+str(monster.getXp())+" xp")
            user.checkLvl(monster.getXp())
            input("Press Enter to Continue")
            lootFound()
            inBattle = False
            break
        if not monster.getIsBoss():
            print("The "+monster.getName()+" attacks you!")
            monster.battle(user,defender)
        else:
            bossBattle(user,defender)
        running = user.deadCheck()
        if running == False:
            inBattle = False
            running = False
            return running
        #At the end of turn, user gains a mana
        if user.getCurrentMana() < user.getMana():
            user.setCurrentMana(1,"+")
    #After battle is over
    if inBattle == False:
        user.setAttack(originalAttack,"=")
        user.setDefence(originalDefence,"=")
        user.setSpeed(originalSpeed,"=")
        while originalLevel < user.getLvl():
            increase = 3
            user.setAttack(increase,"+")
            user.setDefence(increase,"+")
            user.setSpeed(increase,"+")
            originalLevel += 1
            newQuestLocationX = random.randint(mapGrid*-1,mapGrid)
            newQuestLocationY = random.randint(mapGrid*-1,mapGrid)
            if unknowns != None:
                unknowns.append((newQuestLocationX,newQuestLocationY))
            questLocations.append((newQuestLocationX,newQuestLocationY))
            #This accounts for level up that might of happened; If we didnt do this, these stats wont be properly set
        return running
#This checks if player's x and y coordinates match any of the coordinates in a list of locations
def checkLocation(x,y,places):
    for cordnate in places:
        if cordnate[0] == x and cordnate[1] == y:
            return True
    else:
        return False
#Depending on how far the player is from spawn(0,0) we will choose different batches of enemies
def enemyDifficulty(x,y,e1,e2,e3,e4,e5):
    enemies = [e5,e4,e3,e2,e1]
    #enRange is how far away the player has to be to get each batch of enemies 
    enRange = [30,24,16,8,1]
    i = 0
    while i < len(enemies):
        if x >= enRange[i] or y >= enRange[i] or x <= enRange[i]*-1 or y <= enRange[i]*-1:
            return enemies[i]
        i += 1
#This looks through the player's notes to see if a location has been discovered or not (upon discovering a location, a message will be added to the note. This distinguishes the old from the news)
def justDiscovered(x,y,notes,description):
    for note in notes:
        if description+str(x)+", "+str(y) in note:
            return False
    return True
#This was a function used to generate an enemy with random stats but I decided to remove it
'''
def randEnemy(user):
    statIndexes = [1,2,3,4]
    random.shuffle(statIndexes)
    print(statIndexes)
    #This will be used to get a random stat (1:health,2:attack,3:defence,4:speed)
    m = ["",1,1,1,1,1,0]
       #("",1,1,1,1,1,xp1)
    m[0] = randomWordGenerator.construct()
    m[0] = m[0].capitalize()
    #Random name using my word generator
    xp = 0
    maxNumber = 15 + user.getLvl()
    while maxNumber > 0:
        number = random.randint(1,round(maxNumber/2))
        x = random.choice(statIndexes)
        m[x] += number
        xp += number
        random.shuffle(statIndexes)
        print(statIndexes)
        print(number)
        maxNumber -= number
    #monster runaway
    if user.getLvl() > 10:
        m[5] = 5 + xp/4
        m[5] = round(m[5])
    else:
        m[5] = 4
    #Monster xp
    m[6] = xp/2
    #dont want xp to be ridiculously high
    #Make sure there are no decimals, just in case
    m[6] = round(m[6])
    return m
'''
#Whenever the player finds loot, we will call this function
def lootFound(minRar=1,maxRar=100,isDrop=True):
    #If loot comes from a treasure chest or monster, its a drop
    if isDrop:
        #User gets coins
        coins = random.randint(1,100)
        user.setMoney(coins,"+")
        print("You found "+str(coins)+" coins")
        #User may get shrinestones
        shrinestonePresent = random.randint(1,10)
        if shrinestonePresent == 1:
            shrinestoneAmount = random.randint(1,5)
            print("You found "+str(shrinestoneAmount)+" shrinestones!")
            user.setShrinestones(shrinestoneAmount,"+")

    #Loot
    luck = random.randint(minRar,maxRar)
    if luck > 1 and luck < 40:
        w = random.choice(normWeapons)
        w = list(w)
        #w was a tuple; probably should have make it a list in the first place but too late now
        w.append(False)
        #Gets an optional parameter; turns outs its not optional but i dont want to rework everything
        #This boolean tells if the item has a special effect of not
        user.lootWeapon(w)
    elif luck > 40 and luck < 80:
        s = random.choice(normSpells)
        s = list(s)
        s.append(False)
        user.lootSpell(s)
    elif luck > 80 and luck < 100:
        spellOrWeapon = random.randint(1,2)
        if spellOrWeapon == 1:
            s = random.choice(specialSpells)
            user.lootSpell(s)
        elif spellOrWeapon == 2:
            w = random.choice(specialWeapons)
            user.lootWeapon(w)
    elif luck == 1 or luck == 80:
        print("You found a hidden stash of shrinestones!")
        shrinestoneAmount = random.randint(10,30)
        print("You found "+str(shrinestoneAmount)+" shrinestones!")
        user.setShrinestones(shrinestoneAmount,"+")
    elif luck == 40:
        w = random.choice(normWeapons)
        w = list(w)
        w.append(False)
        user.lootWeapon(w)
        print("There is another item!")
        s = random.choice(normSpells)
        s = list(s)
        s.append(False)
        user.lootSpell(s)
    elif luck >= 100:
        s = random.choice(legendarySpells)
        user.lootSpell(s)
    
#This fills a shop with loot. This will be called whenever the player discovers a new town      
def fillStock(weapons,spells):
    stock = []
    i = 0
    while i < 5:
        itemType = random.randint(1,100)
        if itemType <= 40:
            stock.append(random.choice(weapons))
        elif itemType >40 and itemType <= 80:
            stock.append(random.choice(spells))
        i += 1
    return stock
    #This picks random items for the shop
#checks if a list has any duplicate values
def checkDuplicates(thingList):
    for x in thingList:
        amount = thingList.count(x)
        if amount > 1:
            return True
    else:
        return False   
#Checks for matching coordinates in 2 lists of coordinates
def overlapCheck(list1,list2):
    for item in list1:
        if item in list2:
            return True
    else:
        if (0,0) in list1 or (0,0) in list2:
            return True
        else:
            return False
#Tells how close the player is to finding all the shrines      
def totalShrineCheck(current,total):
    #current shrines found and total shrines
    print("-------------------------------------")
    if current == total:
        print("You found all shrines!")
        input("Press Enter to Continue")
        #Reward for finding all shrines is a guarented legendary spell
        lootFound(100,100)
        print("You win... for now")
    elif current == total-1:
        print("You are so close to victory")
    elif current > total/2:
        print("You feel like your goal is near")
    elif current == total/2:
        print("You feel as if you are halfway to victory")
    else:
        print("You feel as if you have a long way to go")
    print("---------------------------------------")
#generates coordinates (x,y) into a list within the map boundries
def generateLocations(places,amount):
    places = []   
    i = 0
    while i < amount:
        location = (random.randint(-1*mapGrid,mapGrid),random.randint(-1*mapGrid,mapGrid))
        places.append(location)
        i += 1
    return places

#This function will check if player is around one of the cordnates in a list
#This takes in the player's x and y coordinates, the list of coordinates to loop through and the distance around the coordinate the player is able to "see"
def around(x,y,places,distance):
    places = sortClosest(x,y,places)
    places.reverse()
    #Reverse the list so that way the loop ends with goX and goY being the closest place
    visablePlaces = []
    for cordnate in places:
        #Checks if x is in player's sight
        if x >= cordnate[0]-distance and x <= cordnate[0]+distance:
            if x > cordnate[0]:
                #goLeft
                goX = "west"
            elif x < cordnate[0]:
                #goRight
                goX = "east"
            else:
                #same axis
                goX = ""
            #Checks if y is in player's sight
            if y >= cordnate[1]-distance and y <= cordnate[1]+distance:
                if y > cordnate[1]:
                    #goLower
                    goY = "south"
                elif y < cordnate[1]:
                    #goHigher
                    goY = "north"
                else:
                    #same axis
                    goY = ""
                #If it got to here, it means the player is able to see this piticular location
                visablePlaces.append(cordnate)
    if len(visablePlaces) > 0:
        visablePlaces = sortClosest(x,y,visablePlaces)
        return True, goX, goY, visablePlaces
    else:
        return False, "nothing detected"

    
#This sorts the closest cordnate in a list reletive to the player's x and y
def sortClosest(x,y,places):
    sorting = True
    while sorting:
        doAgain = False
        i = 0
        while i < len(places)-1:
            location1 = places[i]
            distanceX1 = abs(location1[0]-x)
            distanceY1 = abs(location1[1]-y)
            totalDistance1 = distanceX1 + distanceY1
        
            location2 = places[i+1]
            distanceX2 = abs(location2[0]-x)
            distanceY2 = abs(location2[1]-y)
            totalDistance2 = distanceX2 + distanceY2
            #compare location1 and location2
            if totalDistance1 > totalDistance2:
               places[i] = location2
               places[i+1] = location1
               doAgain = True
               #If there was a change in the list, we check it again to make sure everything is in the right order
            i+=1
        if not doAgain:
            sorting = False
    return places
#Removes an item from a list without an error 
def removeFromList(thing,selectedList):
    for item in selectedList:
        if item == thing:
            selectedList.remove(thing)
            return list(selectedList)
    else:
        print("\n")
#Displays the world map. This takes in all locations the player has discovered so far and gives them a visual representation
def worldMap(xAxis,yAxis,mapGrid,towns,shrines,unknowns,mountains,kingdoms):
    print("Map legend: - = nothing found, ? = unknown, T = town, S = shrine, M = mountain, K = kingdom X = player location")
    yIterator = mapGrid
    while yIterator  >= mapGrid * -1:
        #Starts from the highest y cordnate and prints each cordnate in that x position
        xRow = ""
        #We start from the lowest x cordnate
        xIterator = mapGrid * -1
        while xIterator <= mapGrid:
            if (xIterator,yIterator) == (xAxis,yAxis):
                xRow += "X"
            elif (xIterator,yIterator) in towns:
                xRow += "T"
            elif (xIterator,yIterator) in shrines:
                xRow += "S"
            elif (xIterator,yIterator) in unknowns:
                xRow += "?"
            elif (xIterator,yIterator) in mountains:
                xRow += "M"
            elif (xIterator,yIterator) in kingdoms:
                xRow += "K"   
            else:
                xRow += "-"
            xRow += " "
            #Were adding a space so map looks nicer
            xIterator += 1
        print(xRow)
        yIterator -= 1
    else:
        print("Explore the world to find new places!")
print("Welcome to my rpg game!")
selecting = True
nameType = input("Choose your own name (o) or generate a random name?(r)")
if "o" == nameType.lower():
    userName = input("What is your name? ")
elif nameType.lower() == "devmode":
    userName = "Developer"
    user = player.playerClass(userName,10000000,10000000,10000000,10000000,10000000)
    user.setWeapon("Nerf Hammer",10000000)
    user.setSpell("Remove From Game",0,"h",10000000,"e")
    user.addInven("Murray Cube",50,"null",0,"null",True)
    user.addInven("Capture",35,"null",0,"null",True)
    user.addInven("Warp Time",25,"null",0,"null",True)
    selecting = False
else:
    choosing = True
    while choosing:
        print("Generating name...")
        userName = randomWordGenerator.construct()
        userName = userName.capitalize()
        print(userName)
        exitChoosing = input("Run again?(y/n)")
        if "n" in exitChoosing.lower():
            choosing = False
print("Hello there "+userName+". Welcome to the world of {}\n".format("Santuario"))
print("Before we begin, you must create a character")
print("You may either choose a preset or create your character stats")
while selecting:
    #playerClass takes in username, max health, attack, defence, speed, mana
    #weapons take in name and damage
    #spells take in name, cost, usage, amount, target OPTINNAL: special(t/f)
    #name, usage and target are strings. Rest are integers
    role = input("1:Rogue, 2:Mage, 3:Beserker, 4:Warrior, x:custom ")
    print("\n")
    if role == "1" or role.lower() == "rogue":
        #Do rogue stats
        print("A swift and deadly hero that will have a good first strike. However, he can't take much hits so be quick!")
        confirm = input("Choose this class?(y/n)")
        if confirm.lower() == "y":
            user = player.playerClass(userName,4,7,2,9,3)
            user.setWeapon("Iron Dagger",1)
            user.setSpell("Disorent",2,"s",2,"e")
            selecting = False
    elif role == "2" or role.lower() == "mage":
        #Do mage stats
        print("Powerful and full of utility, this hero has a wide vareity of spells to use her mana. Be mindful though as she may not be fit for hand to hand combat.")
        confirm = input("Choose this class?(y/n)")
        if confirm.lower() == "y":
            user = player.playerClass(userName,6,3,4,2,10)
            user.setWeapon("Birchwood Wand",1)
            user.setSpell("Magic Missile",3,"h",3,"e")           
            selecting = False
    elif role == "3" or role.lower() == "beserker":
        #Do beserker stats
        print("Brute strong and forceful, this hero will plow through the enemy whilst taking hits. He may be tough but foes he can't reach can really be annoying!")
        confirm = input("Choose this class?(y/n)")
        if confirm.lower() == "y":
            user = player.playerClass(userName,7,4,9,2,3)
            user.setWeapon("Iron Axe",1)
            user.setSpell("Rage",3,"a",2,"p")
            selecting = False
    elif role == "4" or role.lower() == "warrior":
        #do warroir stats
        print("A versitile and battle-ready hero that is able to adapt well to his situation. While he well rounded, certain traits others excel in could be useful.")
        confirm = input("Choose this class?(y/n)")
        if confirm.lower() == "y":
            user = player.playerClass(userName,7,5,5,4,4)
            user.setWeapon("Iron Sword",1)
            user.setSpell("Defence Stance",3,"d",2,"p")
            selecting = False
    elif role.lower() == "x" or role.lower() == "custom":
        print("If you want to make your own class, we have a character maker!")
        confirm = input("Choose this class?(y/n)")
        if confirm.lower() == "y":
            s = customCharacter()
            #this returns a list of the stats in order
            user = player.playerClass(userName,s[0],s[1],s[2],s[3],s[4])
            user.setWeapon("Fazed Darksword",1)
            user.setSpell("Nightshade",int((s[0]+s[4])/2*1),"h",s[1]+s[2]+s[3],"e")
            selecting = False
print("Finished making character")
input("Press Enter to Continue")
print("======================================")
user.showStats()
user.showEquipted()
#EXPLAINING STATS
#health is well, health
#Attack will be the highest amount of damage possible. Damage will be a random number from 1 to your attack stat plus your weapon
#Defence will be the highest possible amount of damage reduced. Reduction will be a random number from 1 to your defence stat
#Speed will be your chance to dodge an attack. Both you and your enemy get a random number, ranging from 1 to your speed. If the defender has more speed, they doge
#mana will be used when casting spells, taking away mana according to the spell's cost

#weapons take in name and damage, OPTINNAL: special(boolan)
#spells take in name, cost, usage, amount, target OPTINNAL: special(boolan)
normWeapons = [("Steel Axe",3),("Steel Sword",2),("Steel Dagger",1),("Steel Spear",3),("Club",3),("Mace",4),("Brass Knuckles",1),("Iron Fist",2),("Wooden Bow",1),
               ("Crossbow",2),("Long Bow",3),("Rock",0),("Knife",1),("Hammer",3),("Scythe",3),("Bat",2)]
normSpells = [("Fear",3,"a",3,"e"),("Agility",4,"s",3,"p"),("Oakflesh",4,"d",3,"p"),("Empower",4,"a",3,"p"),("Frost Wind",3,"s",3,"e"),("Heal",4,"h",3,"p"),
              ("Soul Shatter",4,"h",5,"e"),("Mind Reader",3,"d",3,"e"),("Spectral Arrow",3,"h",3,"e"),("Barrier",5,"d",5,"p"),("Silence",8,"a",7,"e"),
              ("Shock",4,"h",4,"e")]

specialSpells = [("Intertwine",5,"s",100,"e",True),("Double Strike",10,"h",8,"e",True),("Life Swap",10,"null",0,"null",True),("Pure Mana",0,"null",0,"null",True)]
specialWeapons = [("Hammer of Decimation",10,True),("Blood Blade",3,True),("Cuffs of Lightning",3,True)]

legendarySpells = [("Murray Cube",50,"null",0,"null",True),("Warp Time",25,"null",0,"null",True),("Capture",35,"null",0,"null",True)]

#NOTE: eneimes do not have a mana stat
#Each enemy is a tuple which is inside a list
#Takes in name, max health, attack, defence, speed, runaway, xp
xp1 = 2
xp2 = 6
xp3 = 8
xp4 = 20
xp5 = 30
#Each group will have stats that sum up to a mulitple of 5. Each group will increase the sum by 5 (slime is an exception to these rules)
enemies1 = [("Slime",1,1,1,1,1,xp1),("Goblin",3,5,2,2,4,xp1),("Bird",2,2,1,5,5,xp1),("Wolf",3,3,2,4,3,xp1),("Dumb Rascal",2,1,1,8,4,xp1)] #sum of 15
enemies2 = [("Orchid",5,5,6,3,1,xp2),("Skeleton",4,3,5,6,2,xp2),("Brawler",4,8,3,4,1,xp2),("Cobra",3,3,2,10,2,xp2),("Rock Crab",5,2,8,2,3,xp2)] #sum of 20
enemies3 = [("Angry Farmer",6,7,4,2,6,xp3),("Orc",8,6,5,3,3,xp3),("Dark Knight",5,8,8,3,1,xp3),("Bear",8,5,8,2,2,xp3),("Rogue Theif",2,4,1,10,8,xp3)] #sum of 25
enemies4 = [("Dark Spirit",5,7,7,9,7,xp4),("Hired Assassin",5,10,4,8,8,xp4),("Minotaur",12,6,8,5,4,xp4)]#sum of 35 (cuz i want to make them really powerful)
enemies5 = [("Ravenous Beast",8,8,6,10,8,xp5),("Demon",9,12,6,6,6,xp5)] #sum of 40

running = True
#This is for location in world. This will be used to see where the user is in the world
yAxis = 0
xAxis = 0
#size of the map
mapGrid = 30
#Damage you start take if you start going off the map
outOfBounds = 1

#Towns
numTowns = random.randint(20,30)
townLocations = []
townLocations = generateLocations(townLocations,numTowns)

#Shrines
shrineLocations = []
numOfShrines = 6
numDiscoveredShrines = 0
shrineLocations = generateLocations(shrineLocations,numOfShrines)
shrineLocations = sortClosest(xAxis,yAxis,shrineLocations)
senseableShrineLocations = shrineLocations.copy()   
#We will remove locations that the player can sense by removing it from this list


#Check if shrine and town overlap cordnates
isTownOverlap = overlapCheck(townLocations,shrineLocations)
while isTownOverlap:
    numTowns = random.randint(20,30)
    townLocations = generateLocations(townLocations,numTowns)
    #Regenerate towns
    isTownOverlap = overlapCheck(townLocations,shrineLocations)
    #Check again for overlaps
townLocations = sortClosest(xAxis,yAxis,townLocations)

#Traps
numOfTraps = random.randint(50,80)
trapLocations = []
trapLocations = generateLocations(trapLocations,numOfTraps)
isTrapOverlap = overlapCheck(trapLocations,townLocations)
#We will only make sure if there is an overlap in towns. Shrines can still have traps
while isTrapOverlap:
    numOfTraps = random.randint(50,80)
    trapLocations = generateLocations(trapLocations,numOfTraps)
    #regenerate trap locations
    isTrapOverlap = overlapCheck(trapLocations,townLocations)
    #Check again
trapLocations = sortClosest(xAxis,yAxis,trapLocations)



questLocations = []
questLocations = generateLocations(questLocations,6)
#Some quests at the start you can find
questTypeList = ["heal","defend","damage"]
questFlavorText = ["You see a skiddish man whomst has an odd request for you","You see a young paladin with an offering","You see a mercenary in training that challanges you","You see a nobel with a contract for you","You see an ambitious young boy who wants to see your combat skills"]
#we will add more quests as player levels up

#Mountains
numOfMountains = random.randint(10,20)
mountains = []
mountains = generateLocations(mountains,numOfMountains)
#No overlap check cuz towns and shrince etc can be in mountians


discoveredShrines = []
discoveredTowns = []
unknowns = []
for location in questLocations:
    unknowns.append(location)
#Unknowns are places of interest for the player, namely the rags you find with either a treasure location, a city location, a shrine location or a trap location



#I found that finding a town is difficult. To combat this, I'll make some kingdoms that the player can use to fast travel to cover more ground
kingdomLocations = []
kingdomLocations = generateLocations(kingdomLocations,3)
isOverlap = True
while isOverlap:
    kingdomLocations = generateLocations(kingdomLocations,3)
    isOverlap = overlapCheck(kingdomLocations,townLocations)
    #If preivous isOverlap is false, check if theres an overlap with shrines
    if isOverlap == False:
        isOverlap = overlapCheck(kingdomLocations,shrineLocations)
user.addToNotes("You have a list of the capitals located of this world: "+str(kingdomLocations[0])+", "+str(kingdomLocations[1])+", "+str(kingdomLocations[2]))
localFlavorTexts = [["A man vigorously slaps you with a fish and demands help with his fishing business",0],["Vees un primo quien es bastante antipatico a tu",0],["You meet a snake oil salesman. He tries to convince you to buy one of his concoctions, but your not sure if its safe...",0]
                    ,["You can see a large italian stallion battalion flirting with the ladies",0],["There is a lowly peasant that tries to sell you a rotten apple. You decide to not buy it",0]]


#If user finds a treasure map, the cordnates will be added to the list
treasureLocations = []
#An xp reward for dicovering a location
disXp = 5
print("\nYou are ready to explore the world around you.")
print("You don't know what it is but something has drawn you to this place Something about it's energy...")
input("Press Enter to continue...")


#This next batch of comments is more for me than anyone else reading this. It shows the games development and ideas I have for the game
#If your just looking for an explainations of the code, you can skip this section
#======================DEV COMMENTS======================

#TASK NOTICES
#Statues that activate somethhing like a boss
#Add a boss
#Add more things to discover (Random quests, boss lairs)


#TO ADD IN FUTURE:
    #===Esentals===
    #Basic spells [DONE]
    #Weapon drops [DONE]
    #Enemy attack [DONE]
    #runaway [DONE]


    #===Wants===
    #Add biomes
        #Have a biome-specific event happen at random
    #Shops with currency system [DONE]
    #Black market
    #Town reputation or wealthness; Towns that change depending on player's actions
    #Day/night cycle
    #Weapon rarities
    #Doge chance using speed stat [DONE]
    #Critical hits?
    #Enemies have random lvls that boosts their stats? [kinda done??]
    #Highscore (Started working on)
    #Special spells (These will have unique effects) Ideas below
        #Spell that costs health
        #Spell that switches stats
        #Spell that converts your mana to damage
        #Spell that has tick damage
        #Spell that turns enemy into a totem that is stored in your inventory
        #Spell that summons
        #Trade-off spells (Tons of attack but less defence)
        #Turn based attacks(increased attack for a couple turns)
    #Save and load games

#======================END OF DEV COMMENTS======================

#This will be the main game loop
while running:
    #this clears the screen basically for the next "turn"
    i = 0
    while i < 10:
        print("\n")
        i += 1
    #LOCATION CHECKING
    #traps
    trapCheck = checkLocation(xAxis,yAxis,trapLocations)
    if trapCheck:
        print("You stepped into a trap!")
        trapDamage = round(user.getCurrentHealth() * 0.75)
        #Traps deal percent damage so players dont die from traps (unless they are REALLY low)
        user.setCurrentHealth(trapDamage,"-")
        print("You took "+str(trapDamage)+" damage!")
        trapLocations.remove((xAxis,yAxis))
        #Remove the trap locations so it can't be triggered again
        unknowns = removeFromList((xAxis,yAxis),unknowns)
        running = user.deadCheck()
        if running == False:
            continue
    else:
        #User will also have a slight chance to sense the trap in the area to warn the player
        senseableTrap = around(xAxis,yAxis,townLocations,1)
        #Checks if trap is near
        if senseableTrap[0]:
            #If the 0th index is a boolean repersenting if the player is near a trap
            trapSensed = random.randint(1,10)
            #Chance of sensing trap
            if trapSensed == 1:
                print("You feel uneasy around your current area. You better watch your step.")
                print("---------------------------------------------------------------------")
    #mountians
    #The purpose of mountains is mainly 2 things; to gain a lot of shrinestones and to get a better look around the area
    mountainCheck = checkLocation(xAxis,yAxis,mountains)
    if mountainCheck:
        print("You are at the base of a mountain")
        climb = input("Try to climb the mountain?(y/n) ")
        if climb == "y":
            print("You attempt to scale the mountain")
            success = random.randint(1,3)
            if success == 1:
                print("You made it to the top of the mountain!")
                foundShrinestones = random.randint(5,15)
                print("You found "+str(foundShrinestones)+" shrinestones!")
                user.setShrinestones(foundShrinestones,"+")
                #Not only user gains shrinestones as a reward but they also get a better look across the land
                #For explanations of what this does, look at the around function
                print("You look arcoss the land from the mountain")
                townLocations = sortClosest(xAxis,yAxis,townLocations)
                canSeeTown = around(xAxis,yAxis,townLocations,15)
                if canSeeTown[0]:
                    print("You see a town in the distance {} of you".format(canSeeTown[2]+canSeeTown[1]))
                    theTowns = canSeeTown[3]
                    theClosestTown = theTowns[0]
                    if theClosestTown[0] > 5 or theClosestTown[1] > 5:
                          print("Its quite far away")
                    else:
                        print("Its quite close")
                    if len(theTowns) > 1:
                        print("There are also "+str(len(canSeeTown[3])-1)+" other towns you can see")
                    print("--------------------------")
                shrineLocations= sortClosest(xAxis,yAxis,shrineLocations)
                canSeeShrine = around(xAxis,yAxis,shrineLocations,15)
                if canSeeShrine[0]:
                    #this decides whether to put the dash in for directions like north-west
                    print("You see a shrine in the distance {} of you".format(canSeeTown[2]+canSeeTown[1]))
                    theShrines = canSeeShrine[3]
                    theClosestShrine = theShrines[0]
                    if theClosestShrine[0] > 5 or theClosestShrine[1] > 5:
                          print("Its quite far away")
                    else:
                        print("Its quite close")
                    if len(theShrines) > 1:
                        print("There are also "+str(len(canSeeShrine[3])-1)+" other shrines you can see")
                    print("--------------------------")
                canSeeMountain = around(xAxis,yAxis,mountains,20)
                if canSeeMountain[0]:
                    if len(canSeeMountain[3]) > 1:
                        print("There are also "+str(len(canSeeMountain[3])-1)+" other mountains you can see")
                    print("--------------------------")
                print("\n")
            else:
                print("You tried to climb the mountain but you slipped")
                fallDamage = random.randint(3,7)
                print("You took "+str(fallDamage)+" damage")
                user.setCurrentHealth(fallDamage,"-")
                running = user.deadCheck()
                if running == False:
                    continue
                print("You back away from the mountain in shame")
                if user.playerMovements[-1] == "w":
                    yAxis -= 1
                elif user.playerMovements[-1] == "s":
                    yAxis += 1
                elif user.playerMovements[-1] == "d":
                    xAxis -= 1
                elif user.playerMovements[-1] == "a":
                    yAxis += 1
                continue
        else:
            print("You back away from the mountain")
            if user.playerMovements[-1] == "w":
                yAxis -= 1
            elif user.playerMovements[-1] == "s":
                yAxis += 1
            elif user.playerMovements[-1] == "d":
                xAxis -= 1
            elif user.playerMovements[-1] == "a":
                yAxis += 1
            continue
    else:
        canSeeMountain = around(xAxis,yAxis,mountains,10)
        if canSeeMountain[0]:
            print("You see a mountain in the distance {} of you".format(canSeeMountain[2]+canSeeMountain[1]))
            if len(canSeeMountain[3]) > 1:
                print("There are also "+str(len(canSeeMountain[3])-1)+" other mountains you can see")
            print("--------------------------------------------------------")
    #Treasure
    treasureCheck = checkLocation(xAxis,yAxis,treasureLocations)
    if treasureCheck:
        print("You see something in the ground.")
        print("Its a treasure chest!")
        user.addToNotes("Found a treasure chest at "+str(xAxis)+", "+str(yAxis))
        unknowns = removeFromList((xAxis,yAxis),unknowns)
        treasureLocations.remove((xAxis,yAxis))
        print("You gained "+str(disXp)+" xp")
        user.checkLvl(disXp)
        lootFound(80,130)
    #quests
    #There are places in the world you can obtain a quest for xp and gold
    questLocationCheck = checkLocation(xAxis,yAxis,questLocations)
    if questLocationCheck:
        newQuest = justDiscovered(xAxis,yAxis,user.getNotes(),"Quest: ")
        if newQuest:
            print(random.choice(questFlavorText))
            questType = random.choice(questTypeList)
            questCompletionAmount = random.randint(10,30) * user.getLvl()           
            user.addQuest(questCompletionAmount,questType)
            #Obtained the quest so now we can remove the location so user can't trigger it again
            questLocations.remove((xAxis,yAxis))
            unknowns = removeFromList((xAxis,yAxis),unknowns)
            playerQuests = user.getQuests()
            currentQuest = playerQuests[-1]
            #Gets the most recently added quests (That would be the one just added in this case)
            if currentQuest.getQuestType() == "damage":
                user.addToNotes("Quest: Deal {} damage".format(str(questCompletionAmount)))
            elif currentQuest.getQuestType() == "defend":
                user.addToNotes("Quest: Block {} damage".format(str(questCompletionAmount)))
            elif currentQuest.getQuestType() == "heal":
                user.addToNotes("Quest: Heal {} health".format(str(questCompletionAmount)))
            else:
                #In case something went wrong, I'll scold myself
                print("Bruh i did a stoooopid")
    #Kingdoms
    #Kingdoms are mainly for fast travel in the beginning of the game and to find towns early on so more fast travel can happen
    inKingdom = checkLocation(xAxis,yAxis,kingdomLocations)
    if inKingdom:
        print("You are in a kingdom at "+str(xAxis)+", "+str(yAxis))
        alreadyAsked = False
        while inKingdom:
            print("--------------------------------")
            action = input("1:ASK FOR DIRECTIONS 2:TALK TO LOCALS X:LEAVE")
            if action == "1":
                if alreadyAsked == False:
                    print("You ask round for directions")
                    #Chooses a random cordnate form towns
                    cord = random.choice(townLocations)
                    print("You hear about a town at "+str(cord[0])+", "+str(cord[1]))
                    user.addToNotes("You hear about a town at "+str(cord[0])+", "+str(cord[1]))
                    #Adds an unknown location so the town will appear as a ? on the map
                    if unknowns != None:
                        unknowns.append((cord[0],cord[1]))
                    alreadyAsked = True
                else:
                    print("All you hear are places you've already heard about")
            
            elif action == "2":
                interaction = random.choice(localFlavorTexts)
                #interaction is a list; 0th index is the text and the 1st is a fun value (an interaction might have a special effect)
                print(interaction[0])
                if interaction[1] == 1:
                    print("OH NO")
            elif action.lower() == "x":
                print("You get ready to leave the kingdom")
                inKingdom = False
    else:
        kingdomLocations = sortClosest(xAxis,yAxis,kingdomLocations)
        canSeeKingdom = around(xAxis,yAxis,kingdomLocations,3)
        if canSeeKingdom[0]:
            print("You see a kingdom in the distance {} of you".format(canSeeKingdom[2]+canSeeKingdom[1]))
            print("--------------------------------------------------------")
    #Towns
    #Used mainly for buying and selling items
    inTown = checkLocation(xAxis,yAxis,townLocations)
    if inTown:
        #Check if this is the first time discovering
        newTown = justDiscovered(xAxis,yAxis,user.getNotes(),"Found a town at ")
        if newTown:
            print("You found a town.")
            user.addToNotes("Found a town at "+str(xAxis)+", "+str(yAxis))
            discoveredTowns.append((xAxis,yAxis))
            print("You gained "+str(disXp)+" xp")
            user.checkLvl(disXp)
            #This next part is filling the shop with items
            stock = fillStock(normWeapons,normSpells)
            questGossip = (random.randint(-30,30),random.randint(-30,30))
                
        else:
            print("You're in a town at "+str(xAxis)+", "+str(yAxis))
        
        while inTown:
            print("--------------------------------")
            print("1:BUY 2:SELL 3:FIND WORK X:LEAVE")
            action = input("What would you like to do in the town?")
            costMultiplier = 60
            if action == "1":
                print("You walk into a shop \n")
                shopping = True
                while shopping:
                    for item in stock:
                        print(item[0])
                    if len(stock) == 0:
                        print("There are no more items in the shop.")
                        break
                    buy = input("What would you like to buy? ")
                    if buy.lower() == "x":
                        shopping = False
                        continue
                    for item in stock:
                        if buy == item[0]:
                            if len(item) == 5 or len(item) == 6:
                                removeMe = item
                                if len(item) == 5:
                                    item = list(item)
                                    item.append(False)
                                product = statSpell.statSpellClass(item[0],item[1],item[2],item[3],item[4],item[5])
                                price = product.getCost() + product.getAmount() * costMultiplier
                                price -= user.getLvl()
                                if product.getIsSpecial():
                                    price += 800
                                #A level discount
                            elif len(item) == 2 or len(item) == 3:
                                removeMe = item
                                if len(item) == 2:
                                    item = list(item)
                                    item.append(False)
                                product = weapon.weaponClass(item[0],item[1],item[2])
                                price = product.getDamage() * costMultiplier
                                price -= user.getLvl()
                                if product.getIsSpecial():
                                    price += 800
                            break
                    else:
                        print("That item is not in the shop")
                        continue
                    product.getDescription()
                    user.showEquipted()
                    print("Your money: "+str(user.getMoney()))
                    confirm = input("This costs {}. Buy it?(y/n) ".format(price))
                    if confirm.lower() == "y":
                        if user.getMoney() - price < 0:
                            print("Not enough money")
                        else:
                            user.setMoney(price,"-")
                            if len(removeMe):
                                user.addInven(removeMe[0],removeMe[1])
                            elif len(removeMe) == 5 or len(removeMe) == 6:
                                user.addInven(removeMe[0],removeMe[1],removeMe[2],removeMe[3],removeMe[4])
                            stock.remove(removeMe)
                            print("You bought the "+product.getName())
                    action = input("Would you like to continue shopping?(y/n)")
                    if "n" in action.lower():
                        shopping = False
            elif action == "2":
                print("You walk into a shop \n")
                selling = True
                while selling:
                    yourItems = user.getInvenList()
                    for item in yourItems:
                        print(item[0])
                    #Prints iventory item names
                    sell = input("What would you like to sell? (Press X to quit)")
                    if sell.lower() == "x":
                        selling = False
                        continue
                    #Checks if user wants to quit
                    for item in yourItems:
                        if sell == item[0]:
                            thing = item
                            break
                    #Checks if input is equal to any of the names
                    else:
                        print("Item not found")
                        continue
                    price = 0
                    for value in item:
                        if type(value) == int:
                            price += value
                    if item[-1] == True:
                        price += 100
                    #Price uses each numeric value in the item 
                    price *= costMultiplier
                    confirm = input("Your "+thing[0]+" is worth "+str(price)+" coins. Sell it?(y/n)")
                    if confirm == "y":
                        stock.append(thing)
                        user.setMoney(price,"+")
                        user.removeInven(thing)
                        print("You sold your "+thing[0]+" for "+str(price)+" coins")
                    action = input("Continue selling?(y/n)")
                    if action == "n":
                        selling = False
            elif action == "3":
                print("You ask around town for work")
                #Might select from more things in the future
                if not "You hear about an area of interest at "+str(questGossip[0])+", "+str(questGossip[1]) in user.getNotes():
                    print("You hear about an area of interest at "+str(questGossip[0])+", "+str(questGossip[1]))
                    user.addToNotes("You hear about an area of interest at "+str(questGossip[0])+", "+str(questGossip[1]))
                    if unknowns != None:
                        unknowns.append((questGossip[0],questGossip[1]))
                    questLocations.append((questGossip[0],questGossip[1]))
                else:
                    print("All you hear are things you already know")
            elif action.lower() == "x":
                print("You get ready to leave town")
                print("---------------------------")
                inTown = False
    else:
        #Check in player can see a town
        townLocations = sortClosest(xAxis,yAxis,townLocations)
        canSeeTown = around(xAxis,yAxis,townLocations,3)
        if canSeeTown[0]:
            print("You see a town in the distance {} of you".format(canSeeTown[2]+canSeeTown[1]))
            print("--------------------------------------------------------")
    #Shrines
    #The main objective of the game. You can also use your shrinestones to get good items and upgrade your stats here
    shrineCheck = checkLocation(xAxis,yAxis,shrineLocations)
    if shrineCheck:
        firstTime = justDiscovered(xAxis,yAxis,user.getNotes(),"Found a shrine at ")
        if firstTime:
            print("You found a shrine!")
            user.addToNotes("Found a shrine at "+str(xAxis)+", "+str(yAxis))
            discoveredShrines.append((xAxis,yAxis))
            print("You gained "+str(disXp)+" xp")
            user.checkLvl(disXp)
            numDiscoveredShrines += 1
            totalShrineCheck(numDiscoveredShrines,numOfShrines)
            senseableShrineLocations.remove((xAxis,yAxis))
        else:
            print("You are at a shrine")
        print("Shrinestones: "+str(user.getShrinestones()))
        action = input("Make an offering?(y/n)")
        if "y" in action:
            offering = True
            while offering:
                print("------------------------")
                print("Shrinestones: "+str(user.getShrinestones()))
                print("1:UPGRADE 2:WISH X:LEAVE")
                action = input("What would you like to do?")
                if action == "1":
                    #Upgrade stat
                    user.showStats()
                    print("h:health a:attack d: defence s:speed m:mana")
                    upStat = input("Select a stat to upgrade. ")
                    print("Every point costs a shrinestone")
                    #Checks each stat. The function returns a boolan
                    thisStat = user.shrineUpgradeStat(upStat,"h","max health")
                    if not thisStat:
                        thisStat = user.shrineUpgradeStat(upStat,"m","max mana")
                        if not thisStat:
                            thisStat = user.shrineUpgradeStat(upStat,"s","speed")
                            if not thisStat:
                                thisStat = user.shrineUpgradeStat(upStat,"d","defence")
                                if not thisStat:
                                    thisStat = user.shrineUpgradeStat(upStat,"a","attack")
                elif action == "2":
                    #Wishing for an items
                    amount = input("How many shrinestones will you wish with? ")
                    try:
                        amount = int(amount)
                    except:
                        continue
                    if user.getShrinestones() - amount < 0:
                        print("Not enough shrinestones")
                        continue
                    elif amount <= 0:
                        print("You must offer shrinestones")
                        continue
                    else:
                        print("You offered "+str(amount)+" shrinestones.")
                        user.setShrinestones(amount,"-")
                        maxLuckyness = 100 + amount
                        lootFound(81,maxLuckyness)
                elif action.lower() == "x":
                    print("You prepare to leave the shrine")
                    print("-------------------------------")
                    offering = False
        else:       
            print("You decide to let the shrine be.")
    else:
        #Check if player can sense a shrine
        senseableShrineLocations = sortClosest(xAxis,yAxis,senseableShrineLocations)
        nearShrine = around(xAxis,yAxis,senseableShrineLocations,7)
        if nearShrine[0]:
            #this decides whether to put the dash in for directions like north-west
            print("You sense an intense energy source {} of you".format(nearShrine[2]+nearShrine[1]))
            print("--------------------------------------------------------")
    #If the player goes outside the map boundries, they start to lose health. The damage inrease if the player continues to stay out of bounds
    if xAxis > 30 or yAxis > 30:
        print("You begin to feel an immense sense of doom. You better go back")
        user.setCurrentHealth(outOfBounds,"-")
        running = user.deadCheck()
        if running == False:
            continue
        outOfBounds *= 2
        print("Your energy starts to drain")
        print("Hp: "+str(user.getCurrentHealth())+"/"+str(user.getMaxHealth()))

    #MOVEMENT/ACTIONS
    print("\n============================================================================")
    print("According to your map, you are at "+str(xAxis)+" latitude and "+str(yAxis)+" longitude.")
    travel = input("Would you like to move(WASD) or other actions(Any other key)?")
    if "w" in travel.lower():
        yAxis += 1
        user.playerMovements.append("w")
        print("You decide to travel North.")
    elif "d" in travel.lower():
        xAxis += 1
        user.playerMovements.append("d")
        print("You decide to travel East.")
    elif "s" in travel.lower():
        yAxis += -1
        user.playerMovements.append("s")
        print("You decide to travel South.")
    elif "a" in travel.lower():
        xAxis += -1
        user.playerMovements.append("a")
        print("You decide to travel West.")
    elif nameType.lower() == "devMode":
        print("Dev Mode activated")
        print("This does nothing lol")
        #Call function
    else:
        #Other actions
        print("You decide to rest for a moment")
        resting = True
        while resting:
            print("--------------------------------------------")
            print("1:World Information 2:Rest 3:Look at character 4:Fast travel 5:Look at quests X:Continue with your journey")
            do = input("What would you like to do? ")
            if do == "1":
                print("1:LOOK AT NOTES 2:LOOK AT MAP X:GO BACK")
                do = input("What would you like to look at? ")
                if do == "1":
                    user.showNotes()
                elif do == "2":
                    worldMap(xAxis,yAxis,mapGrid,discoveredTowns,discoveredShrines,unknowns,mountains,kingdomLocations)
            elif do == "2":
                print("1:SLEEP 2:MEDITATE X:GO BACK")
                do = input("What would you like to do? ")
                if do == "1":
                    print("You decide to sleep")
                    user.setCurrentHealth(user.getMaxHealth(),"=")
                    user.setCurrentMana(user.getMana(),"=")
                    print("Health and mana restored")
                    print("You wake up feeling refreshed")
                    resting = False
                elif do == "2":
                    print("You sit down and relax. You focus your energy on the world around you.")
                    senseableShrineLocations = sortClosest(xAxis,yAxis,senseableShrineLocations)
                    nearShrine = around(xAxis,yAxis,senseableShrineLocations,25)
                    if nearShrine[0]:
                        #this decides whether to put the dash in for directions like north-west
                        print("You sense an intense energy source {} of you".format(nearShrine[2]+nearShrine[1]))
                    else:
                        print("There seemes to be no sign of high energy around you")
            elif do == "3":
                print("1:LOOK AT STATS 2:LOOK AT EQUIPTED 3:LOOK AT INVENTORY X:GO BACK")
                do = input("What would yo like to look at? ")
                if do == "1":
                    user.showStats()
                elif do == "2":
                    user.showEquipted()
                elif do == "3":
                    user.inven()
            elif do == "4":
                action = input("Kingdom fast travel or town fast travel(t/k)")
                if action.lower() == "t":
                    i = 1
                    for town in discoveredTowns:
                        print(str(i)+": Town "+str(town[0])+", "+str(town[1]))
                        i += 1
                    else:
                        if len(discoveredTowns) == 0:
                            print("You have not discovered any towns")
                            continue
                    townChoice = input("What place would you like to go to?")
                    try:
                        townChoice = int(townChoice)
                        goToThis = discoveredTowns[townChoice-1]
                        xAxis = goToThis[0]
                        yAxis = goToThis[1]
                        print("Fast traveled to the place")
                    except:
                        print("Not a valid number")
                
                elif action.lower() == "k":
                    i = 1
                    for town in kingdomLocations:
                        print(str(i)+": Kingdom "+str(town[0])+", "+str(town[1]))
                        i += 1
                    townChoice = input("What place would you like to go to?")
                    try:
                        townChoice = int(townChoice)
                        goToThis = kingdomLocations[townChoice-1]
                        xAxis = goToThis[0]
                        yAxis = goToThis[1]
                        print("Fast traveled to the place")
                    except:
                        print("Not a valid number")
            elif do == "5":
                questCounter = 0
                for note in user.getNotes():
                    if "Quest: " in note:
                        print(note)
                        allQuests = user.getQuests()
                        #Returns a list of objects
                        currentQuest = allQuests[questCounter]
                        #Get the quest object
                        print(str(currentQuest.getAmount())+"/"+str(currentQuest.getTotal()))
                        questCounter += 1
                else:
                    if questCounter == 0:
                        print("You have no quests")
            elif do.lower() == "x":
                print("Satified with your break, you continue with your journey.")
                resting = False
        continue
    #EVENT CHECKING
    event = random.randint(1,100)
    #monster event
    if event >= 1 and event <= 40:
        #Player can't fight an enemy at spawn
        if xAxis == 0 and yAxis == 0:
            print("You felt a strange chill down your spine")
            continue
        enemies = enemyDifficulty(xAxis,yAxis,enemies1,enemies2,enemies3,enemies4,enemies5)
        m = random.choice(enemies)
        m = list(m)
        #Converts to a list cuz enemies are origanally tuples
        scale = user.getLvl() - 1
        #This next part scales the stats with the player
        #Starts at 1 because 0 index is the name which is a string
        i = 1
        while i < 6:
            j = 0
            while j < scale:
                m[i] += 1 
                j += 1
            i += 1
        monster = enemy.enemyClass(m[0],m[1],m[2],m[3],m[4],m[5],m[6])
        print("You found a "+monster.getName())
        running = mainCombatLoop(user,monster)
        if running == False:
            continue
    #Found a coordinate event
    #===============================================================================================================================================================================================
    elif event >= 41 and event <= 100:
        print("You find a rag on the ground with cordnates")
        catagory = random.randint(1,4)
        if catagory == 1:
            cord = random.choice(townLocations)
            user.addToNotes("Found what looks like a city with the cordnates "+str(cord[0])+", "+str(cord[1]))
            print(cord)
        elif catagory == 2:
            cord = (random.randint(mapGrid*-1,mapGrid),random.randint(mapGrid*-1,mapGrid))
            treasureLocations.append(cord)
            user.addToNotes("Found some sort of treasure map with the cordnates "+str(cord[0])+", "+str(cord[1]))
            print(cord)
        elif catagory == 3:
            cord = random.choice(shrineLocations)
            user.addToNotes("Found a mysterious rag with cordnates "+str(cord[0])+", "+str(cord[1]))
            print(cord)
        #>:)
        elif catagory == 4:
            cord = random.choice(trapLocations)
            user.addToNotes("Found a mysterious rag with cordnates "+str(cord[0])+", "+str(cord[1]))
            print(cord)
        if unknowns != None:
            unknowns.append((cord[0],cord[1]))
    #At the end of the "turn", player regenarates health and mana
    user.regen()
