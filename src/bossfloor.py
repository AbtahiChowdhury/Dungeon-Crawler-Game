import random
import os
import player
import monster

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def playerDamageCalculator(damage,defence):
    if (damage-defence)<5:
        return 5
    else:
        return damage-defence

def monsterDamageCalculator(damage,defence):
    if (damage-defence)<1:
        return 1
    else:
        return damage-defence

class Bossfloor():
    def __init__(self,difficulty,level,player):
        self.maze=[[1 for i in range(0,7)] for j in range(0,7)]
        self.difficulty=difficulty
        self.level=level

        for row in self.maze:
            row[0]=0
            row[len(row)-1]=0
        for i in range(0,len(self.maze[1])):
            self.maze[0][i]=0
            self.maze[len(self.maze)-1][i]=0
        
        self.maze[0][3]=1
        #self.maze[6][3]=1
        self.startrow=0
        self.startcol=3
        self.endrow=6
        self.endcol=3

        self.player=player
        self.playerposrow=self.startrow
        self.playerposcol=self.startcol

        if self.difficulty=='easy':
            #level + 12
            self.bossmonster=monster.Monster(self.level+15)
            self.bossposrow=3
            self.bossposcol=3
        elif self.difficulty=='hard':
            #level + 17
            self.bossmonster=monster.Monster(self.level+20)
            self.bossposrow=3
            self.bossposcol=3
    
    #Move player
    def movePlayer(self,direction):
        if direction=='up':
            if self.maze[self.playerposrow-1][self.playerposcol] is 1:
                self.playerposrow-=1
        elif direction=='down':
            if self.maze[self.playerposrow+1][self.playerposcol] is 1:
                self.playerposrow+=1
        elif direction=='right':
            if self.maze[self.playerposrow][self.playerposcol+1] is 1:
                self.playerposcol+=1
        elif direction=='left':
            if self.maze[self.playerposrow][self.playerposcol-1] is 1:
                self.playerposcol-=1
        
        if self.playerposrow==self.bossposrow and self.playerposcol==self.bossposcol:
            self.battle(self.bossmonster)
            if self.bossmonster.getCurrentHp()==0:
                self.bossposrow=-1
                self.bossposcol=-1
                self.maze[self.endrow][self.endcol]=1
        
        if self.player.getCurrentHp() is not 0:
                self.player.healHp(5)
                self.player.regenMp(1)

    #Battle against a monster
    def battle(self,monster):
        turncounter=0
        trapstate=False
        trapcounter=-1
        shieldstate=False
        shieldcounter=-1
        playerspelllist=self.player.getSpellList()
        while self.player.getCurrentHp()!=0 and monster.getCurrentHp()!=0:
            clearScreen()
            turncounter+=1
            print(f'Player\tMonster\n{self.player.getCurrentHp()} HP\t{monster.getCurrentHp()} HP\n{self.player.getCurrentMp()} MP')
            print('\tAttack\n\tDefend\n\tSpell\n\tRun')
            action=input('What will you do?\n')
            if action.lower()=='attack':
                playerdamage=playerDamageCalculator(self.player.getStrength(),monster.getDefence())
                input(f'You did {playerdamage} damage to the monster.')
                if monster.takeDamage(playerdamage)!=-1:
                    monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                    if shieldstate:
                        input(f'The monster attacked you for {monsterdamage/2} damage')
                        self.player.takeDamage(monsterdamage/2)
                    else:
                        input(f'The monster attacked you for {monsterdamage} damage')
                        self.player.takeDamage(monsterdamage)
            elif action.lower()=='defend':
                input('You defended against the monster.')
                monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                if shieldstate:
                    input(f'The monster attacked you for {monsterdamage/4} damage')
                    self.player.takeDamage(monsterdamage/4)
                else:
                    input(f'The monster attacked you for {monsterdamage/2} damage')
                    self.player.takeDamage(monsterdamage/2)
            elif action.lower()=='spell':
                if bool(playerspelllist):
                    print('Select spell to use:')
                    for k,v in playerspelllist.items():
                        print(f'\t{v.getName()}\t{v.getCost()} MP')
                    spell=input().lower()
                    if spell=='fire':
                        if self.player.useMp(playerspelllist['fire'].getCost())!=-1:
                            damageamount=int((playerspelllist['fire'].getMultiplier())*(self.player.getMagic()))
                            playerdamage=playerDamageCalculator(damageamount,monster.getDefence())
                            input(f'You did {playerdamage} damage to the monster.')
                            if monster.takeDamage(playerdamage)!=-1:
                                monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                                if shieldstate:
                                    input(f'The monster attacked you for {monsterdamage/2} damage')
                                    self.player.takeDamage(monsterdamage/2)
                                else:
                                    input(f'The monster attacked you for {monsterdamage} damage')
                                    self.player.takeDamage(monsterdamage)
                                '''
                                if shieldstate:
                                    input(f'The monster attacked you for {int((monster.getStrength())/2)} damage')
                                    self.player.takeDamage(int((monster.getStrength())/2))
                                else:
                                    input(f'The monster attacked you for {monster.getStrength()} damage')
                                    self.player.takeDamage(monster.getStrength())
                                '''
                        else:
                            input('Insufficient Mana')
                    elif spell=='thunder':
                        if self.player.useMp(playerspelllist['thunder'].getCost())!=-1:
                            damageamount=int((playerspelllist['thunder'].getMultiplier())*(self.player.getMagic()))
                            playerdamage=playerDamageCalculator(damageamount,monster.getDefence())
                            input(f'You did {playerdamage} damage to the monster.')
                            if monster.takeDamage(playerdamage)!=-1:
                                monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                                if shieldstate:
                                    input(f'The monster attacked you for {monsterdamage/2} damage')
                                    self.player.takeDamage(monsterdamage/2)
                                else:
                                    input(f'The monster attacked you for {monsterdamage} damage')
                                    self.player.takeDamage(monsterdamage)
                        else:
                            input('Insufficient Mana')
                    elif spell=='shield':
                        if self.player.useMp(playerspelllist['shield'].getCost())!=-1:
                            shieldstate=True
                            shieldcounter=int((playerspelllist['shield'].getMultiplier())*(self.player.getMagic()))
                            input(f'You are shielded from attacks for {shieldcounter} turns')
                            monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                            if shieldstate:
                                input(f'The monster attacked you for {monsterdamage/2} damage')
                                self.player.takeDamage(monsterdamage/2)
                            else:
                                input(f'The monster attacked you for {monsterdamage} damage')
                                self.player.takeDamage(monsterdamage)
                        else:
                            input('Insufficient Mana')
                    elif spell=='heal':
                        if self.player.useMp(playerspelllist['heal'].getCost())!=-1:
                            healamount=int((playerspelllist['heal'].getMultiplier())*(self.player.getMagic()))
                            input(f'You healed for {healamount}.')
                            self.player.healHp(healamount)
                            monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                            if shieldstate:
                                input(f'The monster attacked you for {monsterdamage/2} damage')
                                self.player.takeDamage(monsterdamage/2)
                            else:
                                input(f'The monster attacked you for {monsterdamage} damage')
                                self.player.takeDamage(monsterdamage)
                        else:
                            input('Insufficient Mana')
                    elif spell=='trap':
                        if self.player.useMp(playerspelllist['trap'].getCost())!=-1:
                            trapstate=True
                            trapcounter=int((playerspelllist['trap'].getMultiplier())*(self.player.getMagic()))
                            input(f'You have traped the monster for {trapcounter} turns')
                            monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                            if shieldstate:
                                input(f'The monster attacked you for {monsterdamage/2} damage')
                                self.player.takeDamage(monsterdamage/2)
                            else:
                                input(f'The monster attacked you for {monsterdamage} damage')
                                self.player.takeDamage(monsterdamage)
                        else:
                            input('Insufficient Mana')
                else:
                    input('No spells available')
            elif action.lower()=='run':
                if trapstate:
                    print('You got away')
                    break
                if self.player.getCurrentHp()>monster.getCurrentHp() and random.randint(0,10)>2:
                    print('You got away')
                    break
                else:
                    input('You could not get get away')
                    monsterdamage=monsterDamageCalculator(monster.getStrength(),self.player.getDefence())
                    if shieldstate:
                        input(f'The monster attacked you for {int((monsterdamage)*0.75)} damage')
                        self.player.takeDamage(int((monsterdamage)*0.75))
                    else:
                        input(f'The monster attacked you for {int((monsterdamage)*1.5)} damage')
                        self.player.takeDamage(int((monsterdamage)*1.5))
            if trapcounter>0:
                trapcounter-=1
            elif trapcounter==0:
                trapcounter=-1
                trapstate=False
                input('The monster escaped the trap')
            if shieldcounter>0:
                shieldcounter-=1
            elif shieldcounter==0:
                shieldstate=False
                shieldcounter=-1
                input('Your shield ran out')
            if monster.getCurrentHp()==0:
                self.player.gainExp(2*monster.getDifficulty())
        clearScreen()

    #Print map
    def printMap(self):
        print(f"{self.player.getCurrentHp()}/{self.player.getMaxHp()} HP\t{self.player.getCurrentMp()}/{self.player.getMaxMp()} MP\tFloor {self.level}\n")
        for i in range(0,len(self.maze)):
            for j in range(0,len(self.maze[1])):
                if i is self.playerposrow and j is self.playerposcol:
                    print('P',end=' ')
                elif i is self.bossposrow and j is self.bossposcol:
                    print('B',end=' ')
                elif self.maze[i][j] is 0:
                    print('0',end=' ')
                else:
                    print(' ',end=' ')
            print()
    
    #Begin the game
    def play(self):
        clearScreen()
        self.printMap()
        while True:
            if self.player.getCurrentHp() is 0:
                print('You died')
                break
            if self.playerposrow is self.endrow and self.playerposcol is self.endcol:
                print('Congrats, you escaped!')
                break
            direction=input()
            clearScreen()
            if direction=='w':
                self.movePlayer('up')
            elif direction=='a':
                self.movePlayer('left')
            elif direction=='s':
                self.movePlayer('down')
            elif direction=='d':
                self.movePlayer('right')
            self.printMap()
        return self.player