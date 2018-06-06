import math
import random
import copy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class k_means:
    def __init__(self, k=4, tolerance=0.05, max_runs = 100):
        self.k = k;
        self.tolerance = tolerance
        self.max_runs = max_runs

    def euclidean_distance(self, data, centroid):
        distance = []
        squared_distance = 0;
        euclidean = 0
        for i in range(len(data)):
            distance.append(centroid[i] - data[i])
        for j in range(len(distance)):
            squared_distance += distance[j]*distance[j]
        euclidean = math.sqrt(squared_distance)
        return euclidean

    def classification(self, data, centroids):
        classes = {}
        for i in range(self.k):
            # choose one of your points as centroid
            classes[i] = []
        for f in data:
            minimum = self.euclidean_distance(f, centroids[0])
            index = 0
            for c in range(len(self.centroids)):
                distance = self.euclidean_distance(f, centroids[c])
                if distance < minimum:
                    minimum = distance
                    index = c
                classes[index].append(f)
        return classes

    def find_average(self, data):
        row = len(data)
        col = len(data[0])
        # average = [[0 for x in range(col)] for y in range(row)]
        average = [0 for x in range(col)]
        for x in range(len(average)):
            average[x] = 0
        for i in range (col):
            for j in range (row):
                average[i] += data[j][i]
        for k in range(col):
            average[k] = average[k]/row
        return average

    def cluster(self, data):
        # print(len(data))
        n = self.k
        m = len(data)
        self.centroids = [[0 for x in range(len(data[0]))] for y in range(n)]
        self.classes = {}
        for i in range(self.k):
            # choose one of your points as centroid
            self.classes[i] = []
            point = random.randrange(len(data[0]))
            oldPoint = point
            if point == oldPoint:
                while point == oldPoint:  # choose new point
                    point = random.randrange(len(data))
            self.centroids[i] = data[point]
        self.classes = self.classification(data, self.centroids)

        optimized = False
        # new centroids run until optimized is true
        counter = 0
        for p in range(self.max_runs):
            counter += 1
            previous_centroids = copy.deepcopy(self.centroids)
            for c in range(len(self.centroids)):
                self.centroids[c] = self.find_average(self.classes[c])

            # reclassify
            self.classes = self.classification(data, self.centroids)
            original = []
            current = []
            difference = []
            for i in range(len(self.centroids[0])):
                original.append(0)
                current.append(0)
                difference.append(0)

            for a in range(len(original)):
                for b in range(len(self.centroids)):
                    original[a] += previous_centroids[b][a]
                    current[a] += self.centroids[b][a]

            max_difference = abs(current[0] - original[0])
            for g in range(len(current)):
                if abs(current[g] - original[g]) > max_difference:
                    max_difference = abs(current[g] - original[g])

            # get out of loop if tolerance is hit
            if max_difference <= self.tolerance:
                break


def main():
    file = open('seeds_dataset.txt', 'r')
    compactness = []
    length = []
    width = []

    for line in file:
        fields = line.split()
        compactness.append(float(fields[2]))
        length.append(float(fields[3]))
        width.append(float(fields[4]))

    data = [[0 for x in range(3)] for y in range(len(compactness))]

    for i in range(len(compactness)):
        data[i][0] = compactness[i]
        data[i][1] = length[i]
        data[i][2] = width[i]

    km = k_means(8)
    km.cluster(data)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # so far can only do up to 5 unless I dynamically update the colors which could take a lot of time
    colors =["r", "g", "c", "b", "k", "y", "m", '#800080']
    counter = 0

    for centroid in km.centroids:
        ax.scatter(centroid[0], centroid[1], centroid[2], s=150, c=colors[counter], marker='x')
        counter += 1

    # reset counter to group everything
    counter = 0
    for classification in km.classes:
        counter +=1
        color = colors[classification]
        print("Group ", counter, ": ")
        for features in km.classes[classification]:
            print(features)
            ax.scatter(features[0], features[1], features[2], s = 50, c=color, marker='o')

    plt.show()


if __name__ == '__main__':
    main()