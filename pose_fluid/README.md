# PoseEstimator using PaddlePaddle
---

## Note

- CCCC人工智能创意赛版本，将核心的姿态检测由TensorFlow改为使用PaddlePaddle的推理引擎实现。

- 本模块可以替换`pilamp_hikey970`中的`pose`模块。

## Requirements

- PaddlePaddle 1.8.2

- dlib 19

## Usage

1. Unzip `params/params.zip`

2. Call `Handler.detect()` in `vision.py`
