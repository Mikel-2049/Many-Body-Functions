'''

En main declarar tus points , el set vacio, el cur_list vacio para tener referencias y i = al valor de i en tu for loop

haces for de 0 a final en tus puntos
    llamas el metodo pasandole las variables y el i actual

ya con eso tienes los unique triplets
'''

'''
Obtienes triplets unicos en un array desde el indice i en adelante
'''

def find_unique_triplets(arr, found_triplets, cur_list, i=0):
    # Base case: if the current list has 3 elements
    if len(cur_list) == 3:
        # Sort the triplet and convert it to a tuple
        triplet = tuple(sorted(cur_list))
        
        # Add the triplet to the set of found triplets
        found_triplets.add(triplet)
        return
    
    # Base case: if we've reached the end of the array
    if i >= len(arr):
        return
    
    # Recursive case 1: include the i-th element and move to the next
    cur_list.append(arr[i])
    find_unique_triplets(arr, found_triplets, cur_list, i + 1)
    
    # Backtrack: remove the i-th element
    cur_list.pop()
    
    # Recursive case 2: exclude the i-th element and move to the next
    find_unique_triplets(arr, found_triplets, cur_list, i + 1)



'''
def find_unique_triplets(arr, found_triplets, cur_list, i=0):
    for triplet in found_triplets:
        print(triplet)
    #base case: out of range
    if(i >= len(arr)):
        return
    
    #add number to list if we are in range
    cur_list.append(arr[i])

    #check if we have found a triplet
    if(len(cur_list) == 3):
        #sort list of points
        cur_list.sort()

        triplet = (inner_list for inner_list in cur_list)

        #check if sorted list already exists in found triplets
        if(triplet in found_triplets):
            return
        #else add point to current list
        else:
            found_triplets.add(triplet)

    #recursive call
    j = i = 1
    while i  < len(arr):
        find_unique_triplets(arr, found_triplets, cur_list, j) #make calls with new values
        cur_list.pop()   #remove newly added value
'''


'''
    if initial_call:
        for start in range(len(arr) - 2):
            find_unique_triplets(arr, i=start, initial_call=False)
        return
    
    if i >= len(arr):
        return
    
    cur_list.append(arr[i])
    
    if len(cur_list) == 3:
        sorted_triplet = tuple(sorted(cur_list))
        if sorted_triplet not in found_triplets:
            print(f"Found unique triplet: {sorted_triplet}")  # Or add it to some list
            found_triplets.add(sorted_triplet)
        cur_list.pop()
        return
    
    for j in range(i + 1, len(arr)):
        find_unique_triplets(arr, cur_list, j, found_triplets, initial_call=False)
        cur_list.pop()
        '''