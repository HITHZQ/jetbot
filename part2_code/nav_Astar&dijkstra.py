# -- coding: utf-8 --
import math, sys, pygame, random
from math import *
from pygame import *
import time

Astar = 0
Dijkstra = 1
#模式选择: Dijkstra or Astar
mode = Astar

GAME_LEVEL =0  #障碍物等级，目前可选项为0或1
delay_sec = 1   #算法延时，单位：秒；可设置延时来观察学习路径规划的逐步实现过程
#颜色RGB值
grey = (169, 169, 169)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
orange = (255, 165, 0)
bg_color = (255, 255, 255)
purple = (160, 32, 240)
#初始化相关
pygame.init()
screen = pygame.display.set_mode((800, 600))
fpsClock = pygame.time.Clock()

#定义Node类，用于存储每个节点信息
class Node(object):
    def __init__(self, point, parent, d, f):
        super(Node, self).__init__()
        self.point = point      #节点坐标
        self.parent = parent    #父节点对象地址
        self.d = d      #Astar算法下：起点至该节点的确定距离；Dijkstra算法下：起点至该节点的估算距离
        self.f = f      #Astar算法下：f = d + h  d为上述确定距离，h为该节点到目标节点的估算距离（欧几里得距离或曼哈顿距离）；Dijkstra算法下此参数置零

#初始化栅格
def init_grid():
    start_point = [0, 0]
    end_point = [0, 600]
    i = 20
    while start_point[0] <= 800:
        pygame.draw.line(screen, grey, start_point, end_point)
        start_point[0] += i
        end_point[0] += i 
    
    start_point = [0, 0]
    end_point = [800, 0]
    while start_point[1] <= 600:
        pygame.draw.line(screen, grey, start_point, end_point)
        start_point[1] += i
        end_point[1] += i 

#判断栅格
def judge_in_grid(p):
    p0 = int(p[0]/20)
    p1 = int(p[1]/20)
    rect1 = ((p0*20, p1*20), (20,20))
    return rect1

#初始化障碍物
def init_obstacles(configNum):
    global rectObs
    rectObs = []
    if configNum == 0:
        rectObs.append(pygame.Rect((300,200),(200,200)))
    if configNum == 1:
        rectObs.append(pygame.Rect((100,100),(100,340)))
        rectObs.append(pygame.Rect((320,240),(160,160)))
        rectObs.append(pygame.Rect((500,60),(200,100)))
    for rect in rectObs:
        pygame.draw.rect(screen, black, rect)

#节点与障碍物碰撞检测
def collides(p):    #check if point collides with the obstacle
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            return True
    return False

#复位函数
def reset():
    screen.fill(bg_color)
    init_grid()
    init_obstacles(GAME_LEVEL)

#文本打印
def text_display(text0, rect, colour, Size):
    fontObj = pygame.font.Font(None,Size)
    textSurfaceObj = fontObj.render(text0,True,colour)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center=(10+(rect[0][0]),10+(rect[0][1]))
    screen.blit(textSurfaceObj,textRectObj)

#欧几里得距离，计算量大
def Euclid(p1, p2):
    m = ((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))**0.5
    return m

#曼哈顿距离，计算量小,简单
def Manhattan(p1, p2):
    m = abs(p1[0]-p2[0])+abs(p1[1]-p2[1])
    return m

#Astar估算函数
def evaluation_Astar(ynode, goalPoint):
    judge_open = False
    judge_close = False
    if collides(ynode.point) == True:
        return
    if ynode.point[0] < 0 or ynode.point[1] < 0:
        return
    ynode.f = ynode.d*1+0.1*Manhattan(ynode.point, goalPoint.point)
    for p in openlist:
        if p.point == ynode.point:
            judge_open = True
            index_open = openlist.index(p)
    for p in closelist:
        if p.point == ynode.point:
            judge_close = True
            index_close = closelist.index(p)
    if judge_close == True:
        return
    if judge_open == False:
        openlist.append(ynode)
        pygame.draw.rect(screen, (255*abs(1-float(ynode.d)*1.2/140), 255*abs(1-float(ynode.d)*1.2/140), 255), (ynode.point, (20, 20)))
        text_display(str(int(ynode.d)), (ynode.point, (20, 20)), black, 15)
        pygame.display.flip()
    else:
        if openlist[index_open].d > ynode.d:
            openlist[index_open] = ynode

#Dijkstra估算函数
def evaluation_Dijkstra(ynode, goalPoint):
    judge_open = False
    judge_close = False
    if collides(ynode.point) == True:
        return
    if ynode.point[0] < 0 or ynode.point[1] < 0:
        return
    for p in closelist:
        if p.point == ynode.point:
            judge_close = True
            index_close = closelist.index(p)
    if judge_close == True:
        return
    for p in openlist:
        if p.point == ynode.point:
            judge_open = True
            index_open = openlist.index(p)
    if judge_open == True:
        if openlist[index_open].d > ynode.d:
            openlist[index_open] = ynode
    else:
        openlist.append(ynode)
        pygame.draw.rect(screen, (255*abs(1-float(ynode.d)*1.2/140), 255*abs(1-float(ynode.d)*1.2/140), 255), (ynode.point, (20, 20)))
        text_display(str(ynode.d), (ynode.point, (20, 20)), black, 15)
        pygame.display.flip()

