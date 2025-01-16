from multiprocessing import Process
import time


from map import *
from entity import *
from vector2 import *
from renderer import *
from consts import *
from actions import *








class Simulation:

    def __init__(self, map_size=DEFAULT_MAP_SIZE):
        self.map = Map(map_size)
        self.renderer = Renderer(self.map)
        self.timer = 0
        self.is_inited = False

        self.init_actions = [
            AddRocks(self.map),
            AddTrees(self.map),
            AddGrass(self.map),
            AddPredators(self.map),
            AddHerbivores(self.map)
        ]
        self.turn_actions = [
            RunCreatures(self.map),
            HitAll(self.map),
            GrassAddOptionally(self.map),
            HerbivoresAddOptionally(self.map)
        ]

    @staticmethod
    def act(actions_):
        for action in actions_:
            action.perform()

    def init(self):
        self.act(self.init_actions)

    def next_turn(self):
        self.act(self.turn_actions)

        self.renderer.display()
        self.timer+=1

    def start_simulation(self):
        self.init()
        while True:
            try:
                self.next_turn()
                time.sleep(TURNS_CD)
            except KeyboardInterrupt:
                break




def main():
    simulation = Simulation()
    simulation.start_simulation()




if __name__ == "__main__":
    main()


