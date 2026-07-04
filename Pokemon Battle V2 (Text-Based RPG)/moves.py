import random

class Moves:
    def __init__(self, name, Type, damage) -> None:
        self.name = name
        self.Type = Type  # e.g., "Fire"
        self.damage = damage  # Base damage (mode)

    def calculate_damage(self, target_type: str) -> tuple[int, float]:
        """Calculates triangular damage, factoring in type weaknesses."""
        
        # 1. Define a simple weakness chart
        # Key: Attacking Type -> Value: List of types it is strong against
        weaknesses = {
            "Fire": ["Grass", "Ice", "Bug", "Steel"],
            "Water": ["Fire", "Ground", "Rock"],
            "Grass": ["Water", "Ground", "Rock"],
            "Normal": [] # Normal has no type advantages
        }

        # 2. Determine the multiplier
        multiplier = 1.0
        if target_type in weaknesses.get(self.Type, []):
            multiplier = 2.0  # Super effective!
            
        # 3. Apply the multiplier to our triangular bounds
        # We multiply the low, high, and mode so the whole triangle shifts up!
        low = (self.damage * 0.8) * multiplier
        high = (self.damage * 1.3) * multiplier
        mode = self.damage * multiplier       
        
        final_damage = random.triangular(low, high, mode)
        
        # Return both the damage and the multiplier so the game loop knows if it was effective!
        return round(final_damage), multiplier

# Instantiate moves
tackle = Moves("Tackle", "Normal", 10)
ember = Moves("Ember", "Fire", 15)
quick_attack = Moves("Quick Attack", "Normal", 12)
gust = Moves("Gust", "Flying", 12)
scratch = Moves("Scratch", "Normal", 10)
