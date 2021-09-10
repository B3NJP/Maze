import math, time, random
import tkinter

class tile:
    def __init__(self, x, y, open):
        self.open = open
        self.x = x
        self.y = y
        
class node:
    def __init__(self, x, y, neigh):
        self.x = x
        self.y = y
        self.neigh = neigh

class maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        for i in range(0, width):
            self.tiles += [[]]
            for j in range(0, height):
                self.tiles[-1] += [tile(i, j, True)]
                
    def rect(self, x, y, x2, y2, open):
        for i in self.tiles[x:x2+1]:
            for j in i[y:y2+1]:
                j.open = open 
                
    def neighbours(self, x, y):
        neigh = []
        if y > 0 and self.tiles[x][y-1].open:
            neigh += [(x,y-1)]
        if x < self.width-1 and self.tiles[x+1][y].open:
            neigh += [(x+1,y)]
        if y < self.height-1 and self.tiles[x][y+1].open:
            neigh += [(x,y+1)]
        if x > 0 and self.tiles[x-1][y].open:
            neigh += [(x-1,y)]
        return neigh
        
    def genPrim(self, time):
        self.rect(0,0,self.width-1,self.height-1, False)
        start = (math.floor(random.random()*(self.width)/2)*2+1, math.floor(random.random()*(self.height)/2)*2+1)
        self.rect(start[0],start[1],start[0],start[1], True)
        walls = [(start[0], start[1]-1), (start[0]+1, start[1]), (start[0], start[1]+1), (start[0]-1, start[1])]
        i=0
        while i < time and walls:
            i += 1
            cells = []
            current = walls.pop(math.floor(random.random()*len(walls)))
            if 0 < current[0] < self.width-1 and 0 < current[1] < self.height-1:
                if len(self.neighbours(current[0], current[1])) == 1:
                    cells += [current]
                    cells += [tuple(sum(x) for x in zip(current, tuple(x2-y2 for (x2, y2) in zip(current, self.neighbours(current[0], current[1])[0]))))] # Gets the opposite end of the side
                    walls += [(cells[-1][0], cells[-1][1]-1), (cells[-1][0]+1, cells[-1][1]), (cells[-1][0], cells[-1][1]+1), (cells[-1][0]-1, cells[-1][1])]
                    for j in cells:
                        self.rect(j[0],j[1],j[0],j[1], True)
        

def solveBreadth(mz):
    queue = []
    totals = []
    for i in range(0,mz.width):
        if mz.tiles[i][0].open == True:
            start = (i,0)
            queue += [[(i, 0)]]
            totals += [(i, 0)]
        if mz.tiles[i][mz.height-1].open == True:
            end = (i,mz.height-1)
    
    while queue:
        croute = queue.pop(0)
        neigh = mz.neighbours(croute[-1][0], croute[-1][1])
        for i in neigh:
            if i == end:
                return croute + [i]
            if not i in totals:
                totals += [i]
                queue += [croute + [i]]
    return None

def solveDepth(mz):
    for i in range(0,mz.width):
        if mz.tiles[i][0].open == True:
            start = (i,0)
        if mz.tiles[i][mz.height-1].open == True:
            end = (i,mz.height-1)
    def recurse(croute):
        neigh = mz.neighbours(croute[-1][0], croute[-1][1])
        for i in neigh:
            if i == end:
                return croute + [i]
            if not i in croute:
                temp = recurse(croute+[i])
                if temp:
                    return temp
        return None
    return recurse([start])

def importantPoints(mz):
    nodes = []
    for i in mz.tiles:
        for j in i:
            neighs = mz.neighbours(j.x, j.y)
            if len(neighs) == 2:
                if not (neighs[0][0] == neighs[1][0] or neighs[0][1] == neighs[1][1]):
                    nodes += [node(j.x, j.y, [])]
            else:
                nodes += [node(j.x, j.y, [])]
    return nodes

def connectNodes(mz, nodes):
    for i in nodes:
        j = 1
        while j<i.x and mz.tiles[i.x-j][i.y].open:
            j -= 1
        j += 1
        for k in nodes:
            if k.x == j:
                k.neigh += [i]
                i.neigh += [k]
        
        j = 1
        while j<i.y and mz.tiles[i.x][i.y-j].open:
            j -= 1
            print(i.y-j)
        j += 1
        for k in nodes:
            if k.y == j:
                k.neigh += [i]
                i.neigh += [k]
                

