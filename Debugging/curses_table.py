import tableprint as tp
import numpy as np
import time

print(tp.header(["A", "B", "C"], width=20) )

for x in range(3):
    data = np.random.randn(3)
    print(tp.row(data, width=20), flush=True)
    time.sleep(1)
    data = np.random.randn(3)
    print(tp.row(data, width=20), flush=True)
    time.sleep(1)
    data = np.random.randn(3)
    print(tp.row(data, width=20), flush=True)
    time.sleep(1)
    print(tp.header(["A", "B", "C"], width=20) )

print(tp.bottom(3, width=20))