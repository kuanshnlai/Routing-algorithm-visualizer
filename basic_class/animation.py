import pygame
import pygame_gui
import time
from basic_class.component import *
from basic_class.constantDef import *
import threading
import numpy


class Animation:
    def __init__(self, Algorithm_Class, graph, manager, window_surface, playState, graphRegionOffset, graphRegion, displayRegion, outputStream=None):
        self.frames = FrameList(Algorithm_Class)
        self.Algorithm_Class = Algorithm_Class
        self.graph = graph
        self.manager = manager
        self.window_surface = window_surface
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(60)/1000.0
        self.playState = playState
        self.graphRegionOffset = graphRegionOffset
        self.graphSurface = graphRegion
        self.displayRegion = displayRegion
        self.res = []
        self.outputStream = outputStream

    def build(self, finish):
        self.res = []
        if(self.graph.is_compile == False):

            t = threading.Thread(
                target=self.Algorithm_Class(self.graph, self.displayRegion).run, args=(finish, self.res, self.outputStream))

            t.start()
        else:
            self.frames = self.frames

    def play(self, finish):
        self.outputStream.clear()
        self.outputStream.appendContent("Start Play")
        print("Now play")
        self.frames = self.res[0]
        print(finish)
        print(self.playState)
        finish[0] = False

        frameCount = 0

        while not finish[0] and frameCount in range(len(self.frames)):
            content = ""
            self.outputStream.clear()
            highlightRate = self.frames.frames[frameCount].highlightRate
            for line in self.frames.frames[frameCount].content:
                content += line
            self.outputStream.appendContent(content)
            self.outputStream.moveToPos(highlightRate)
            delay_rate = self.frames.frames[frameCount].delay
            if(self.playState[0] == PLAYSTATE):
                pass
            elif(self.playState[0] == PAUSESTATE):
                pass
            elif(self.playState[0] == PREVIOUS):
                pass
            elif (self.playState[0] == NEXT):
                pass
            else:
                finish[0] = True
                return
            if frameCount == 1:
                self.playState[1] = FIRSTSTATE
            elif frameCount == len(self.frames)-1:
                self.playState[1] = LASTSTATE
            else:
                self.playState[1] = INTERMIDIATESTATE
            if self.frames.frames[frameCount].subFrame != None:
                curve = self.frames.frames[frameCount].subFrame[0]
                angle = self.frames.frames[frameCount].subFrame[1]
                descreasing = self.frames.frames[frameCount].subFrame[2]
                print("type = ", type(self.frames.frames[frameCount].surface))
                subFrame = curve.rotateToAngle(
                    angle, self.frames.frames[frameCount].surface, descreasing)
                subId = 0
                subFinish = False
                for f in subFrame:
                    if(subFinish):
                        break
                    for d in range(3):
                        if(subFinish):
                            break
                        self.displayRegion.blit(
                            f, (0, 0))
                        # self.window_surface.blit(
                        #     self.graphSurface, self.graphRegionOffset)
                        self.graphSurface.set_image(self.displayRegion)
                        pygame.display.update()
                        self.manager.draw_ui(self.window_surface)
                        self.manager.update(self.time_delta)
                        if(self.playState[0] == PAUSESTATE):
                            # print("Pause signal")
                            pauseFrameInd = frameCount
                            frameCount = self.pause(
                                frameCount, finish, subFrame, subId)
                            if finish[0]:
                                break
                            if frameCount != pauseFrameInd:
                                subFinish = True
                                break
                        elif(self.playState[0] == PREVIOUS):
                            frameCount = self.previousStep(frameCount)
                            subFinish = True
                            break
                        elif(self.playState[0] == NEXT):
                            frameCount = self.nextStep(frameCount)
                            subFinish = True
                            break
                        elif(self.playState[0] == PLAYSTATE):
                            pass
                        else:
                            finish[0] = True
                            return
                    subId += 1
            else:
                for c in range(delay_rate):
                    # 測試
                    self.displayRegion.blit(
                        self.frames.frames[frameCount].surface, (0, 0))
                    # self.window_surface.blit(
                    #     self.graphSurface, self.graphRegionOffset)
                    self.graphSurface.set_image(self.displayRegion)
                    pygame.display.update()
                    self.manager.draw_ui(self.window_surface)
                    self.manager.update(self.time_delta)
                    if(self.playState[0] == PAUSESTATE):
                        # print("Pause signal")
                        frameCount = self.pause(frameCount, finish)
                        if finish[0]:
                            break
                    elif(self.playState[0] == PREVIOUS):
                        frameCount = self.previousStep(frameCount)
                        break
                    elif(self.playState[0] == NEXT):
                        frameCount = self.nextStep(frameCount)
                        break
                    elif(self.playState[0] == PLAYSTATE):
                        pass
                    else:
                        print("Stop signal")
                        finish[0] = True
                        return
            if(self.playState[0] == PAUSESTATE):
                frameCount = self.pause(frameCount, finish)
            elif(self.playState[0] == PREVIOUS):
                frameCount = self.previousStep(frameCount)
            elif(self.playState[0] == NEXT):
                frameCount = self.nextStep(frameCount)
            frameCount += 1
        finish[0] = True

    def pause(self, nowFrameInd, finish, subFrame=None, subFrameInd=None):
        # print("Now Pause")
        if(subFrame != None and subFrameInd != None):
            while(self.playState[0] != PLAYSTATE or subFrame != None):
                # pygame.time.delay(1000)
                if self.playState[0] == PREVIOUS:
                    subFrame = None
                    subFrameInd = None
                    nowFrameInd = self.previousStep(nowFrameInd)
                    break
                elif self.playState[0] == NEXT:
                    # Call previous function to return new frame want show on screen
                    subFrame = None
                    subFrameInd = None
                    nowFrameInd = self.nextStep(nowFrameInd)
                    break
                elif self.playState[0] == PAUSESTATE:
                    pass
                elif self.playState[0] == PLAYSTATE:
                    break
                else:
                    print("Terminate!")
                    finish[0] = True
                    return -1
                # 測試

                self.displayRegion.blit(subFrame[subFrameInd], (0, 0))
                # self.window_surface.blit(
                #     self.graphSurface, self.graphRegionOffset)
                self.graphSurface.set_image(self.displayRegion)
                pygame.display.update()
                self.manager.draw_ui(self.window_surface)
                self.manager.update(self.time_delta)
        if(subFrame == None and subFrameInd == None):
            while(self.playState[0] != PLAYSTATE):
                # pygame.time.delay(1000)
                if self.playState[0] == PREVIOUS:
                    subFrame = None
                    subFrameInd = None
                    nowFrameInd = self.previousStep(nowFrameInd)
                elif self.playState[0] == NEXT:
                    # Call previous function to return new frame want show on screen
                    subFrame = None
                    subFrameInd = None
                    nowFrameInd = self.nextStep(nowFrameInd)
                elif self.playState[0] == PAUSESTATE:
                    pass
                elif self.playState[0] == PLAYSTATE:
                    break
                else:
                    finish[0] = True
                    return -1
                # 測試
                self.displayRegion.blit(
                    self.frames.frames[nowFrameInd].surface, (0, 0))
                # self.window_surface.blit(
                #     self.graphSurface, self.graphRegionOffset)
                self.graphSurface.set_image(self.displayRegion)
                pygame.display.update()
                self.manager.draw_ui(self.window_surface)
                self.manager.update(self.time_delta)

        print("Pause Finish")
        return nowFrameInd

    def nextStep(self, nowFrameInd):
        print("Now next")
        if nowFrameInd == len(self.frames)-1:
            print("No more frame")
            nextInd = nowFrameInd
        else:
            nextInd = nowFrameInd+1
            if nextInd == len(self.frames)-1:
                self.playState[1] = LASTSTATE
        self.playState[0] = PAUSESTATE
        return nextInd

    def previousStep(self, nowFrameInd):
        print("Now Pause")
        if nowFrameInd == 0:
            print("No previous frame")
            nextInd = nowFrameInd
        else:
            nextInd = nowFrameInd-1
            if nextInd == 0:
                self.playState[1] = FIRSTSTATE
        self.playState[0] = PAUSESTATE
        return nextInd

    def clear(self):
        pass
