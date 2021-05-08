class Ant:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.image = "ant.png"
        self.recent_path = []
        self.recent_path_cost = 0
        self.recent_pheromone_value = 0
