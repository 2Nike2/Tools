## Auto3DModelMakerの使い方
(不要なところは適宜飛ばしてください。)

### 各種前提
- pythonのバージョンは3.10.x  
- Blenderのバージョンは3.2.x  
- 環境変数BLENDER_PATHにBlenderのパスを設定  

ChatGPTのAPI(有料)を使って3Dモデル作成プロンプトの自動生成も行いたい場合は、  
- 環境変数OPENAI_API_KEYにOpenAIのAPIキーを設定  
も行う。  

未検証ですが余程離れたバージョンでなければ一応動くと思います。  

### 仮想環境構築
cd Auto3DModelMaker  
python -m venv auto3dmodelmaker_env  
auto3dmodelmaker_env\Scripts\activate  

### torchのインストール
torchはShap-Eのインストール時におそらくCPU版が一緒にインストールされるが、それだと処理が遅くなるので予めGPU版をインストールする。  
https://pytorch.org/  
のINSTALL PYTORCHにを参考にインストールする。  
参考(Windows CUDA 11.8)  
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  
(pip3->pipに変更した。)  

### Shap-Eのインストール
git clone https://github.com/openai/shap-e  
pip install -e shap-e  

基本的に  
https://github.com/openai/shap-e/blob/main/README.md  
の手順と同じ。  

### その他ライブラリのインストール
pip install -r requirements.txt  

### 実行
#### 1つのプロンプトを直接指定して作成
python text2model.py --prompt "dog"  
("dog"は作りたいモデルのプロンプトに置き換える。)  
(初実行時はShap-Eのモデルのダウンロード(約5GBくらい?)で時間がかかります。)  

#### テーマを渡してそれに関連するオブジェクトを複数(3~5個)作成
python autocreate_3dmodel_text2model.py --theme "豪華な家のダイニング"

#### imagesフォルダに格納した各画像からモデルを作成  
imagesフォルダに画像('*.png', '*.jpg', '*.jpeg')を格納して下記を実行  
python image2model.py  

#### 画像を自動生成して各画像からモデルを作成
python autocreate_3dmodel_image2model.py --prompt "blender simple 3d model dog" --num 3  

#### Blenderでの処理の設定について
blender_config.jsonの内容を変えることで、Blenderでの処理の設定を変更できます。  

作成されたモデルについては、  
- plyフォルダ(Shap-Eで作成直後のplyのモデル)  
- fbxフォルダ(デシメート、テクスチャ焼き付け、fbxへのファイル形式変換を行ったモデル)  
に格納されます。  