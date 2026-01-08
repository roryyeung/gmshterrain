import math

def wave_generator(N,M):
    coords = []
    for i in range(N + 1):
        for j in range(M + 1):
            coords.extend([
                float(i) / N,
                float(j) / N,
                0.05 * math.sin(10 * float(i + j) / N)
            ])
    return coords

# TODO - This seems to use other and inner loops the opposite way round to our resipy data. Does this matter?

#Generate test data
# import numpy as np
# list = wave_generator(50,20)
# size = len(list)/3
# chunks = np.array_split(list, size)
# np.savetxt('basic_array.csv', chunks, delimiter=',',fmt="%1f")

