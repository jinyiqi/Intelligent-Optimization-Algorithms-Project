# SA算法接口
import numpy as np
import random

class sa:
    # 输入函数的左右边界和函数
    def __init__(self, start_x, start, end, f, T0=3000, Tf=10, alpha=0.95, iter=200):
        # 函数信息
        self.start = start
        self.end = end
        self.f = f
        # 在定义域内随机生成初始点
        self.x = start_x
        self.all_x = [self.x]
        # 物理信息
        self.T = T0
        self.Tf = Tf
        self.alpha = alpha
        self.iter = iter

    # 解是否在边界内
    def is_valid(self, x):
        if self.start <= x <= self.end:
            return True
        return False

    # 按照高斯分布随机选择下一个点
    def next_solution(self):
        sigma = max(self.end - self.x, self.x - self.start) / 3
        while True:
            new_x = random.gauss(self.x, sigma)
            if self.is_valid(new_x):
                break
        return new_x

    # metropolis准则
    def metropolis(self, x, new_x):
        e = self.f(x)
        new_e = self.f(new_x)
        if new_e <= e:
            return True
        else:
            p = np.exp((e - new_e) / self.T)
            return True if random.random() < p else False

    # 在迭代得到的解集中得到最好的x
    def min_x(self):
        all_y = list(map(self.f, self.all_x))
        return self.all_x[all_y.index(min(all_y))]

    # 搜索函数
    def search(self):
        # 温度循环
        while self.T > self.Tf:
            # 找出目前为止的最优解
            self.x = self.min_x()
            # print(self.x)
            # 内层循环
            for i in range(self.iter):
                new_x = self.next_solution()
                if self.metropolis(self.x, new_x):
                    self.x = new_x
            self.all_x.append(self.x)
            self.T *= self.alpha
        return self.min_x()



import math
def square(x):
    return pow(x, 3) * math.cos(x)

x = np.random.uniform(-1, 2)
a = sa(x, -1.57, 20.18, square, iter=200)
print(a.search())

