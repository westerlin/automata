## Automata

from tkinter import *
import time
import random
import math

def updateAutomata():
    for pop in population:
        pop.act()
        
    for popidx in range(len(population)):
        pop = population[popidx]
        vx = 0
        vy = 0
        vv = 0
        for popcolidx in range(popidx+1,len(population)):
            popcol = population[popcolidx]
            dx = pop.x - popcol.x
            dy = pop.y - popcol.y
            dist = dx*dx + dy*dy
            if dist < 100:
                vx += dx
                vy += dy
                vv += 1
        if vv > 0:
            dist = math.sqrt(vx*vx + vy*vy)
            pop.x += vx / vv  / dist * 2.5
            pop.y += vy / vv  / dist * 2.5

    gx = 0
    gy = 0 
    for pop in population:
        gx += pop.x
        gy += pop.y
        
    gx /= len(population)
    gy /= len(population)
    gx -= size/2
    gy -= size/2

    for pop in population:
        pop.walk(-gx,-gy)
    #now = time.strftime("%H:%M:%S")
    #theLabel.configure(text=now)
    #canvas.delete("all")
    #x=random.randint(0,200)
    #y=random.randint(0,200)
    #r=8
    #canvas.coords(circle,x-r, y-r, x+r, y+r)
    root.after(1, updateAutomata)

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


class Guest:

    def __init__(self,x=0,y=0,color=None):
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.r = 8
        self.friend = None
        self.enemy = None
        if random.uniform(0,1)>.5:
            self.act = self.__coward
            color = "green"
        else:
            self.act = self.__brave
            color = "purple"
        self.circle = canvas.create_circle(x,y,8,fill=color, outline="")

    def addFriend(self,other_guest):
        self.friend = other_guest
        self.fline = canvas.create_line(self.x,self.y,other_guest.x,other_guest.y,fill="green")

    def addEnemy(self,other_guest):
        self.enemy = other_guest
        self.eline = canvas.create_line(self.x,self.y,other_guest.x,other_guest.y,fill="red")
    
    def __coward(self):
        if self.enemy != None and self.friend != None:
            dx = self.friend.x - self.enemy.x
            dy = self.friend.y - self.enemy.y
            #dist = math.sqrt(dx*dx+dy*dy)
            #dist2 = min(10,dist)
            #if dist2 != dist:
            #    dx *= dist2/dist
            #    dy *= dist2/dist
            self.tx = dx/2 + self.friend.x
            self.ty = dy/2 + self.friend.y
        #self.keepdistance()
        
    def __brave(self):
        if self.enemy != None and self.friend != None:
            self.tx = (self.enemy.x + self.friend.x) / 2
            self.ty = (self.enemy.y + self.friend.y) / 2
        #self.keepdistance()

    def keepdistance(self):
            if self.enemy != None:
                dx = self.x - self.enemy.x
                dy = self.y - self.enemy.y
                dist = math.sqrt(dx*dx+dy*dy)
                if dist < 20:
                    self.tx = dx * 2 + self.enemy.x
                    self.ty = dy * 2 + self.enemy.y

    def walk(self,gx,gy):
        #self.x = self.tx
        #self.y = self.ty
        if self.tx > self.x:
            self.x = self.x + 1
        elif self.tx < self.x:
            self.x = self.x - 1
        if self.ty > self.y:
            self.y = self.y + 1
        elif self.ty < self.y:
            self.y = self.y - 1
        canvas.coords(self.circle,self.x-self.r+gx, self.y-self.r+gy, self.x+self.r+gx, self.y+self.r+gy)
        if self.enemy != None:
            canvas.coords(self.eline,self.x+gx, self.y+gy, self.enemy.x+gx, self.enemy.y+gy)
        if self.friend != None:            
            canvas.coords(self.fline,self.x+gx, self.y+gy, self.friend.x+gx, self.friend.y+gy)
        
Canvas.create_circle = _create_circle

size = 1000

root = Tk()
theLabel = Label(root, text="Automata")
theLabel.pack()

canvas = Canvas(root,width=size,height=size)
canvas.pack()
#circle = canvas.create_circle(random.randint(0,size),random.randint(0,size),8,fill="#003366", outline="")

#blackline = canvas.create_rectangle(0,0,50,50,fill="blue",outline="")

population = []
newguest = None

for a in range(25):
    prev = newguest
    if a % 2 == 0:
        color = "#ff0000"
    else:        
        color = "#0000ff"
    #circle = canvas.create_circle(random.randint(0,size),random.randint(0,size),8,fill=color, outline="")
    newguest = Guest(x=random.randint(0,size),y=random.randint(0,size),color=color)
    if prev != None:
        prev.addFriend(newguest)
        newguest.addEnemy(prev)
    population.append(newguest)


newguest.addFriend(population[0])
population[0].addEnemy(newguest)

#for pop in population:
#    print(pop.enemy,pop.friend)


root.after(10, updateAutomata)

root.mainloop()