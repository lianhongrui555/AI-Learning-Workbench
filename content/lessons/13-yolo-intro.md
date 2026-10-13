# 目标检测与 YOLO 入门

> 本节目标：理解分类、目标检测、边界框、置信度和 YOLO 单阶段检测的基本思路。

## 一句话理解

图像分类回答“图里有什么”，目标检测还要回答“它在图里的哪个位置、有多确定”。YOLO 就像一次性扫描整张图片，同时给出类别和位置。

## 核心概念

- **分类**：只输出一个或几个类别，例如“猫”。
- **目标检测**：同时输出类别、边界框和置信度。
- **边界框**：用矩形标出目标位置，常见表示是左上角和右下角坐标。
- **置信度**：模型对当前检测结果有多确定。
- **YOLO**：You Only Look Once，一次前向计算即可得到大量检测结果。
- **单阶段检测**：不需要先生成大量候选区域，速度通常更快。

打比方：分类像老师判断“这张照片里有猫”；检测像老师不仅说“有猫”，还用笔把每只猫圈出来。

## 核心概念与阅读要点

阅读检测结果时，重点看三类字段：

```text
类别 class
边界框 bbox
置信度 confidence
```

只看到类别还不够，因为同一张图可能有多个目标；只看到坐标也不够，因为还需要知道它是什么。

## 代码阅读示例

```python
det = {"class": "car", "confidence": 0.91}
print(f"{det['class']} {det['confidence']:.0%}")
```

阅读时先判断 `det` 里保存了什么，再看 `:.0%` 会把小数转换成百分比。

## 课后小测

1. 分类和目标检测的区别是什么？
2. 边界框和置信度分别表示什么？
3. YOLO 为什么被称为单阶段检测器？

## 深度阅读

- [Ultralytics YOLO Docs](https://docs.ultralytics.com/)
- [Ultralytics Notebooks](https://github.com/ultralytics/notebooks)
- [YOLO-Detection](https://github.com/lianhongrui555/YOLO-Detection)