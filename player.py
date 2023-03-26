import weapon
import statSpell
import quests
import random
class playerClass:
    xp = 0
    #the indivual points til next lvl. This might be hidden from user
    lvl = 1
    #The lvl milestone player is at
    lvlUpRe = 10
    #The level up requirement
    notes = []
    eqWeapon = weapon.weaponClass("Pet Rock",0,False)
    eqSpell = statSpell.statSpellClass("Repair",1,"h",1,"p",False)
    #These are placeholders
    money = 0
    invenList = []
    shrinestones = 0
    playerMovements = []
    quests = []
    def __init__(self,name="Joe",h=5,a=5,d=5,s=5,m=5):
        self.name = name
        self.maxHealth = h
        self.currentHealth = self.maxHealth
        self.attack = a
        self.defence = d
        self.speed = s
        self.mana = m
        self.currentMana = self.mana
    #Whenever the user gains xp, we check their level
    def checkLvl(self,amount):
        #amount should be the amount of points you get after defeating enemy
        self.xp += amount
        while self.xp >= self.lvlUpRe:
            self.lvl += 1
            self.lvlUpRe = self.lvlUpRe * 2
            #new level reached. increaed level and level requirement
            increase = 3
            self.maxHealth += increase
            self.currentHealth = self.maxHealth
            self.attack += increase
            self.defence += increase
            self.mana += increase
            self.currentMana = self.mana
            #Stat increases
            print("You leveled up to lvl "+str(self.lvl))
            self.showStats()
    #Set functions
    #I added modes to the set functions: = means setting, + means adding, - means subtracting
    def setMaxHealth(self,amount,m="="):
        if m == "=":
            self.maxHealth = amount
        elif m == "+":
            self.maxHealth += amount
        elif m == "-":
            self.maxHealth -= amount
            self.deadCheck()
    def setCurrentHealth(self,amount,m="="):
        if m == "=":
            self.currentHealth = amount
        elif m == "+":
            self.currentHealth += amount
            #Heal quest checking
            for quest in self.getQuests():
                if quest.getQuestType() == "heal":
                    quest.setAmount(amount,"+",self)
        elif m == "-":
            self.currentHealth -= amount
    def setAttack(self,amount,m="="):
        if m == "=":
            self.attack = amount
        elif m == "+":
            self.attack += amount
        elif m == "-":
            self.attack -= amount
    def setDefence(self,amount,m="="):
        if m == "=":
            self.defence = amount
        elif m == "+":
            self.defence += amount
        elif m == "-":
            self.defence -= amount
    def setSpeed(self,amount,m="="):
        if m == "=":
            self.speed = amount
        elif m == "+":
            self.speed += amount
        elif m == "-":
            self.speed -= amount
    def setMana(self,amount,m="="):
        if m == "=":
            self.mana = amount
        elif m == "+":
            self.mana += amount
        elif m == "-":
            self.mana -= amount
    def setCurrentMana(self,amount,m="="):
        if m == "=":
            self.currentMana = amount
        elif m == "+":
            self.currentMana += amount
        elif m == "-":
            self.currentMana -= amount
    def setMoney(self,amount,m="="):
        if m == "=":
            self.money = amount
        elif m == "+":
            self.money += amount
        elif m == "-":
            self.money -= amount
    def setShrinestones(self,amount,m="="):
        if m == "=":
            self.shrinestones = amount
        elif m == "+":
            self.shrinestones += amount
        elif m == "-":
            self.shrinestones -= amount
    #sets player's equipted weapon
    def setWeapon(self,name,damage,isSpecial=False):
        switch = [self.eqWeapon.getName(),self.eqWeapon.getDamage(),self.eqWeapon.getIsSpecial()]
        #Transforms prevoius equipted weapon to a list for information storage
        self.invenList.append(switch)
        #Add it to iventory
        self.eqWeapon = weapon.weaponClass(name,damage,isSpecial)
        #Reassgin equipted weapon with new data
        print("Equipted "+self.eqWeapon.getName())
    #Same thing as weapon but with spells
    def setSpell(self,name,cost,usage,amount,target,special=False):
        switch = [self.eqSpell.getName(),self.eqSpell.getCost(),self.eqSpell.getUsage(),self.eqSpell.getAmount(),self.eqSpell.getTarget(),self.eqSpell.getIsSpecial()]
        #Transform prevoius equipted weapon to a list for information storage
        self.invenList.append(switch)
        #Add it to iventory
        self.eqSpell = statSpell.statSpellClass(name,cost,usage,amount,target,special)
        print("Equipted "+self.eqSpell.getName())
    #Adds an item to inventory. This expects the spell or weapon data such as name, damage etc.
    def addInven(self,p0,p1,p2="",p3="",p4="",p5=""):
        #First 2 indexes are minumim data for a weapon
        info = [p0,p1,p2,p3,p4,p5]
        removeCounter = 0
        for x in info:
            if x == "":
                removeCounter += 1
        i = 0
        while i < removeCounter:
            info.remove("")
            i += 1
        #We remove any defualts that were set
        self.invenList.append(info)
    def removeInven(self,thing):
        self.invenList.remove(thing)
    #Adds to a note system i made
    def addToNotes(self,thing):
        self.notes.append(thing)
        print("Your notes have been updated")
    #Get functions
    def getName(self):
        return self.name    
    def getMaxHealth(self):
        return self.maxHealth
    def getCurrentHealth(self):
        return self.currentHealth
    def getAttack(self):
        return self.attack
    def getDefence(self):
        return self.defence
    def getSpeed(self):
        return self.speed
    def getMana(self):
        return self.mana
    def getCurrentMana(self):
        return self.currentMana
    def getMoney(self):
        return self.money
    def getLvl(self):
        return self.lvl
    def getNotes(self):
        return self.notes
    def getInvenList(self):
        return self.invenList
    def getShrinestones(self):
        return self.shrinestones
    def showStats(self):
        print("-----------------")
        print(self.getName()+"'s Stats")
        print("Level: "+str(self.getLvl()))
        print("Points til next level: "+str(self.lvlUpRe-self.xp))
        print("Max Health: "+str(self.getMaxHealth()))
        print("Current Health: "+str(self.getCurrentHealth()))
        print("Attack: "+str(self.getAttack()))
        print("Defence: "+str(self.getDefence()))
        print("Speed: "+str(self.getSpeed()))
        print("Max Mana: "+str(self.getMana()))
        print("Current Mana: "+str(self.getCurrentMana()))
    #Notes are a cool thing i added. They hold cordnates of certain places
    def showNotes(self):
        if len(self.notes) == 0:
            print("Your notes are blank")
        else:
            for note in self.notes:
                print("-"+note)
    def showEquipted(self):
        print(self.getName()+"'s Equipted")
        print("------------------")
        self.eqWeapon.getDescription()
        print("------------------")
        self.eqSpell.getDescription()
        print("------------------")
    #This is the inventory function where you can look at your items
    def inven(self):
        inInventory = True
        while inInventory:
            print("Money: "+str(self.money))
            for item in self.invenList:
                print(item[0])
            if len(self.invenList) == 0:
                print("Your inventory is empty")
            action = input("Select an item or type \"x\" to exit ")
            if action.upper() == "X":
                inInventory = False
            else:
                try:
                    #have the option to access items through their index
                    thing = self.invenList[int(action)]
                except:         
                    for item in self.invenList:
                        if action == item[0]:
                            thing = item
                            break
                    else:
                        print("Item not found")
                        continue
                if len(thing) == 2 or len(thing) == 3 :
                    if len(thing) == 2:
                        thing.append(False)
                    selected = weapon.weaponClass(thing[0],thing[1],thing[2])
                elif len(thing) == 5 or len(thing) == 6:
                    if len(thing) == 5:
                        thing.append(False)
                        #Adding False for isSpecial. Most of the time there is no need to specify this parameter (its an optional parameter)but it will be needed for clarity in storage
                    selected = statSpell.statSpellClass(thing[0],thing[1],thing[2],thing[3],thing[4],thing[5])
                selected.getDescription()
                print("1:EQUIPT 2:DISCARD X:BACK\n")
                
                if selected.getName() == "Murray Cube":
                    print("Or you can use the cube's power...")
                    ACTIVATEMURRAYCUBE = input("Use it's power?(y/n)")
                    if ACTIVATEMURRAYCUBE == "y":
                        print("Are you sure about this? There is no going back")
                        confirm = input("Type YES to confirm")
                        if confirm == "YES":
                            print("This is NOT a joke. If anything were to happen, it would be ENTIRELY YOUR FAULT")
                            confirm = input("Type YES to confirm")
                            if confirm == "YES":
                                print("This is your LAST CHANCE of thinking about your decision. ARE. YOU. SURE?!")
                                confirm = input("Type YES to confirm")
                                if confirm == "YES":
                                    input("Don't say I didn't warn you.")
                                    selected.murrayCube(self)
                
                action = input("What would you like to do with "+thing[0])
                if action == "1":
                    if len(thing) == 3:
                        self.setWeapon(thing[0],thing[1])
                        self.invenList.remove(thing)
                    elif len(thing) == 5 or len(thing) == 6:
                        if len(thing) == 6:
                            thing.append(False)
                        #Adding False for isSpecial. Most of the time there is no need to specify this parameter (its an optional parameter)but it will be needed for clarity in storage
                        self.setSpell(thing[0],thing[1],thing[2],thing[3],thing[4],thing[5])
                        self.invenList.remove(thing)
                    else:
                        print("Error: Thing length is uncharted")
                        print("Length:"+str(len(thing)))
                elif action == "2":
                    self.invenList.remove(thing)
                    print("Discarded "+thing[0])
                    
    #Attacking a monster      
    def battle(self, enemy):
        print("You attack the "+enemy.getName()+" with your "+self.eqWeapon.getName())
        #Speed rolls to see if enemy will dodge
        userSpeedRoll = random.randint(1,self.getSpeed())
        enemySpeedRoll = random.randint(1,enemy.getSpeed())
        if enemySpeedRoll > userSpeedRoll+2:
            #I added + 2 so its harder to dodge
            print("The "+enemy.getName()+" doged your attack!")
            return False
        else:
            #If attack wasn't dodged, apply defence to damage
            damage = random.randint(1,self.getAttack()) + self.eqWeapon.getDamage()
            damage -= random.randint(1,enemy.getDefence())
            if damage <= 0:
                print("You hit the "+enemy.getName()+" but you didn't even faze it.")
                return False
            enemy.setCurrentHealth(damage, "-")
            #Damage quest checking
            for quest in self.getQuests():
                if quest.getQuestType() == "damage":
                    quest.setAmount(damage,"+",self)
            print("You did "+str(damage)+" damage!")
            #checks if weapon has a special effect
            if self.eqWeapon.getIsSpecial():
                self.eqWeapon.weaponEffect(self,enemy,damage)
    #using a spell         
    def useStatSpell(self,enemy):
        if self.eqSpell.getCost() > self.getCurrentMana():
            print("Not enough mana")
        else:
            self.setCurrentMana(self.eqSpell.getCost(),"-")
            target = self.eqSpell.getTarget()
            stat = self.eqSpell.getUsage()
            amount = self.eqSpell.getAmount()
            print("You cast "+self.eqSpell.getName())
            #target is enemy
            if target == "e":
                #Spell dodge rolls only involve the defender and the user's mana
                enemySpeedRoll = random.randint(1,enemy.getSpeed())
                maxHitRate = self.getMana() - self.getCurrentMana()
                maxHitRate += 1
                #+ 1 because we dont want randint(1,0) 
                spellHitRate = random.randint(1,maxHitRate)
                if enemySpeedRoll > spellHitRate :
                    print("The "+enemy.getName()+" doged your attack!")
                    return False
                else:
                    #Depending on the spell, it will change a stat
                    if stat == "h":
                        enemy.setCurrentHealth(amount,"-")
                        print("The "+enemy.getName()+"'s health dropped by "+str(amount))
                    elif stat == "a":
                        enemy.setAttack(amount,"-")
                        print("The "+enemy.getName()+"'s attack dropped by "+str(amount))
                        if enemy.getAttack() < 1:
                            enemy.setAttack(1,"=")
                            print("The "+enemy.getName()+"'s {} cant go any lower!".format("attack"))
                    elif stat == "d":
                        enemy.setDefence(amount,"-")
                        print("The "+enemy.getName()+"'s defence dropped by "+str(amount))
                        if enemy.getDefence() < 1:
                            enemy.setDefence(1,"=")
                            print("The "+enemy.getName()+"'s {} cant go any lower!".format("defence"))
                    elif stat == "s":
                        enemy.setSpeed(amount,"-")
                        print("The "+enemy.getName()+"'s speed dropped by "+str(amount))
                        if enemy.getSpeed() < 1:
                            enemy.setSpeed(1,"=")
                            print("The "+enemy.getName()+"'s {} cant go any lower!".format("speed"))
            #target is player   
            elif target == "p":
                #Depending on the spell, it will change a stat
                if stat == "h":
                    self.setCurrentHealth(amount,"+")
                    print("You gained "+str(amount)+" hp")
                    self.healthCap()
                elif stat == "a":
                    self.setAttack(amount,"+")
                    print("Your attack was raised by "+str(amount))
                elif stat == "d":
                    self.setDefence(amount,"+")
                    print("Your defence was raised by "+str(amount))
                elif stat == "s":
                    self.setSpeed(amount,"+")
                    print("Your speed was raised by "+str(amount))
            #At the very end, check if spell has a unique effect
            if self.eqSpell.getIsSpecial():
                self.eqSpell.spellEffect(self,enemy)
    #Makes sure health is not over max
    def healthCap(self):
        if self.getCurrentHealth() > self.getMaxHealth():
            self.currentHealth = self.maxHealth
            print("Your hp was maxed out")
    #Checks if player is dead; returns a boolean
    def deadCheck(self):
        if self.currentHealth <= 0:
            print("Your vision starts to fade to darkness...")
            input("Enter any key to continue...")
            print("GAME OVER")
            print("Your level: "+str(self.getLvl()))
            print("Total distance traveled: "+str(len(self.playerMovements))+"km")
            '''
            try:
                file = open("highscore.txt","r")
                highscore = file.readline()
                hiscore = highscore.strip()
                highscore = int(highscore)
                file.close()
                if highscore < self.getLvl:
                    print("New Highscore!")
                    file = open("highscore.txt","w")
                    file.write(self.getLvl)
                    file.close()
            except:
                file = open("highscore.txt","w")
                file.write(self.getLvl)
                file.close()
                print("Don't delete files dude. Not cool")
            '''
            return False
        else:
            return True
    #if player tries to run away
    def canRunAway(self, enemy):
        #This will scale with enemy run away difficulty
        canRun = random.randint(1,enemy.getRunAway())
        #This makes it so its easier to run away the higher the lvl
        canRun -= round(self.getLvl()/2)            
        if canRun <= 1:
            return True
        else:
            return False
    #regen mana and health
    def regen(self):
        if self.getCurrentHealth() < self.getMaxHealth():
            self.setCurrentHealth(1,"+")
        if self.getCurrentMana() < self.getMana():
            self.setCurrentMana(1,"+")
    #if player uses shrine to upgrade a stat
    def shrineUpgradeStat(self,upStat,lookFor,text):
        if lookFor in upStat:
            upgradeAmount = input("How much will you upgrade your {} by? ".format(text))
            try:
                upgradeAmount = int(upgradeAmount)
            except:
                print("   ")
                return False 
            if self.getShrinestones() - upgradeAmount < 0:
                print("Not enough shrinestones")
            else:
                self.setShrinestones(upgradeAmount,"-")
                if text == "max health":
                    self.setMaxHealth(upgradeAmount,"+")
                elif text == "attack":
                    self.setAttack(upgradeAmount,"+")
                elif text == "defence":
                    self.setDefence(upgradeAmount,"+")
                elif text == "speed":
                    self.setSpeed(upgradeAmount,"+")
                elif text == "max mana":
                    self.setMana(upgradeAmount,"+")
                print("Your {} was increased by ".format(text)+str(upgradeAmount))
                return True
        else:
            return False
    #looting a spell
    def lootSpell(self,s):
        foundS = statSpell.statSpellClass(s[0],s[1],s[2],s[3],s[4],s[5])
        choosing = True
        while choosing:
            print("You found a "+foundS.getName()+" spell book")
            foundS.getDescription()
            print("1:EQUIPT 2:STORE IN INVENTORY 3:CHECK STATS/EQUIPTED 4:LEAVE IT")
            action = input("What do you want to do?")
            if action == "1":
                self.setSpell(s[0],s[1],s[2],s[3],s[4],s[5])
                print("You equipted the "+foundS.getName())
                choosing = False
            elif action == "2":
                self.addInven(s[0],s[1],s[2],s[3],s[4],s[5])
                print("The spell "+foundS.getName()+" was added to your inventory.")
                choosing = False
            elif action == "3":
                self.showStats()
                self.showEquipted()
            elif action == "4":
                print("You decide to leave the spell")
                choosing = False
    #looting a weapon
    def lootWeapon(self,w):
        foundW = weapon.weaponClass(w[0],w[1],w[2])
        choosing = True
        while choosing:
            print("You found a "+foundW.getName())
            foundW.getDescription()
            print("1:EQUIPT 2:STORE IN INVENTORY 3:CHECK STATS/EQUIPTED 4:LEAVE IT")
            action = input("What do you want to do?")
            if action == "1":
                self.setWeapon(w[0],w[1],w[2])
                print("You equipted the "+foundW.getName())
                choosing = False
            elif action == "2":
                self.addInven(w[0],w[1],w[2])
                print("The "+foundW.getName()+" was added to your inventory.")
                choosing = False
            elif action == "3":
                self.showStats()
                self.showEquipted()
            elif action == "4":
                print("You decide to leave the weapon")
                choosing = False
    #quests
    def addQuest(self,total,qType):
        newQuest = quests.questClass(total,qType)
        self.quests.append(newQuest)
        print("You got a new quest")
    def getQuests(self):
        return self.quests
    def setQuests(self,newQuests):
        self.quests = newQuests

        
        
        
    
