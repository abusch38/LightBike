##Light Bike game based on tkinter

import time
import sys
from tkinter import *

class Game (object):
    global both_trails
    
    def __init__(self):
        #Set up the canvas
        self.tk = Tk()
        self.tk.title("Light Bike")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=700, height=600, bd=0, highlightthickness=0, bg = 'white')
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.pack()
        self.tk.update()

        #set both scores to 0
        self.bike1_score = 0
        self.bike2_score = 0

        #Put the text on the screen
        self.width_variable = self.canvas_width-100
        self.s1 = self.canvas.create_text(100, 25, text= self.bike1_score, fill='red', font ="Arial 16")
        self.s2 = self.canvas.create_text(600, 25, text= self.bike2_score, fill='blue', font ="Arial 16")

    def play_again(self):
        global both_trails

        #gets rid of the onscreen buttons
        self.button_quit.destroy()
        self.button_again.destroy()

        #resets the bikes
        Bike1.new_game(self)
        Bike2.new_game(self)

        #resets the bike trails
        both_trails = []
        
        #starts the game over again
        self.mainloop()
            
    def crashed(self):
        #this program is run every time a bike crashes.
        global both_trails

        frame = Frame(self.tk)
        frame.pack()
        
        self.button_quit = Button(frame, text="QUIT", bg="green", command=quit)
        self.button_quit.pack(side=LEFT)
        self.button_again = Button(frame,text="PLAY AGAIN", bg = 'green', command=self.play_again)
        self.button_again.pack(side=LEFT)

        #Uncomment this option for playing again via the shell. 
        '''
        play_again = input("Would you like to play again? Y/N: ")
        
        if play_again == "Y" or play_again =="y":
            print("Okay, here we go!")
            #reseting the bikes
            
            Bike1.new_game(self)
            Bike2.new_game(self)
            both_trails = []
            
            self.mainloop()
            
        elif play_again == "N" or play_again=="n":
            print("Thanks for playing! See you soon.")
            self.tk.destroy()
        else:
            print("Please enter either the letter 'Y' or the letter 'N'.")
            #run the crashed() program again.
            self.crashed()
            '''
        
    def score(self):
        #Develop a way to keep score between the light bikes.

        if Bike1.crash==True:
            self.canvas.delete(self.s2)
            self.bike2_score = self.bike2_score + 1
            self.s2 = self.canvas.create_text(600, 25, text= self.bike2_score, fill='blue', font ="Arial 16")
            print("Player 1 crashed! \n Player 2 wins!")
        if Bike2.crash==True:
            self.canvas.delete(self.s1)
            self.bike1_score = self.bike1_score + 1
            self.s1 = self.canvas.create_text(100, 25, text= self.bike1_score, fill='red', font ="Arial 16")
            print("Player 2 crashed! \n Player 1 wins!")
 
    def mainloop(self):
        #The 'condition' is True until a bike crashes. Then it is set to false.
        condition = True
        print("starting mainloop()")

        while condition:
            Bike1.MoveBike()
            Bike2.MoveBike()
            Bike1.checkhit()
            Bike2.checkhit()
           
            #checks to see if the Bike has crashed. If it has, end the while loop.
            if Bike1.crash == True or Bike2.crash == True:
                condition = False
                self.score()

            #Have tkinter update the canvas    
            self.tk.update_idletasks()
            self.tk.update()
            #Controls the speed at which the bikes move, i.e. it slows down the while loop. 
            time.sleep(0.05)

        #when a bike crashes, run this program
        self.crashed()
        
