import arcade


class Player:
    def __init__(self, x, y):
        # Initialize center coordinates
        self.x = x
        self.y = y


class X(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 50

    def draw(self):
        arcade.draw_line(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, arcade.color.WHITE, 4)
        arcade.draw_line(self.x - self.size, self.y + self.size, self.x + self.size, self.y - self.size, arcade.color.WHITE, 4)


class O(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 50

    def draw(self):
        arcade.draw_circle_outline(self.x, self.y, self.radius, arcade.color.WHITE, 4)
