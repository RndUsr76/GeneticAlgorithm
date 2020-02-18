# GeneticAlgorithm

Ready to use Genetic Algorithm

Steps:
1. In main.ipynb ln[2]: Define variables with name (for you to reference them later on) and the allowed value range they can have. Note that these values can be int, float, string etc
2. In main.ipynb ln[3]: Set the size (number of individuals) of the starting population (randomized individuals)
3. In GA.py: In "calculateFitness" of class Individual; add the fitness function. This function must set self.fitness as a single number where higher is better. This is then the basis for evaluation of each individual.
4. In GA.py: In "breedThePopulation" of class Population; define the "breeding rules" i.e. who breeds with whom
5. In main.ipynb ln[7]: Set the number of generations to evolve
6. Run main.ipynb to find the optimal parameter setting
