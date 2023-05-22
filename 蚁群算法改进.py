import random
import copy
import sys
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
'''
ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
      ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
     加快，但是随机性不高，容易得到局部的相对最优
'''
(max_pharomone,min_pharomone)=(1,0.1)
(ALPHA, BETA, RHO, Q) = (2.0, 3.0, 0.45, 1000.0)
best_res={'bier127':118282,'eil101':629,'st70':675,'pr76':108159}
# 城市数，蚁群
(city_num, ant_num) = (0, 50)
distance_x = []
distance_y = []

# 城市距离和信息素
distance_graph = [[0.0 for col in range(city_num)] for raw in range(city_num)]
pheromone_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]

def set_dataset(path):
    global city_num
    global distance_x
    global distance_y
    global distance_graph
    global pheromone_graph
    distance_x=[]
    distance_y=[]
    res=[]
    with open(path,'r') as file:
        for item in file:
            if len(item.strip())!=0:
                res.append(item.split())
    print(res)
    for items in res:
        if items[0]=='EDGE_WEIGHT_TYPE' and items[2]!='EUC_2D':
            raise Exception('This is distance error message.')
            return
        if items[0].isdigit():
            distance_x.append(int(items[1]))
            distance_y.append(int(items[2]))
    city_num=len(distance_y)
    distance_graph = [[0.0 for col in range(city_num)] for raw in range(city_num)]
    pheromone_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]

# ----------- 蚂蚁 -----------
class Ant(object): ##search_path->__move->得到__cal_total_distance
    # 初始化
    def __init__(self, ID):
        self.ID = ID  # ID
        self.__clean_data()  # 随机初始化出生点

    # 初始数据
    def __clean_data(self):
        self.path = []  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = -1  # 当前停留的城市
        self.open_table_city = [True for i in range(city_num)]  # 禁忌表

        city_index = random.randint(0, city_num - 1)  # 随机初始出生点
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    # 选择下一个城市
    def __choice_next_city(self):
        next_city = -1
        select_citys_prob = [0.0 for i in range(city_num)]  # 存储去下个城市的概率
        total_prob = 0.0
        # 获取去下一个城市的概率
        for i in range(city_num):
            if self.open_table_city[i]:
                try:
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow(
                        (1.0 / distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID=self.ID,current=self.current_city,target=i))
                    sys.exit(1)

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if (next_city == -1):  ##表明禁忌表全为False
            print(self.open_table_city)
            next_city = random.randint(0, city_num - 1)
            while ((self.open_table_city[next_city]) == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, city_num - 1)

        return next_city

    # 计算路径总距离
    def __cal_total_distance(self):
        temp_distance = 0.0
        for i in range(1, city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += distance_graph[start][end]

        # 回路
        #end = self.path[0]
        #temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance

    # 移动操作
    def __move(self, next_city):
        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    # 搜索路径
    def search_path(self):
        # 初始化数据
        self.__clean_data()
        # 搜素路径，遍历完所有城市为止
        while self.move_count < city_num:
            # 移动到下一个城市
            next_city = self.__choice_next_city()
            self.__move(next_city)
        # 计算路径总长度
        self.__cal_total_distance()

# ----------- TSP问题 -----------

class TSP(object):

    def __init__(self,dataset):
        self.bestdist=[]
        self.new()
        self.dataset=dataset
        # 计算城市之间的距离
        for i in range(city_num):
            for j in range(city_num):
                temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                distance_graph[i][j]=pow(temp_distance, 0.5)


    # 初始化
    def new(self, evt=None):
        # 初始城市之间的距离和信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = 1.0

        self.ants = [Ant(ID) for ID in range(ant_num)]  # 初始蚁群
        self.best_ant = Ant(-1)  # 初始最优解
        self.best_ant.total_distance = 1 << 31  # 初始最大距离
        self.iter = 1  # 初始化迭代次数


    # 开始搜索
    def search_path(self):
        self.bestdist=[]
        turns = [i + 1 for i in range(500)]
        line=[best_res[self.dataset] for i in range(500)]
        for j in range(500):
            # 遍历每一只蚂蚁
            for ant in self.ants:
                # 搜索一条路径
                ant.search_path()
                # 与当前最优蚂蚁比较
                if ant.total_distance < self.best_ant.total_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
            # 更新信息素
            self.__update_pheromone_gragh()  ##也就是说遍历完成就更新一波
            self.bestdist.append(self.best_ant.total_distance)
            print(u"迭代次数：", self.iter, u"最佳路径总距离：", int(self.best_ant.total_distance))
            self.iter += 1

        for i in range(1, city_num):
            start, end = self.best_ant.path[i - 1], self.best_ant.path[i]
            plt.plot([distance_x[start],distance_x[end]],[distance_y[start],distance_y[end]],'b')
        plt.show()
        plt.plot(turns,self.bestdist,color='b',label='AS')
        plt.plot(turns,line,'r--')
        plt.xlabel('迭代次数')
        plt.ylabel('当前最优值')
        plt.grid()
        #plt.show()

    def search_path_1(self,alpha,beta,rho):
        self.bestdist=[]
        turns = [i + 1 for i in range(500)]
        line=[best_res[self.dataset] for i in range(500)]
        for j in range(500):
            # 遍历每一只蚂蚁
            for ant in self.ants:
                # 搜索一条路径
                ant.search_path()
                # 与当前最优蚂蚁比较
                if ant.total_distance < self.best_ant.total_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
            # 更新信息素
            temp_pheromone=[[0.0 for col in range(city_num)] for raw in range(city_num)]
            for i in range(1, city_num):
                start, end = self.best_ant.path[i - 1], self.best_ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                temp_pheromone[start][end] += Q / self.best_ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]
            self.bestdist.append(self.best_ant.total_distance)
            for i in range(city_num):
                for j in range(city_num):
                    pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]
                    if(pheromone_graph[i][j]<min_pharomone):
                        pheromone_graph[i][j]=min_pharomone
                    if(pheromone_graph[i][j]>max_pharomone):
                        pheromone_graph[i][j]=max_pharomone
            #print(pheromone_graph)
            print(u"迭代次数：", self.iter, u"最佳路径总距离：", int(self.best_ant.total_distance))
            self.iter += 1
        plt.plot(turns,self.bestdist,label=f'MMAS alpha={alpha} beta={beta} rho={rho}')
        plt.legend()


    # 更新信息素
    def __update_pheromone_gragh(self):
        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
        for ant in self.ants:
            for i in range(1, city_num):
                start, end = ant.path[i - 1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]
        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]

# ----------- 程序的入口处 -----------

if __name__ == '__main__':
    #tsp_dataset=[]
    result=[]
    dataset='eil101'
    path='D:/Desktop/'+dataset+'.tsp'
    set_dataset(path)
    #plt.plot(distance_x,distance_y,'r*')
    #plt.scatter(distance_x,distance_y)
    #plt.show()
    #tsp_as=TSP(dataset)
    tsp_mmas1=TSP(dataset)
   #tsp_as.search_path()
    tsp_mmas1.search_path_1(2,3,0.4)
    ALPHA,BETA,RHO=1,1,0.5
    tsp_mmas2=TSP(dataset)
    tsp_mmas2.search_path_1(1,1,0.5)
    ALPHA,BETA,RHO=2,3,0.5
    tsp_mmas3=TSP(dataset)
    tsp_mmas3.search_path_1(2,3,0.5)
    plt.show()
