import time

from PySide2.QtCore import QThread, Signal, Slot


class RunCar(QThread):
    sig_console = Signal(str)
    sig_car = Signal(list, float, float)
    sig_car_collided = Signal()
    sig_dists = Signal(list, list, list)
    sig_results = Signal(list)

    def __init__(self, car, fuzzy_system, ending_area=None, fps=20):
        super().__init__()
        self.car = car
        self.fuzzy_system = fuzzy_system
        self.abort = False
        self.ending_lt = ending_area[0]
        self.ending_rb = ending_area[1]
        self.waiting_time = 1 / fps

    @Slot()
    def run(self):
        results = list()
        radar_dir = ['front', 'left', 'right']
        while True:
            if self.abort:
                break
            time.sleep(self.waiting_time)
            radars = tuple(self.car.dist(d) for d in radar_dir)
            self.sig_car.emit(self.car.pos, self.car.angle,
                              self.car.wheel_angle)
            self.sig_dists.emit(self.car.pos, *map(list, zip(*radars)))

            if (self.ending_lt[0] <= self.car.pos[0] <= self.ending_rb[0]
                    and self.ending_lt[1] >= self.car.pos[1] >= self.ending_rb[1]):
                self.sig_console.emit("Note: Car has arrived at the ending "
                                      "area.")
                self.abort = True
                break

            if self.car.is_collided:
                self.sig_console.emit("Note: Car has collided.")
                self.sig_car_collided.emit()
                self.abort = True
                break

            dists = list(zip(*radars))[1]
            try:
                dists = list(map(float, dists))
            except ValueError:
                self.abort = True
                self.sig_console.emit("Error: Cannot input the fuzzy system "
                                      "since the distance type error.")
                break

            next_wheel_angle = self.fuzzy_system.singleton_result(
                dists[0], dists[1] - dists[2])

            results.append({
                'x': self.car.pos[0],
                'y': self.car.pos[1],
                'front_dist': radars[0][1],
                'right_dist': radars[2][1],
                'left_dist': radars[1][1],
                'wheel_angle': next_wheel_angle
            })

            self.car.move(next_wheel_angle)
        self.sig_results.emit(results)

    @Slot()
    def stop(self):
        if self.isRunning():
            self.sig_console.emit("WARNING: User interrupts running thread.")

        self.abort = True
