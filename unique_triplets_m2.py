from itertools import combinations

def find_unique_triplets(arr, found_triplets, cur_list=None, i=0):
    for triplet in combinations(arr, 3):
        sorted_triplet = tuple(sorted(triplet))
        if sorted_triplet not in found_triplets:
            found_triplets.add(sorted_triplet)


'''
points = [1, 2, 3, 4, 5]
unique_triplets = find_unique_triplets(points)
for triplet in unique_triplets:
    print(f"Found unique triplet: {triplet}")
'''


