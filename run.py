import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class RunCar(QThread):

    sig_console = pyqtSignal(str)
    sig_car = pyqtSignal(tuple, float, float)
    sig_dists = pyqtSignal(tuple, list, list)

    def __init__(self, car):
        super().__init__()
        self.car = car
        self.abort = True

    @pyqtSlot()
    def run(self):
        radar_dir = ['front', 'left', 'right']
        for i in range(5):
            time.sleep(0.25)
            self.sig_console.emit(str(i))
            self.sig_car.emit(self.car.pos, self.car.angle, self.car.wheel_angle)
            self.sig_dists.emit(self.car.pos,
                                [self.car.dist_radar(d) for d in radar_dir],
                                [self.car.dist_radar(d, True) for d in radar_dir])

    def stop(self):
        if self.is_alive():
            self.sig_console.emit("WARNING: User interrupts running thread.")

        self.abort = False
