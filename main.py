import ransac
import pickle


def main():
    path = '/home/michal/ransac_images/'
    suffix = '.haraff.sift'
    file_image_a = 'numero_uno.png'
    file_image_b = 'numero_dos.png'
    threshold = 0.3                            # 0.1, 0.3, 0.5
    n = 20                                     # 10, 20, 35
    all_consistent = False

    image_a = ransac.load_image(path + file_image_a + suffix)
    image_b = ransac.load_image(path + file_image_b + suffix)
    print("Key Points A - " + str(image_a.number_of_key_points))
    print("Key Points B - " + str(image_b.number_of_key_points))

    pairs = ransac.pair_of_points(image_a, image_b)
    with open('pairs.pickle', 'wb') as handle:
        pickle.dump(pairs, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('pairs.pickle', 'rb') as handle:
        pairs = pickle.load(handle)

    print("Pairs - " + str(len(pairs)))

    consistent_pairs, consistencies = ransac.filter_consistent_pairs(image_a, image_b, pairs, n, threshold)
    print("Consistent Pairs - " + str(len(consistent_pairs)))

    ransac.visualize(path + file_image_a, path + file_image_b, image_a, image_b, pairs, consistencies, threshold, all_consistent)


if __name__ == '__main__':
    main()
