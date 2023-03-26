class questClass:
    def __init__(self,total,qType):
        #qType is what kind of quest (heal, block, or damage)
        #total is the amount of thing needed to complete the quest
        self.total = total
        self.amount = 0
        self.xpGain = self.total * 2
        self.qType = qType
    def setAmount(self,amount,m,user):
        if m == "+":
            self.amount += amount
        elif m == "-":
            self.amount -= amount
        elif m == "=":
            self.amount = amount
        #checks if quest is complete
        if self.amount >= self.total:
            print("---------------")
            print("QUEST COMPLETED")
            print("---------------")
            user.checkLvl(self.xpGain)
            user.setMoney(1000,"+")
            print("You gained "+str(self.xpGain)+" xp and 1000 gold")
            for quest in user.getQuests():
                if quest.getAmount() >= quest.getTotal():
                    newQuests = user.quests.remove(quest)
                    user.setQuests(newQuests)
            return True
        else:
            return False
        #Returns a boolean for if quest is complete
    def getTotal(self):
        return self.total
    def getAmount(self):
        return self.amount
    def getXpGain(self):
        return self.xpGain
    def getQuestType(self):
        return self.qType
