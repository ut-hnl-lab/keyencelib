# KeyenceLib
keyence のプロファイル測定器を python で扱うためのツールです.

## Description
LJ-V7000 シリーズの測定器を接続し, python プログラムで以下を簡単に実行できます.
* 直線状の測定データをnumpy配列形式で取得
* 同データのcsv出力
* 同データのリアルタイムプロット

## Demo
▼FDM方式3Dプリンターの造形物表面を観察した例

<img src="https://user-images.githubusercontent.com/88641432/163707718-4045fb65-121a-416b-b63c-976e642626b9.png" height="200">　<img src="https://user-images.githubusercontent.com/88641432/163707086-21b5b5b2-2675-40e4-a898-6b603c9ff8ef.gif" height="200">


## Usage
１. 機器を下の写真の通りに接続する.


<img src="https://user-images.githubusercontent.com/88641432/163779065-156cf1a9-42a7-44a9-acfc-4622e1b00dbe.png" width=600>

２. プログラムを実行する.

```python
import time
from keyencelib import Profiler

profiler = Profiler(savedir='./test')

# 10秒間プロファイルを表示した後, 配列で取得・保存する
with profiler.open(with_monitor=True):
    time.sleep(10)
    array = profiler.get()
    print(array)
```

## Installation
```
pip install keyencelib
```
