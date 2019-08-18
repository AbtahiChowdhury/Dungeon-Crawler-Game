import spell
import csv
import math

class Player():
    def __init__(self,name,build):
        self.name=name
        self.build=build.lower()
        self.spelllist={}
        self.itemlist={}
        self.level=1
        self.exp=0
        '''
        Warrior-medium attack,defence,hp, low magic,mp
        Berserker-high attack, medium hp, low defence, no magic,mp
        Guardian-high hp,defence, low attack, no magic,mp
        Paladin-medium defence,hp,magic,mp low attack
        Mage-high attack,magic,mp low defence,hp
        '''
        if self.build=='warrior':
            self.maxhp=100
            self.maxmp=25
            self.currenthp=100
            self.currentmp=25
            self.strength=10
            self.defence=10
            self.magic=5
            self.spelllist.update({'fire':spell.fire, 'trap':spell.trap})
        elif self.build=='berserker':
            self.maxhp=50
            self.maxmp=0
            self.currenthp=50
            self.currentmp=0
            self.strength=20
            self.defence=5
            self.magic=0
        elif self.build=='guardian':
            self.maxhp=150
            self.maxmp=0
            self.currenthp=150
            self.currentmp=0
            self.strength=5
            self.defence=20
            self.magic=0
        elif self.build=='paladin':
            self.maxhp=100
            self.maxmp=50
            self.currenthp=100
            self.currentmp=50
            self.strength=5
            self.defence=10
            self.magic=10
            self.spelllist.update({'fire':spell.fire, 'trap':spell.trap, 'heal':spell.heal})
        elif self.build=='mage':
            self.maxhp=50
            self.maxmp=100
            self.currenthp=50
            self.currentmp=100
            self.strength=2
            self.defence=5
            self.magic=20
            self.spelllist.update({'fire':spell.fire, 'trap':spell.trap, 'heal':spell.heal, 'thunder':spell.thunder, 'shield':spell.shield})

    def takeDamage(self,amount):
        if self.currenthp-amount<0:
            self.currenthp=0
            return -1
        else:
            self.currenthp-=amount
    def healHp(self,amount):
        if self.currenthp+amount>self.maxhp:
            self.currenthp=self.maxhp
        else:
            self.currenthp+=amount
    def useMp(self,amount):
        if self.currentmp-amount<0:
            return -1
        else:
            self.currentmp-=amount
    def regenMp(self,amount):
        if self.currentmp+amount>self.maxmp:
            self.currentmp=self.maxmp
        else:
            self.currentmp+=amount

    def gainExp(self,amount):
        if (self.exp+amount)>(10*self.level):
            self.increaseStats()
            self.exp=(self.exp+amount)-(10*self.level)
        else:
            self.exp+=amount

    def increaseStats(self):
        input('Level Up!')
        self.level+=1
        multiplier=(math.exp((-0.15)*(self.level)))+1
        self.maxhp=int(multiplier*self.maxhp)
        self.maxmp=int(multiplier*self.maxmp)
        self.currenthp=self.maxhp
        self.currentmp=self.maxmp
        self.strength=int(multiplier*self.strength)
        self.defence=int(multiplier*self.defence)
        self.magic=int(multiplier*self.magic)
    
    def learnSpell(self):
        pass

    def getName(self):
        return self.name
    def getBuilt(self):
        return self.build
    def getLevel(self):
        return self.level
    def getExp(self):
        return self.exp
    def getMaxHp(self):
        return self.maxhp
    def getMaxMp(self):
        return self.maxmp
    def getCurrentHp(self):
        return self.currenthp
    def getCurrentMp(self):
        return self.currentmp
    def getStrength(self):
        return self.strength
    def getDefence(self):
        return self.defence
    def getMagic(self):
        return self.magic
    def getSpellList(self):
        return self.spelllist
    def printstats(self):
        return (f'Name\t\t {self.name}\n'
                f'Build\t\t {self.build}\n'
                f'Level\t\t {self.level}\n'
                f'HP\t\t {self.currenthp}/{self.maxhp}\n'
                f'MP\t\t {self.currentmp}/{self.maxmp}\n'
                f'Strength\t {self.strength}\n'
                f'Defence\t\t {self.defence}\n'
                f'Magic\t\t {self.magic}\n')
    
    def loadPlayer(self):
        with open('remote/playerdata') as csv_file:
            csv_reader=csv.reader(csv_file,delimiter=',')
            linecount=0
            for row in csv_reader:
                if linecount==1:
                    self.name=str(row[0])
                    self.build=str(row[1])
                    self.level=int(row[2])
                    self.exp=int(row[3])
                    self.maxhp=int(row[4])
                    self.maxmp=int(row[5])
                    self.currenthp=int(row[6])
                    self.currentmp=int(row[7])
                    self.strength=int(row[8])
                    self.defence=int(row[9])
                    self.magic=int(row[10])
                if linecount>1:
                    self.spelllist.update({row[11]:spell.spelldictionary[row[11]]})
                linecount+=1

    def savePlayer(self):
        with open('remote/playerdata',mode='w') as csv_file:
                csv_writer=csv.writer(csv_file,delimiter=',')
                csv_writer.writerow(['Name','Build','Level','Exp','Max HP','Max MP','Current HP','Current MP','Strength','Defence','Magic','Spell List'])
                csv_writer.writerow([self.getName(),self.getBuilt(),self.getLevel(),self.getExp(),self.getMaxHp(),self.getMaxMp(),self.getCurrentHp(),self.getCurrentMp(),self.getStrength(),self.getDefence(),self.getMagic()])
                for k in self.spelllist.keys():
                    csv_writer.writerow(['','','','','','','','','','','',k])

