from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse
from random import randint

# Optional: set a fixed window size for testing
Window.size = (400, 600)


class Ball(Widget):
    velocity_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.size = (30, 30)
        with self.canvas:
            Color(1, 0, 0)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics_pos)

    def update_graphics_pos(self, *args):
        self.ellipse.pos = self.pos

    def move(self):
        self.y += self.velocity_y


class Paddle(Widget):
    def __init__(self, **kwargs):
        super(Paddle, self).__init__(**kwargs)
        self.size = (100, 20)
        with self.canvas:
            Color(0.2, 0.6, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics_pos)

    def update_graphics_pos(self, *args):
        self.rect.pos = self.pos

    def move_left(self):
        if self.x > 0:
            self.x -= 20

    def move_right(self):
        if self.x + self.width < Window.width:
            self.x += 20


class Game(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        self.ball = Ball()
        self.add_widget(self.ball)

        self.paddle = Paddle()
        self.add_widget(self.paddle)

        self.label = Label(text="Score: 0", font_size=24, pos=(10, Window.height - 40))
        self.add_widget(self.label)

        self.paddle.pos = (Window.width / 2 - 50, 10)
        self.spawn_ball()

        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_key_down(self, *args):
        key = args[1]
        if key == 276:  # Left arrow
            self.paddle.move_left()
        elif key == 275:  # Right arrow
            self.paddle.move_right()

    def spawn_ball(self):
        x_pos = randint(0, int(Window.width - self.ball.width))
        self.ball.center_x = x_pos
        self.ball.y = Window.height
        self.ball.velocity_y = -5

    def update(self, dt):
        self.ball.move()

        if self.ball.y <= 0:
            self.spawn_ball()

        if self.ball.collide_widget(self.paddle):
            self.score += 1
            self.label.text = f"Score: {self.score}"
            self.spawn_ball()


class CatchTheBallApp(App):
    def build(self):
        return Game()


if __name__ == '__main__':
    CatchTheBallApp().run()
