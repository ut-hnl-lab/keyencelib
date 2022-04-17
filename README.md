# KeyenceLib
keyence のプロファイル測定器を python で扱うためのツールです.

## Description
LJ-V7000 シリーズの測定器を接続し, python プログラムで以下を簡単に実行できます.
* 直線状の測定データをnumpy配列形式で取得
* 同データのcsv出力
* 同データのリアルタイムプロット

## Demo
▼FDM方式3Dプリンターの造形物表面を観察した例
![device](https://user-images.githubusercontent.com/88641432/163707075-b3b7dead-c918-415b-a302-62402418c24b.png)
![profile](https://user-images.githubusercontent.com/88641432/163707086-21b5b5b2-2675-40e4-a898-6b603c9ff8ef.gif)


## Usage
１. 機器を下の写真の通りに接続する.
[coming soon...]

２. プログラムを実行する.
```
import time
from keyencelib import Profiler

profiler = Profiler(savedir='./test')

# 10秒間プロファイルを表示した後, 配列で取得・保存する
with profiler.open(with_monitor=True):
    time.sleep(10)
    array = profiler.get()
    print(array)
```

## Install
```
pip install keyencelib
```
