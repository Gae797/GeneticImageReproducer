# -*- coding: utf-8 -*-

import random
import numpy as np

class Individual:
    
    def __init__(self, params, copy_individual = None):
        
        if copy_individual==None:
            
            length, image_size, square_size = params
            
            self.chromosome = [self.pickRandomColor() for i in range(length)]
            self.width, self.height = image_size
            self.size = square_size        
            self.pixels = None
            self.fitness = None
            
        else:
            self.copy(copy_individual)
        
    def copy(self, other):
        
        self.chromosome = other.chromosome[0:]
        self.width = other.width
        self.height = other.height
        self.size = other.size
        self.pixels = None
        self.fitness = None
        
    def getPixels(self):
        
        if self.pixels!=None:
            return self.pixels
        
        if self.size==1:
            pixels = np.reshape(self.chromosome,(self.height,self.width))
        
        else:
            #pixels = np.zeros((self.height, self.width), dtype=(int,3))
            pixels = np.zeros((self.height, self.width))
            
            for i in range(len(self.chromosome)):
                gene = self.chromosome[i]
                current_index = i * self.size
                row = (current_index // self.width) * self.size
                col = current_index % self.width
                
                for j in range(self.size):
                    for k in range(self.size):
                        pixels[row+j][col+k] = gene
             
        self.pixels = pixels
        return pixels
        
    def pickRandomColor(self):
        
        return random.randint(0, 255)