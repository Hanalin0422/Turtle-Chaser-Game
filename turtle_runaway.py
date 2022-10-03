# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser ,catch_radius=50, init_dist=400):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()
        self.runner.setx(+init_dist / 2)
        self.runner.setheading(180)

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()
        self.chaser.setx(-init_dist / 2)

        # Instantiate an another turtle for drawing
        self.drawer1 = turtle.RawTurtle(canvas)
        self.drawer1.hideturtle()
        self.drawer1.penup()
        
        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.penup()
        
        self.drawer3 = turtle.RawTurtle(canvas)
        self.drawer3.hideturtle()
        self.drawer3.penup()
        
        # 랜덤으로 생성되는 목적지
        self.goal = turtle.RawTurtle(canvas)
        self.goal.shape('classic')
        self.goal.color('black')
        self.goal.penup()
        self.goal.setx(random.randrange(-300, 300))
        self.goal.sety(random.randrange(-300, 300))
        
        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.speed(0)
        self.drawer2.penup()
        
        
    def  is_arrived(self):
        p = self.goal.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
        

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    

    def start(self, init_dist=400, ai_timer_msec=100, score = 0):

        self.ai_timer_msec = ai_timer_msec
        self.score = score
        self.start_time = time.time()
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        
 

    def step(self):
        self.runner.run_ai(self.chaser)
        self.chaser.run_ai(self.runner)
        
        if self.is_catched() == True:
            self.score = self.score - 20
            new_x=random.randint(-300, 300)
            new_y=random.randint(-300, 300)
            self.chaser.goto(new_x, new_y)
            
        
        if self.is_arrived() == False:
            pass
        else:
            new_x=random.randint(-300, 300)
            new_y=random.randint(-300, 300)
            self.goal.goto(new_x, new_y)
            
            self.score = self.score + 20
            
                   
        now = time.time() - self.start_time
        limitTime = 100 - now
        
        self.drawer1.undo()
        self.drawer1.penup()
        self.drawer1.setpos(-290, 250)
        self.drawer1.write(f'Time {limitTime:.0f}', font={'굴림', 12})
        
        self.drawer2.undo()
        self.drawer2.penup()
        self.drawer2.setpos(-290, 220)
        self.drawer2.write(f'Score {self.score}', font={'굴림', 12})
        
        if self.score < 0:
            self.drawer2.undo()
            self.drawer2.write('Score Zero!!', font={'굴림', 12})
            self.drawer3.undo()
            self.drawer3.write('Game Over', font={'굴림', 12})
            return
        elif self.score >= 100:
            self.drawer2.undo()
            self.drawer2.write('***Score is Full***', font={'굴림', 12})
            self.drawer3.undo()
            self.drawer3.write('You WIN', font={'굴림', 12})
            return
            
        
        self.drawer3.undo()
        self.drawer3.penup()
        self.drawer3.setpos(-290, 190)
        self.drawer3.write('Playing Now...', font={'굴림', 12})
        
        if limitTime <= 0:
            self.drawer3.undo()
            self.drawer3.write('Game Over', font={'굴림', 12})
            return
        
    
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()
    
    def run_ai(self, opponent):
            pass
    

class ChaseMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=30):
        super().__init__(canvas)
        self.step_move = step_move

    def run_ai(self, opponent):
        prob = random.random()
        opp_pos=opponent.pos()
        ang=self.towards(opp_pos)
        if prob <= 0.2:
            self.setheading(ang)
            self.forward(self.step_move)

if __name__ == '__main__':
    canvas = turtle.Screen()
    runner = ChaseMover(canvas)
    chaser = ManualMover(canvas)

    game = RunawayGame(canvas, runner, chaser)
    game.start()
    canvas.mainloop()