import moves
from pokemon import Pokemon
import random

print("=== Pokemon: Semen White Version ===\n\n")

trainer = input("Enter your name: ").strip()
if not trainer:
    trainer = "Hero"

print(f"Welcome to Pokemon, Trainer {trainer}!")

cyndaquil = Pokemon("Cyndaquil", "Fire", 75, moves.tackle, moves.ember, moves.quick_attack, None)
pidgey = Pokemon("Pidgey", "Flying", 50, moves.scratch, moves.quick_attack, moves.gust, None)

pokemon_party = [cyndaquil, pidgey]
active_pokemon = pokemon_party[0]

rattata = Pokemon("Rattata", "Normal", 50, moves.tackle, moves.quick_attack, None, None)

print(f"\nA wild {rattata} appeared!\n")

# Main Battle Loop
while (cyndaquil.is_alive() or pidgey.is_alive()) and rattata.is_alive():
    print(f"What will {active_pokemon} do?\n")
    choices = input("Choose an Action: \n 1. Attack \n 2. Switch Pokemon \n Type the number of your choice: ").strip()

    valid_turn = False

    # ==========================================
    # ACTION 1: ATTACK WITH MOVES MENU
    # ==========================================
    if choices == "1":
        # Gather slots and filter out None elements dynamically
        all_slots = [active_pokemon.firstmove, active_pokemon.secondmove, active_pokemon.thirdmove, active_pokemon.fourthmove]
        known_moves = [move for move in all_slots if move is not None]

        print(f"\nWhich move will {active_pokemon} use?\n")
        for index, move in enumerate(known_moves, start=1):
            print(f"{index}. {move.name} (Type: {move.Type}, Damage: {move.damage})")
        print(f"{len(known_moves) + 1}. Back")

        move_choice = input("Select a move by typing its number: ").strip()

        # Handle numeric index parsing safely
        if move_choice.isdigit():
            move_index = int(move_choice) - 1
            
            # Allow the player to go back to the main action choices menu
            if move_index == len(known_moves):
                continue
                
            if 0 <= move_index < len(known_moves):
                selected_move = known_moves[move_index]
                
                # Execute attack safely
                print(f"\n⚡ {active_pokemon.name} used {selected_move.name}!")
                combat_report = active_pokemon.attack(selected_move, rattata)
                print(combat_report)
                
                valid_turn = True
            else:
                print("❌ Invalid selection! Please pick a valid move number.\n")
                continue
        else:
            print("❌ Invalid input! Please enter a number.\n")
            continue

    # ==========================================
    # ACTION 2: SWITCHING PARTY MEMBERS
    # ==========================================
    elif choices == "2":
        print("\nWhich Pokemon will you switch to?\n")
        for idx, pokemon in enumerate(pokemon_party):
            if pokemon.is_alive():
                print(f"{idx + 1}. {pokemon.name} (Type: {pokemon.type}, Health: {pokemon.health}/{pokemon.max_health})")
        
        switch_pokemon = input("Select a Pokemon by typing its number: ").strip()

        try:
            switch_index = int(switch_pokemon) - 1
            if 0 <= switch_index < len(pokemon_party) and pokemon_party[switch_index].is_alive():
                if pokemon_party[switch_index] == active_pokemon:
                    print(f"❌ {active_pokemon.name} is already on the field!\n")
                    continue
                    
                active_pokemon = pokemon_party[switch_index]
                print(f"\n🔄 You switched to {active_pokemon.name}!")
                valid_turn = True  # Consumes the turn layout framework!
            else:
                print("❌ Invalid choice or Pokemon has fainted!\n")
                continue
        except ValueError:
            print("❌ Invalid input! Please enter a number.\n")
            continue
    
    else:
        print("❌ Invalid choice! Please type 1 or 2.\n")
        continue

    # ==========================================
    # ENEMY ROUND: AUTOMATED COUNTER ATTACK
    # ==========================================
    if valid_turn and rattata.is_alive() and (cyndaquil.is_alive() or pidgey.is_alive()):
        # Filter enemy valid moves safely
        enemy_slots = [rattata.firstmove, rattata.secondmove, rattata.thirdmove, rattata.fourthmove]
        enemy_known_moves = [move for move in enemy_slots if move is not None]
        
        enemy_move = random.choice(enemy_known_moves)
        print(f"\n🤖 The wild {rattata.name} retaliates and uses {enemy_move.name}!")
        
        combat_report = rattata.attack(enemy_move, active_pokemon)
        print(combat_report)

    # ==========================================
    # KO EVALUATION STATE
    # ==========================================
    if not active_pokemon.is_alive():
        print(f"\n💀 {active_pokemon.name} has fainted!")
        alive_pokemon = [pokemon for pokemon in pokemon_party if pokemon.is_alive()]
        if alive_pokemon:
            active_pokemon = alive_pokemon[0]
            print(f"🔄 You automatically sent out {active_pokemon.name} to continue the match!\n")
        else:
            print("💀 All your Pokemon have fainted! You whited out...")
            break

# ==========================================
# END GAME RESOLUTION WINDOW REPORT
# ==========================================
print(f"\n==========================================")

if (cyndaquil.is_alive() or pidgey.is_alive()) and not rattata.is_alive():
    print(f"🎉 Congratulations, Trainer {trainer}! You defeated the wild {rattata.name}!")
else:
    print(f"🏃 Trainer {trainer} has no pokemon left! He ran away to the nearest Pokemon Center to heal.")