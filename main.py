import copy
import tkinter as tk
import tkinter.filedialog
import math
import matplotlib.pyplot as plt
from itertools import product
import numpy as np
from sklearn.cluster import KMeans
import random
import statistics

points = []
clusters = [[]]


def assignment_k_means():
    global points, clusters

    for point in points:
        distance = []

        for i in range(len(clusters)):
            cluster = clusters[i]
            x, y = cluster[0]
            point_x, point_y = point
            distance.append(math.sqrt((point_x - x) ** 2 + (point_y - y) ** 2))

        clusters[distance.index(min(distance))].append(point)


def update_k_means():
    global clusters

    for i in range(len(clusters)):
        cluster = clusters[i]
        x, y = cluster.pop(0)
        x1, y1 = [sum(x)/len(x) for x in zip(*cluster)]
        #print(x1-x, y1-y)
        cluster.clear()
        cluster.insert(0, (x1, y1))


def analyze():
    label['text'] = 'Calculating..'
    plt.close()
    global points, clusters
    clusters.clear()
    text = text_field.get('1.0', 'end-1c')
    clusters_number = 0

    try:
        if text == '':
            clusters_number = random.choice(range(1, 10))
        else:
            clusters_number = int(text)
    except Exception:
        print('Can not read number of clusters')

    for i in range(clusters_number):
        clusters.append([])
        clusters[i].insert(0, points[random.choice(range(0, len(points)))])

    for point in points:
        distance = []

        for cluster in clusters:
            x, y = cluster[0]
            point_x, point_y = point
            distance.append(math.sqrt((point_x - x) ** 2 + (point_y - y) ** 2))

        clusters[distance.index(min(distance))].append(point)

    flag = True
    count = 0
    while flag:
        count +=1
        clusters_copy = copy.deepcopy(clusters)
        update_k_means()
        assignment_k_means()

        #for i in range(len(clusters)):
            #cluster = clusters[i]
            #cluster_copy = clusters_copy[i]
            #if cluster[0] == cluster_copy[0]:
                #flag = False
        if clusters == clusters_copy:
            flag = False

    for i in range(len(clusters)):
        plt.style.use('fivethirtyeight')
        # plt.figure(figsize=(15, 10))
        # plt.plot(points, marker='.', color='black')
        # plt.legend(loc='best')
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.title('Points')
        values = clusters[i].pop(0)
        mean_x, mean_y = values
        color = (random.random(), random.random(), random.random())
        plt.scatter(mean_x, mean_y, color=color, edgecolors='k', zorder=1)
        cluster = clusters[i]
        plt.scatter(*zip(*cluster), color=color, alpha=0.5, zorder=-1)

    label['text'] = 'Count of steps: ' + str(count)
    plt.show()


def open_file_for_analyze():
    label['text'] = 'Loading..'
    plt.close()
    global points
    points.clear()
    file_dialog = tk.filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"),
                                                                                                ("all files", "*.*")))
    file = open(file_dialog, "r")
    file_content = file.readlines()

    for line in file_content:
        try:
            x, y = line.strip().split()
            points.append((int(x), int(y)))
        except Exception:
            print('Can not read line')

    plt.style.use('fivethirtyeight')
    # plt.figure(figsize=(15, 10))
    # plt.plot(points, marker='.', color='black')
    plt.scatter(*zip(*points))
    # plt.legend(loc='best')
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.title('Points')
    label['text'] = ''
    plt.show()


# Window GUI
window = tk.Tk()
label = tk.Label(window, text="", fg='black', font=("Consolas", 11))
label.place(x=0, y=0)
text_field = tk.Text(window, bd=3)
text_field.place(x=0, y=30, height=60, width=300)
open_file_for_analyze_button = tk.Button(window, text="Select file", fg='black', command=open_file_for_analyze)
open_file_for_analyze_button.place(x=160, y=100)
analyze_button = tk.Button(window, text="Clustering", fg='black', command=analyze)
analyze_button.place(x=90, y=100)
window.title('K-means')
width = window.winfo_width() + (2 * window.winfo_rootx() - window.winfo_x())
height = window.winfo_height() + (window.winfo_rooty() - window.winfo_y() + window.winfo_rootx() - window.winfo_x())
window.geometry('300x130')
window.eval('tk::PlaceWindow . center')
window.resizable(width=False, height=False)
window.mainloop()
# END Window GUI
