from PIL import Image, ImageDraw

class Map:

    def __init__(self, filename):
        '''Reads in text file, places elevations into list, and finds highest and lowest elevations'''
        self.elevations = []
        with open(filename) as file:
            for line in file:
                self.elevations.append([int(e) for e in line.split()])
 
        self.highest_elevation = max([max(row) for row in self.elevations])
        self.lowest_elevation = min([min(row) for row in self.elevations])

    def get_elevation(self, x, y):
        '''Adjust coordinates order'''
        return self.elevations[y][x]

    def color(self, x, y): 
        return int((self.get_elevation(x, y) - self.lowest_elevation) / (self.highest_elevation - self.lowest_elevation) * 255)

class DrawMap:
    
    def __init__(self, Map, point):
        self.Map = Map
        self.picture = Image.new('RGBA', (len(self.Map.elevations[0]), len(self.Map.elevations)))
        # self.drawing = ImageDraw.Draw(self.picture)
        self.point = point

    def draw(self):
        '''Draws map'''
        for x in range(len(self.Map.elevations[0])):
            for y in range(len(self.Map.elevations)):
                self.picture.putpixel((x, y), (self.Map.color(x, y), self.Map.color(x, y), self.Map.color(x, y)))
        self.picture.save('map.png')

    # This is the part that is messed up...
    def print_path(self, point):
        '''This should plot the pathfinder points'''
        for item_point in point:
            self.picture.putpixel(item_point, (156, 226, 227))
        self.picture.save('pathfinder_map.png')
        return self.picture

class Pathfinder:

    def __init__(self, Map):
        self.Map = Map

    def jank_pathfinder(self):
        self.point = []
        cur_x = 0
        cur_y = 50
        while cur_x < len(self.Map.elevations[0]) - 1:
            possible_ys = [cur_y]
            if cur_y - 1 >= 0:
                possible_ys.append(cur_y - 1)
            if cur_y + 1 < len(self.Map.elevations):
                possible_ys.append(cur_y + 1)

            diffs = [
                abs(self.Map.elevations[poss_y][cur_x + 1] - self.Map.elevations[cur_y][cur_x])
                for poss_y in possible_ys
            ]

            min_diff = min(diffs)
            min_diff_index = diffs.index(min_diff)
            next_y = possible_ys[min_diff_index]

            cur_x += 1
            cur_y = next_y
            self.point.append((cur_x, cur_y))
        return self.point


if __name__ == '__main__':

    elevation_map = Map('elevation_small.txt')
    point = Pathfinder(elevation_map)
    draw_elevation_map = DrawMap(elevation_map, point.jank_pathfinder())
    draw_elevation_map.draw()
    draw_elevation_map.print_path(point.jank_pathfinder())
    pathfinder = Pathfinder(elevation_map)
    