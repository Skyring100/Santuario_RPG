import random
class enemyClass:
    isBoss = False
    def __init__(self, name, h, a, d, s, r, xp):
        self.name = name
        self.maxHealth = h
        self.currentHealth = h
        self.attack = a
        self.defence = d
        self.speed = s
        self.runAway = r
        self.xp = xp
        if self.name == "Grim Reaper":
            isBoss = True
    #set functions
    def setMaxHealth(self,amount,m="="):
        if m == "=":
            self.maxHealth = amount
        elif m == "+":
            self.maxHealth += amount
        elif m == "-":
            self.maxHealth -= amount
    def setCurrentHealth(self,amount,m="="):
        if m == "=":
            self.currentHealth = amount
        elif m == "+":
            self.currentHealth += amount
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
    def getIsBoss(self):
        return self.isBoss
    def getRunAway(self):
        return self.runAway
    def getXp(self):
        return self.xp
    def showStats(self):
        print("-----------------")
        print(self.getName()+" Stats")
        print("Max Health: "+str(self.getMaxHealth()))
        print("Attack: "+str(self.getAttack()))
        print("Defence: "+str(self.getDefence()))
        print("Speed: "+str(self.getSpeed()))
    def battle(self, user, defending):
        #doge
        if defending:
            maxSpeed = user.getSpeed() + 5 * user.getLvl() / 2
            #Blocking scales up with your lvl. However, i dont want it to be too absurd so i divide by 2
            maxSpeed = round(maxSpeed * 1)
            #Round to not get decimal and * 1 to make sure its not 0
            userSpeedRoll = random.randint(1,maxSpeed)
        else:
            if user.getSpeed() < 1:
                user.setSpeed(1,"=")
            userSpeedRoll = random.randint(1,user.getSpeed())
        enemySpeedRoll = random.randint(1,self.getSpeed())
        if userSpeedRoll > enemySpeedRoll+2:
            #I added + 2 so its harder to dodge
            print("You doged the "+self.getName()+"'s attack!")
        else:
            damage = random.randint(1,self.getAttack())
            #Apply defence
            if defending:
                maxDefence = user.getDefence() + 5 * user.getLvl() / 2
                #Blocking scales up with your lvl. However, i dont want it to be too absurd so i divide by 2
                maxDefence = round(maxDefence * 1)
                blocked = random.randint(1,maxDefence)
                damage -= blocked
            else:
                blocked = random.randint(1,user.getDefence())
                damage -= blocked
            #Defend quest checking
            checkQuests = user.getQuests()
            for quest in checkQuests:
                if quest.getQuestType() == "defend":
                    quest.setAmount(blocked,"+",user)
            if damage <= 0:
                print("The "+self.getName()+" tried to attack you but you didn't feel a thing.")
            else:
                print("The "+self.getName()+" dealt "+str(damage)+" damage")
                user.setCurrentHealth(damage, "-")
        #i started making a boss battle but i didn't get to finish it
        #checks if the enemy is a boss
        def bossBattle(self,user,defender):
            bossName = self.getName()
            if bossName == "Grim Reaper":
                grimReaperBattle(user,defender)
        #boss battle
        def grimReaperBattle(self,user,defender):
            flavorText = ["The Grim Reaper laughs at your petty excuse for a weapon.","The Grim Reaper swings his lantern from side to side, taunting you.",
                          "You can see all the suffering souls within the Grim Reaper's lantern.","You hear screams of agony from within the lantern."]
            print(random.choice(flavorText))
            #Do logic here
            randMove = random.randint(1,10)
            if self.getCurrentHealth() < self.getMaxHealth/2 and randMove > 5:
                print("The Grim Reaper draws life force from the world around it.")
                print("You start to feel uneasy.")
                self.battle(user,defending)
                healGain = random.randint(1,15)
                self.setCurrentHealth(healGain,"+")
                print("The Grim Reaper gained "+str(healGain)+" health")
                self.setSpeed(5,"-")
                print("The Grim Reaper's speed dropped!")
            else:
                print("The Grim Reaper lunges at you with it's scythe!")
                i = 0
                slash = "\\"
                while i < 70:
                    print(slash)
                    slash = " "+slash
                    i += 1
                self.battle(user,defending)
                self.setSpeed(3,"+")
                print("The Grim Reaper's speed rose!")

    
    
