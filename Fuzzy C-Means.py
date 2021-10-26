import random
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np


def pltcolor(list):
    colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']
    a = len(list[0])
    colors = colors[0:a]
    output = []
    for i in range(len(list)):
        max_value = max(u[i])
        output.append(colors[u[i].index(max_value)])
    return output


def distance(list1, list2):
    res = 0
    for i in range(len(list1)):
        res += pow(list1[i] - list2[i], 2)
    return sqrt(res)


if __name__ == "__main__":
    clusters = int(input("Enter C > "))

    for d in range(1, 5):
        print("Data", d, "Costs:")
        data = open("data"+str(d)+".csv", "r")
        arr = []
        centroids = []
        u = []
        m = 2
        line = data.readline().strip('\n').split(',')
        while line != ['']:
            arr.append(list(map(float, line)))
            line = data.readline().strip('\n').split(',')
        costs = []
        for c in range(1, clusters+1):
            indices = random.sample(range(0, len(arr)), c)
            # print(indices)
            centroids = []
            for i in range(c):
                # print(arr[indices[i]])
                centroids.append(arr[indices[i]])
            # print("Chosen Indices:", indices, "; Centroids:", centroids)
            for n in range(100):
                u = []
                for j in range(len(arr)):
                    if arr[j] in centroids:
                        index = centroids.index(arr[j])
                        u.append([1 if x == index else 0 for x in range(c)])
                        continue
                    x = []
                    for k in range(c):
                        res = 0
                        for l in range(c):
                            res += pow(distance(arr[j], centroids[k])/distance(arr[j], centroids[l]), 2/(m-1))
                        x.append((1 / res))
                    u.append(x)
                    # print("This was added to u: ", x)
                centroids = []
                for i in range(c):
                    x = []
                    for j in range(len(arr[0])):
                        x.append(0)
                    denominator = 0
                    for j in range(len(arr)):
                        # print(arr[j][1], u[j][i], i)
                        for k in range(len(arr[0])):
                            x[k] += (float(arr[j][k]) * pow(u[j][i], m))
                        denominator += pow(u[j][i], m)
                    centroids.append(list(element/denominator for element in x))
                # print("This:", centroids)

            # print("Final centroids", centroids)
            # print("Final u", u)
            if d == 1:
                cols = pltcolor(u)
                plt.plot()
                plt.xlim([-100, 600])
                plt.ylim([-100, 600])
                plt.title('Dataset')
                arr_x = [i[0] for i in arr]
                arr_y = [i[1] for i in arr]
                plt.scatter(arr_x, arr_y, c=cols)
                cen_x = [i[0] for i in centroids]
                cen_y = [i[1] for i in centroids]
                plt.scatter(cen_x, cen_y, c='k', s=100, edgecolors="black")
                plt.savefig("Dataset" + str(d) + "-C=" + str(c) + ".png")
                plt.show()
            if d == 3:
                cols = pltcolor(u)
                plt.plot()
                plt.xlim([0, 1])
                plt.ylim([0, 1])
                plt.title('Dataset')
                arr_x = [i[0] for i in arr]
                arr_y = [i[1] for i in arr]
                plt.scatter(arr_x, arr_y, c=cols)
                cen_x = [i[0] for i in centroids]
                cen_y = [i[1] for i in centroids]
                plt.scatter(cen_x, cen_y, c='k', s=100, edgecolors="black")
                plt.savefig("Dataset" + str(d) + "-C=" + str(c) + ".png")
                plt.show()
            J = 0
            for i in range(len(arr)):
                for j in range(c):
                    J += pow(distance(arr[i], centroids[j]), 2) * pow(u[i][j], m)
            print(J, "; Number of clusters:", c)
            costs.append(J)

        plt.xlabel('C (Number of Clusters)')
        plt.ylabel('Cost')
        plt.plot(np.arange(1, clusters + 1, step=1), costs, '-bo')
        plt.savefig("Cost per Cluster"+str(d)+".png")
        plt.show()
        plt.clf()


