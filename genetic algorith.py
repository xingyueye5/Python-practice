#genetic algorithm,2*sin(x)-1 [1/8,9/8]
#每一轮：生成->选择交叉->变异
import numpy as np
POP_SIZE=30
DNA_SIZE=8

def fun(x):
    return np.sin(x)

def squeeze(touple):
    tem=[]
    for i in touple:
        tem.append(1/8+i*1/(2**DNA_SIZE-1))
    return tem

def select(pop,fitness):
    idx=np.random.choice(np.arange(POP_SIZE),size=POP_SIZE,replace=True,p=fitness/fitness.sum())
    return pop[idx]

def mutation(child,MUTATION_RATE=0.03):
    if np.random.rand()<MUTATION_RATE:
        mutate_point=np.random.randint(0,DNA_SIZE)
        child[mutate_point]=child[mutate_point]^1

def crossover_mutation(pop,CROSSOVER_RATE=0.8):
    new_pop=[]
    for father in pop:
        child=father
        if np.random.rand()<CROSSOVER_RATE:
            mother=pop[np.random.randint(POP_SIZE)]
            cross_points=np.random.randint(0,DNA_SIZE)
            child[cross_points]=mother[cross_points]
        mutation(child)
        new_pop.append(child)
    return new_pop

pop=np.random.randint(2,size=(POP_SIZE,DNA_SIZE))##每一次n个，每组8位
val=pop.dot(2**np.arange(DNA_SIZE-1,-1,-1))
fitness=fun(squeeze(val))+2

if __name__=='__main__':
    for i in range(100):
        select(pop,fitness)
        crossover_mutation(pop)
        val = pop.dot(2 ** np.arange(DNA_SIZE - 1, -1, -1))
        fitness=fun(squeeze(val))+2
        #print(pop)
        print('The ',i,'th train get the maximun val= ',max(fitness)-2)
