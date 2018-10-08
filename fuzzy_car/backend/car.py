"""Define the `Car` class in the simulator."""

import math

import numpy as np

from .planecoord import Line2D, LineSeg2D

np.set_printoptions(suppress=True)


class Car(object):
    def __init__(self, pos, angle, radius, wall_points):
        """The car controlled by fuzzy system.

        Args:
            pos (list): (x, y) position of the car.
            angle (float): the angle of the car in degree and always in
                [0, 360).
            radius (int): the size (radius) of the car.
            wall_points (list): a list with all the edge points of the map.
        """

        self.pos = list(pos)
        self.angle = angle % 360
        self.radius = radius
        self.wheel_angle = 0
        self.walls = []
        for idx in range(len(wall_points) - 1):
            self.walls.append(
                LineSeg2D(wall_points[idx], wall_points[idx + 1]))

    def move(self, wheel_angle):
        """Make the car move to mext position according to the current wheel
        angle.

        Args:
            wheel_angle (float): the current wheel angle which should be in
                [-40, 40].
        """

        self.wheel_angle = max(min(wheel_angle, 40), -40)
        wheel_angle = math.radians(self.wheel_angle)
        car_angle = math.radians(self.angle)

        self.pos[0] += math.cos(car_angle + wheel_angle) + \
            math.sin(wheel_angle) * math.sin(car_angle)
        self.pos[1] += math.sin(car_angle + wheel_angle) - \
            math.sin(wheel_angle) * math.cos(car_angle)
        self.angle = (
            self.angle - math.degrees(math.asin(
                math.sin(wheel_angle) / self.radius))) % 360

    def dist(self, direction):
        """Get the distance between car and any closest wall.

        Args:
            direction (string): Can take 'front', 'left' and 'right', determine
                which distance of radar.

        Returns:
            tuple: (intersection, distance).
        """

        if direction == 'front':
            degree = self.angle % 360
        elif direction == 'left':
            degree = (self.angle + 45) % 360
        else:
            degree = (self.angle - 45) % 360

        radar = Line2D(self.pos, (self.pos[0] + math.cos(math.radians(degree)),
                                  self.pos[1] + math.sin(math.radians(degree))))
        intersections = []
        for wall in self.walls:
            inter = wall.intersection(radar)
            if inter is not None:
                if (0 < degree < 180 and inter[1] > self.pos[1]
                        or 180 < degree < 360 and inter[1] < self.pos[1]
                        or (90 > degree >= 0 or 360 > degree > 270) and inter[0] > self.pos[0]
                        or 90 < degree < 270 and inter[0] < self.pos[0]):
                    intersections.append(inter)

        if not intersections:
            return (None, '--')
        return (min(intersections, key=lambda item: dist(self.pos, item)),
                min(dist(self.pos, i) for i in intersections))

    @property
    def is_collided(self):
        """Check the car if it is collided against any walls or not.

        Returns:
            boolean: if the car is collided.
        """

        for wall in self.walls:
            if wall.point_dist(self.pos) <= self.radius:
                return True
        return False


def dist(pt0, pt1):
    """Return the distance between pt0 and pt1."""
    return math.sqrt(sum(map(lambda a, b: (a - b)**2, pt0, pt1)))
