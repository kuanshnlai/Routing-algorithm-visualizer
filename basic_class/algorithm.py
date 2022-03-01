import pygame_gui
import math
import random
from basic_class.curve import *
from basic_class.component import *
from pygame.locals import *
import pygame
import threading


class Algorithm:
    def __init__(self, graph):
        self.frames = []
        self.graph = graph

    def run(self):
        '''
        return a series of frames produce by this algorithm 
        '''
        pass


class TestAlgorithm(Algorithm):
    def __init__(self, graph):
        super().__init__(graph)

    def run(self):  # Generate frames
        frames = []
        for v in self.graph.nodesInfo:
            color = self.graph.nodesInfo[v]['Color']
            self.graph.update_node_color(v, (255, 0, 0))
            frames.append(self.graph.draw())
            self.graph.update_node_color(v, color)
        self.graph.compile_graph()
        return frames


class CS(Algorithm):
    def __init__(self, graph, surface):
        super().__init__(graph)
        self.curNodeID = self.graph.parasList["Start"]
        self.destNodeID = self.graph.parasList["Destination"]
        self.InitSurface = surface
        self.radius = self.graph.parasList['Radius']
        self.frames = FrameList(1)
        self.preID = None

    def distance(self, NodeAID=None, NodeBID=None, PosA=None, PosB=None):
        if(NodeAID == None and NodeBID == None):
            x1 = PosA[0]
            y1 = PosA[1]
            x2 = PosB[0]
            y2 = PosB[1]
        else:
            x1 = self.graph.nodesInfo[NodeAID]['PosX']
            y1 = self.graph.nodesInfo[NodeAID]['PosY']
            x2 = self.graph.nodesInfo[NodeBID]['PosX']
            y2 = self.graph.nodesInfo[NodeBID]['PosY']
        return (((x1-x2)**2)+((y1-y2)**2))**0.5

    def chooseSp(self, stuckNodeID, pre):
        if self.curNodeID == pre:
            v = (self.graph.nodesInfo[self.destNodeID]['PosX']-self.graph.nodesInfo[self.curNodeID]['PosX'],
                 self.graph.nodesInfo[self.destNodeID]['PosY']-self.graph.nodesInfo[self.curNodeID]['PosY'])
            vlen = (v[0]**2+v[1]**2)**0.5
            sp = (int(self.graph.nodesInfo[self.curNodeID]['PosX']+v[0]/vlen*self.radius), int(
                self.graph.nodesInfo[self.curNodeID]['PosY']+v[1]/vlen*self.radius))
            return sp
        else:
            nowPointX = self.graph.nodesInfo[self.curNodeID]['PosX']
            nowPointY = self.graph.nodesInfo[self.curNodeID]['PosY']
            prePointX = self.graph.nodesInfo[pre]['PosX']
            prePointY = self.graph.nodesInfo[pre]['PosY']
            pointList = self.intersection(pre)
            u = (nowPointX-prePointX, nowPointY-prePointY)
            v1 = (pointList[0][0]-nowPointX, pointList[0][1]-nowPointY)
            v2 = (pointList[1][0]-nowPointX, pointList[1][1]-nowPointY)
            ulen = (u[0]**2+u[1]**2)**0.5
            v1len = (v1[0]**2+v1[1]**2)**0.5
            v2len = (v2[0]**2+v2[1]**2)**0.5
            c1 = (u[0]*v1[0]+u[1]*v1[1])/(ulen*v1len)
            c2 = (u[0]*v2[0]+u[1]*v2[1])/(ulen*v2len)
            # 選擇點錯誤
            s1 = (u[0]*v1[1]-u[1]*v1[0])/(ulen*v1len)
            s2 = (u[0]*v2[1]-u[1]*v2[0])/(ulen*v2len)
            # if c1 < 0:
            #     return pointList[0]
            # else:
            #     return pointList[1]

            if s1 > 0:
                return pointList[0]
            else:
                return pointList[1]

    def intersection(self, otherID):

        nowPoint = (self.graph.nodesInfo[self.curNodeID]['PosX'],
                    self.graph.nodesInfo[self.curNodeID]['PosY'])
        prePoint = (self.graph.nodesInfo[otherID]['PosX'],
                    self.graph.nodesInfo[otherID]['PosY'])

        delta = 10E-4
        x1 = nowPoint[0]
        y1 = nowPoint[1]
        x2 = prePoint[0]
        y2 = prePoint[1]
        r = self.radius
        a = 2*r*(x1-x2)
        b = 2*r*(y1-y2)
        c = -(x1-x2)**2-(y1-y2)**2

        p = a**2+b**2
        q = -2*a*c
        s = c**2-b**2
        if p == 0:
            p = delta
        c1 = (-q+(q**2-4*p*s)**0.5)/(2*p)  # cos theta
        c2 = (-q-(q**2-4*p*s)**0.5)/(2*p)
        s1 = (1-c1**2)**0.5
        s2 = (1-c2**2)**0.5
        p1 = self.calPos(c1, s1)
        p2 = self.calPos(c1, -s1)
        p3 = self.calPos(c2, s2)
        p4 = self.calPos(c2, -s2)
        realPoint = self.check([p1, p2, p3, p4])
        # print("real", realPoint)
        return realPoint

    def calPos(self, cos, sin):  # given cos and sin and cur point determine the point's pos
        nowPoint = (self.graph.nodesInfo[self.curNodeID]['PosX'],
                    self.graph.nodesInfo[self.curNodeID]['PosY'])
        newPoint = ((nowPoint[0]+self.radius*cos),
                    (nowPoint[1]-self.radius*sin))
        return newPoint

    def check(self, pointList):
        nowPoint = (self.graph.nodesInfo[self.curNodeID]['PosX'],
                    self.graph.nodesInfo[self.curNodeID]['PosY'])
        prePoint = (self.graph.nodesInfo[self.preID]['PosX'],
                    self.graph.nodesInfo[self.preID]['PosY'])
        delta = 0.1
        realPoint = []
        for p in pointList:
            if math.fabs(self.distance(PosA=p, PosB=nowPoint)-self.radius) <= delta and math.fabs(self.distance(PosA=p, PosB=prePoint)-self.radius) <= delta:
                realPoint.append((int(p[0]), int(p[1])))
        return realPoint

    def get_nextnode(self):
        # 取得下一個node，如果沒有就回傳None
        curDistance = self.distance(self.curNodeID, self.destNodeID)
        minDistance = curDistance
        nextNodeID = None
        curNeighbor = self.graph.get_neighbor(self.curNodeID)
        for nodeID in curNeighbor:
            newDistance = self.distance(nodeID, self.destNodeID)
            # print("new Distance", nodeID, newDistance)
            if newDistance < minDistance:
                nextNodeID = nodeID
        return nextNodeID

    def run(self, buildFinish, Frames, console=None):
        if console == None:
            outputStream = print
        else:
            outputStream = console.appendContent
            print("hello")

        print("Build function", threading.get_ident())
        print("Now threads = ", threading.active_count())
        count = 0
        # outputStream("I want run")
        origin = console.content
        while self.curNodeID != self.destNodeID:
            # print("I still building")
            nextNodeId = self.get_nextnode()
            outputStream("next node is" + str(nextNodeId))
            if nextNodeId != None:
                # greedy part
                curx = self.graph.nodesInfo[self.curNodeID]['PosX']
                cury = self.graph.nodesInfo[self.curNodeID]['PosY']
                nextx = self.graph.nodesInfo[nextNodeId]['PosX']
                nexty = self.graph.nodesInfo[nextNodeId]['PosY']
                self.preID = self.curNodeID
                self.curNodeID = nextNodeId
                color = self.graph.nodesInfo[self.curNodeID]['Color']
                self.graph.update_node_color(self.curNodeID, (255, 255, 0))
                self.frames.append(self.graph.draw())
                self.graph.update_node_color(self.curNodeID, color)
            else:
                # recovery part

                stuckDis = self.distance(
                    NodeAID=self.curNodeID, NodeBID=self.destNodeID)
                self.stuckNodeID = self.curNodeID
                self.preID = self.curNodeID
                hopCount = 10
                # -----------------------CS------------------------------
                while hopCount > 0 and self.distance(NodeAID=self.curNodeID, NodeBID=self.destNodeID) >= stuckDis:

                    end_point = self.chooseSp(self.stuckNodeID, self.preID)
                    # outputStream("end_point"+str(end_point))
                    curx = self.graph.nodesInfo[self.curNodeID]['PosX']
                    cury = self.graph.nodesInfo[self.curNodeID]['PosY']
                    maxLen1 = int(self.maxNeighbor(self.preID))
                    maxLen2 = int(self.maxNeighbor(self.curNodeID))
                    Len1 = int(self.distance(self.curNodeID, self.preID))
                    if Len1 == 0:
                        Len1 = maxLen1
                    print(Len1)
                    circle1 = RadiusCircle(
                        self.frames.frames[-1].surface, Len1, (curx, cury))
                    circle1.show()
                    prex = self.graph.nodesInfo[self.preID]['PosX']
                    prey = self.graph.nodesInfo[self.preID]['PosY']
                    circle2 = RadiusCircle(
                        self.frames.frames[-1].surface, Len1, (prex, prey))
                    circle2.show()
                    # maxLen = self.maxNeighbor()
                    curve = Curve((curx, cury), end_point,
                                  maxLen2, self.InitSurface)
                    neighborsPos = []
                    for n in self.graph.get_neighbor(self.curNodeID):
                        tmp = []
                        tmp.append(n)
                        tmp.append(self.graph.nodesInfo[n]['PosX'])
                        tmp.append(self.graph.nodesInfo[n]['PosY'])
                        neighborsPos.append(tmp)
                    angle, nextNodeId = curve.findNext(neighborsPos)
                    if nextNodeId != None:
                        outputStream("next node is" + str(nextNodeId))
                        self.frames.append(
                            self.graph.draw(), curve=curve, angle=angle)
                        self.preID = self.curNodeID
                        self.curNodeID = nextNodeId
                        curNeighbor = self.graph.get_neighbor(self.curNodeID)
                        # 更新curNode的顏色
                        color = self.graph.nodesInfo[self.curNodeID]['Color']

                        self.graph.update_node_color(
                            self.curNodeID, (255, 255, 0))
                        tmpColor = []
                        for n in curNeighbor:
                            tmpColor.append(self.graph.nodesInfo[n]['Color'])
                            self.graph.update_node_color(
                                n, (255, 0, 255))
                        self.frames.append(self.graph.draw())
                        self.graph.update_node_color(self.curNodeID, color)
                        # 更新curNeighbor的顏色
                        count = 0
                        for n in curNeighbor:
                            self.graph.update_node_color(n, tmpColor[count])
                            count += 1
                        hopCount -= 1
                    else:
                        # outputStream("stuck")
                        hopCount = 0
                        break

                if hopCount > 0:
                    outputStream("find it")
                else:
                    outputStream("No find")
                    break
        buildFinish[0] = True
        Frames.append(self.frames)

    def maxNeighbor(self, ID):
        neighbor = self.graph.get_neighbor(ID)
        maxDistance = 0
        premaxDistance = 0
        n = 0
        for i in neighbor:
            maxDistance = max(maxDistance, self.distance(ID, i))
            if(premaxDistance != maxDistance):
                premaxDistance = maxDistance
                n = i
        print(ID, n, " : ", maxDistance)
        return maxDistance


