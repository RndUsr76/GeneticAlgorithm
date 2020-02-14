import random, copy
from classes.Individual import *

class Population(object):
    def __init__(self, params):
        self.params = params
        self.individuals = []
    
    
    def sortPopulation(self):
        self.individuals = sorted(self.individuals,key=lambda individual: individual.fitness, reverse=True)
             
    def printPopulation(self, number_to_print=-1):
        self.sortPopulation()
        printed = 0
        print('Top list of fitness')
        for individual in self.individuals:
            #individual.printGenes()
            print('{:.1f}%'.format(individual.fitness))
            printed += 1
            if number_to_print != -1 and printed >= number_to_print:
                return
            
            
    def breedThePopulation(self, generation, mutation_probability = 0.25):
        # De två bästa med varandra
        self.sortPopulation()
        i1 = self.individuals[0]
        i2 = self.individuals[1]
        text = 'Breading top two individuals with fitness: {:.1f}% and  {:.1f}% with mutation prob: {:.2f} in generation {}'.format(
                                    i1.fitness, i2.fitness, mutation_probability, generation+1)

        child_1, child_2 = self.breedTwoIndividuals(i1,i2,mutation_probability, text)
        self.individuals.append(child_1)
        self.individuals.append(child_2)
        self.sortPopulation()
        
        
        if len(self.individuals)<10:
            return
        text = 'Breading random two among top ten'
        ix_a, ix_b = random.sample(set([1, 2, 3, 4, 5, 6, 7, 8, 9]), 2)
        parent_a = self.individuals[ix_a]
        parent_b = self.individuals[ix_b]
        
        child_1, child_2 = self.breedTwoIndividuals(parent_a, parent_b, mutation_probability, text)
        
        self.individuals.append(child_1)
        self.individuals.append(child_2)        
        
        self.sortPopulation()

    def breedTwoIndividuals(self,i1,i2,mutation_probability, text = ''):
        split_idx = int(len(i1.genes)/2) 
        
        i3 = Individual(self.params)
        i4 = Individual(self.params)

        i3.genes[0:split_idx] = copy.deepcopy(i1.genes[0:split_idx])
        i3.genes[split_idx:] = copy.deepcopy(i2.genes[split_idx:])

        i4.genes[0:split_idx] = copy.deepcopy(i2.genes[0:split_idx])
        i4.genes[split_idx:] = copy.deepcopy(i1.genes[split_idx:])

        # mutate
        def mutate(individual):
            for gene in individual.genes:
                if random.random()<mutation_probability:
                    gene.value = gene.pickRandomValue()
            return individual
        
        print('')
        print(text)
        print('First child')
        i3 = mutate(i3)
        #i3.initData()
        i3.initModel()
        i3.calculateFitness()
        
        print('')
        print(text)
        print('Second child')        
        i4 = mutate(i4)
        #i4.initData()
        i4.initModel()
        i4.calculateFitness()

        return i3, i4