class Bike (object):
    global both_trails

    #define the bike class. 
    def __init__(self,game,color):
        self.canvas = game.canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.color = color
        self.id = game.canvas.create_rectangle(0,0,5,5, fill=color, outline="")
        self.canvas.move(self.id, 100, 200)
        self.canvas.create_text(100, 10, text="Player 1: ", fill=self.color, font ="Arial 12")
        self.x = 0
        self.y = 0
        self.canvas.bind_all('<KeyPress-a>', self.turn_left)
        self.canvas.bind_all('<KeyPress-d>', self.turn_right)
        self.canvas.bind_all('<KeyPress-w>', self.turn_up)
        self.canvas.bind_all('<KeyPress-s>', self.turn_down)
        self.direction = ""
        
        self.trail = []
        self.crash = False
        self.started = False

    #turning the bike. 
    def turn_left(self, evt):
        if self.direction == 'right':
            pass
        else:
            self.x = -5
            self.y= 0
            self.direction = "left"
            self.started = True

    def turn_right(self, evt):
        if self.direction == 'left':
            pass
        else:
            self.x = 5
            self.y= 0
            self.direction = "right"
            self.started = True

    def turn_up(self, evt):
        if self.direction == 'down':
            pass
        else:
            self.y = -5
            self.x = 0
            self.direction = "up"
            self.started = True

    def turn_down(self, evt):
        if self.direction == 'up':
            pass
        else:
            self.y = 5
            self.x = 0
            self.direction = "down"
            self.started = True

    def check_position(self):
        #this function is for the sole purpose of debugging
        #prints the Bike's tkinter canvas id
        print (self.id)
        #prints the Bike's coordinates
        print(self.canvas.coords(self.id))

    def MoveBike(self):
        global both_trails
        #get the position of the bike
        pos = self.canvas.coords(self.id)
        #put the bike position into an array which keeps track of all bikes' previous positions
        both_trails.append(self.canvas.coords(self.id))
        #create a rectangle in front of the bike based on direction it's moving
        self.id = game.canvas.create_rectangle(pos[0]+self.x, pos[1]+self.y, pos[2]+self.x, pos[3]+self.y,fill=self.color, outline="")
    
    def checkhit(self):
        global both_trails
        pos = self.canvas.coords(self.id)
        
        if pos[1] <= 0:
            self.y = 0
            #id = canvas.create_text(self.x, self.y, font = 'helvetica', color = 'grey' )
            self.crash = True
            
        if pos[3] >= self.canvas_height:
            self.y = 0
            self.crash = True
            
        if pos[0] <= 0:
            self.x = 0
            self.crash = True
            
        if pos[2] >= self.canvas_width:
            self.x= 0
            self.crash = True
            
        if self.started == True:           
            for array in both_trails:
                if pos == array:
                    self.crash = True

    
    def new_game(self, game):
        #this resets the bike if the user wants to play again. 
        self.canvas.delete('all')
        self.canvas = game.canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.color = 'red'
        self.id = game.canvas.create_rectangle(0,0,5,5, fill=self.color, outline="")
        self.canvas.move(self.id, 100, 200)
        self.canvas.create_text(100, 10, text="Player 1: ", fill=self.color, font ="Arial 12")
        game.s1 = self.canvas.create_text(100, 25, text= game.bike1_score, fill='red', font ="Arial 16")
        self.x = 0
        self.y = 0
        self.canvas.bind_all('<KeyPress-a>', self.turn_left)
        self.canvas.bind_all('<KeyPress-d>', self.turn_right)
        self.canvas.bind_all('<KeyPress-w>', self.turn_up)
        self.canvas.bind_all('<KeyPress-s>', self.turn_down)
        self.direction = ""
        self.trail = []
        self.crash = False
        self.started = False

class Bike2(Bike):
    
    def __init__(self, game, color):
        #sets up the bike.
        self.canvas = game.canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.color = color
        self.id = game.canvas.create_rectangle(0,0,5,5, fill=color, outline="")
        self.canvas.move(self.id, self.canvas_width-100, 200)
        self.canvas.create_text(self.canvas_width-100, 10, text="Player 2: ", fill=self.color, font ="Arial 12")
        self.x = 0
        self.y = 0
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)
        self.direction = ""
        self.trail = []
        self.crash = False
        self.started = False

    def new_game(self, game):
        #this resets the bike if the user wants to play again. 
        self.canvas = game.canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.color = 'blue'
        self.id = game.canvas.create_rectangle(0,0,5,5, fill=self.color, outline="")
        self.canvas.move(self.id, self.canvas_width-100, 200)
        self.canvas.create_text(self.canvas_width-100, 10, text="Player 2: ", fill=self.color, font ="Arial 12")
        game.s2 = self.canvas.create_text(self.canvas_width-100, 25, text=game.bike2_score, fill='blue', font ="Arial 16")
        self.x = 0
        self.y = 0
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)
        self.direction = ""
        self.trail = []
        self.crash = False
        self.started = False

#this is the array which holds all the trail information for both bikes. 
both_trails = []

#declare the game class
game = Game()           

#declare the Bike objects
Bike1 = Bike(game, 'Red')
Bike2 = Bike2(game, 'Blue')

#run the game
game.mainloop()



