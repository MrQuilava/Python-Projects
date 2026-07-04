import random
import moves

class Pokemon:
    race = "Pokemon"

    def __init__(self, name, type, health, firstmove, secondmove, thirdmove, fourthmove) -> None:
        self.name = name
        self.type = type
        self.max_health = health
        self.health = health
        self.firstmove = firstmove
        self.secondmove = secondmove
        self.thirdmove = thirdmove
        self.fourthmove = fourthmove
    
    def __str__(self) -> str:
        """Tells Python to automatically use the Pokemon's name when printed."""
        return self.name
        
    def is_alive(self) -> bool:
        return self.health > 0
    
    def attack(self, move, target_pokemon) -> str:
        """Calculates damage and processes the target's reaction."""
        # 1. Get damage and multiplier from the move
        inflicted_damage, multiplier = move.calculate_damage(target_pokemon.type)
        
        # 2. Apply damage and CATCH the returned string report!
        report = target_pokemon.take_damage(inflicted_damage)
        
        # 3. Create the initial move text
        combat = f"💥 {self.name} used {move.name}!"
        if multiplier == 2.0:
            combat += "\n✨ It's super effective!"
            
        # 4. Glue them together. (This is where it crashes if 'report' is None)
        return combat + "\n" + report

    def take_damage(self, damage: int) -> str:
        """Deducts health and RETURNS a damage report string."""
        self.health -= damage
        self.health = max(0, self.health)
        
        # ❌ DO NOT USE print() HERE! 
        #  MUST USE 'return' so it sends text back up to the attack function!
        return f"🤕 {self.name} took {damage} damage!\n❤️ HP: {self.health}/{self.max_health}"



