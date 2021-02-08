# 快速排序
import random
def quicksort(ls):
    # 列表只有一个元素返回
    if len(ls) <= 1:
        return ls
    # 将列表拆分成两个
    left, right = [], []
    # 基准数,选择数组中间一个数
    base = ls[len(ls) // 2]
    # 将基准数从原列表移除
    ls.remove(base)
    # 对剩余列表进行划分
    for x in ls:
        if x < base:
            left.append(x)
        else:
            right.append(x)
    # 递归调用
    return quicksort(left) + [base] + quicksort(right)

listnum = [i for i in range(1000000)]
random.shuffle(listnum)
print(quicksort(listnum))
