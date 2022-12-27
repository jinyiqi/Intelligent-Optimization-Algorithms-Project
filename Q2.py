import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx

class sa_TSP:
    # 输入参数以及地图矩阵
    def __init__(self, mat, start_x, T0=3000, Tf=10, alpha=0.95, iter=200):
        self.mat = mat
        # 在定义域内随机生成初始点
        self.x = start_x
        self.all_x = []
        # 物理信息
        self.T = T0
        self.Tf = Tf
        self.alpha = alpha
        self.iter = iter

    # 解是否有效
    def is_valid(self, x):
        for i in range(len(x) - 1):
            if self.mat[x[i]][x[i+1]] == 0:
                return False
        if mat[x[-1]][x[0]] == 0:
            return False
        return True

    # 解的总cost
    def cost(self, x):
        cost = 0
        for i in range(len(x) - 1):
            if self.mat[x[i]][x[i+1]] != 0:
                cost += self.mat[x[i]][x[i+1]]
            else:
                return False
        return cost + mat[x[-1]][x[0]]

    # 随机选择下一个点
    # 考虑到两个解不能差的太远，选择类似洗牌的随机方法，随机选择一半数的顺序不变，另一半打乱顺序随机插进去
    # 但这样做会导致时间慢，后来之间改成纯shuffle了
    def next_solution(self, x):
        # print(x, end = ' ')
        x = x[1:]
        l_shuffle = int(len(x) / 2)
        while True:
            # shuffle_choice = np.random.choice(list(range(len(x))), replace=False, size=l_shuffle)
            # shuffle_order = np.random.choice(list(range(len(x))), replace=False, size=l_shuffle)
            # new_x = [-1] * len(x)
            # for i in range(l_shuffle):
            #     new_x[shuffle_order[i]] = x[shuffle_choice[i]]
            # unshuffle = []
            # for i in range(len(x)):
            #     if i not in shuffle_choice:
            #         unshuffle.append(i)
            # mark = 0
            # for i, n in enumerate(new_x):
            #     if n == -1:
            #         new_x[i] = x[unshuffle[mark]]
            #         mark += 1
            random.shuffle(x)
            new_x = [0] + x

            if self.is_valid(new_x):
                break
        # print(new_x, self.is_valid(new_x))
        return new_x

    # metropolis准则
    def metropolis(self, x, new_x):
        e = self.cost(x)
        new_e = self.cost(new_x)
        if new_e <= e:
            return True
        else:
            p = np.exp((e - new_e) / self.T)
            return True if random.random() < p else False

    # 在迭代得到的解集中得到最好的x
    def min_x(self):
        all_y = list(map(self.cost, self.all_x))
        return self.all_x[all_y.index(min(all_y))]

    # 绘制迭代图像
    def iter_pic(self, all_x, path=""):
        l = len(all_x)
        all_y = list(map(self.cost, all_x))
        plt.xlabel("Iteration")
        plt.ylabel("f(x)")
        plt.plot(range(l), all_y)
        if path:
            plt.savefig(path)
        else:
            plt.show()

    # 搜索函数
    def search(self):
        # 首先找到可行解
        self.x = self.next_solution(self.x)
        self.all_x.append(self.x)
        # 温度循环
        while self.T > self.Tf:
            # 找出目前为止的最优解
            self.x = self.min_x()
            # print(self.x)
            # 内层循环
            for i in range(self.iter):
                new_x = self.next_solution(self.x)
                if self.metropolis(self.x, new_x):
                    self.x = new_x
            self.all_x.append(self.x)
            self.T *= self.alpha
        # self.iter_pic()
        return self.min_x(), self.cost(self.min_x()), self.all_x

if __name__ == '__main__':
    # 编辑路程map
    graph = nx.Graph()
    graph.add_nodes_from(range(0, 8))
    edges = [(0, 1, 3), (0, 4, 2),
             (1, 4, 3), (1, 5, 4), (1, 7, 2),
             (2, 3, 5), (2, 4, 1), (2, 5, 4), (2, 6, 3),
             (3, 6, 1),
             (4, 5, 5),
             (5, 6, 2), (5, 7, 4),
             (6, 7, 4)]
    graph.add_weighted_edges_from(edges)
    mat = nx.to_numpy_array(graph)
    print(mat)

    # 多次模拟
    x_list = []
    y_list = []
    all_x_list = []
    for i in range(20):
        start_x = np.random.choice(list(range(1, mat.shape[0])), replace=False, size=mat.shape[0] - 1)
        start_x = [0] + list(start_x)
        a = sa_TSP(mat, start_x, T0=3000, Tf=100, alpha=0.95, iter=20)
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
    plt.plot(list(range(1, 21)), y_list)
    plt.show()