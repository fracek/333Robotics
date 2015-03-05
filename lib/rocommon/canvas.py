import numpy as np


class Canvas:

    def __init__(self, map_size=546):
        self.map_size = map_size  # in cm
        self.canvas_size = 768    # in pixels
        self.margin = 0.05 * map_size
        self.scale = self.canvas_size / (map_size + 2 * self.margin)

    def draw_line(self, line):
        x1 = self._screenX(line[0])
        y1 = self._screenY(line[1])
        x2 = self._screenX(line[2])
        y2 = self._screenY(line[3])
        print "drawLine:" + str((x1, y1, x2, y2))

    def draw_particles(self, data, w=[]):
        display = [(self._screenX(d[0]), self._screenY(d[1])) + tuple(np.concatenate((d[2:], w)))
                for d in data]
        print "drawParticles:" + str(display)

    def _screenX(self, x):
        return (x + self.margin) * self.scale

    def _screenY(self, y):
        return (self.map_size + self.margin - y) * self.scale