class AdaptiveCS(CS):
    def __init__(self, graph, surface):
        super().__init__(graph, surface)
        self.frames = FrameList(0)
        self.minSize = self.graph.parasList['MinSize']
        # self.highlights = {"Initial":["adCS.html",0,2],"Greedy":["adCS.html",4,9],"Recovery":["att.html",]}
        self.highlights = {"Initial": ["adCS.html", 0, 2], "Greedy": ["adCS.html", 4, 9], "RecoveryInit": ["adCS.html", 18, 24], "RecoverySame": [
            "adCS.html", 40, 51], "RecoveryDiff": ["adCS.html", 29, 32], "RecoveryTerminate": ["adCS.html", 27, 28]}
        '''
        super().__init__(graph)
        self.curNodeID = self.graph.parasList["Start"]
        self.destNodeID = self.graph.parasList["Destination"]
        self.InitSurface = surface
        self.radius = self.graph.parasList['Radius']
        self.frames = FrameList()
        self.preID = None
        '''

    def findNext(self, curve):
        N_cur = self.graph.get_neighbor(self.curNodeID)
        neighborPos = []
        for n in N_cur:
            x = self.graph.nodesInfo[n]['PosX']
            y = self.graph.nodesInfo[n]['PosY']
            neighborPos.append((n, x, y))
        angle, nextNode = curve.findNext(neighborPos)
        return nextNode, angle

    def greedy(self):
        '''
        if greedy success
            return next
        else
            return None
        '''
        N_cur = self.graph.get_neighbor(self.curNodeID)
        for n in N_cur:
            if self.distance(n, self.destNodeID) < self.distance(self.curNodeID, self.destNodeID):
                return n
        return None

    def att(self, V_cur, N_cur, V_pre, stuckNode):
        V_k = self.graph.get_longest_neighbor(self.curNodeID)
        print("V_k = ", V_k)
        r = math.ceil(max(self.minSize, self.distance(self.curNodeID, V_k)))
        print("In att V_pre = ", V_pre, "V_cur = ", V_cur)
        endPoint = self.chooseSp(stuckNode, V_pre)
        curx = self.graph.nodesInfo[self.curNodeID]['PosX']
        cury = self.graph.nodesInfo[self.curNodeID]['PosY']

        curve = Curve((curx, cury), endPoint, r, self.InitSurface)
        V_next, angle = self.findNext(curve)
        self.frames.append(self.graph.draw(), curve=curve,
                           angle=angle, highlight=self.highlights["RecoveryInit"])
        r = math.ceil(
            max(self.minSize, self.distance(self.curNodeID, V_next)))
        curve = Curve((curx, cury), endPoint, r, self.InitSurface)
        count = 0
        while V_next != None:
            if count >= 20:
                break
            print("In att next = ", V_next)
            if r <= self.minSize:
                print("smaller than minSzie")
                break
            elif r > self.minSize and V_next != V_k:
                print("V_next != V_k")
                V_k = V_next

                # curve.radius = r
                V_next, angle = self.findNext(curve)

                self.frames.append(self.graph.draw(
                ), curve=curve, angle=angle, highlight=self.highlights["RecoveryDiff"])
                print("previous radius = ", curve.radius)
                r = math.ceil(
                    max(self.minSize, self.distance(self.curNodeID, V_next)))

                curve = Curve((curx, cury), endPoint, r, self.InitSurface)
                print("after radius = ", curve.radius)
            elif r > self.minSize and V_next == V_k:
                print("V_next == V_k")
                V_next = self.eSW(self.curNodeID, N_cur, V_pre, V_k)
                if V_next == V_k:
                    print("same as V_k")
                    return V_next
                else:
                    r = math.ceil(
                        max(self.minSize, self.distance(self.curNodeID, V_next)))
            count += 1
        return None

    def eSW(self, V_cur, N_cur, V_pre, V_k):
        hitNode = V_k
        newR = self.distance(self.curNodeID, V_k)
        ratio = 0.995
        curx = self.graph.nodesInfo[V_cur]['PosX']
        cury = self.graph.nodesInfo[V_cur]['PosY']
        endx = self.graph.nodesInfo[V_k]['PosX']
        endy = self.graph.nodesInfo[V_k]['PosY']
        curve = Curve((curx, cury), (endx, endy), newR, self.InitSurface)
        angle = 360
        originalRadius = curve.radius
        for theta in range(360):
            # print("In esw")
            newR *= ratio
            curve.radius = newR

            if(newR < self.minSize):
                angle = theta
                break
            (hing, end) = curve.afterRotatePos(theta)
            for n in N_cur:
                nx = self.graph.nodesInfo[n]['PosX']
                ny = self.graph.nodesInfo[n]['PosY']
                if(curve.hitNode(hing, end, (nx, ny))):
                    # print("hit", n)
                    hitNode = n
                    angle = theta
        curve.radius = originalRadius
        color = self.graph.nodesInfo[self.curNodeID]['Color']
        self.graph.update_node_color(self.curNodeID, (255, 255, 0))
        self.frames.append(self.graph.draw(), curve=curve,
                           angle=angle, descreasing=True, highlight=self.highlights['RecoverySame'])
        self.graph.update_node_color(self.curNodeID, color)
        print("return hitnode", hitNode)
        return hitNode

        # pass

    def run(self, buildFinish, Frames, console=None):
        N_cur = self.graph.get_neighbor(self.curNodeID)
        count = 0
        while self.curNodeID != self.destNodeID and self.curNodeID != None:
            count += 1
            if count > 20:
                break
            nextNode = self.greedy()
            if nextNode != None:
                print("greedy success")
                self.curNodeID = nextNode
                N_cur = self.graph.get_neighbor(self.curNodeID)
                color = self.graph.nodesInfo[self.curNodeID]['Color']
                self.graph.update_node_color(self.curNodeID, (255, 255, 0))
                self.frames.append(self.graph.draw(),
                                   highlight=self.highlights["Greedy"])
                self.graph.update_node_color(self.curNodeID, color)
            else:
                print("Stuck at ", self.curNodeID)
                V_pre = self.curNodeID
                self.preID = V_pre
                stuckNodeID = self.curNodeID
                while self.distance(self.curNodeID, self.destNodeID) >= self.distance(stuckNodeID, self.destNodeID):
                    color = self.graph.nodesInfo[self.curNodeID]['Color']
                    self.graph.update_node_color(self.curNodeID, (255, 255, 0))
                    self.frames.append(
                        self.graph.draw(), highlight=self.highlights["RecoveryInit"])
                    self.graph.update_node_color(self.curNodeID, color)
                    tmp = self.curNodeID
                    self.curNodeID = self.att(
                        self.curNodeID, N_cur, V_pre, stuckNodeID)
                    if self.curNodeID == None:
                        break
                    N_cur = self.graph.get_neighbor(self.curNodeID)
                    V_pre = tmp
                    self.preID = V_pre
        buildFinish[0] = True
        Frames.append(self.frames)


