# YOLO 训练实战：从配置到 best.pt

> 本节目标：理解 data、epochs、batch、imgsz、device 和预训练权重，掌握一次最小训练闭环。

## 一句话理解

训练就是把图片和标签一批批喂给模型，让它不断调整参数。训练结束后，通常留下 `best.pt` 和 `last.pt` 两个权重文件。

## 核心概念

- **data**：数据集配置文件，告诉模型图片、标签和类别在哪里。
- **epochs**：把所有训练数据完整看几遍。
- **batch**：一次送入模型多少张图片。
- **imgsz**：训练输入尺寸。
- **device**：使用 CPU 还是 GPU。
- **预训练权重**：例如 `yolo11n.pt`，帮助模型从通用视觉特征开始。
- **best.pt**：验证表现最好的权重。
- **last.pt**：最后一轮训练权重。

最小训练代码通常长这样：

```python
from ultralytics import YOLO

model = YOLO("yolo11n.pt")
model.train(data="coco128.yaml", epochs=10, imgsz=640, batch=16, device=0)
```

## 代码阅读示例

```python
model.train(data="coco128.yaml", epochs=10, imgsz=640)
```

阅读时先找关键参数：

- 数据集是什么？
- 训练多少轮？
- 图片输入多大？
- 输出权重会保存在哪里？

## 课后小测

1. data 和 epochs 分别控制什么？
2. 为什么常使用预训练权重？
3. best.pt 和 last.pt 有什么区别？

## 深度阅读

- [Ultralytics Train Mode](https://docs.ultralytics.com/modes/train/)
- [Ultralytics YOLO 训练 Notebooks](https://github.com/ultralytics/notebooks)
- [YOLO-Detection 训练代码](https://github.com/lianhongrui555/YOLO-Detection)