#程序主要函数
def run_game():
    currentState = 'init'
    initPoseSet = False
    goalPoseSet = False
    global openlist
    openlist = []
    global closelist
    closelist = []
    reset()
    #主循环
    while True:
        #处理不同currentState状态下的工作，其中包括规划路径的实现
        if currentState == 'init':
            print('goal point not yet set')
            pygame.display.set_caption('Select Starting Point and then Goal Point')
            fpsClock.tick(10)
        elif currentState == 'lookingForGoal':
            run = True
            while(len(openlist) != 0):
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN :
                        if run == True:
                            run = False
                        else:
                            run = True
                if run == True:
                    xnode = openlist[0]
                    if xnode.point == goalPoint.point:
                        pygame.draw.rect(screen, orange, (xnode.point, (20, 20)))
                        text_display("G",(xnode.point, (20, 20)), black, 32)
                        currentState = 'goalFound'
                        flag = 1
                        goalNode = xnode
                        break
                    closelist.append(xnode)
                    del openlist[0]
                    if delay_sec > 0:
                        pygame.draw.circle(screen, red, (xnode.point[0]+10, xnode.point[1]+10), 2)
                    i = 0
                    while i < 8:
                        if i == 0:
                            ynode = Node((xnode.point[0],xnode.point[1]-20), xnode, xnode.d+2, 0)
                        elif i == 1:
                            ynode = Node((xnode.point[0],xnode.point[1]+20), xnode, xnode.d+2, 0)
                        elif i == 2:
                            ynode = Node((xnode.point[0]-20,xnode.point[1]), xnode, xnode.d+2, 0)
                        elif i == 3:
                            ynode = Node((xnode.point[0]+20,xnode.point[1]), xnode, xnode.d+2, 0)
                        elif i == 4:
                            ynode = Node((xnode.point[0]-20,xnode.point[1]-20), xnode, xnode.d+3, 0)
                        elif i == 5:
                            ynode = Node((xnode.point[0]+20,xnode.point[1]-20), xnode, xnode.d+3, 0)
                        elif i == 6:
                            ynode = Node((xnode.point[0]+20,xnode.point[1]+20), xnode, xnode.d+3, 0)
                        elif i == 7:
                            ynode = Node((xnode.point[0]-20,xnode.point[1]+20), xnode, xnode.d+3, 0)
                        if mode == 0:
                            evaluation_Astar(ynode, goalPoint)
                        elif mode == 1:
                            evaluation_Dijkstra(ynode, goalPoint)
                        i += 1
                    for i in range(0, len(openlist)-1):
                        for j in range(0, len(openlist)-1-i):
                            if mode == 0:
                                data_j = openlist[j].f
                                data_j1 = openlist[j+1].f
                            elif mode == 1:
                                data_j = openlist[j].d
                                data_j1 = openlist[j+1].d
                            if data_j > data_j1:
                                temp = openlist[j]
                                openlist[j] = openlist[j+1]
                                openlist[j+1] = temp
                    pygame.display.flip()
                    for i in range(0, len(openlist)):
                        print(str(openlist[i].point)+"\t--- d = "+str(openlist[i].d)+"  &  f = "+str(openlist[i].f))
                        print("parent:"+str(openlist[i].parent.point))
                    print("-------------------")
                    time.sleep(delay_sec)
                if len(openlist) == 0:
                    print('False to find the path')
        elif currentState == 'goalFound':
            if flag == 1:
                print('goalFound!!!!!!')
                currNode = goalNode.parent
                print("******************")
                print("startPoint = "+(str(initialPoint.point)))
                print("goalPoint = "+(str(goalPoint.point)))
                print("******************")
                for i in range(0, len(closelist)):
                    print(str(closelist[i].point)+"\t--- d = "+str(closelist[i].d)+"  &  f = "+str(closelist[i].f))
                    if i > 0:
                        print("parent:"+str(closelist[i].parent.point))
            while currNode.parent != None:
                pygame.draw.rect(screen, green, (currNode.point, (20, 20)))
                text_display(str(currNode.d), (currNode.point, (20, 20)), black, 15)
                currNode = currNode.parent
                flag = 0
                pygame.display.flip()
                time.sleep(float(delay_sec)/2)
            fpsClock.tick(10)
        #处理鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if currentState == 'init':
                    rect = judge_in_grid(event.pos)
                    if initPoseSet == False:
                        if collides(event.pos) == False:
                            initialPoint = Node(rect[0], None, 0, 0)
                            
                            pygame.draw.rect(screen, red, rect)
                            text_display("S",rect, black, 32)
                            initPoseSet = True
                    elif  goalPoseSet == False:
                        if collides(event.pos) == False:
                            if rect[0] != initialPoint.point:
                                goalPoint = Node(rect[0],None, 0, 0)
                                print("******************")
                                print("startPoint = "+(str(initialPoint.point)))
                                print("goalPoint = "+(str(goalPoint.point)))
                                print("******************")
                                if mode == 0:
                                    initialPoint.f = initialPoint.d+0.1*Manhattan(goalPoint.point, initialPoint.point)
                                openlist.append(initialPoint)
                                pygame.draw.rect(screen, orange, rect)
                                text_display("G",rect, black, 32)
                                goalPoseSet = True
                                currentState = 'lookingForGoal'
                else:
                    currentState = 'init'
                    initPoseSet = False
                    goalPoseSet = False
                    openlist = []
                    closelist = []
                    reset()
        init_grid()
        pygame.display.flip()
        
if __name__ == '__main__':
    run_game()
