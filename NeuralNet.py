import numpy as np

# Params for randomization
STANDARD_DEV = 0.0001
np.seterr(all='raise')


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


def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2


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
        #min = 10 ** -15
        dZ2 = (A2 - Y)
        # for r in range(dZ2.shape[0]):
        #     for c in range(dZ2.shape[1]):
        #         if abs(dZ2[r, c]) < min:
        #             dZ2[r, c] = 0
        #         else:
        #             dZ2[r, c] = dZ2[r, c] ** 2
        # #dZ2 = (A2 - Y) ** 2
    dW2 = 1 / m * dZ2.dot(A1.T)
    err = np.sum(dZ2 ** 2)
    db2 = 1 / m * np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1)
    return dW1, db1, dW2, db2, err


def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2


# Example code from YT -----
# https://www.kaggle.com/code/wwsalmon/simple-mnist-nn-from-scratch-numpy-no-tf-keras/notebook

def get_predictions(A2):
    return np.argmax(A2, 0)


def get_accuracy(predictions, Y):
    #print(predictions, Y)
    return np.sum(predictions == Y) / Y.size


def gradient_descent(X, Y, params, alpha, iterations, useOneHot=True):
    x = X[0, :]
    W1, b1, W2, b2 = params
    # TODO implement for all (remove [0])

    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
    dW1, db1, dW2, db2, sse = backward_prop(
        Z1, A1, Z2, A2, W1, W2, X, Y, useOneHot)
    W1, b1, W2, b2 = update_params(
        W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
    if sse < 1.:
        a = 3
    #print(f'Error: {sse}')
    # if i % 10 == 0:
    #     print("Iteration: ", i)
    #     predictions = get_predictions(A2)
    #     print(get_accuracy(predictions, Y))
    return W1, b1, W2, b2, sse, A2


def forwardPropAndOneHot(W1, b1, W2, b2, input):
    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, input)
    return getForwardOneHot(A2)


# W1, b1, W2, b2 = init_params()
# _, index = forwardPropAndOneHot(W1, b1, W2, b2, INPUT_DATA)
# atest = 1
