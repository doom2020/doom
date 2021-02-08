def shell_sort(arr):
    """希尔排序"""
    # 取整计算增量（间隔）值
    gap = len(arr) // 2
    while gap > 0:
        # 从增量值开始遍历比较
        for i in range(gap, len(arr)):
            j = i
            current = arr[i]
            # 元素与他同列的前面的每个元素比较，如果比前面的小则互换
            while j - gap >= 0 and current < arr[j - gap]:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = current
        # 缩小增量（间隔）值
        gap //= 2
    return arr

print(shell_sort([11, 11, 22, 33, 33, 36, 39, 44, 55, 66, 69, 77, 88, 99]))

# 返回结果[11, 11, 22, 33, 33, 36, 39, 44, 55, 66, 69, 77, 88, 99]