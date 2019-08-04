import numpy as np
import sys
from image import ImageFeatures
from PIL import Image, ImageDraw


def load_image(file):

    with open(file, mode='r') as image_file:
        data = image_file.readlines()
        data = [d.rstrip() for d in data]

        number_of_features = int(data[0])
        number_of_key_points = int(data[1])
        key_points = np.zeros(shape=(number_of_key_points, number_of_features + 2))

        for i in range(number_of_key_points):
            feature = [float(d) for d in data[2 + i].split(' ')]

            key_points[i][0] = feature[0]
            key_points[i][1] = feature[1]

            for j in range(number_of_features):
                key_points[i][j + 2] = float(feature[j + 5])

    return ImageFeatures(number_of_features, number_of_key_points, key_points)


def pair_of_points(image_a, image_b):

    neighbours_indices_a = [0] * image_a.number_of_key_points
    neighbours_indices_b = [0] * image_b.number_of_key_points
    pairs = []

    for i in range(image_a.number_of_key_points):
        best_distance = sys.maxsize
        features_a = image_a.key_points[i][2:]

        for j in range(image_b.number_of_key_points):
            features_b = image_b.key_points[j][2:]

            distance = abs(np.sum((features_a - features_b) ** 2))

            if distance < best_distance:
                best_distance = distance
                neighbours_indices_a[i] = j

    for i in range(image_b.number_of_key_points):
        best_distance = sys.maxsize
        features_b = image_b.key_points[i][2:]

        for j in range(image_a.number_of_key_points):
            features_a = image_a.key_points[j][2:]

            distance = abs(np.sum((features_a - features_b) ** 2))

            if distance < best_distance:
                best_distance = distance
                neighbours_indices_b[i] = j

    for i in range(image_a.number_of_key_points):
        if i == neighbours_indices_b[neighbours_indices_a[i]]:
            pairs.append([i, neighbours_indices_a[i]])

    return pairs


def filter_consistent_pairs(image_a, image_b, pairs, n, threshold):
    adjacent_points_a = []
    adjacent_points_b = []

    for i in range(len(pairs)):
        adjacent_points = []
        coords_i = image_a.key_points[pairs[i][0]][:2]

        for j in range(len(pairs)):
            coords_j = image_a.key_points[pairs[j][0]][:2]
            distance = abs(np.sum((coords_i - coords_j) ** 2))
            if distance != 0:
                adjacent_points.append((pairs[j][0], distance))

        adjacent_points_a.append(sorted(adjacent_points, key=lambda x: x[1])[:n])

    for i in range(len(pairs)):
        adjacent_points = []
        coords_i = image_b.key_points[pairs[i][1]][:2]

        for j in range(len(pairs)):
            coords_j = image_b.key_points[pairs[j][1]][:2]
            distance = abs(np.sum((coords_i - coords_j) ** 2))
            if distance != 0:
                adjacent_points.append((pairs[j][1], distance))

        adjacent_points_b.append(sorted(adjacent_points, key=lambda x: x[1])[:n])

    consistencies = []

    for i in range(len(pairs)):
        sum = 0

        for j in range(n):
            for k in range(n):
                if [adjacent_points_a[i][j][0], adjacent_points_b[i][k][0]] in pairs:
                    sum += 1
        consistencies.append(sum / n)

    consistent_pairs = [pairs[i] for i in range(len(pairs)) if consistencies[i] > threshold]

    return consistent_pairs, consistencies


def visualize(path_a, path_b, image_a, image_b, pairs, consistencies, threshold, all_consistent=False):
    width = 1610
    height = 600

    img_a = Image.open(path_a)
    img_b = Image.open(path_b)
    img = Image.new('RGB', (width, height))

    img.paste(img_a, (0, 0))
    img.paste(img_b, (810, 0))

    draw = ImageDraw.Draw(img)

    for i in range(len(pairs)):
        if consistencies[i] > threshold or all_consistent:
            color = (0, 255, 0)
        else:
            color = (255, 255, 51)
        draw.line((image_a.key_points[pairs[i][0]][0], image_a.key_points[pairs[i][0]][1],
                   image_b.key_points[pairs[i][1]][0] + width / 2 + 10, image_b.key_points[pairs[i][1]][1]),
                  fill=color, width=2)

    img.show()


def affine_transformation():
    pass


def perspective_transformation():
    pass
