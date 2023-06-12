import numpy as np

# Params for randomization
STANDARD_DEV = 0.0001
np.seterr(all='raise')

W_INDEX = 0
B_INDEX = 1

Z_INDEX = 0
A_INDEX = 1


def init_params(numInputs, allLayerNodes, numOutputs):
    wAndB = []
    numHiddenLayers = len(allLayerNodes)
    W = np.random.rand(allLayerNodes[0], numInputs) - 0.5
    b = np.random.rand(allLayerNodes[0], 1) - 0.5
    wAndB.append([W, b])
    if numHiddenLayers >= 2:
        for i in range(1, numHiddenLayers):
            W = np.random.rand(allLayerNodes[i], allLayerNodes[i-1]) - 0.5
            b = np.random.rand(allLayerNodes[i], 1) - 0.5
            wAndB.append([W, b])
    W = np.random.rand(numOutputs, allLayerNodes[numHiddenLayers-1]) - 0.5
    b = np.random.rand(numOutputs, 1) - 0.5
    wAndB.append([W, b])
    return wAndB


def ReLU(Z):
    return np.maximum(Z, 0)


def sig(Z):
    return 1/(1 + np.exp(-Z))


def softmax(Z):
    if np.max(Z) > 100.0:
        a = 1
    try:
        A = np.exp(Z) / sum(np.exp(Z))
        s = np.sum(A, axis=0)

    except:
        A = 1.0 * (Z == np.max(Z)) + 0.001
    return A


def robust_softmax(Z):
    """Compute softmax for each element in x in
    a robust way to avoid underflow and overflow. """
    z = Z - np.max(Z)
    return np.exp(z) / np.sum(np.exp(z), axis=0)

# def forward_prop(W1, b1, W2, b2, X):


def forward_prop(weightsAndBiases, X):
    numHiddenLayers = len(weightsAndBiases) - 1
    zAndA = []
    # input to first HL
    W = weightsAndBiases[0][W_INDEX]
    b = weightsAndBiases[0][B_INDEX]
    Z = W.dot(X) + b
    A = ReLU(Z)
    zAndA.append([Z, A])

    # HL to HL
    for i in range(1, numHiddenLayers):
        lastA = zAndA[-1][A_INDEX]
        W = weightsAndBiases[i][W_INDEX]
        b = weightsAndBiases[i][B_INDEX]
        Z = W.dot(lastA) + b
        A = ReLU(Z)
        zAndA.append([Z, A])

    # HL to output
    lastA = zAndA[-1][A_INDEX]
    W = weightsAndBiases[numHiddenLayers][W_INDEX]
    b = weightsAndBiases[numHiddenLayers][B_INDEX]
    Z = W.dot(lastA) + b
    A = softmax(Z)
    zAndA.append([Z, A])
    return zAndA


def reshape(data, neededDims):
    while data.ndim < neededDims:
        data = np.expand_dims(data, axis=data.ndim)
    return data


def ReLU_deriv(Z):
    return Z > 0


def getForwardOneHot(array):
    one_hot = np.zeros(array.shape[0], dtype=int)
    maxArg = np.array(array).argmax()
    one_hot[maxArg] = 1
    return array, one_hot, maxArg


def wiggleValues(vals):
    # W is always a 2-D matrix
    dim = vals.shape
    mutatedWeights = np.zeros(dim)
    for r in range(dim[0]):
        for c in range(dim[1]):
            # TODO check that we don't need to bound and re-select if
            # out of bounds
            mutatedWeights[r, c] = np.random.normal(vals[r, c], STANDARD_DEV)
    return mutatedWeights


def one_hot(Y, A):
    one_hot_Y = np.zeros((Y.size, A.shape[0]))
    one_hot_Y[np.arange(Y.size), Y] = 1
    one_hot_Y = one_hot_Y.T
    return one_hot_Y


