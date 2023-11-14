from itertools import combinations

def find_unique_triplets(arr):
    found_triplets = set()
    for triplet in combinations(arr, 3):
        sorted_triplet = tuple(sorted(triplet))  # Sort to avoid duplicates in different orders
        found_triplets.add(sorted_triplet)
    return found_triplets



'''
points = [1, 2, 3, 4, 5]
unique_triplets = find_unique_triplets(points)
for triplet in unique_triplets:
    print(f"Found unique triplet: {triplet}")
'''


