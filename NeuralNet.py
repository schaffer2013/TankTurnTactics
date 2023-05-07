import numpy as np

# placeholder input data
# NUM_INPUT_DATA = 15
# INPUT_DATA = np.random.rand(NUM_INPUT_DATA, 1)
# NODES_LAYER_1 = 12
# NUM_OUTPUTS = 14

# Params for randomization
STANDARD_DEV = 0.02


def init_params(numInputs, layer1Nodes, numOutputs):
    W1 = np.random.rand(layer1Nodes, numInputs) - 0.5
    b1 = np.random.rand(layer1Nodes, 1) - 0.5
    W2 = np.random.rand(numOutputs, layer1Nodes) - 0.5
    b2 = np.random.rand(numOutputs, 1) - 0.5
    return W1, b1, W2, b2


def ReLU(Z):
    return np.maximum(Z, 0)


def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A


def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2


def ReLU_deriv(Z):
    return Z > 0


def getForwardOneHot(array):
    one_hot = np.zeros(array.shape[0], dtype=int)
    maxArg = np.array(array).argmax()
    one_hot[maxArg] = 1
    return one_hot, maxArg


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


# def one_hot(Y):
#     one_hot_Y = np.zeros((Y.size, Y.max() + 1))
#     one_hot_Y[np.arange(Y.size), Y] = 1
#     one_hot_Y = one_hot_Y.T
#     return one_hot_Y


# def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
#     one_hot_Y = one_hot(Y)
#     dZ2 = A2 - one_hot_Y
#     dW2 = 1 / m * dZ2.dot(A1.T)
#     db2 = 1 / m * np.sum(dZ2)
#     dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
#     dW1 = 1 / m * dZ1.dot(X.T)
#     db1 = 1 / m * np.sum(dZ1)
#     return dW1, db1, dW2, db2


# def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
#     W1 = W1 - alpha * dW1
#     b1 = b1 - alpha * db1
#     W2 = W2 - alpha * dW2
#     b2 = b2 - alpha * db2
#     return W1, b1, W2, b2

def forwardPropAndOneHot(W1, b1, W2, b2, input):
    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, input)
    return getForwardOneHot(A2)


# W1, b1, W2, b2 = init_params()
# _, index = forwardPropAndOneHot(W1, b1, W2, b2, INPUT_DATA)
# atest = 1
