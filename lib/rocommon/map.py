from canvas import Canvas
import ast
import os


class Map:

    def __init__(self, filename):
        self.walls = []
        self.read_from_file(filename)

    def add_wall(self, wall):
        self.walls.append(wall)

    def clear(self):
        self.walls = []

    def _parse_wall_line(self, s):
        try:
            wall = ast.literal_eval(s)
            if type(wall) == tuple and len(wall) == 4:
                return wall
        except (SyntaxError, ValueError) as _:
            pass
        return None

    def read_from_file(self, filename):
        self.clear()
        with open(filename, 'r') as f:
            for line in f:
                wall = self._parse_wall_line(line)
                if wall:
                    self.add_wall(wall)
                else:
                    print('Error reading {}'.format(line))

    def draw(self):
        canvas = Canvas()
        for wall in self.walls:
            canvas.draw_line(wall)


class LabMap(Map):

    def __init__(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        Map.__init__(self, cur_dir + '/maps/lab.txt')
