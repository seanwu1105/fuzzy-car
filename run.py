import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class RunCar(QThread):

    sig_console = pyqtSignal(str)
    sig_car = pyqtSignal(tuple, float)
    sig_dists = pyqtSignal(list)

    def __init__(self, car):
        super().__init__()
        self.car = car
        self.abort = True

    @pyqtSlot()
    def run(self):
        for i in range(10):
            time.sleep(0.25)
            self.sig_console.emit(str(i))

    def stop(self):
        if self.is_alive():
            self.sig_console.emit("WARNING: User interrupts running thread.")
        self.abort = False
