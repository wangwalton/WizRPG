from random import randint
import math


class Character:
    def __init__(self):
        self.name = ""
        self.health = 10
        self.max_health = 10
        self.mana = 0
        self.max_mana = 10
        self.battle_state = ""
        self.state = "normal"
        self.enemy = ""
        self.nature = "fire"
        self.stage = 0

    def block(self):
        self.battle_state = "blocking"
        print("%s puts up a magic shield!" % self.name)

    def charge(self):
        self.mana += 1; self.battle_state = "charging"
        print("%s charges, %s's mana: %d/%d --> %d/%d" % (self.name, self.name, self.mana - 1, self.max_mana, self.mana, self.max_mana))

    def attack(self):
        self.mana -= 1
        self.battle_state = "attacking"
        print("%s shoots out a orb of %s, mana: %d/%d --> %d/%d" % (self.name, self.nature, self.mana + 1, self.max_mana, self.mana, self.max_mana))


class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
        self.name = "Minion"
        self.health = randint(1, math.ceil(p.max_health/2 - 3))
        self.max_health = self.health
        self.nature = "ice"

    def action(self):
        if self.mana == 0:
            if randint(0, 1):
                self.block()
            else:
                self.charge()
        else:
            a = randint(0, 2)
            if a == 0:
                self.block()
            elif a == 1:
                self.charge()
            else:
                self.attack()
        if p.battle_state == "attacking" and self.battle_state == "charging":
            self.health -= 1
            print("%s took blast to the face. %s's health: %d/%d" %
                  (self.name, self.name, self.health, self.max_health))
            if self.health == 0:
                print("%s withers into the darkness. %s continues his journey." % (self.name, p.name))
                p.state = "normal"
                if self.name == "Dark Mage":
                    print("%s finds his love shivering in the corner\n"
                          "However, she is unharmed.\n"
                          "%s brings her home and had a happy life." % (self.name, self.name))
                    p.health = 0
        elif p.battle_state == "charging" and self.battle_state == "attacking":
            p.health -= 1
            print("%s took a blast to the face. %s's health: %d/%d" %
                  (p.name, p.name, p.health, p.max_health))
            if p.health == 0:
                print("%s froze and perished under the ice magic" % p.name)
        elif p.battle_state == "attacking" and self.battle_state == "attacking":
            print("The magic was evenly matched, no health deduction.")
        elif p.battle_state == "blocking" and self.battle_state == "attacking":
            print("%s's magic shield blocks %s's attack!" % (p.name, self.name))
        elif p.battle_state == "attacking" and self.battle_state == "blocking":
            print("%s's magic shield blocks %s's attack!" % (self.name, p.name))
        p.battle_state = self.state = "normal"


class Player(Character):
    def __init__(self):
        Character.__init__(self)

    def help(self):
        for key in Commands.keys():
            print(key)

    def rest(self):
        if self.state == "fight":
            print("You can't rest now!")
            self.enemy.action()
        else:
            if randint(0, 4) == 0:
                self.enemy = Enemy()
                self.state = "fight"
                print("A minion rudely wakes up %s, prepare for battle!" % self.name)
            else:
                if self.health < self.max_health:
                    self.health += 1
                    print("%s has recovered some strength." % (self.name))
                else:
                    self.health -= 1
                    print("%s slepted for too long." % self.name)
                print("%s's health: %d/%d"
                      "" % (self.name, self.health, self.max_health))

    def status(self):
        print("%s's health: %d/%d" % (self.name, self.health, self.max_health))
        print("%s's mana: %d/%d" % (self.name, self.mana, self.max_mana))

    def ccharge(self):
        if self.state != "fight":
            print("You can't charge without encountering an enemy, that would be cheap!")
        else:
            if not self.mana < self.max_mana:
                print("%s's mana is full, it can no longer be charged." % self.name)
            else:
                self.charge()
            self.enemy.action()

    def cblock(self):
        if self.state != "fight":
            print("%s puts up a magic shield!\nHowever, no attack seems to be aimed his way." % self.name)
        else:
            self.block()
            self.enemy.action()

    def cattack(self):
        if self.state != "fight":
            print("%s has no target to attack." % self.name)
        else:
            if self.mana == 0:
                print("%s do not have enough mana for this attack." % self.name)
            else:
                self.attack()
            self.enemy.action()

    def explore(self):
        if self.state == "fight":
            print("%s cannot advance any further with the minion blocking his way." % (self.name))
            self.enemy.action()
        else:
            if randint(0,3) == 0:
                self.enemy = Enemy()
                self.state = "fight"
                print("A minion has appeared to stop you from advancing further.")
            else:
                self.stage += 1
                print("{0} wonders up to level ".format(self.name) + str(self.stage) + " of the Tower of Pain.")
                if self.stage == 10:
                    print("\n%s has finally advanced to the top of the tower\n"
                          "The Dark Mage appears before his eyes, along with his loved one.\n"
                          "The final battle begins!" % self.name)
                    self.state = "fight"
                    self.enemy = Enemy()
                    self.enemy.health = 10
                    self.enemy.max_health = 10
                    self.enemy.name = "Dark Mage"

    def flee(self):
        if self.state != "fight":
            print("There is no enemies to flee from.")
        else:
            if randint(0,1) == 0:
                print("The %s caught out to you!" % self.enemy.name)
                self.enemy.action()
            else:
                print("%s got out by the skin of his teeth." % self.name)
                self.state = "normal"

    def quit(self):
        self.health = 0

Commands = {
    "attack": Player.cattack,
    "block": Player.cblock,
    "charge": Player.ccharge,
    "help": Player.help,
    "status": Player.status,
    "rest": Player.rest,
    "explore": Player.explore,
    "flee": Player.flee
}


tryAgain = "Y"
name = input("What is your name? ")

while tryAgain != "N":
    p = Character()
    p.name = name
    print("You are a young magician on a quest to save your-\nloved one who was stolen by the Dark Mage.")
    print("To do this, you have entered Tower of Pain\nin order to defeat the Dark Mage.")
    print("Type help for a list of actions.")
    while p.health > 0:
        inputCommand = input("> ")
        commandFound = False  # commandFound defaults to false
        for c in Commands.keys():  # loops through all keys
            if inputCommand == c[:len(inputCommand)]:
                Commands[c](p)
                commandFound = True
                break
        if not commandFound:
            print("%s doesn't understand the suggestion." % p.name)

    tryAgain = input("Play again? (Y/N) ")
print("Thank you for playing the game.")

'''
Copyright 2016 Walton Wang
University of Toronto TrackOne Engineering 2T0
https://github.com/wangwalton

'''