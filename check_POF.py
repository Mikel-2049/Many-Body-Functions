import pickle

# Open the POF file for reading in binary mode
with open('WFG3_03D.pof', 'rb') as file:
    # Load the object from the file
    loaded_object = pickle.load(file)

# Now you can work with the loaded object
print(loaded_object)
