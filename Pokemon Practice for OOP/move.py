class Moves:
    def __init__(self, name, Type, damage) -> None:
        self.name = name
        self.Type = Type
        self.damage = damage

tackle = Moves("tackle", "Normal", 10)

ember = Moves("ember", "Fire", 15)
