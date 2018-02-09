import pygame
import numpy as np

playerX, playerY = 0,0
blockWidth,blockHeight = 50,50
gameExit = False
NUM_EPOCHS = 1000
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

GAMMA = 0.99
PCorrect = 0.8
PWrong = 0.1

nBlocksHorizontal, nBlocksVertical = 4, 3
displayWidth, displayHeight = blockWidth * nBlocksHorizontal, blockHeight * nBlocksVertical
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

r = -0.02 * np.ones((3,4))
r[0][3] = 1
r[1][3] = -1

viableStates = np.ones((nBlocksVertical,nBlocksHorizontal))
viableStates[1][1] = 0 

valueMtx = np.zeros((nBlocksVertical, nBlocksHorizontal))

def getViable(value, bound):
	# viableValue = (value + bound) % bound
	if value < 0:
		return 0
	if value >= bound:
		return bound-1
	return value
	# return viableValue

def findBestMoveReward(playerY, playerX):
	global r, valueMtx
	nextX, nextY = 0,0
	maxReward = 0
	rewardsPerAction = np.zeros((4,1))
	for i in range(0,rewardsPerAction.shape[0]):
		if i == 0:
			nextX = getViable(playerX, nBlocksHorizontal)
			nextY = getViable(playerY - 1, nBlocksVertical)
			veerLeftX = getViable(playerX - 1, nBlocksHorizontal)
			veerLeftY = getViable(playerY, nBlocksVertical)
			veerRightX = getViable(playerX + 1, nBlocksHorizontal)
			veerRightY = getViable(playerY, nBlocksVertical)
		elif i == 1:
			nextX = getViable(playerX + 1, nBlocksHorizontal)
			nextY = getViable(playerY, nBlocksVertical)
			veerLeftX = getViable(playerX, nBlocksHorizontal)
			veerLeftY = getViable(playerY - 1, nBlocksVertical)
			veerRightX = getViable(playerX, nBlocksHorizontal)
			veerRightY = getViable(playerY + 1, nBlocksVertical)
		elif i == 2:
			nextX = getViable(playerX, nBlocksHorizontal)
			nextY = getViable(playerY + 1, nBlocksVertical)
			veerLeftX = getViable(playerX + 1, nBlocksHorizontal)
			veerLeftY = getViable(playerY, nBlocksVertical)
			veerRightX = getViable(playerX - 1, nBlocksHorizontal)
			veerRightY = getViable(playerY, nBlocksVertical)
		elif i == 3:
			nextX = getViable(playerX, nBlocksHorizontal)
			nextY = getViable(playerY - 1, nBlocksVertical)
			veerLeftX = getViable(playerX, nBlocksHorizontal)
			veerLeftY = getViable(playerY + 1, nBlocksVertical)
			veerRightX = getViable(playerX, nBlocksHorizontal)
			veerRightY = getViable(playerY - 1, nBlocksVertical)
		if viableStates[nextY][nextX] == 0:
			nextY,nextX = playerY, playerX
		if viableStates[veerLeftY][veerLeftX] == 0:
			veerLeftY,veerLeftX = playerY, playerX
		if viableStates[veerRightY][veerRightX] == 0:
			veerRightY,veerRightX = playerY, playerX
		# if np.abs(r[playerY][playerX]) < 1: 
		# print "i = {}\t nextX = {}\tnextY = {}\tveerLeftX = {}\tveerLeftY = {}\tveerRightX = {}\tveerRightY = {}\t".format(i,nextX,nextY,veerLeftX,veerLeftY,veerRightX,veerRightY)
		rewardsPerAction[i] = 0.8 * valueMtx[nextY][nextX] + 0.1* valueMtx[veerRightY][veerRightX] + 0.1 * valueMtx[veerLeftY][veerLeftX]
	maxReward = np.max(rewardsPerAction)
	return maxReward

def updateScreen():
	global gameDisplay
	gameDisplay.fill(black)
	for i in range(0, r.shape[0]):
		for j in range(0, r.shape[1]):
			if viableStates[i][j] == 1:
				if(np.abs(r[i][j]) < 1):
					pygame.draw.rect(gameDisplay, white, [blockWidth * j, blockWidth * i, blockWidth, blockHeight])
				elif(r[i][j] == 1):
					pygame.draw.rect(gameDisplay, green, [blockWidth * j, blockWidth * i, blockWidth, blockHeight])
				elif(r[i][j] == -1):
					pygame.draw.rect(gameDisplay, red, [blockWidth * j, blockWidth * i, blockWidth, blockHeight])
			else:
				pygame.draw.rect(gameDisplay, black, [blockWidth * j, blockHeight * i, blockWidth, blockHeight])
	pygame.draw.rect(gameDisplay, blue, [blockWidth * playerX, blockHeight * playerY, blockWidth, blockHeight])
	pygame.display.update()

def valueIteration():
	global playerY, playerX, valueMtx
	#for a specific number of epochs:
	for i in range(NUM_EPOCHS):
		#traverse all states:
		for j in range(0, nBlocksVertical):
			for k in range(0, nBlocksHorizontal):
				playerY, playerX = j, k
				if viableStates[playerY][playerX] == 1:
					updateScreen()
					if np.abs(r[playerY][playerX]) < 1:
						valueMtx[playerY][playerX] = r[playerY][playerX] + GAMMA * findBestMoveReward(playerY, playerX)
					elif np.abs(r[playerY][playerX]) == 1 :
						valueMtx[playerY][playerX] = r[playerY][playerX]
				print valueMtx

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()
	updateScreen()
	valueIteration()

'''
Actions:
	0 : North
	1 : East
	2 : South
	3 : West
Psa = 0.1 LeftVeer, 0.8 Correct , 0.1 RightVeer
''' 
