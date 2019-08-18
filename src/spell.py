import csv

class Spell():
    def __init__(self,name,description,cost,multiplier,spelltype):
        self.name=name
        self.description=description
        self.cost=cost
        self.multiplier=multiplier
        self.spelltype=spelltype
    
    def getName(self):
        return self.name
    def getDescription(self):
        return self.description
    def getCost(self):
        return self.cost
    def getMultiplier(self):
        return self.multiplier
    def getSpellType(self):
        return self.spelltype

#List of Spells
fire=Spell('Fire','[insert description]',10,0.75,'damage')
thunder=Spell('Thunder','[insert description]',30,1.5,'damage')
shield=Spell('Shield','[insert description]',15,0.25,'buff')
trap=Spell('Trap','[insert description]',15,0.1,'debuff')
heal=Spell('Heal','[insert description]',20,2,'heal')

#Dictionary of Spells
spelldictionary={'fire':fire,
                 'thunder':thunder,
                 'shield':shield,
                 'trap':trap,
                 'heal':heal}