scale = 20

mz = maze(101, 101)


# mz.rect(0,0,9,7,False)
# 
# mz.rect(2,0,2,0,True)
# mz.rect(1,1,8,1,True)
# 
# mz.rect(3,2,3,5,True)
# mz.rect(3,6,5,6,True)
# mz.rect(5,5,8,5,True)
# mz.rect(8,6,8,7,True)
# 
# mz.rect(1,2,1,4,True)
# 
# mz.rect(7,2,7,3,True)
# mz.rect(5,3,6,3,True)

mz.genPrim(100000)
mz.rect(1,0,1,0,True)
mz.rect(mz.width-2,mz.height-1,mz.width-2,mz.height-1,True)

# nodes = importantPoints(mz)
# connectNodes(mz, nodes)

# route = solveBreadth(mz)
# route = solveDepth(mz)

app = tkinter.Tk()
app.title = "test"
app.resizable(0,0)

canv = tkinter.Canvas(app, width=800, height=800, scrollregion=(-100,-100,mz.width*scale+100,mz.height*scale+100))
verScroll = tkinter.Scrollbar(app, orient=tkinter.VERTICAL)
horScroll = tkinter.Scrollbar(app, orient=tkinter.HORIZONTAL)

verScroll.config(command = canv.yview)
horScroll.config(command = canv.xview)
canv.config(xscrollcommand = horScroll.set, yscrollcommand = verScroll.set)

verScroll.pack(side = "right", fill = 'y')
canv.pack(expand = True)
horScroll.pack(fill = 'x')

def solveDraw():
    # route = solveBreadth(mz)
    route = solveDepth(mz)
    for i in route:
        canv.create_rectangle(i[0]*scale, i[1]*scale, (i[0]+1)*scale, (i[1]+1)*scale, fill="blue")
        
solveButton = tkinter.Button(app, text="Solve", command = solveDraw)
solveButton.pack(side = "left")
def gen():
    canv.delete('all')
    mz.genPrim(100000)
    mz.rect(1,0,1,0,True)
    mz.rect(mz.width-2,mz.height-1,mz.width-2,mz.height-1,True)
    for i in mz.tiles:
        for j in i:
            canv.create_rectangle(j.x*scale, j.y*scale, (j.x+1)*scale, (j.y+1)*scale, fill="white" if j.open else "black")

randButton = tkinter.Button(app, text="Randomise", command = gen)
randButton.pack(side = "left")

for i in mz.tiles:
    for j in i:
        canv.create_rectangle(j.x*scale, j.y*scale, (j.x+1)*scale, (j.y+1)*scale, fill="white" if j.open else "black")
        
# for i in nodes:
#     canv.create_oval(i.x*scale, i.y*scale, (i.x+1)*scale, (i.y+1)*scale)
        
# for i in route:
#     canv.create_rectangle(i[0]*scale, i[1]*scale, (i[0]+1)*scale, (i[1]+1)*scale, fill="blue")
def solveDepthDraw(mz):
    for i in range(0,mz.width):
        if mz.tiles[i][0].open == True:
            start = (i,0)
        if mz.tiles[i][mz.height-1].open == True:
            end = (i,mz.height-1)
    def recurse(croute):
        canv.delete('all')
        for i in mz.tiles:
            for j in i:
                canv.create_rectangle(j.x*scale, j.y*scale, (j.x+1)*scale, (j.y+1)*scale, fill="white" if j.open else "black")
        for i in croute:
            canv.create_rectangle(i[0]*scale, i[1]*scale, (i[0]+1)*scale, (i[1]+1)*scale, fill="blue")
        app.update()
        neigh = mz.neighbours(croute[-1][0], croute[-1][1])
        for i in neigh:
            if i == end:
                return croute + [i]
            if not i in croute:
                temp = recurse(croute+[i])
                if temp:
                    return temp
        return None
    return recurse([start])
# solveDepthDraw(mz)
slowSolveButton = tkinter.Button(app, text="Slow Solve", command = lambda:solveDepthDraw(mz))
slowSolveButton.pack(side = "left")

app.mainloop()