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
python text2model.py --prompt "dog"  
("dog"は作りたいモデルのプロンプトに置き換える。)  
(初実行時はShap-Eのモデルのダウンロード(約5GBくらい?)で時間がかかります。)  
