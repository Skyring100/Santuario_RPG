#Spells that affect stats
import random
import time
class statSpellClass:
    isSpecial = False
    def __init__(self,name,cost,usage,amount,target,isSpecial):
        self.name = name
        self.cost = cost
        #cost to cast
        self.usage = usage
        #Spells have a "usage" attribute. This is meant to show what stat it effects
        #h = currentHealth, a = attack, d = defence, s = speed
        self.amount = amount
        #How much it will change a stat by
        self.target = target
        #Target can be "p" for player or "e" for enemy
        #I dont want set functions because i want these varables to never change
        self.isSpecial = isSpecial
    def getName(self):
        return self.name
    def getCost(self):
        return self.cost
    def getAmount(self):
        return self.amount
    def getUsage(self):
        return self.usage
    def getTarget(self):
        return self.target
    def getIsSpecial(self):
        return self.isSpecial
    def getDescription(self):
        print("Name: "+self.name)
        print("Mana Cost: "+str(self.cost))
        if self.getIsSpecial():
            if self.name == "Life Swap":
                print("Description: Switches your current healh with your enemy's")
            elif self.name == "Pure Mana":
                print("Description: Converts all your mana into a damaging attack.")
            elif self.name == "Intertwine":
                print("Description: Detrimentally lowers both your enemy's speed stat and your own")
            elif self.name == "Double Strike":
                print("Description: Attacks your enemy with a damage spell and then attacks with a normal attack")
            elif self.name == "Warp Time":
                print("Description: Stops time and drains both your hp and your enemy's hp until one of you dies")
            elif self.name == "Capture":
                print("Description: Captures your enemy's soul into a totem, turning them into a useable spell")
            elif self.name == "Murray Cube":
                print("Description: A dangerous cube that if given enough time will make the user a god")
        else:
            stat = self.getUsage()
            if stat == "h":
                stat = "health"
            elif stat == "a":
                stat = "attack"
            elif stat == "d":
                stat = "defence"
            elif stat == "s":
               stat = "speed"
            else:
                print("An error has occured")
            if self.getTarget() == "e":
                print("Description: Takes away {} points from the enemy's {} when used".format(self.getAmount(),stat))
            elif self.getTarget() == "p":
                print("Description: Increases your {} by {} when used".format(stat,self.getAmount()))
    #some specific spells have special effects
    def spellEffect(self,user,enemy):
        name = self.getName()
        if name == "Intertwine":
            user.setSpeed(1,"=")
            print("Your speed was lowered!")
        elif name == "Double Strike":
            print("You attack before your enemy could recover!")
            user.battle(enemy)
        elif name == "Life Swap":
            user.setCurrentHealth(enemy.getCurrentHealth(),"=")
            enemy.setCurrentHealth(user.getCurrentHealth(),"=")
            print("Your healths were switched!")
        elif name == "Pure Mana":
            enemy.setCurrentHealth(user.getCurrentMana(),"-")
            print("You channel all your mana into raw energy! You did "+str(user.getCurrentMana())+" damage!")
            user.setCurrentMana(0,"=")
        elif name == "Warp Time":
            print("The world around you halts to a complete stop")
            frozen = True
            while frozen:
                print("You conscrew time to your biding")
                input("Press Enter to continue...")
                while enemy.getCurrentHealth() != 0:
                    enemy.setCurrentHealth(1,"-")
                    user.setCurrentHealth(1,"-")
                    user.deadCheck()
                    print("Killing with time")
                else:
                    print("Your enemy so warped it is unrecognizeable")
                    frozen = False
        elif name == "Capture":
            print("You cast a totem!")
            print("The "+enemy.getName()+" was consumed by the totem")
            enemy.setCurrentHealth(0,"=")
            user.addInven(enemy.getName(),enemy.getMaxHealth()+enemy.getDefence(),"h",enemy.getAttack()+enemy.getSpeed(),"e",False)
            print("You turned the "+enemy.getName()+" to a useable spell!")
        elif name == "Murray Cube":
            murrayCube(user)

    #MURRAY CUBE IS A SUPER SPECIAL LEGENDARY SPELL
    def murrayCube(self,user):
        print("You unleash the power of THE MURRAY CUBE")
        print("The world starts twisting and blurring while also prutruding immense energy. The world begins to shroud itself in darkness.")
        time.sleep(4)
        message = "Press Enter to continue..."
        for letter in message:
            print(letter ,end="")
            time.sleep(0.25)
        input()
        MURRAYED = True
        symbols = ["+","=","-","/","#","@","%","*","*","~","1","2","3","4","5","6","7","8","9","0","b","c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y","z","a","e","i","o","u"]
        start = time.perf_counter()
        while MURRAYED:
            i = 0
            code = ""
            while i < 70:
                code += random.choice(symbols)
                i +=1
            print(code)
            if "murray" in code or "mush" in code:
                end = time.perf_counter()
                MURRAYED = False
                user.setMaxHealth(1000000000,"=")
                user.setCurrentHealth(1000000000,"=")
                user.setAttack(1000000000,"=")
                user.setDefence(1000000000,"=")
                user.setSpeed(1000000000,"=")
                user.setMana(1000000000,"=")
                user.setCurrentMana(1000000000,"=")
                message = "YOU ARE A GOD"
                for letter in message:
                    print(letter ,end="")
                    time.sleep(0.25)
                else:
                    print("\n")
                passed = round(end - start)
                print("Time elasped: "+str(passed)+" seconds")
            
