import maze
import bossfloor
import os
import csv

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

loretext1=('Welcome to Tower of Babylon, a dungeon crawler game\n'
           'made by Abtahi Chowdhury. In this game, you will be thrown\n'
           'into a randomly generated dungeon in which you must fend\n'
           'for yourself against many deadly monsters. Travel through\n'
           'the maze and find the exit in order to esacpe.\n')
buildtext1=('Choose your class:\n'
            '\tWarrior\t\tA well rounded class that is good for beginners. Has\n'
            '\t\t\ta moderate amount of attack, defence, and health, but lacks\n'
            '\t\t\tin the magic catagory due to its low magic power and mana.\n\n'
            '\tBerserker\tA class based around doing high amounts of damage. Has\n'
            '\t\t\ta large amount of attack, but lacks in defence and has no magic\n'
            '\t\t\tpower and mana.\n\n'
            '\tGuardian\tA class built for taking hits and outlasting the opponent.\n'
            '\t\t\tHas a large amount of health and defence, but is paired with\n'
            '\t\t\tlow attack and no magic power and mana.\n\n'
            '\tPaladin\t\tA class for incorporating both physical strength and magic\n'
            '\t\t\tinto its playstyle. Has a moderate amount of health, defence,\n'
            '\t\t\tmagic, and mana, but lacks in attack.\n\n'
            '\tMage\t\tA class for doing explosive damage using its magic power. Has\n'
            '\t\t\ta high amount of attack, magic, and mana, but is paired with\n'
            '\t\t\tlow defence and health.\n\n')
mazedifficultytext1=('Choose your difficulty:\n'
                     '\teasy\tIn this mode the monsters are much easier and you are given\n'
                     '\t\ta map of the maze.\n'
                     '\thard\tIn this mode the monsters are much harder and you are not\n'
                     '\t\tgiven a map of the maze.\n')
mazesizetext1=('Enter a number to determine the size of the maze. A bigger number will\n'
               'result in a bigger maze. (i.e. entering 10 will result in a 10x10 maze)\n')
gamemechanictext1=('Use WASD to move your character.\n\n'
                   'When prompted with an action, type out the entire word of the\n'
                   'action and press enter.\n\n'
                   'While traversing the dungeon you will encounter monsters of random\n'
                   'difficulty. You will have to defeat these monsters in order to\n'
                   'continue on.\n\n'
                   'During your battles you will be given four commands to battle against\n'
                   'the monsters. These actions include Attack, Defend, Spell, and Run.\n\n'
                   'Attack will make you attack the monster, dealing damage to it based off\n'
                   'your strength.\n\n'
                   'Defend will make you defend against the monster, taking half the damage\n'
                   'you would normally take.\n\n'
                   'Spell will give you access to various spells, each having various utilities.\n\n'
                   'Run will give you the chance to run from battle, but there is a chance you\n'
                   'could not get away. In that case, the monster will deal more damage than\n'
                   'normal.\n\n')

def main():
    continuegame=input('\tNew Game\n\tLoad Game\n').lower()
    if continuegame=='new game':
        #Create player
        clearScreen()
        input(loretext1)
        clearScreen()
        #name='Abtahi'
        #build='warrior'
        name=input('Character name: ')
        clearScreen()
        build=input(buildtext1)
        clearScreen()
        player=maze.player.Player(name,build)
        input(player.printstats())
        clearScreen()
        input(gamemechanictext1)
        clearScreen()
        floorcounter=1
    elif continuegame=='load game':
        player=maze.player.Player('temp','berserker')
        player.loadPlayer()
        input(player.printstats())
        with open('remote/extdata') as csv_file:
            csv_reader=csv.reader(csv_file,delimiter=',')
            linecount=0
            for row in csv_reader:
                if linecount==1:
                    floorcounter=int(row[0])+1
                linecount+=1

    #Create maze
    mazesize=10
    mazedifficulty='easy'
    #mazesize=int(input(mazesizetext1))
    #clearScreen()
    #mazedifficulty=input(mazedifficultytext1)

    while True:
        if floorcounter%5==0:
            maze1=bossfloor.Bossfloor(mazedifficulty,floorcounter,player)
        else:
            maze1=maze.Maze(mazesize,mazedifficulty,floorcounter,player)
        player=maze1.play()
        print('\n'+player.printstats())
        if player.getCurrentHp()!=0:
            player.savePlayer()
            with open('remote/extdata',mode='w') as csv_file:
                csv_writer=csv.writer(csv_file,delimiter=',')
                csv_writer.writerow(['Floor'])
                csv_writer.writerow([floorcounter])
        floorcounter+=1
        if input('Continue? [y/n]').lower() != 'y':
            break

main()