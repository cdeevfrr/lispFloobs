
import random
import time

foodMultiplier = 5
foodsPerRain = 7
jungleFoodsPerRain = 15
rainFrequency = 4
boardWidth = 20
jungleLengthRatio = 2
startingFood = 10
foodForBirth = 30
birthCost = 5
numMutations = 2
excessMoveFoodCost = 1
unavoidableFoodCost = .1
directionalities = {
            0: '↖',
            1: '↑',
            2: '↗',
            3: '←',
            4: '•',
            5: '→',
            6: '↙',
            7: '↓',
            8: '↘',
        }
foodSymbol = '*'


class Floob:
    # int[] genotype
    # int[] location
    # int food
    def __init__(self, genotype, location):
        genotype = list(map(lambda x: 0 if x < 0 else x, genotype))
        sm = sum(genotype)
        self.genotype = list(map(lambda x: x / sm, genotype))
        self.location = location
        # Let everyone start off with some food.
        self.food = startingFood
        self.age = 0

    def __str__(self):
        return "Fd: " + str(round(self.food)) + " Age: " + str(self.age) + " Loc: " + str(self.location) + " MaxGene: " + str(self.maxGene())

    def representation(self):
        return directionalities[self.maxGene()['index']]
        
    def maxGene(self):
        maxGene = {'index': -1, 'value': 0}
        for i, gene in enumerate(self.genotype):
            if (gene > maxGene['value']):
                maxGene['index'] = i
                maxGene['value'] = gene
        return maxGene

    # From the point of view of a floob, the board is infinite.
    # We'll let the board handle wrapping concerns after a floob moves.
    # Returns new location.
    def move(self):
        direction = self.randomDirection()
        # We could just use a switch, but I wanted to be cleverer.
        # Careful ordering of the genes allows this to work
        self.location = [self.location[0] + direction // 3 - 1, self.location[1] + direction % 3 - 1]
        if (direction != 4):
            self.food -= excessMoveFoodCost
        self.food -= unavoidableFoodCost
        self.age += 1
       
    # returns int, 4 = no movement because 4%3 == 4//3 == 1 for convenience.
    # Relies on the fact that sum(genotype) is within roundoff of 1.
    def randomDirection(self):
        runningSum = 0
        cutoff = random.random()
        for i, gene in enumerate(self.genotype):
            runningSum += gene
            if (runningSum > cutoff):
                return i
        # This should almost never happen
        print("Not respecting genotype due to roundoff: " + str(self))
        return random.randint(0,8)


    def child(self):
        self.food -= birthCost

        newGenotype = [ i for i in self.genotype]
        for i in range(numMutations):
            toMutate = random.randint(0, len(newGenotype) - 1)
            newGenotype[toMutate] += 5*random.random() - 1
        result = Floob(newGenotype, self.location)
        return result


class Board:
    # The board is just 0 if there's no food, 1 if there's food.
    # To render, make the board in text, then replace each floob
    # location with an M.
    def __init__(self, width, numFloobs):
        self.board = [[0 for x in range(width)] for _ in range(width)]
        self.floobs = [Floob(randomGenotype(), self.randomLocation(width)) for _ in range(numFloobs)]
        self.width = width
        self.raincount = 0

    # Consume the food at this location and return the amount of food consumed.
    def eatFoodAt(self, location):
        x = self.board[location[0]][location[1]]
        self.board[location[0]][location[1]] = 0
        return x

    def makeFood(self):
        # make the same number of pieces of food in the jungle, (1/4 of the area) and anywhere.
        for i in range(foodsPerRain):
            self.addFood(self.randomLocation(self.width))
        for i in range(jungleFoodsPerRain):
            self.addFood(self.randomLocation(self.width // jungleLengthRatio)) 

    def addFood(self, location):
        self.board[location[0]][location[1]] = 1

    def randomLocation(self, maxWidth):
        return [random.randint(0, maxWidth - 1), random.randint(0, maxWidth - 1)]
        
    def tick(self):
        self.raincount += 1
        if (self.raincount > rainFrequency):
            self.raincount = 0
            # Make it RAIN!!!
            self.makeFood()
        nextGeneration = []
        for floob in self.floobs:
            # Eat, move, possibly eat again
            floob.food += foodMultiplier * self.eatFoodAt(floob.location)
            floob.move()
            floob.location = self.withinBounds(floob.location)
            floob.food += foodMultiplier * self.eatFoodAt(floob.location)
            # Give birth
            if(floob.food > foodForBirth):
                nextGeneration.append(floob.child())
            # die by not being included in the next generation
            if (floob.food >= 0):
                nextGeneration.append(floob)
        self.floobs = nextGeneration

    def withinBounds(self, location):
        return [location[0]%self.width, location[1]%self.width]

    def __str__(self):
        output = [ [' ' if i==0 else foodSymbol for i in row] for row in self.board]
        for floob in self.floobs:
            output[floob.location[0]][floob.location[1]] = floob.representation()
        return "\n".join(["".join(map(str, row)) for row in output])

    def printPopulation(self):
        for floob in self.floobs:
            print(floob) 


def randomGenotype():
    result = [random.random() for _ in range(9)]
    result[4] += 1
    return result


b = Board(boardWidth, 10)
for i in range(3):
    b.makeFood()
for i in range(3000):
    print(b)
    b.tick()
    time.sleep(.2)
print(b)
b.printPopulation()

            
        

