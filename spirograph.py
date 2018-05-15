#spirograph

import pygame, sys, math, time, os, random
from pygame.locals import *
screen = pygame.display.set_mode((1000, 1000))
canvas=pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('spirograph')
pygame.init()

class point():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
    def showCoords(self):
        print(self.x," ",self.y)
    def drawCoords(self,surface):
        surface.set_at((int(self.x),int(self.y)),(255,255,255))
class connection():
    def __init__(self,p0,p1,velocity):
        self.p0=p0
        self.p1=p1
        self.deltaAngle=0
        self.angle=math.atan2(p1.y-p0.y,p1.x-p0.x)
        self.distance=distance(p0,p1)
        self.velocity=velocity
        self.phase=0
def addConnection(p0,p1,velocity):
    global connections
    c=connection(p0,p1,velocity)
    connections.append(c)
def updateConnections():
    global connections
    connections[0].angle+=connections[0].velocity*0.05*globalVelocity
##    if connections[0].angle>math.pi*2:
##        connections[0].angle-=math.pi*2
##        connections[0].velocity+=0.1
    for i in range(0,len(connections)):
        connections[i].deltaAngle+=connections[i].velocity*0.05*globalVelocity
        if i!=0:
            connections[i].angle=connections[i-1].angle+connections[i].deltaAngle
            connections[i].p1.x=connections[i].p0.x+math.cos(connections[i].angle)*connections[i].distance
            connections[i].p1.y=connections[i].p0.y+math.sin(connections[i].angle)*connections[i].distance
        else:
            connections[i].p1.x=connections[i].p0.x+math.cos(connections[i].angle)*connections[i].distance
            connections[i].p1.y=connections[i].p0.y+math.sin(connections[i].angle)*connections[i].distance
        if i==len(connections)-1:
            addToTrail(connections[i].p1)
def distance(p0,p1):
    return math.sqrt((p1.x-p0.x)**2+(p1.y-p0.y)**2)
def drawConnections():
    global connections
    for i in range(0,len(connections)):
        pygame.draw.line(screen,(160,0,0),(connections[i].p0.x,connections[i].p0.y),(connections[i].p1.x,connections[i].p1.y),2)
        if i == len(connections)-1:
            pygame.draw.circle(canvas,(255,0,0),(int(connections[i].p1.x),int(connections[i].p1.y)),3,0)
        elif i==0:
            pygame.draw.circle(canvas,(0,0,0),(int(connections[i].p0.x),int(connections[i].p0.y)),3,0)
def addToTrail(p):
    global tPoints
    tPoints.append((p.x,p.y))
    #tPoints.remove(tPoints[0])
def drawTrail():
    if polyMode:
        try:pygame.draw.polygon(canvas,(100,100,100),tPoints,0)
        except: None
    else:
        try: pygame.draw.aalines(canvas,(100,100,100),False,tPoints,1)
        except: None
def loadSpirograph(num):
    f=open("saved.txt","r")
    saves=f.readlines()
    velocities=saves[num][3:].split(",")
    for i in range(len(velocities)):
        velocities[i]=float(velocities[i])
    constructConnections(int(saves[num][0]+saves[num][1]),0,velocities)
def constructConnections(m_pointNum,randomVel,m_velocities):
    global connections, tPoints, pointNum, velocities, IDText
    string=""
    if pointNum>=10:
        string=str(pointNum)+":"
    else:
        string="0"+str(pointNum)+":"
    for i in range(pointNum-1):
        string+=str(velocities[i])+","
    string=string[:-1]
    IDText=helpFont.render("ID= "+string,True,(0,0,0))
    pointNum=m_pointNum
    velocities=m_velocities
    tPoints=[]
    connections=[]
    points=[point(500+i*(500/pointNum),500) for i in range(pointNum)]
    if randomVel==1:
        velocities=[]
        for i in range(len(points)-1):
            if i==0:
                velocities.append(random.randint(0,3)+0.01)
            else:
                velocities.append(random.randint(-4,4))     
    for i in range(len(points)-1):
        addConnection(points[i],points[i+1],velocities[i])
def handleLoadChoices():
    global loadRects, pressing, state
    loadFont=pygame.font.Font(None,40)
    if Rect(1,100,998,800).collidepoint(pygame.mouse.get_pos()):
        for button in loadRects:
            if button[0].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.ellipse(screen,(150,150,150),button[0],0)
                if pygame.mouse.get_pressed()[0]:
                    if not pressing:
                        loadSpirograph(button[1])
                        state="running"
                        pressing=True
                else:
                    pressing=False
            else:
                pygame.draw.ellipse(screen,(90,90,90),button[0],0)
            loadText=loadFont.render(str(button[1]),True,(255,255,255))
            screen.blit(loadText,(button[0].left+400-loadText.get_width()/2,button[0].top+40))
    else:
        for button in loadRects:
            pygame.draw.ellipse(screen,(170,170,170),button[0],0)
            loadText=loadFont.render(str(button[1]),True,(255,255,255))
            screen.blit(loadText,(button[0].left+400-loadText.get_width()/2,button[0].top+40))
