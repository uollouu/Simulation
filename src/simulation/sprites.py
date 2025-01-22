from colorama import Back, Fore

from simulation.entity import *

sprites_table = {
    type(None): Back.BLACK + Fore.BLACK + " E " + Fore.RESET + Back.RESET,
    Predator  : Back.BLUE + " P " + Back.RESET,
    Herbivore : Back.RED + " H " + Back.RESET,
    Grass     : Back.GREEN + " G " + Back.RESET,
    Rock      : Back.WHITE + Fore.WHITE + " R " + Fore.RESET + Back.RESET,
    Tree      : Back.LIGHTGREEN_EX + Fore.LIGHTGREEN_EX + " T " + Fore.RESET+ Back.RESET,
}

def get_sprite(entity) -> str:
    return sprites_table[type(entity)]