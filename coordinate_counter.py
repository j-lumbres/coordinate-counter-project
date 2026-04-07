class CoordinateCounter:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.grid = []

        for row_index in range(height):
            current_row = []

            for column_index in range(width):
                current_row.append(0)

            self.grid.append(current_row)

    def update(self, x: int, y: int):
        if x >= 0 and x < self.width:
            
            if y >= 0 and y < self.height:
                
                self.grid[y][x] = self.grid[y][x] + 1
            
            else:
                print("Y coordinate is outside the grid.")

        else:
            print("X coordinate is outside the grid.")