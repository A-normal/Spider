my_list = [1, 2, 3]

# 在索引 -1 处插入元素，实际上是在最后一个元素前面插入
my_list.insert(-1, 4)
print(my_list)  # 输出: [1, 2, 4, 3]

# 在索引 -2 处插入元素
my_list.insert(-2, 5)
print(my_list)  # 输出: [1, 2, 5, 4, 3]

# 在索引 0 处插入元素
my_list.insert(0, 6)
print(my_list)  # 输出: [6, 1, 2, 5, 4, 3]