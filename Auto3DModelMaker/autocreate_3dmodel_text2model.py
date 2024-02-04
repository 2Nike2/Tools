import argparse

from make_prompt_list import make_prompt_list_from_theme
from text2model import create_fbx_model

parser = argparse.ArgumentParser()
parser.add_argument('--theme', type=str, default='公園')


args = parser.parse_args()

theme = args.theme

print('テーマ:' , theme)

prompt_list = make_prompt_list_from_theme(theme)

print('以下のプロンプトで3Dモデルを作成します。')
for prompt in prompt_list:
    print(prompt)

for prompt in prompt_list:
    print('3Dモデル作成中: ' + prompt + '...')
    create_fbx_model(prompt)
    print('3Dモデル作成終了: ' + prompt)