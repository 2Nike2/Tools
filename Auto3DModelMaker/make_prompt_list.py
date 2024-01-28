import os
import openai
import argparse

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

openai.openai_api_key = os.environ.get('OPENAI_API_KEY')

def make_prompt_list_from_theme(theme):

    prompt = ChatPromptTemplate.from_template('''\
### 指示
あなたは優秀な3Dモデルクリエイターです。また生成AIを用いた創作活動も得意としています。
これから入力に与えたテーマをもとに、どのような3Dモデル作成プロンプトを作成すれば良いかを入出力例を参考にして考えてください。
出力はCSV形式でコンマ区切りで出してください。

### 制約
・入力は日本語、英語、その他の言語の可能性がありますが、出力するプロンプトは必ず英語にすること、英語以外の言語のプロンプトは出力しないでください。
・各プロンプトの最大字数は10単語までにすること、字数制限は厳密に守ってください。
・モデルのデシメート(間引き)処理で細い部分は消えたり分離する恐れがあるので、細い部分のあるオブジェクトは太めにしたり、厚さをつけたりする形容詞などを足してください。
・あまり複雑なオブジェクトは作れない為、焦点をあてるオブジェクトは1つにして、そのオブジェクトの具体的に形容する方針で作ってください。
・プロンプトの個数については最小3個、最大5個で数量を守ってください。

### 入力例
公園

### 出力例
Simple wooden park bench, Single oak tree, Thick and sturdy lamp post, Small shallow pond, Durable plastic slide for children, Children's sandbox with border, Spring-mounted ride-on toy, Panda-shaped spring-mounted ride-on toy, Statue of a sitting lion

### 入力
{theme}

### 出力
''')

    model = ChatOpenAI(model="gpt-4")
    output_parser = CommaSeparatedListOutputParser()

    chain = prompt | model | output_parser

    return chain.invoke({"theme": theme})

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--theme', type=str, default='豪華な家のダイニングルーム')

    args = parser.parse_args()

    theme = args.theme
    
    prompt_list = make_prompt_list_from_theme(theme)
    for prompt in prompt_list:
        print(prompt)
            