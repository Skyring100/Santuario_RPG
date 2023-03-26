class weaponClass:
    def __init__(self,name,damage,isSpecial):
        self.name = name
        self.damage = damage
        self.isSpecial = isSpecial
    def getName(self):
        return self.name
    def getDamage(self):
        return self.damage
    def getDescription(self):
        print("Name: "+self.getName())
        print("Damage: "+str(self.getDamage()))
        if self.getIsSpecial() == True:
            if self.name == "Hammer of Decimation":
                print("Special effect: Increases your attack but also lowers your speed after every successful hit")
            elif self.name == "Cuffs of Lightning":
                print("Special effect: Increases your speed after every successful hit")
            elif self.name == "Blood Blade":
                print("Special effect: You steal health from the enemy, healing as much as you deal")
    def getIsSpecial(self):
        return self.isSpecial
    def changeWeapon(self,name,damage):
        self.name = name
        self.damage = damage

    #These are special weapons that have a unique effect when used
    def weaponEffect(self,user,enemy,damageDealt):
        name = self.getName()
        if name == "Blood Blade":
            user.setCurrentHealth(damageDealt,"+")
            print("You gained "+str(damageDealt)+" health!")
            user.healthCap()
        elif name == "Hammer of Decimation":
            user.setAttack(3,"+")
            user.setSpeed(3,"-")
            print("The hammer brought down your speed!")
            print("The hammer also brought up your attack")
        elif name == "Cuffs of Lightning":
            user.setSpeed(5,"+")
            print("Your speed was raised!")
