# -*- coding: utf-8 -*-

import Individual as ind
import random
import numpy as np

class ImageGenerator:
    
    def __init__(self, pop_size, img_path, square_size, max_gen, optimal_thr, tournament_size, mutate_n, mutation_prob,
                 rnd_save_rate, reset_save_rate, reset_time, target, channel):
        
        self.POPULATION_SIZE = pop_size
        self.IMAGE_PATH = img_path
        self. SQUARE_SIZE = square_size
        self.MAX_GENERATION = max_gen
        self.TOURNAMENT_SAMPLE_SIZE = tournament_size
        self.MUTATION_NUMBER = mutate_n
        self. MUTATION_PROB = mutation_prob
        self.RANDOM_SAVE_RATE = rnd_save_rate
        self. RESET_SAVE_RATE = reset_save_rate
        self.RESET_TIME = reset_time
        
        self.target = target
        self.channel = channel
        
        self.population = []
        self.OPTIMAL = target.size[0] * optimal_thr
        self.channel_pixels = self.imageToPixels(channel)

#Initialization
    def initialize(self):
        
        self.chromosome_length = (self.target.size[0]  * self.target.size[1]) // (self.SQUARE_SIZE**2)
        
        for i in range(self.POPULATION_SIZE):
            self.addRandomIndividual()
            
    def addRandomIndividual(self):
        params = (self.chromosome_length,self.target.size,self.SQUARE_SIZE)
        self.population.append(ind.Individual(params))
    
#Fitness
    def fitness(self, individual):
        
        if individual.fitness!=None:
            return individual.fitness
        
        pixels = individual.getPixels()
        diff = pixels - self.channel_pixels
        mse = np.linalg.norm(diff)
        
        individual.fitness = mse
        return mse
    
#Selection
    def selection(self):
        
        parent_1 = self.tournament()
        parent_2 = self.tournament()
        
        return parent_1, parent_2
        
    def tournament(self):
        
        samples = random.sample(self.population, self.TOURNAMENT_SAMPLE_SIZE)
        fitness_values = [self.fitness(sample) for sample in samples]
        return samples[fitness_values.index(min(fitness_values))]
    
#Crossover
    def crossover(self, parent_1, parent_2):
        
        crossover_point = random.randrange(0,self.chromosome_length-1)
        
        offspring_1 = ind.Individual(None, copy_individual=parent_1)
        offspring_2 = ind.Individual(None, copy_individual=parent_2)
        
        offspring_1.chromosome = self.merge(parent_1.chromosome, parent_2.chromosome, crossover_point)
        offspring_2.chromosome = self.merge(parent_2.chromosome, parent_1.chromosome, crossover_point)
        
        return offspring_1, offspring_2
    
    def merge(self, seq_1, seq_2, point):
        
        sub_seq_1 = seq_1[0:point]
        sub_seq_2 = seq_2[point:]
        
        return sub_seq_1 + sub_seq_2
    
#Mutations
    def mutate(self, individual):
        
        #mutation_points = random.sample(range(self.chromosome_length),self.MUTATION_NUMBER)
        random_point = random.randrange(0,self.chromosome_length-self.MUTATION_NUMBER)
        mutation_points = range(random_point,random_point+self.MUTATION_NUMBER)
        new_color = individual.pickRandomColor()
        for mutation_point in mutation_points:
            #self.replaceMutate(individual, mutation_point)
            individual.chromosome[mutation_point] = new_color
    
    def replaceMutate(self, individual, mutation_point):
        
        individual.chromosome[mutation_point] = individual.pickRandomColor()
        
#Elitism
    def killByRank(self):
        
        self.population.sort(key=self.fitness)
        kill_mask = self.randomSave()
            
        next_generation = [self.population[i] for i in range(len(self.population)) if not kill_mask[i]]
        self.population.clear()
        self.population.extend(next_generation)
        
    def randomSave(self):
        
        kill_number = len(self.population) - self.POPULATION_SIZE
        kill_mask = [False]*self.POPULATION_SIZE + [True]*(kill_number)
        
        save_number = int(self.POPULATION_SIZE * self.RANDOM_SAVE_RATE)
        for i in range(save_number):
            kill_index = random.randrange(0,self.POPULATION_SIZE)
            while kill_mask[kill_index]==True:
                kill_index = random.randrange(0,self.POPULATION_SIZE)
            
            save_index = random.randrange(self.POPULATION_SIZE,len(self.population))
            while kill_mask[save_index]==False:
                save_index = random.randrange(self.POPULATION_SIZE,len(self.population))
                
            kill_mask[kill_index] = True
            kill_mask[save_index] = False
            
        return kill_mask
    
#Reset
    def reset(self):
        
        save_number = int(self.POPULATION_SIZE * self.RESET_SAVE_RATE)
        reset_number = self.POPULATION_SIZE - save_number
        
        self.saveBest(save_number)
        
        for i in range(reset_number):
            self.addRandomIndividual()
        
    def saveBest(self, save_number):
        
        self.population.sort(key=self.fitness)
        save_list = self.population[0:save_number]
        self.population.clear()
        self.population.extend(save_list)
    
#Run generation
    def runGeneration(self):
        
        for i in range(self.POPULATION_SIZE//2):
            
            parent_1, parent_2 = self.selection()
            offsprings = self.crossover(parent_1, parent_2)
            
            for child in offsprings:
                mutation_event = self.eventTest(self.MUTATION_PROB)
                if mutation_event:
                    self.mutate(child)
                self.population.append(child)
        
        self.killByRank()
    
#Auxiliary functions
    def imageToPixels(self,img):
        
        return np.array(img.getdata()).reshape(img.size[1], img.size[0])
        
    def eventTest(self,probability):
        
        event = random.uniform(0.0, 1.0)
        return event<probability
    
#Run
    def run(self, print_channel, display_channel, display_sample, exception_raised):

        self.initialize()
        current_generation = 0
        current_score = None
        gen_without_impr = 0
        best_solutions = []
        
        while current_generation<=self.MAX_GENERATION and (current_score==None or current_score>self.OPTIMAL) and not exception_raised:
            self.runGeneration()
            best_solution = self.population[0]
            new_score = self.fitness(best_solution)
            best_solutions.append(best_solution)
            current_generation+=1
            
            print_channel.append(new_score)
            
            if current_generation % display_sample == 0 or current_generation==1:
                display_channel.append(best_solution.pixels)
                  
            diff = current_score - new_score if current_score!=None else None
            if current_score!=None and diff<1:
                gen_without_impr+=1
                
            else:
                gen_without_impr=0
                
            current_score=new_score
            
            if gen_without_impr==15:
                self.MUTATION_NUMBER = 1
            
            if gen_without_impr==self.RESET_TIME:
                self.reset()
                gen_without_impr=0

        return [solution.fitness for solution in best_solutions]