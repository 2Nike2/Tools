import argparse

from create_images import create_images
from image2model import create_fbx_model

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', type=str, default='blender simple 3d model dog')
parser.add_argument('--num', type=str, default=1)

args = parser.parse_args()
prompt = args.prompt
num = int(args.num)

print('プロンプト:' , prompt)
print('枚数:' , num)

create_images(prompt, num)

create_fbx_model()
