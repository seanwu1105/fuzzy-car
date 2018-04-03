class Car(object):
    def __init__(self, pos, angle, radius, walls):
        self.pos = pos
        self.angle = angle
        self.radius = radius
        self.walls = walls
        self.wheel_angle = 0

    def move(self):
        pass

    def front_dist(self):
        pass

    def left_dist(self):
        pass

    def right_dist(self):
        pass
