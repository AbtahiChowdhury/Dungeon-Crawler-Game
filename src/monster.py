class Monster():
    def __init__(self,difficulty):
        self.difficulty=difficulty
        self.maxhp=difficulty*5
        self.currenthp=difficulty*5
        self.strength=int(difficulty*1.5)
        self.defence=difficulty
    
    def takeDamage(self,amount):
        if self.currenthp-amount<0:
            self.currenthp=0
            return -1
        else:
            self.currenthp-=amount
    
    def getMaxHp(self):
        return self.maxhp
    def getCurrentHp(self):
        return self.currenthp
    def getStrength(self):
        return self.strength
    def getDefence(self):
        return self.defence
    def getDifficulty(self):
        return self.difficulty
