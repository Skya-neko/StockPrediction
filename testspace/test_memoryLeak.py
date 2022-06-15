from matplotlib import pyplot as plt
from memory_profiler import profile

@profile
def plot_func(x_data, y_data):
    plt.plot(x_data, y_data)
    plt.savefig("my_img.png")
    plt.clf()



if __name__ == "__main__":
    x = [x for x in range(1700)]
    y = [y for y in range(1700)]
    for _ in range(100):
        plot_func(x, y)
    plt.close()