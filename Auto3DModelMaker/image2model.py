import argparse
from shape_image2model import image2model
import subprocess
import os
import glob

def create_fbx_model():

    file_list = glob.glob('images/*')

    for file in file_list:
        
        if os.path.splitext(file)[1] in ['.png', '.jpg', '.jpeg']:
            ply_filepath = image2model(file)
            subprocess.run([ 'blender', '--background', '--python', 'convert_ply2fbx.py', '--', ply_filepath])

if __name__ == "__main__":
        
    create_fbx_model()