def updateSaveNo():
    global saveNo
    f=open("saved.txt","r")
    saveNo=len(f.readlines())
    f.close()
def updateLoadRects():
    global loadRects, saveNo
    loadRects=[[Rect(100,50+105*i+scrollPos,800,100),i] for i in range(saveNo)]
def saveSpriograph():
    global velocities, pointNum
    f=open("saved.txt","r")
    data=f.readlines()
    f.close()
    if pointNum>=10:
        string=str(pointNum)+":"
    else:
        string="0"+str(pointNum)+":"
    for i in range(pointNum-1):
        string+=str(velocities[i])+","
    string=string[:-1]
    string+="\n"
    if string not in data:
        data.append(string)
    f=open("saved.txt","w")
    for string in data:
        f.write(string)
    
scrollPos=80
scrollVel=0

globalVelocity=0.5

helpFont=pygame.font.Font(None,35)
helpText1=helpFont.render("Number keys change speed and r to randomize",True,(0,0,0))
helpText2=helpFont.render("Current Speed: "+str(globalVelocity),True,(0,0,0))
loadText=helpFont.render("Load",True,(255,255,255))
IDText=helpFont.render("ID",True,(0,0,0))

connections=[]
velocities=[]
pointNum=0
constructConnections(random.randint(3,25),1,None)

saveNo=0
updateSaveNo()
loadRects=[]
updateLoadRects()

loadButtonRect=Rect(895,5,100,50)
tPoints=[]
canvas.fill((255,255,255))

frameNo=0
skipFrames=2500#number of frames to skip
skipStart=1#skip bool

pressing=False
showArm=True
polyMode=False

if skipStart:
    while frameNo<skipFrames:
        frameNo+=1
        updateConnections()

currentTime=0

fps=0
fpsText=helpFont.render("FPS: "+str(fps),True,(255,128,0))
state="running"
c=0
n=random.randint(0,117)
refresh=False
while 1:
    if c>498:
        loadSpirograph(n)
        if n<117:
            n+=1
        else:
            n=0
        c=0
    elif state=="running" and refresh==True:
        c+=1
    oldTime=currentTime
    currentTime=pygame.time.get_ticks()
    deltaTime=currentTime-oldTime
    screen.fill((255,255,255))
    if state=="running":
        screen.blit(helpText1,(5,5))
        screen.blit(helpText2,(5,35))
        screen.blit(fpsText,(5,65))
        screen.blit(IDText,(5,970))
        screen.blit(canvas,(0,0))
        updateConnections()
        drawTrail()
        if showArm:
            drawConnections()
        if loadButtonRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.ellipse(screen,(90,90,90),loadButtonRect,0)
            if pygame.mouse.get_pressed()[0] and not pressing:
                state="loading"
                pressing=True
            else:
                pressing=False        
        else:
            pygame.draw.ellipse(screen,(150,150,150),loadButtonRect,0)
        screen.blit(loadText,(917,17))
    elif state=="loading":
        scrollPos+=scrollVel
        if scrollPos<840-saveNo*105:
            scrollPos=840-saveNo*105
            scrollVel=0
        elif scrollPos>80:
            scrollPos=80
            scrollVel=0
        scrollVel*=0.97
        updateLoadRects()
        handleLoadChoices()
        pygame.draw.rect(screen,(180,180,180),(0,0,1000,100),0)
        pygame.draw.rect(screen,(180,180,180),(0,900,1000,100),0)
    clock=pygame.time.Clock()
    if fps!=int(1000/deltaTime):
        fps=int(1000/deltaTime)
        fpsText=helpFont.render("FPS: "+str(fps),True,(255,128,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state=="loading":
                if event.button == 4:
                    if scrollVel<=1:
                        scrollVel*=0.5
                        if scrollVel>-0.5:
                            scrollVel=5
                    else:
                        scrollVel*=1.25
                if event.button == 5:
                    if scrollVel>=-1:
                        scrollVel*=0.5
                        if scrollVel<0.5:
                            scrollVel=-5
                    else:
                        scrollVel*=1.25
        if event.type == KEYDOWN:
            if event.key == K_r:
                constructConnections(random.randint(3,25),1,None)
                state="running"
                c=0
                n=0
            if event.key == K_s:
                saveSpriograph()
            if event.key == K_o:
                if showArm:
                    showArm=False
                else:
                    showArm=True
            if event.key == K_p:
                if polyMode:
                    polyMode=False
                else:
                    polyMode=True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_1:
                globalVelocity=0.25
            if event.key == K_2:
                globalVelocity=0.5
            if event.key == K_3:
                globalVelocity=0.75
            if event.key == K_4:
                globalVelocity=1
            if event.key == K_5:
                globalVelocity=1.25
            if event.key == K_6:
                globalVelocity=1.5
            if event.key == K_7:
                globalVelocity=2
            if event.key == K_8:
                globalVelocity=5
            if event.key == K_9:
                globalVelocity=10
            if event.key == K_0:
                globalVelocity=20
            helpText2=helpFont.render("Current Speed: "+str(globalVelocity),True,(0,0,0))
    clock.tick(60)
    pygame.display.update()
    pygame.display.flip()
