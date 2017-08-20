import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
import statistics
import sys

from sklearn.svm import SVC
from sklearn import decomposition


def space_gg(x, a_list, b_list):
    title = 'Memory cost for building the model'
    fig, ax = plt.subplots()

    plt.xlabel('Record time length (second)')
    plt.ylabel('Space needed (MegaBytes)')

    ax.plot(x, a_list, label='storage_memory')
    ax.plot(x, b_list, label='running_memory')
    ax.legend()
    ax.set_title(title)

    plt.savefig(title + 'line_chart.png')
    # plt.show()


def time_gg(x, time_list):
    title = 'Time cost for building the model'
    fig, ax = plt.subplots()

    plt.xlabel('Record time length (second)')
    plt.ylabel('Time needed (second)')

    ax.plot(x, time_list, label='time')
    ax.legend()
    ax.set_title(title)

    plt.savefig(title + 'line_chart.png')
    # plt.show()


def main():
    fp = open('exp.txt', 'r')
    x = []
    y = []
    z1 = []
    z2 = []
    for line in fp:
        items = line.strip().split(' ')
        if len(items) < 4:
            continue
        print(items)
        x.append(int(items[0]))
        y.append(float(items[1]))
        z1.append(float(items[2]))
        z2.append(float(items[3]))
    time_gg(x, y)
    space_gg(x, z1, z2)


if __name__ == '__main__':
    main()

