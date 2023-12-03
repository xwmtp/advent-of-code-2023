class Grid2D:

    def __init__(self, rows):
        self.grid = rows

    def size(self):
        if len(self.grid) > 0:
            return len(self.grid[0]), len(self.grid)
        else:
            return 0, 0

    def get(self, x, y):
        return self.grid[y][x]

    def set(self, x, y, to):
        self.grid[y][x] = to

    def dimensions(self):
        return {
            'x': {'min': 0, 'max': len(self.grid[0]) - 1},
            'y': {'min': 0, 'max': len(self.grid) - 1}
        }

    # includes diagonals
    def adjacent_coords(self, x, y):
        adjacents = set()
        for x_diff in [-1, 1]:
            for y_diff in [-1, 1]:
                adj_x = x + x_diff
                adj_y = y + y_diff

                adj_x_in_range = 0 <= adj_x < self.size()[0]
                adj_y_in_range = 0 <= adj_y < self.size()[1]

                if adj_x_in_range:
                    adjacents.add((adj_x, y))
                if adj_y_in_range:
                    adjacents.add((x, adj_y))
                if adj_x_in_range and adj_y_in_range:
                    adjacents.add((adj_x, adj_y))

        if (x, y) in adjacents:
            adjacents.remove((x, y))
        return adjacents

    # includes diagonals
    def adjacent_values(self, x, y):
        coords = self.adjacent_coords(x, y)
        return [self.get(x, y) for x, y in coords]

    def __str__(self):
        return '\n'.join([''.join(str(r) for r in row) for row in self.grid])

    def copy(self):
        return Grid2D([row.copy() for row in self.grid])
