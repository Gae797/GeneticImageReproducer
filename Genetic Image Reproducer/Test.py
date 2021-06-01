# -*- coding: utf-8 -*-

import Main

population_sizes = [50,75,100,150,200,300,500]
tournament_sizes = []
mutation_numbers = [1]
mutation_probs = [1]

f = open("test.txt", "a")
f.write("Pop\tTou\tMut_n\tMut_pr\tTime\tGen\n\n")

for population_size in population_sizes:
    tournament_sizes = [population_size, population_size//2, population_size//4, population_size//10]
    for tournament_size in tournament_sizes:
        for mutation_number in mutation_numbers:
            for mutation_prob in mutation_probs:
                
                time, gen = Main.test(population_size, tournament_size, mutation_number, mutation_prob)
                
                if time!=None and gen!=None:
                    f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
                        population_size,
                        tournament_size, mutation_number, mutation_prob, time, gen
                        ))
                    f.flush()
                
f.close()
print("Test finished")