import argparse
from shape_text2model import text2model
import subprocess
import os

def create_fbx_model(prompt):

    ply_filepath = text2model(prompt)

    subprocess.run([ 'blender', '--background', '--python', 'convert_ply2fbx.py', '--', ply_filepath])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', type=str, default='a shark')

    args = parser.parse_args()

    prompt = args.prompt
    
    create_fbx_model(prompt)