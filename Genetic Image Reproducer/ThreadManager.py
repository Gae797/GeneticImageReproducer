# -*- coding: utf-8 -*-

import threading
import ImageHandler

class ChannelThread(threading.Thread):
    
    def __init__(self, channel_generator, print_channel, display_channel, display_sample, exception_raised):
        
        threading.Thread.__init__(self)
        self.generator = channel_generator
        self.print_channel = print_channel
        self.display_channel = display_channel
        self.display_sample = display_sample
        self.exception_raised = exception_raised
        
    def run(self):
        
        self.channel = self.generator.run(self.print_channel, self.display_channel, self.display_sample, self.exception_raised)
        
    def join(self):
        
        threading.Thread.join(self)
        return self.channel
    
class PrintThread(threading.Thread):
    
    def __init__(self, print_channels):
        
        threading.Thread.__init__(self)
        self.red_print, self.green_print, self.blue_print = print_channels
        self.current_generation = 0
        
    def run(self):
        
        self.is_running = True
        while self.is_running:
            if self.red_print and self.green_print and self.blue_print:
                red_value = self.red_print.pop(0)
                green_value = self.green_print.pop(0)
                blue_value = self.blue_print.pop(0)
                
                mean = round((red_value + green_value + blue_value) / 3,2)
                print("Generation: {}; Best score: {}".format(self.current_generation,mean))
                
                self.current_generation+=1
                
    def stop(self):
        
        self.is_running = False
        
class DisplayThread(threading.Thread):
    
    def __init__(self, display_channels, display_sample, display_resize, target):
        
        threading.Thread.__init__(self)
        self.red_display, self.green_display, self.blue_display = display_channels
        self.display_sample = display_sample
        self.display_resize = display_resize
        self.target = target
        
    def run(self):
        
        self.pipe = []
        current_generation = 0
        aux_thread = AuxDisplayThread(self.pipe, self.target, self.display_resize)
        aux_running = False
        
        self.is_running = True
        while self.is_running:
            if self.red_display and self.green_display and self.blue_display:
                red = self.red_display.pop(0)
                green = self.green_display.pop(0)
                blue = self.blue_display.pop(0)
                
                self.pipe.append((red,green,blue,current_generation))
                
                if not aux_running:
                    aux_thread.start()
                    aux_running = True
                
                current_generation+=self.display_sample
                
        aux_thread.join()
            
    def stop(self):
        
        self.pipe.append(None)
        self.is_running = False
        
class AuxDisplayThread(threading.Thread):
    
    def __init__(self, pipe, target, display_resize):
        
        threading.Thread.__init__(self)
        self.pipe = pipe
        self.target = target
        self.display_resize = display_resize
        
    def run(self):
        
        ImageHandler.display(self.pipe,self.target, self.display_resize)