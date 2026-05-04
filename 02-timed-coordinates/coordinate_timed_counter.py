class CoordinateTimedCounter:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.reset()

    def update(self, x: int, y: int, t: int):
        if x >= 0 and x < self.width:
            
            if y >= 0 and y < self.height:
                
                self.grid[y][x] = self.grid[y][x] + 1
            
            else:
                print("Y coordinate is outside the grid.")

        else:
            print("X coordinate is outside the grid.")

    def reset(self):
        self.grid = []

        for row_index in range(self.height):
            current_row = []
            for column_index in range(self.width):
                current_row.append(0)
            self.grid.append(current_row)
    
    def export(self):
        grid_copy = []

        for row in self.grid:
            row_copy = []
            for value in row:
                row_copy.append(value)
            grid_copy.append(row_copy)
            
        return grid_copy