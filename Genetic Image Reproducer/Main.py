# -*- coding: utf-8 -*-

import GeneticImageGenerator as gen
import ImageHandler
import ThreadManager

import random
import time

#Parameters
POPULATION_SIZE = 100
IMAGE_PATH = "Lena.jpg"
SQUARE_SIZE = 1
MAX_GENERATION = 2000
OPTIMAL_THRESHOLD = 12.5

TOURNAMENT_SAMPLE_SIZE = 100
MUTATION_NUMBER = 1
MUTATION_PROB = 1
RANDOM_SAVE_RATE = 0.05

RESET_SAVE_RATE = 0.05
RESET_TIME = 50

SEED = 24
IMAGE_SIZE = 40

VERBOSE = False

DISPLAY = True
DISPLAY_SAMPLE = 5
DISPLAY_RESIZE = IMAGE_SIZE * 10

SHOW_PLOT = True

#Variables
target = None
channels = []

#Test
def test(pop_size, tourn_size, mut_n, mut_prob):
    
    global POPULATION_SIZE, TOURNAMENT_SAMPLE_SIZE, MUTATION_NUMBER, MUTATION_PROB, DISPLAY, SHOW_PLOT
    
    POPULATION_SIZE = pop_size
    TOURNAMENT_SAMPLE_SIZE = tourn_size
    MUTATION_NUMBER = mut_n
    MUTATION_PROB = mut_prob
    DISPLAY = False
    SHOW_PLOT = False
    
    return main()

#Initialization
def initialize():
    
    global target, channels
    
    if not isValidSquareSize():
        raise Exception("Image size must be a multiple of Square size")
    
    random.seed(SEED)
    target, channels = ImageHandler.openImage(IMAGE_PATH,IMAGE_SIZE)
    
    red_generator = gen.ImageGenerator(POPULATION_SIZE, IMAGE_PATH, SQUARE_SIZE,
                       MAX_GENERATION, OPTIMAL_THRESHOLD, TOURNAMENT_SAMPLE_SIZE, 
                       MUTATION_NUMBER, MUTATION_PROB,
                       RANDOM_SAVE_RATE, RESET_SAVE_RATE, RESET_TIME,
                       target, channels[0])
    
    green_generator = gen.ImageGenerator(POPULATION_SIZE, IMAGE_PATH, SQUARE_SIZE,
                       MAX_GENERATION, OPTIMAL_THRESHOLD, TOURNAMENT_SAMPLE_SIZE, 
                       MUTATION_NUMBER, MUTATION_PROB,
                       RANDOM_SAVE_RATE, RESET_SAVE_RATE, RESET_TIME,
                       target, channels[1])
    
    blue_generator = gen.ImageGenerator(POPULATION_SIZE, IMAGE_PATH, SQUARE_SIZE,
                       MAX_GENERATION, OPTIMAL_THRESHOLD, TOURNAMENT_SAMPLE_SIZE, 
                       MUTATION_NUMBER, MUTATION_PROB,
                       RANDOM_SAVE_RATE, RESET_SAVE_RATE, RESET_TIME,
                       target, channels[2])
    
    return red_generator, green_generator, blue_generator

def isValidSquareSize():
    
    ratio = IMAGE_SIZE // SQUARE_SIZE
    return (ratio * SQUARE_SIZE)==IMAGE_SIZE

#-----------------------------------------------------------------------------
#Main
    
def main():

    start = time.time()
    
    red_generator, green_generator, blue_generator = initialize()
    print_channels = ([],[],[])
    display_channels = ([],[],[])
    exception_raised = False
    
    red_thread = ThreadManager.ChannelThread(red_generator, print_channels[0], 
                                             display_channels[0], DISPLAY_SAMPLE, 
                                             exception_raised)
    green_thread = ThreadManager.ChannelThread(green_generator, print_channels[1], 
                                               display_channels[1], DISPLAY_SAMPLE, 
                                               exception_raised)
    blue_thread = ThreadManager.ChannelThread(blue_generator, print_channels[2], 
                                              display_channels[2], DISPLAY_SAMPLE, 
                                              exception_raised)
    
    if VERBOSE:
        print_thread = ThreadManager.PrintThread(print_channels)
    
    if DISPLAY:
        display_thread = ThreadManager.DisplayThread(display_channels, DISPLAY_SAMPLE, DISPLAY_RESIZE ,target)
    
    try:
        red_thread.start()
        green_thread.start()
        blue_thread.start()
        
        if VERBOSE:
            print_thread.start()
            
        if DISPLAY:
            display_thread.start()
        
        red_channel = red_thread.join()
        green_channel = green_thread.join()
        blue_channel = blue_thread.join()
        
        if VERBOSE:
            print_thread.stop()
            print_thread.join()
            
        if DISPLAY:    
            display_thread.stop()
            display_thread.join()
            
        means = [round((red+green+blue) / 3,2) for red, green, blue in zip(red_channel,green_channel,blue_channel)]
        if SHOW_PLOT:
            ImageHandler.plot(means,"Generation","Score", OPTIMAL_THRESHOLD*IMAGE_SIZE)
        
        time_spent = round(time.time() - start,2)
        generations = len(means)
    
        return time_spent, generations
    
    except Exception as e:
        print()
        print(e.__cause__())
        exception_raised = True
        
        return None, None
        #Kill all the threads
        
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    time_spent, generations = main()
    
    if time_spent!=None and generations!=None:
        print()
        print("-------------------------------")
        print("Time spent: {} s".format(time_spent))
        print("Solved after {} generations".format(generations))