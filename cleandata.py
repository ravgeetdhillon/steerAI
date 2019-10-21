from screen import convert_image
import numpy as np
import os


def setup():
    if not os.path.exists('data/cleaned_dataset'):
        os.mkdir('data/cleaned_dataset')


def convert_files_in_part(part):
    '''
    Converts all the files in the given part.
    '''

    if not os.path.exists(f'data/cleaned_dataset/{part}'):
        os.mkdir(f'data/cleaned_dataset/{part}')

    files = os.listdir(f'data/raw_dataset/{part}')
            
    # picks up a file and converts all the images and stores to a new folder
    for file_name in files:
        
        print(f'Converting {file_name} in {part}')
        images = np.load(f'data/raw_dataset/{part}/{file_name}', allow_pickle=True)

        training_data = []
        
        for image in images:
            converted_image = convert_image(image[0])
            training_data.append([converted_image, image[1]])
        np.save(f'data/cleaned_dataset/{part}/{file_name}', training_data)

    return True


def main(part_name=None):
    
    setup()

    parts = os.listdir('data/raw_dataset')

    if not part_name:
        for part in parts:
            convert_files_in_part(part)

    else:        
        part = part_name
        convert_files_in_part(part)


main()
