import argparse
from shape_text2model import text2model
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', type=str, default='a shark')

args = parser.parse_args()

prompt = args.prompt

ply_filepath = text2model(prompt)

subprocess.run([ 'blender', '--background', '--python', 'convert_ply2fbx.py', '--', ply_filepath])
