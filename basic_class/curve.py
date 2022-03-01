import pygame
import pygame_gui
import numpy as np
import math


class Curve():
    def __init__(self, hing_point, end_point, radius, startSurface):
        # hing point 弧掛在某個固定的點
        # end_point 弧隨著時間可能會旋轉改變位置
        # radius   弧的半徑
        # startSurface 弧一開始的frame
        self.hing_point = hing_point
        self.end_point = end_point
        self.radius = radius
        self.startSurface = startSurface
        self.count = 0

    def afterRotatePos(self, angle):
        # 算出curve rotate 某個角度後他的hing_point和end_point會在哪裡
        # print("In curve radius = ", self.radius)
        initAngle = self.calAngle(self.hing_point, self.end_point)
        times = int(angle/360)
        angle %= 360
        # print("times: ", times, "angle: ", angle)
        theta = angle/180*3.14
        start_point = (int(self.hing_point[0]+self.radius*math.cos(initAngle+theta)),
                       int(self.hing_point[1]-self.radius*math.sin(initAngle+theta)))
        return (self.hing_point, start_point)

    def rotateToAngle(self, angle, surface, descreasing=False):
        # 直接畫在傳來的surface上

        self.count += 1
        initAngle = self.calAngle(self.hing_point, self.end_point)
        count = 0
        times = int(angle/360)
        angle %= 360
        # print("times: ", times, "angle: ", angle)
        frames = []
        # surface = self.startSurface.copy()
        init_end_point = self.end_point
        tmpRadius = self.radius
        for theta in range(0, angle):
            if descreasing == True:
                if self.radius > 50:
                    self.radius = self.radius*0.995
            count += 1
            theta = theta/180*3.14
            start_point = (int(self.hing_point[0]+self.radius*math.cos(initAngle+theta)),
                           int(self.hing_point[1]-self.radius*math.sin(initAngle+theta)))
            self.end_point = start_point
            surface = self.startSurface.copy()
            frames.append(self.draw_curve(surface))
        self.end_point = init_end_point
        self.radius = tmpRadius
        return frames

    def resume(self, bit_array, surface):
        cur_array = bit_array
        pygame.surfarray.blit_array(surface, cur_array)

    def draw_curve(self, surface):
        # 把curve畫在傳入的新surface上
        center = self.calcenter(self.hing_point, self.end_point, self.radius)
        startAngle = self.calAngle(center, self.hing_point)
        endAngle = self.calAngle(center, self.end_point)

        pygame.draw.arc(surface, (0, 0, 0),
                        (center[0]-self.radius, center[1]-self.radius, 2*self.radius, 2*self.radius), endAngle, startAngle)  # surface 是還沒畫過曲線的frame
        pygame.draw.circle(
            surface, (0, 255, 0), (int(self.hing_point[0]), int(self.hing_point[1])), 1, 1)
        pygame.draw.circle(
            surface, (255, 0, 0), (int(self.end_point[0]), int(self.end_point[1])), 1, 1)
        return surface

    def calAngle(self, center, target):
        vectorA = (1, 0)
        vectorB = (target[0]-center[0], target[1]-center[1])
        Alen = (vectorA[0]**2+vectorA[1]**2)**0.5
        Blen = (vectorB[0]**2+vectorB[1]**2)**0.5
        AdotB = vectorA[0]*vectorB[0]+vectorA[1]*vectorB[1]
        if(Alen*Blen == 0):
            ctheta = AdotB/10e-9
        else:
            ctheta = AdotB/(Alen*Blen)
        # return np.arccos(ctheta)
        if(center[1]-target[1] >= 0):
            return np.arccos(ctheta)

        else:
            return -np.arccos(ctheta)+6.28

    def calcenter(self, hing_point, end_point, radius):
        v = np.array((end_point[0] - hing_point[0],
                      end_point[1] - hing_point[1]))
        theta = np.radians(60)
        c, s = np.cos(theta), np.sin(theta)
        rotateMatrix = np.array([[c, -s], [s, c]])
        rv = rotateMatrix.dot(v)
        rvlen = (rv[0]**2+rv[1]**2)**0.5
        if rvlen == 0:
            rvlen = 10e-9
        center = (int(hing_point[0]+(rv[0]/rvlen)*radius),
                  int(hing_point[1]+(rv[1]/rvlen)*radius))
        return center

    def distance(self, PosA, PosB):
        x1 = PosA[0]
        y1 = PosA[1]
        x2 = PosB[0]
        y2 = PosB[1]
        return (((x1-x2)**2)+((y1-y2)**2))**0.5

    def between(self, target, bound1, bound2):
        if bound1 > bound2:
            bound1 -= 6.28
        if bound1 <= target <= (bound2+0.05):
            return True
        return False

    def hitNode(self, hing_point, end_point, nodePos):
        # 回傳curve是否hit到點
        delta = 3
        center = self.calcenter(hing_point, end_point, self.radius)
        # print("determine nodePos ", nodePos)
        if math.fabs(self.distance(center, nodePos) - self.radius) <= delta:
            startAngle = self.calAngle(center, hing_point)
            endAngle = self.calAngle(center, end_point)
            nowAngle = self.calAngle(center, nodePos)
            # print("Angle = ", startAngle, endAngle, nowAngle)
            if self.between(nowAngle, endAngle, startAngle):
                return True
        return False

    def findNext(self, neighborsPos):
        # 回傳(angle,node)
        # angle 表示要旋轉幾度才會找到下個node
        # node 表示下個node是誰
        # 如果沒找到下個點則回傳(360,None)
        # 表示轉一圈都沒找到節點
        angle = 0
        while angle <= 360:
            (hing_point, end_point) = self.afterRotatePos(angle)
            for n in neighborsPos:
                nextNode = n[0]
                x = n[1]
                y = n[2]
                res = self.hitNode(hing_point, end_point, (x, y))
                if res:
                    print("find point", nextNode)
                    return (angle, nextNode)
            else:
                angle += 1
        return (360, None)
