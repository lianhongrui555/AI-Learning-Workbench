# 模型评估与调参：Precision、Recall、mAP

> 本节目标：理解 Precision、Recall、IoU、mAP50、mAP50-95 以及置信度阈值对检测结果的影响。

## 一句话理解

检测模型不能只问“答对几个”，还要看：报出来的准不准、真正的目标有没有漏掉、框和真实位置重叠得够不够。

## 核心概念

- **Precision**：报出来的检测结果里，有多少是正确的。
- **Recall**：真正的目标里，有多少被找出来。
- **IoU**：预测框和真实框的重叠程度。
- **mAP50**：IoU 阈值为 0.5 时的平均精度。
- **mAP50-95**：多个 IoU 阈值下的综合平均精度。
- **conf 阈值**：低于阈值的检测结果会被过滤。
- **过拟合**：训练指标继续提升，但验证指标不再提升。

打比方：

- Precision 高：老师说“我点名的都是真猫”。
- Recall 高：老师说“图里的猫我基本都点到了”。

## 代码阅读示例

```python
metrics = {"mAP50": 0.78, "mAP50-95": 0.52}
print(metrics["mAP50"])
```

阅读重点：

- 字典里的键代表指标名称。
- 方括号里写错键名会触发 KeyError。
- mAP50 高不一定代表所有尺寸目标都检测得好。

## 课后小测

1. Precision 和 Recall 分别关注什么？
2. mAP50 里的 50 表示什么？
3. 提高 conf 阈值通常会带来什么变化？

## 深度阅读

- [Ultralytics Val Mode](https://docs.ultralytics.com/modes/val/)
- [Microsoft AI for Beginners - Object Detection](https://github.com/microsoft/AI-For-Beginners)