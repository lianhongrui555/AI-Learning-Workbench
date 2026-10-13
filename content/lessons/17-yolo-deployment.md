# YOLO 推理与 Flask 摄像头部署

> 本节目标：理解图像预处理、模型推理、结果解析、Web 上传和摄像头实时检测的完整部署链路。

## 一句话理解

训练得到 `best.pt` 后，推理就是让模型面对新图片或摄像头画面，实时给出类别、置信度和边界框。

## 核心概念

- **推理**：训练完成后使用模型处理新输入。
- **预处理**：缩放、颜色转换、张量转换等。
- **后处理**：解析边界框、类别和置信度。
- **Flask 接口**：浏览器上传图片，后端返回检测结果。
- **Canvas**：浏览器把框和类别画到画面上。
- **延迟**：处理一帧需要多少毫秒。
- **FPS**：每秒能处理多少帧。
- **imgsz**：推理输入尺寸，影响速度和精度。

典型链路：

```text
摄像头取帧
→ 编码为 JPEG
→ 上传 Flask
→ YOLO 推理
→ 返回坐标和类别
→ Canvas 绘制检测框
```

## 代码阅读示例

```python
results = model.predict(frame, conf=0.5, imgsz=640)
```

阅读重点：

- `frame` 是输入图像。
- `conf` 过滤低置信度结果。
- `imgsz` 影响推理速度和细节保留。
- 还要继续读取 `results` 中的框和类别，不能只调用预测。

## 课后小测

1. 一次 YOLO 推理通常包含哪些步骤？
2. 浏览器和 Flask 后端如何分工？
3. 减小 imgsz 通常会带来什么变化？

## 深度阅读

- [Ultralytics Predict Mode](https://docs.ultralytics.com/modes/predict/)
- [YOLO-Detection Web 项目](https://github.com/lianhongrui555/YOLO-Detection)