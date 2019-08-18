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


class Maze():
    def __init__(self,size,difficulty,level,player):
        #Create maze of 1s & 0s: 0=wall 1=pathway
        self.maze=[[random.randint(0,1) for i in range(size)] for j in range(size)]
        #Set difficulty
        self.difficulty=difficulty
        if self.difficulty=='hard':
            self.map=[[0 for i in range(size)] for j in range(size)]
        #Create monster timer
        self.monstertimer=0
        #Set floor level
        self.level=level
        #Avoid making single block rooms
        for i in range(1,len(self.maze)-1):
            for j in range(1,len(self.maze[1])-1):
                if self.maze[i][j] is 1 and self.maze[i+1][j] is 0 and self.maze[i-1][j] is 0 and self.maze[i][j+1] is 0 and self.maze[i][j-1] is 0:
                    #easy difficulty
                    if self.difficulty=='easy':
                        self.maze[i+1][j]=1
                        self.maze[i-1][j]=1
                        self.maze[i][j+1]=1
                        self.maze[i][j-1]=1
                    
                    #hard difficulty
                    if self.difficulty=='hard':
                        x=random.randint(1,4)
                        if x is 1:
                            self.maze[i+1][j]=1
                        elif x is 2:
                            self.maze[i-1][j]=1
                        elif x is 3:
                            self.maze[i][j+1]=1
                        elif x is 4:
                            self.maze[i][j-1]=1

        #Create outer walls
        for row in self.maze:
            row[0]=0
            row[len(row)-1]=0
        for i in range(0,len(self.maze[1])):
            self.maze[0][i]=0
            self.maze[len(self.maze)-1][i]=0

        #Create start
        if random.randint(0,1) is 0:
            self.startrow=0
            self.startcol=random.randint(1,int(len(self.maze)/2))
            self.maze[self.startrow][self.startcol]=1
            self.maze[self.startrow+1][self.startcol]=1
            if self.difficulty=='hard':
                self.map[self.startrow][self.startcol]=1
                self.map[self.startrow+1][self.startcol]=1
        else:
            self.startrow=random.randint(1,int(len(self.maze)/2))
            self.startcol=0
            self.maze[self.startrow][self.startcol]=1
            self.maze[self.startrow][self.startcol+1]=1
            if self.difficulty=='hard':
                self.map[self.startrow][self.startcol]=1
                self.map[self.startrow][self.startcol+1]=1
        
        #Create end
        if random.randint(0,1) is 0:
            self.endrow=len(self.maze)-1
            self.endcol=random.randint(int(len(self.maze)/2),len(self.maze)-2)
            self.maze[self.endrow][self.endcol]=1
            self.maze[self.endrow-1][self.endcol]=1
            if self.difficulty=='hard':
                self.map[self.endrow][self.endcol]=1
                self.map[self.endrow-1][self.endcol]=1
        else:
            self.endrow=random.randint(int(len(self.maze)/2),len(self.maze)-2)
            self.endcol=len(self.maze)-1
            self.maze[self.endrow][self.endcol]=1
            self.maze[self.endrow][self.endcol-1]=1
            if self.difficulty=='hard':
                self.map[self.endrow][self.endcol]=1
                self.map[self.endrow][self.endcol-1]=1
        
        #Create character
        self.player=player
        self.playerposrow=self.startrow
        self.playerposcol=self.startcol
    
    #Move player
    def movePlayer(self,direction):
        self.monstertimer+=1
        if direction=='up':
            if self.maze[self.playerposrow-1][self.playerposcol] is 1:
                self.playerposrow-=1
            else:
                self.breakWall(direction)
        elif direction=='down':
            if self.maze[self.playerposrow+1][self.playerposcol] is 1:
                self.playerposrow+=1
            else:
                self.breakWall(direction)
        elif direction=='right':
            if self.maze[self.playerposrow][self.playerposcol+1] is 1:
                self.playerposcol+=1
            else:
                self.breakWall(direction)
        elif direction=='left':
            if self.maze[self.playerposrow][self.playerposcol-1] is 1:
                self.playerposcol-=1
            else:
                self.breakWall(direction)
        
        if self.difficulty=='hard' and self.playerposrow!=self.endrow and self.playerposcol!=self.endcol:
            self.map[self.playerposrow][self.playerposcol]=self.maze[self.playerposrow][self.playerposcol]
            self.map[self.playerposrow+1][self.playerposcol]=self.maze[self.playerposrow+1][self.playerposcol]
            self.map[self.playerposrow-1][self.playerposcol]=self.maze[self.playerposrow-1][self.playerposcol]
            self.map[self.playerposrow][self.playerposcol+1]=self.maze[self.playerposrow][self.playerposcol+1]
            self.map[self.playerposrow][self.playerposcol-1]=self.maze[self.playerposrow][self.playerposcol-1]
            self.map[self.playerposrow+1][self.playerposcol+1]=self.maze[self.playerposrow+1][self.playerposcol+1]
            self.map[self.playerposrow+1][self.playerposcol-1]=self.maze[self.playerposrow+1][self.playerposcol-1]
            self.map[self.playerposrow-1][self.playerposcol+1]=self.maze[self.playerposrow-1][self.playerposcol+1]
            self.map[self.playerposrow-1][self.playerposcol-1]=self.maze[self.playerposrow-1][self.playerposcol-1]
        
        if self.monstertimer>3:
            if random.randint(1,10)>=7:
                self.monstertimer=0
                input('Monster Encountered')
                clearScreen()
                if self.difficulty=='easy':
                    monster1=monster.Monster((random.randint(1,6))+self.level)
                elif self.difficulty=='hard':
                    monster1=monster.Monster((random.randint(6,10))+self.level)
                self.battle(monster1)
        
        if self.player.getCurrentHp() is not 0:
                self.player.healHp(5)
                self.player.regenMp(1)

    
    #Break wall
    def breakWall(self,direction):
        if direction=='up':
            if self.playerposcol==0 or self.playerposrow==1:
                return
            self.maze[self.playerposrow-1][self.playerposcol]=1
            if self.difficulty=='hard':
                self.map[self.playerposrow-1][self.playerposcol]=1
            self.playerposrow-=1
        elif direction=='down':
            if self.playerposcol==0 or self.playerposrow==((len(self.maze))-2):
                return
            self.maze[self.playerposrow+1][self.playerposcol]=1
            if self.difficulty=='hard':
                self.map[self.playerposrow+1][self.playerposcol]=1
            self.playerposrow+=1
        elif direction=='right':
            if self.playerposcol==((len(self.maze[1]))-2) or self.playerposrow==0:
                return
            self.maze[self.playerposrow][self.playerposcol+1]=1
            if self.difficulty=='hard':
                self.map[self.playerposrow][self.playerposcol+1]=1
            self.playerposcol+=1
        elif direction=='left':
            if self.playerposcol==1 or self.playerposrow==0:
                return
            self.maze[self.playerposrow][self.playerposcol-1]=1
            if self.difficulty=='hard':
                self.map[self.playerposrow][self.playerposcol-1]=1
            self.playerposcol-=1
        
        input('Monster encountered')
        clearScreen()
        self.monstertimer=0
        if self.difficulty=='easy':
            monster1=monster.Monster((random.randint(6,8))+self.level)
        elif self.difficulty=='hard':
            monster1=monster.Monster((random.randint(10,12))+self.level)
        self.battle(monster1)

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

    #Print maze
    def printMaze(self):
        for i in self.maze:
            print(*i)
    
    #Print map
    def printMap(self):
        print(f"{self.player.getCurrentHp()}/{self.player.getMaxHp()} HP\t{self.player.getCurrentMp()}/{self.player.getMaxMp()} MP\tFloor {self.level}\n")
        if self.difficulty=='easy':
            for i in range(0,len(self.maze)):
                for j in range(0,len(self.maze[1])):
                    if i is self.playerposrow and j is self.playerposcol:
                        print('P',end=' ')
                    elif self.maze[i][j] is 0:
                        print('0',end=' ')
                    else:
                        print(' ',end=' ')
                print()
        elif self.difficulty=='hard':
            for i in range(0,len(self.map)):
                for j in range(0,len(self.map[1])):
                    if i is self.playerposrow and j is self.playerposcol:
                        print('P',end=' ')
                    elif self.map[i][j] is 0:
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
