# 经典机器学习：分类、回归与评估

> 本节目标：理解分类和回归的区别，知道准确率、精确率、召回率和过拟合为什么重要。

## 一句话理解

分类是在几个选项中选标签，回归是预测一个连续数字。评估指标就是给模型的考试打分表。

## 核心概念

- **分类**：输出离散类别，例如垃圾邮件/正常邮件。
- **回归**：输出连续数值，例如房价、温度、销量。
- **准确率**：所有预测中正确的比例。
- **精确率**：模型说“是”的样本里，真正是的比例。
- **召回率**：所有真正的正样本里，被找出来的比例。
- **训练集、验证集、测试集**：分别用于学习、调参和最终验收。

打比方：分类像判断邮件是不是垃圾邮件；回归像预测一辆二手车能卖多少钱。

## 必须掌握的代码/命令

```python
# 用最简单的规则演示二分类。
def classify_temperature(value):
    return "炎热" if value >= 30 else "舒适"

print(classify_temperature(35))
print(classify_temperature(22))
```

## 代码阅读示例

先不要运行代码，直接阅读并尝试判断它做了什么：

```python
def classify(value):
    return "炎热" if value >= 30 else "舒适"

print(classify(35))
print(classify(22))
```

阅读提示：

- 先找变量分别保存了什么。
- 再追踪每一行执行的顺序。
- 最后判断输出、错误或参数变化。

页面下方有对应的代码理解题，提交后可以查看逐行解释。


## 课后小测

1. 预测“是否会下雨”属于分类还是回归？
2. 精确率和召回率关注的问题有什么不同？
3. 为什么只看训练集准确率不够？

## 深度阅读

- [Microsoft ML for Beginners](https://github.com/microsoft/ML-For-Beginners)
- [Scikit-learn 用户指南](https://scikit-learn.org/stable/user_guide.html)