import pickle

def process_nibabel(test_image):
    # Load the pickled dictionary containing the function
    with open('preprocessing_functions.pkl', 'rb') as file:
        loaded_functions = pickle.load(file)

    loaded_process_scan = loaded_functions['process_scan']
    return loaded_process_scan(test_image)



