from move import Moves, tackle

class Pokemon:
    race = "Pokemon"

    def __init__(self, name, Type, health) -> None:
        self.name = name
        self.Type = Type
        self.health = health
        self.maxhealth = health

        self.move = tackle #default move

    def attack(self, target) -> None:
        target.health -= self.move.damage
        target.health = max(target.health, 0)  # Ensure health doesn't go below 0
        print(f"{self.name} used {self.move.name}!")
        print(f"{target.name} took {self.move.damage} damage!")

        if self.move.Type == "Fire" and target.Type == "Grass":
            target.health -= self.move.damage * 0.5
            print("It's super effective!")
        print(f"{target.name}'s health: {target.health}/{target.maxhealth}")

class YourPokemon(Pokemon):
    def __init__(self, name, Type, health) -> None:
        super().__init__(name, Type, health)
        self.default_move = self.move

    def switch_move(self, move) -> None:
        self.move = move
        print(f"{self.name} used {move.name}!")


class WildPokemon(Pokemon):
    def __init__(self, name, Type, health, move) -> None:
        super().__init__(name, Type, health)
        self.default_move = move


    