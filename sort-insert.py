def insertion_sort(arr):
    """插入排序"""
    # 第一层for表示循环插入的遍数
    for i in range(1, len(arr)):
        # 设置当前需要插入的元素
        current = arr[i]
        # 与当前元素比较的比较元素
        pre_index = i - 1
        while pre_index >= 0 and arr[pre_index] > current:
            # 当比较元素大于当前元素则把比较元素后移
            arr[pre_index + 1] = arr[pre_index]
            # 往前选择下一个比较元素
            pre_index -= 1
        # 当比较元素小于当前元素，则将当前元素插入在 其后面
        arr[pre_index + 1] = current
    return arr

insertion_sort([11, 11, 22, 33, 33, 36, 39, 44, 55, 66, 69, 77, 88, 99])


# 返回结果[11, 11, 22, 33, 33, 36, 39, 44, 55, 66, 69, 77, 88, 99]