def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y, useOneHot):
    m = Y.shape[0]  # TODO Check this
    if useOneHot:
        one_hot_Y = one_hot(Y, A2)
        dZ2 = A2 - one_hot_Y
    else:
        dZ2 = (A2 - Y)
    dW2 = 1 / m * dZ2.dot(A1.T)
    err = np.sum(dZ2 ** 2)
    db2 = 1 / m * np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)

    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1)
    return dW1, db1, dW2, db2, err


def backward_prop(zAndA, weightsAndBiases, X, Y, useOneHot):
    m = Y.shape[0]  # TODO Check this
    # Last
    lastZAndA = zAndA[-1]
    secondLastZAndA = zAndA[-2]
    if useOneHot:
        one_hot_Y = one_hot(Y, lastZAndA[A_INDEX])
        dZ = lastZAndA[A_INDEX] - one_hot_Y
    else:
        dZ = (lastZAndA[A_INDEX] - Y)

    dW = 1 / m * dZ.dot(secondLastZAndA[A_INDEX].T)
    err = np.sum(dZ ** 2)
    db = [1 / m * np.sum(dZ)]
    derivativeWeightsAndBiases = []
    derivativeWeightsAndBiases = [[dW, db]] + derivativeWeightsAndBiases

    dZ = weightsAndBiases[-1][W_INDEX].T.dot(dZ) * ReLU_deriv(secondLastZAndA[Z_INDEX])
    # Middle
    for i in range(len(zAndA) - 1, 1, -1):
        print(i)
        dW = 1 / m * dZ.dot(zAndA[i-1][A_INDEX].T)
        db = [1 / m * np.sum(dZ)]
        derivativeWeightsAndBiases = [[dW, db]] + derivativeWeightsAndBiases

        wb = weightsAndBiases[i-2][W_INDEX].T.dot(dZ)
        relu_d = ReLU_deriv(zAndA[i-1][Z_INDEX])
        dZ = wb * relu_d

    # First

    dW = 1 / m * dZ.dot(X.T)
    db = 1 / m * np.sum(dZ)
    derivativeWeightsAndBiases = [[dW, db]] + derivativeWeightsAndBiases
    return derivativeWeightsAndBiases, err


def update_params(oldParams, dWB, alpha):
    newParams = []
    for i in range(len(oldParams)):
        newW = oldParams[i][W_INDEX] - alpha * dWB[i][W_INDEX]
        newB = oldParams[i][B_INDEX] - alpha * dWB[i][B_INDEX]
        newParams.append([newW, newB])
    return newParams


# Example code from YT -----
# https://www.kaggle.com/code/wwsalmon/simple-mnist-nn-from-scratch-numpy-no-tf-keras/notebook

def get_predictions(A2):
    return np.argmax(A2, 0)


def get_accuracy(predictions, Y):
    #print(predictions, Y)
    return np.sum(predictions == Y) / Y.size


def gradient_descent(X, Y, weightsAndBiases, alpha, iterations, useOneHot=True):
    x = X[0, :]
    # TODO implement for all (remove [0])

    zAndA = forward_prop(weightsAndBiases, X)
    dWB, sse = backward_prop(
        zAndA, weightsAndBiases, X, Y, useOneHot)
    newParams = update_params(
        weightsAndBiases, dWB, alpha)
    if sse < 1.:
        a = 3
    #print(f'Error: {sse}')
    # if i % 10 == 0:
    #     print("Iteration: ", i)
    #     predictions = get_predictions(A2)
    #     print(get_accuracy(predictions, Y))
    return W1, b1, W2, b2, sse, A2


def forwardPropAndOneHot(weightsAndBiases, input):
    zAndA = forward_prop(weightsAndBiases, input)
    return getForwardOneHot(zAndA[-1][A_INDEX])


# W1, b1, W2, b2 = init_params()
# _, index = forwardPropAndOneHot(W1, b1, W2, b2, INPUT_DATA)
# atest = 1
