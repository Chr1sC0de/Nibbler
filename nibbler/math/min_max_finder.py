import numpy as np
from numba import njit

def find_max_from_gradients(gradients):
    find = np.logical_and(
        gradients[:-1] > 0, gradients[1:] < 0
    )

    maxes = np.argwhere(find).squeeze()

    try:
        len(maxes)
    except:
        return np.array([maxes, ])

    return maxes


def find_min_from_gradients(gradients):
    find = np.logical_and(
        gradients[:-1] < 0, gradients[1:] > 0
    )

    maxes = np.argwhere(find).squeeze()

    try:
        len(maxes)
    except:
        return np.array([maxes, ])


    return maxes

# @njit
# def find_max_from_gradients_jit(gradients):
#     # do not use its really slow
#     output = []
#     for i in range(len(gradients)-1):
#         if gradients[i]>0:
#             if gradients[i+1]<0:
#                 output.append(i)
#     return output


# @njit
# def find_min_from_gradients_jit(gradients):
#     # do not use its really slow
#     output = []
#     for i in range(len(gradients)-1):
#         if gradients[i]<0:
#             if gradients[i+1]>0:
#                 output.append(i)
#     return output