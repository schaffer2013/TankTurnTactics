import numpy as np
from numpy.linalg import pinv


def fit(list_x, list_y):
    A_list = []
    for x in list_x:
        A_list.append([x, 1])
    A = np.array(A_list)

    B_list = []
    for y in list_y:
        B_list.append([y])
    B = np.array(B_list)

    A_inv = pinv(A)
    x_hat = A_inv.dot(B)

    # print(x_hat)
    m = x_hat[0][0]
    b = x_hat[1][0]

    y_hat = np.transpose(np.array([m*np.array(list_x)+b]))
    l = len(y_hat)
    if (l > 2):
        diff = y_hat-B
        res = np.square(diff)
        ssr = np.sum(res)
        s_r = np.sqrt((ssr)/(l-2))
        sum_x = np.sum(list_x)
        sum_x2 = np.sum(np.square(list_x))
        sb1=np.sqrt((l*np.square(s_r))/(l*sum_x2-np.square(sum_x)))
        sb2=np.sqrt((np.square(s_r)*sum_x2)/(l*sum_x2-np.square(sum_x)))
        m_res_95 = 2.78 * sb1
        b_res_95 = 2.78 * sb2
        return m, m_res_95, b, b_res_95

    return m, b
