import argparse
from shape_text2model import text2model
import subprocess
import os

def create_fbx_model(prompt, num_trials=1):

    for i in range(num_trials):
        ply_filepath = text2model(prompt, i)

        subprocess.run([ 'blender', '--background', '--python', 'convert_ply2fbx.py', '--', ply_filepath])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', type=str, default='a shark')
    parser.add_argument('--num_trials', type=int, default=1)

    args = parser.parse_args()

    prompt = args.prompt
    num_trials = args.num_trials
    
    create_fbx_model(prompt, num_trials)