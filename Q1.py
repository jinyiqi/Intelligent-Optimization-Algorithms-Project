import numpy as np
import matplotlib.pyplot as plt
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

    # 绘制迭代图像
    def iter_pic(self, all_x, path=""):
        l = len(all_x)
        all_y = list(map(self.f, all_x))
        plt.xlabel("Iteration")
        plt.ylabel("f(x)")
        plt.plot(range(l), all_y)
        if path:
            plt.savefig(path)
        else:
            plt.show()

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
        # self.iter_pic()
        return self.min_x(), self.f(self.min_x()), self.all_x


if __name__ == '__main__':
    # 多极小函数 y = x^2 / 1000 + cos(x)
    def func(x):
        return x ** 2 / 1000 + np.cos(x)
    # 区间
    start = -3
    end = 100
    # 绘制真实函数图像
    x_list = np.arange(start, end, 0.1).tolist()
    y_list = list(map(func, x_list))
    plt.plot(x_list, y_list)
    # plt.show()
    plt.savefig("./pics/f1.jpg")
    plt.cla()
    # 多次模拟
    x_list = []
    y_list = []
    all_x_list = []
    for i in range(20):
        x = np.random.uniform(start, end)
        a = sa(x, start, end, func, T0=3000, Tf=0.1, alpha=0.98, iter=200)
        min_x, min_y, all_x = a.search()
        print(min_x, min_y)
        x_list.append(min_x)
        y_list.append(min_y)
        all_x_list.append(all_x)
    k = y_list.index(min(y_list))
    print('最小值x：', x_list[k])
    print('最小值f(x)：', y_list[k])
    print('f(x)平均值：', np.mean(y_list))
    print('f(x)方差：', np.var(y_list))
    a.iter_pic(all_x_list[k])
    plt.cla()
    plt.plot(list(range(1, 21)), x_list)
    plt.show()
    plt.cla()
    plt.plot(list(range(1, 21)), y_list)
    plt.show()


