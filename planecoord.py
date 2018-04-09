""" Define the line in 2D plane and its basic methods. """

from decimal import Decimal
import math

import numpy as np


class Line2D(object):
    def __init__(self, arg1, arg2, arg3=None):
        """Create a 2D-plane line.

        Args:
            arg1 (tuple or float): If the type is tuple, this is the first point
                in two-points form. Otherwise, this is the slope or the
                x-coefficient.
            arg2 (tuple or float): If the type is tuple, this is the first point
                in two-points form. Otherwise, this is the y-intercept or the
                y-coefficient.
            arg3 (float, optional): Defaults to None. If not None, arg1, arg2,
                and arg3 are the x-coefficient, y-coefficient, and constant
                repectively in general (standard) form (ax + by = c).
        """

        if arg3 is None:
            # two-points form
            if isinstance(arg1, (tuple, list)):
                arg1 = (Decimal(str(arg1[0])), Decimal(str(arg1[1])))
                arg2 = (Decimal(str(arg2[0])), Decimal(str(arg2[1])))
                # vertical line
                if arg1[0] == arg2[0]:
                    self.x_coef, self.y_coef, self.const = 1, 0, arg1[0]
                # oblique line
                else:
                    m = (arg1[1] - arg2[1]) / (arg1[0] - arg2[0])
                    c = arg1[1] - m * arg1[0]
                    self.x_coef, self.y_coef, self.const = self.si2general(
                        m, c)
            # slope-intercept form
            else:
                self.x_coef, self.y_coef, self.const = self.si2general(
                    Decimal(arg1), Decimal(arg2))
        else:
            self.x_coef, self.y_coef, self.const = Decimal(
                arg1), Decimal(arg2), Decimal(arg3)

    def y(self, x):
        return 0 if self.y_coef == 0 else (self.const - self.x_coef * x) / self.y_coef

    def x(self, y):
        return 0 if self.x_coef == 0 else (self.const - self.y_coef * y) / self.x_coef

    def intersection(self, line):
        """Get the point of intersection between two lines. May loss precision while
        calculating the result from `Decimal` to `float`.

        Args:
            line (Line2D): The 2D line to calculate with.

        Returns:
            ndarray: The point of intersection.
        """

        coefs = np.array([[float(self.x_coef), float(self.y_coef)],
                          [float(line.x_coef), float(line.y_coef)]])
        consts = np.array([float(self.const), float(line.const)])
        try:
            inter = np.linalg.solve(coefs, consts)
        except np.linalg.LinAlgError:
            # infinite or none solution
            return None
        else:
            # exactly one solution
            return inter

    def point_dist(self, pt):
        """Get the distance between a point and self.

        Args:
            pt (tuple): the target point.

        Returns:
            float: the distance between the given point and self (line).
        """
        return abs(float(self.x_coef) * pt[0]
                   + float(self.y_coef * pt[1])
                   - float(self.const)) / math.sqrt(self.x_coef ** 2
                                                    + self.y_coef ** 2)

    @staticmethod
    def si2general(slope, y_intercept):
        """Convert the parameter of slope-intercept form into the one of general
        form.

        Args:
            slope (float): the slope of the 2D line.
            y_intercept (float): the y_intercept of the 2D line.

        Returns:
            tuple: a tuple containing (x coefficient, y coefficient, constant
            term).
        """

        return slope, -1, -y_intercept


class LineSeg2D(Line2D):
    def __init__(self, arg1, arg2):
        super().__init__(arg1, arg2)
        self.pt1, self.pt2 = arg1, arg2
        self.xmax, self.xmin = max(arg1[0], arg2[0]), min(arg1[0], arg2[0])
        self.ymax, self.ymin = max(arg1[1], arg2[1]), min(arg1[1], arg2[1])

    def intersection(self, line):
        """Get the point of intersection between self (a line segment) and a
        line or line segment. May loss precision while calculating the result
        from `Decimal` to `float`.

        Args:
            line (Line2D or LineSeg2D): The 2D line or line segment to calculate
                with.

        Returns:
            ndarray: The point of intersection.

        Raises:
            TypeError: line should only be Line2D or LineSeg2D.
        """
        inter = super().intersection(line)
        if inter is None:
            return None
        if type(line) == Line2D:
            if self.pt1[0] - self.pt2[0] == 0:
                # self is vertical line segment
                if self.ymin <= inter[1] <= self.ymax:
                    return inter
            elif self.xmin <= inter[0] <= self.xmax:
                # self is oblique line
                return inter
            else:
                return None
        elif type(line) == LineSeg2D:
            if self.pt1[0] - self.pt2[0] == 0:
                # vertical line segment (self)
                if (self.ymin <= inter[1] <= self.ymax
                        and line.xmin <= inter[0] <= line.xmax):
                    return inter
            elif line.ranging_pt1[0] - line.pt2[0] == 0:
                # vertical line segment (line)
                if (line.ymin <= inter[1] <= line.ymax
                        and self.xmin <= inter[0] <= self.xmax):
                    return inter
            elif (self.xmin <= inter[0] <= self.xmax
                  and line.xmin <= inter[0] <= line.xmax):
                return inter
            else:
                return None
        else:
            raise TypeError("'line' should be a instance of Line2D or "
                            "LineSeg2D")

    def point_dist(self, pt):
        """Get the distance between a point and self.

        Args:
            pt (tuple): the target point.

        Returns:
            float: the distance between the given point and self (line segment).
        """

        seg_len = dist(self.pt1, self.pt2)
        if seg_len == 0:
            return dist(pt, self.pt1)
        t = max(0, min(1, ((pt[0] - self.pt1[0])
                           * (self.pt2[0] - self.pt1[0])
                           + (pt[1] - self.pt1[1])
                           * (self.pt2[1] - self.pt1[1]))
                       / seg_len ** 2))
        return dist(pt, (self.pt1[0] + t * (self.pt2[0] - self.pt1[0]),
                         self.pt1[1] + t * (self.pt2[1] - self.pt1[1])))


def dist(pt0, pt1):
    """Return the distance between pt0 and pt1."""
    return math.sqrt(sum(map(lambda a, b: (a - b)**2, pt0, pt1)))
