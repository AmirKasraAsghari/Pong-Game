from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

# Updates position of the ball = vleocity (vector) + current position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class paddle(Widget):
    score = NumericProperty(0)

    def collide_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.2


# update - moving the ball by by calling move() and others
class pongGame(Widget):

    ball = ObjectProperty(None)
    player_1 = ObjectProperty(None)
    player_2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        # bouncing top and bottom
        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1

        # bouncing off of the left and increasing the score
        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player_2.score += 1
        # bounsing of the right and increasing the score
        if self.ball.x > self.width - 50:
            self.ball.velocity_x *= -1
            self.player_1.score += 1

        self.player_1.collide_ball(self.ball)
        self.player_2.collide_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 4:
            self.player_1.center_y = touch.y
        if touch.x > self.width * 3/4:
            self.player_2.center_y = touch.y


class pongapp(App):

    def build(self):
        game = pongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


pongapp().run()
