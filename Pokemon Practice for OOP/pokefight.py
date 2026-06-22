from pokemon import YourPokemon, WildPokemon
from move import tackle, ember

Cyndaquil = YourPokemon("Cyndaquil", "Fire", 100)
Cyndaquil.switch_move(ember)
Chikorita = WildPokemon("Chikorita", "Grass", 100, tackle)

while True:
    Cyndaquil.attack(Chikorita)
    if Chikorita.health <= 0:
        print(f"{Chikorita.name} fainted!")
        break
    Chikorita.attack(Cyndaquil)
    if Cyndaquil.health <= 0:
        print(f"{Cyndaquil.name} fainted!")
        break
    input()

