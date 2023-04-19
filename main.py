MAX=2
MIN=-2
MUTSTEP=1.2
L=20
P=50
MUTRATE=2.1


from sympy import *
import math 
import matplotlib.pyplot as plt
import random
from statistics import mean
import copy
import time 

#process time starts
time_start= time.time()

class individual:
    def __init__(self):
        self.gene = [0]*L
        self.fitness = 0

#formulas provided in specification

def test_function(ind):
    x=ind.gene
    total=0
    

    # for i in range(0,len(x)):
    #     d=20
    #     total= total + (x[i]*math.sin(sqrt(abs(x[i]))))     
    #     d+=1
    # return (418.9829)*d - (total)
    

    
    for i in range(0,len(x)):
        d=10
        m=10
        total=total+ (math.sin(x[i])* pow( math.sin(i*pow(x[i],2)/math.pi),2*m))
        d+=1
        m+=1
    return total*(-1)






# initiliasing random 1st generation
def initialise(populationNumber, geneNumber):
    population=[]
    for x in range(0, populationNumber):
        tempgene = []
        for y in range(0, (geneNumber)):
            tempgene.append(random.uniform(0,1.0))
        newind = individual()
        newind.gene = tempgene.copy()
        newind.fitness = test_function(newind)
        population.append(newind)
    return population
      





#Selecting minimal fitness among parents
def select_min(populationNumber,population):
    offspring = []
    for i in range(0, populationNumber):
        parent1 = random.randint(0, populationNumber - 1)
        off1 = copy.deepcopy(population[parent1])
        parent2 = random.randint(0, populationNumber - 1)
        off2 = copy.deepcopy(population[parent2])
        if off1.fitness < off2.fitness:
            offspring.append(off1)
        else:
            offspring.append(off2)
    return offspring



#recombining genes with 2 points crossover (crosspoint2)
def recombine(populationNumber,geneNumber,offspring):
    toff1 = individual()
    toff2 = individual()
    temp = individual()
    for i in range(0, populationNumber, 2):
        toff1 = copy.deepcopy(offspring[i])
        toff2 = copy.deepcopy(offspring[i + 1])
        temp = copy.deepcopy(offspring[i])
        crosspoint = random.randint(0, geneNumber)
        crosspoint2 = random.randint(crosspoint, geneNumber)
        for j in range(crosspoint, crosspoint2):
            toff1.gene[j] = toff2.gene[j]
            toff2.gene[j] = temp.gene[j]
        toff1.fitness=test_function(toff1)
        toff2.fitness=test_function(toff2)
        offspring[i] = copy.deepcopy(toff1)
        offspring[i + 1] = copy.deepcopy(toff2)
    return offspring


#Mutation process
def mutate(populationNumber,geneNumber,offspring):
    for i in range( 0, populationNumber):
        newind = individual()
        newind.gene = []
        for j in range( 0, geneNumber):
            gene = offspring[i].gene[j]
            mutprob = random.random()
            MUTSTEP= random.uniform(0,1.0)
            MUTRATE=random.uniform(0,1.0)
            if mutprob < MUTRATE:
                alter = random.uniform(-MUTSTEP,MUTSTEP)
                gene = gene + alter
                if gene > MAX:
                    gene = MAX
                if gene < MIN:
                    gene = MIN
            newind.gene.append(gene)

        newind.fitness = test_function(newind)
        offspring[i]=newind
    return offspring

#function that shows the minimum fitness (checking genes by value)
def minFitness (offsprings):
    result = offsprings[0]
    for o in offsprings:
        if (o.fitness<result.fitness):
            result=o
    
    return result


#function that shows the maximum fitness (checking genes by index)
def maxFitness (offsprings):
    result = offsprings[0]
    index=0
    for i in range (0,len(offsprings)):
        if (offsprings[i].fitness>result.fitness):
            result=offsprings[i]
            index=i

    return index


#Calling the functions we defined above
values=[]
means=[]
population = initialise(P,L)
parents=select_min(P,population)
offspring=recombine(P,L,parents)
#mutated offspring(below)
offspring=mutate(P,L,offspring)
lowest_fitness=0



x=0
while(x<50): #50 generations
    offspring = recombine(P, L, parents)
    offspring = mutate(P, L, offspring)
    parents =select_min(P,offspring)
    parents[maxFitness(parents)]=minFitness(parents)

    for i in range(0,P):
        if lowest_fitness>offspring[i].fitness:
            lowest_fitness=offspring[i].fitness
        
        
    
    values.append(min(x.fitness for x in offspring))
    means.append(mean(x.fitness for x in offspring))
    x+=1
    
#process time ends    
time_end=time.time()

print("lowest fitness is = %f" % lowest_fitness)
print("process time :" ,time_end -time_start)



#printing out a graph by using 'mathplotlib' library
plt.ylabel('Fitness')
plt.xlabel('Generation')
plt.plot(values,label='Best')
plt.plot(means,label='Means')
plt.legend(loc=0)
plt.show()                                                      



