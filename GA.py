import random, copy

class Gene(object):
    def __init__(self, _name, _range):
        self.name = _name
        self.value_range = _range
        self.value = self.pickRandomValue()
    
    def pickRandomValue(self):
        return random.choice(self.value_range)

class Individual(object):    
    def __init__(self, params):
        self.fitness = []
        self.genes = []

        for  param in params:
            self.genes.append(Gene(param[0],param[1]))   
        
        self.calculateFitness()
        
    def gene_dict(self):
        gdict = {}
        for g in self.genes:
            gdict[g.name] = g.value
        return gdict
    
    def calculateFitness(self):
        genes = self.gene_dict()
        
        ######################################## TBA: Fitness function
        # set variables with the references from the variables defined in main.ipynb
        # Variable_1 = genes['Variable 1']
        # Variable_2 = genes['Variable 2']
        # Variable_3 = genes['Variable 3']
        # etc...
        
        # fitness = my_fitness_function(Variable_1, Variable_2, Variable_3)
        
        ########################################
        
        
        self.fitness = random.random()  # Replace with self.fitness = my_fitness_function(Variable_1, Variable_2, Variable_3)
        
    def printFitness(self):
        print(f'Fitness: {self.fitness}')
    
    def printGenes(self):
        for g in self.genes:
            print(f'{g.name}: {g.value}')       
            
    def dumpParameters(self):
        self.printGenes()
        self.printFitness()


class Population(object):
    def __init__(self, number_of_individuals, params):
        self.params = params
        
        self.individuals = []
        for _ in range(number_of_individuals):
            self.individuals.append(Individual(self.params))
    
    
    def sortPopulation(self):
        self.individuals = sorted(self.individuals,key=lambda individual: individual.fitness, reverse=True)
             
    def printPopulation(self, details=True, number_to_print=-1):
        self.sortPopulation()
        printed = 0
        print('Top list of individuals')
        for individual in self.individuals:
            if details==True:
                individual.dumpParameters()
            else:
                individual.printFitness()
            printed += 1
            if number_to_print != -1 and printed >= number_to_print:
                return
            
            
    def breedThePopulation(self, generation, mutation_probability = 0.25):
        
        # Whom to breed
        top_two = True  # Best two individuals
        top_with_random_top10 = True # Best individual with random other individual (among top ten)
        two_random_top10s = True # Two random individual among top 10
        

        # Breed the top two individuals        
        if top_two:
            self.sortPopulation()
            parent_a = self.individuals[0]
            parent_b = self.individuals[1]
            
            text = 'Breading top two individuals with fitness: {} and {} with mutation prob: {:.2f} in generation {}'.format(parent_a.fitness, parent_b.fitness, mutation_probability, generation+1)

            child_1, child_2 = self.breedTwoIndividuals(parent_a,parent_b,mutation_probability, text)
            
            self.individuals.append(child_1)
            self.individuals.append(child_2)
        
        if top_with_random_top10 == True:
            self.sortPopulation()
            parent_a = self.individuals[0]            
            
            ix_b = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            parent_b = self.individuals[ix_b]
            
            text = 'Breading best individual with random among top ten'
            
            child_1, child_2 = self.breedTwoIndividuals(parent_a,parent_b,mutation_probability, text)
            
            self.individuals.append(child_1)
            self.individuals.append(child_2)
            
        if two_random_top10s == True:
            self.sortPopulation()    
            if len(self.individuals)<10:
                return
            
            ix_a, ix_b = random.sample(set([1, 2, 3, 4, 5, 6, 7, 8, 9]), 2)
            parent_a = self.individuals[ix_a]
            parent_b = self.individuals[ix_b]

            text = 'Breading random two among top ten'
            
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
        i3.calculateFitness()
        
        print('')
        print(text)
        print('Second child')        
        i4 = mutate(i4)
        i4.calculateFitness()

        return i3, i4