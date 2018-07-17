# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
freqs_horizontal = None
freqs_vertical = None
data = None
with open("2D_AOD_Efficiency.csv", "r") as f:
    freqs_vertical = np.array([float(freq) for freq in f.readline().split(";")[1:]])
    freqs_horizontal = []
    data = []
    for line in f.readlines():
        line_data = [float(it) for it in line.split(";")]
        freqs_horizontal.append(line_data[0])
        data.append(line_data[1:])
    freqs_horizontal = np.array(freqs_horizontal)
    data = np.array(data)

# %%
plt.pcolormesh(freqs_horizontal, freqs_vertical, data.T)
plt.xlabel("Horizontal AOD frequency [MHz]")
plt.ylabel("Vertical AOD frequency [MHz]")
plt.gca().set_aspect(1)

plt.show()