class BFS(Algorithm):
    def __init__(self, graph, graphSurface):
        self.graphSurface = graphSurface
        super().__init__(graph)
        self.frames = FrameList(1)

    def run(self, buildFinish, Frames, console=None):
        if console != None:
            ostream = console.appendContent
        else:
            ostream = print
        explored = []

        start = self.graph.parasList['Start']
        parent = {start: None}
        queue = [start]
        curNode = start
        end = self.graph.parasList['Destination']
        while queue != [] and curNode != end:
            curNode = queue[0]
            queue.pop(0)
            self.graph.update_node_color(
                curNode, (255, 255, 0))
            self.frames.append(self.graph.draw())
            self.graph.update_node_color(curNode, (0, 0, 0))
            explored.append(curNode)
            for v in self.graph.get_neighbor(curNode):
                if v not in explored and v not in queue:
                    print("append", v)
                    print("Now queue", queue)
                    print("Now explored", explored)
                    queue.append(v)
                    parent[v] = curNode
        if curNode == end:
            ostream("Find path !")
        else:
            ostream("No solution !")
            buildFinish[0] = True
            Frames.append(self.frames)
            return

        curNode == end
        while(parent[curNode] != None):
            self.graph.update_node_color(curNode, (50, 100, 200))
            curNode = parent[curNode]
        self.graph.update_node_color(curNode, (50, 100, 200))
        self.frames.append(self.graph.draw())
        Frames.append(self.frames)
        buildFinish[0] = True


class TestCurve(Algorithm):
    def __init__(self, graph, surface):
        super().__init__(graph)
        self.InitSurface = surface
        self.frames = FrameList(TestCurve)

    def run(self, buildFinish, Frames, console=None):
        width = self.InitSurface.get_width()
        height = self.InitSurface.get_height()
        centerX = width/2
        centerY = height/2
        r = 200
        end_point = (centerX+200, centerY)
        curve = Curve((centerX, centerY), end_point, r, self.InitSurface)
        self.frames.append(self.graph.draw(), curve=curve,
                           angle=230, descreasing=True)
        buildFinish[0] = True
        Frames.append(self.frames)
