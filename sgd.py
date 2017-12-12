import numpy as np
import random
import sys
import numpy.linalg as lin

# Convert text file to a matrix
def getMatrix(fileName):
    matrix = np.loadtxt(fileName, usecols=range(54), delimiter=",")
    return matrix


# Add a ones column to the matrix at column 0
def appendOnesCol(matrix):
    onesCol = np.ones(shape=(len(matrix), 1))
    return np.c_[onesCol, matrix]


# Generate a random weight vector of dimension d
def getRandomWeightVector(d):
    rand = np.zeros(d)
    for i in range(len(rand)):
        rand[i] = random.uniform(0, 1)
    return rand


def sgd():
    # Input
    train = sys.argv[1]
    test = sys.argv[2]
    eps = float(sys.argv[3])
    eta = float(sys.argv[4])

    trainingSet = getMatrix(train)
    testSet = getMatrix(test)

    # d = d + 1
    d = len(trainingSet[0]) + 1

    trainingSet = appendOnesCol(trainingSet)

    # Create a copy of the training set
    newTrainingSet = appendOnesCol(getMatrix(train))
    testSet = appendOnesCol(testSet)

    randWeight = getRandomWeightVector(d)

    prevWeight = np.zeros(d)

    for  i in range(0, len(trainingSet)):
        if trainingSet[i][d-1] == 2:
            trainingSet[i][d-1] = -1
        # Consider borderline as a AT RISK
        elif trainingSet[i][d-1] == 3:
            trainingSet[i][d-1] = 1

    for i in range(0, len(testSet)):
        if testSet[i][d-1] == 2:
            testSet[i][d-1] = -1
        # Consider borderline as a AT RISK
        elif testSet[i][d-1] == 3:
            testSet[i][d-1] = 1

    for i in range(len(newTrainingSet)):
        newTrainingSet[i][d - 1] = 1

    r = list(range(len(trainingSet)))
    random.shuffle(r)
    i = 0
    while (lin.norm(randWeight - prevWeight) > eps):
        i += 1
        print("Iteration {0} {1}".format(i, lin.norm(randWeight - prevWeight)))

        prevWeight = randWeight
        for k in r:
            randWeight = randWeight + (
                eta * 1.0 / (1.0 + np.exp(trainingSet[k][d - 1] * randWeight.dot(newTrainingSet[k][:])))
                * trainingSet[k][d - 1] * newTrainingSet[k][:])

    # Create a new set for testing
    newTestSet = getMatrix(test)
    newTestSet = appendOnesCol(newTestSet)

    for i in range(len(newTestSet)):
        newTestSet[i][d - 1] = 1

    numCorrect = 0

    for i in range(len(newTestSet)):
        if (randWeight.dot(newTestSet[i][:]) >= .5 and testSet[i][d - 1] == 1):
            numCorrect += 1
        elif (randWeight.dot(newTestSet[i][:]) < .5 and testSet[i][d - 1] == -1):
            numCorrect += 1

    print("w: " + str(randWeight))
    print("Accuracy: " + str((float(numCorrect) / len(testSet))*100).format() + "%")

    return randWeight

# Run SGD
w = sgd()

m = appendOnesCol(getMatrix("data.csv"))
mNew = appendOnesCol(getMatrix("data.csv"))

for i in range(len(m)):
    if m[i][len(m[0])-1] != 1 or m[i][len(m[0])-1] != 3:
        np.delete(m, i, 0)
    if mNew[i][len(m[0])-1] != 1 or mNew[i][len(m[0])-1] != 3:
        np.delete(mNew, i, 0)

for i in range(len(m)):
    if m[i][len(m[0])-1] == 2:
        m[i][len(m[0])-1] = -1
    # Consider borderline as a AT RISK
    elif m[i][len(m[0])-1] == 3:
        m[i][len(m[0])-1] = 1

for i in range(len(mNew)):
    mNew[i][len(mNew[0])-1] = 1

numCorrect = 0

for i in range(len(m)):
    if w.dot(mNew[i][:]) >= .5 and m[i][len(m[0])-1] == 1:
        numCorrect += 1
    if w.dot(mNew[i][:]) < .5 and m[i][len(m[0])-1] == -1:
        numCorrect += 1

print("Accuracy on actual Diabetics: "
        + str((float(numCorrect) / len(m))*100).format() + "%")
