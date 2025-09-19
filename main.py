from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)

            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        max = 10
        vel = Vector(*self.velocity)
        if vel.length() > max:
            vel = vel.normalize() * max
        self.velocity = vel.x, vel.y
        
        self.prev_pos = self.pos
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    

    
    def serve_ball(self, vel=(randint(-8,8),0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        #updat paddle bounce (doesnt work)
        #if (self.ball.prev_pos[0] + self.ball.width < self.player1.right and 
        #    self.ball.x + self.ball.width >= self.player1.x and
        #    self.ball.top >= self.player1.y and
        #    self.ball.y <= self.player1.top):
        #        self.player1.bounce_ball(self.ball)

        #if (self.ball.prev_pos[0] + self.ball.width < self.player1.right and 
        #    self.ball.x + self.ball.width >= self.player2.x and
        #    self.ball.top >= self.player2.y and
        #    self.ball.y <= self.player2.top):
        #        self.player2.bounce_ball(self.ball)
        
        
        #"ai" for second paddle
        self.enemy_paddle(dt)
        
        #bounce ball off of top
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        #bounce ball off of sides
        #if (self.ball.x < 0) or (self.ball.right > self.width):
         #   self.ball.velocity_x *= -1
        
        if self.ball.x < self.x:
            self.player2.score +=1
            self.serve_ball(vel=(4,0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        #if touch.x < self.width/3:
            self.player1.center_y = touch.y
        
        #controll for second paddle
        #if touch.x > self.width - self.width/3:
            #self.player2.center_y = touch.y

    def enemy_paddle(self, dt):
        if self.ball.y > self.player2.center_y:
            self.player2.center_y += min(self.player2.height/2, self.ball.y - self.player2.center_y)
        if self.ball.y < self.player2.center_y:
            self.player2.center_y -= min(self.player2.height/2, self.player2.center_y - self.ball.y)

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        
        return game
    
if __name__ == '__main__':
    PongApp().run()