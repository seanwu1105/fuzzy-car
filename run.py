import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class RunCar(QThread):

    sig_console = pyqtSignal(str)
    sig_car = pyqtSignal(list, float, float)
    sig_dists = pyqtSignal(list, list, list)

    def __init__(self, car, fuzzy_system):
        super().__init__()
        self.car = car
        self.fuzzy_system = fuzzy_system
        self.abort = False

    @pyqtSlot()
    def run(self):
        radar_dir = ['front', 'left', 'right']
        for i in range(20):
            if self.abort:
                break
            time.sleep(0.25)
            radars = tuple(self.car.dist(d) for d in radar_dir)
            self.sig_car.emit(self.car.pos, self.car.angle,
                              self.car.wheel_angle)
            self.sig_dists.emit(self.car.pos, *map(list, zip(*radars)))

            dists = list(zip(*radars))[1]
            try:
                dists = list(map(float, dists))
            except ValueError:
                self.abort = True
                self.sig_console.emit("Error: Cannot input the fuzzy system "
                                      "since the distance type error.")
                break

            self.car.move(self.fuzzy_system.singleton_result(dists[0], dists[1] - dists[2]))

    def stop(self):
        if self.is_alive():
            self.sig_console.emit("WARNING: User interrupts running thread.")

        self.abort = True
