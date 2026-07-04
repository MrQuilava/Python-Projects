import random
import moves
import pokemon
import tkinter as tk
from tkinter import messagebox, simpledialog

root = tk.Tk()
root.withdraw()  # Hide main window while dialogs run

trainer_name = simpledialog.askstring("Name Entry", "What is your name trainer? ", initialvalue="Red")
if not trainer_name:
    trainer_name = "Red"

cyndaquil = pokemon.Pokemon("Cyndaquil", "Fire", 75, moves.tackle, moves.ember, moves.quick_attack, None)
pidgey = pokemon.Pokemon("Pidgey", "Flying", 50, moves.scratch, moves.quick_attack, moves.gust, None)
rattata = pokemon.Pokemon("Rattata", "Normal", 50, moves.tackle, moves.quick_attack, None, None)

pokemon_party = [cyndaquil, pidgey]
active_pokemon = pokemon_party[0]

root.deiconify()
root.title("Pokemon! Semen White Version")
root.geometry("550x550")
root.resizable(False, False)

# ==========================================
# UI HELPER FUNCTIONS & WINDOW REFRESHES
# ==========================================
def log_message(message: str) -> None:
    log_text.config(state="normal")
    log_text.insert("end", message + "\n")
    log_text.see("end")
    log_text.config(state="disabled")

def update_ui() -> None:
    active_pokemon_label.config(
        text=f"ACTIVE: {active_pokemon.name} ({active_pokemon.type})\nHP: {active_pokemon.health}/{active_pokemon.max_health}"
    )
    wild_pokemon_label.config(
        text=f"WILD: {rattata.name} ({rattata.type})\nHP: {rattata.health}/{rattata.max_health}"
    )

def end_game(status: str) -> None:
    for widget in action_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(state="disabled")
    messagebox.showinfo("Battle Finished", status)

# ==========================================
# COMBAT TURNS & GAME ENGINE
# ==========================================
def run_turn(combat_story: str) -> None:
    global active_pokemon
    
    if combat_story:
        log_message(combat_story)
    update_ui()

    if rattata.is_alive() and active_pokemon.is_alive():
        enemy_slots = [rattata.firstmove, rattata.secondmove, rattata.thirdmove, rattata.fourthmove]
        enemy_known_moves = [move for move in enemy_slots if move is not None]
        
        wild_move = random.choice(enemy_known_moves)
        wild_combat_report = rattata.attack(wild_move, active_pokemon)
        log_message(f"\n🤖 The wild {rattata.name} attacks!\n{wild_combat_report}")
    
    if not rattata.is_alive():
        log_message(f"\n🎉 The wild {rattata.name} has fainted!")
        update_ui()
        end_game("Victory! You gained 75 XP!")
        return

    if not active_pokemon.is_alive():
        log_message(f"\n💀 {active_pokemon.name} has fainted!")
        alive_pokemon = [poke for poke in pokemon_party if poke.is_alive()]
        if alive_pokemon:
            active_pokemon = alive_pokemon[0]
            log_message(f"🔄 {trainer_name} sent out {active_pokemon.name}!")
        else:
            update_ui()
            end_game(f"Game Over! {trainer_name} whited out...")
            return

    update_ui()
    show_main_menu()

# ==========================================
# MENUS & INTERACTION LOGIC
# ==========================================
def clear_action_frame() -> None:
    for widget in action_frame.winfo_children():
        widget.destroy()

def show_main_menu() -> None:
    clear_action_frame()
    
    btn_attack = tk.Button(action_frame, text="⚔️ Attack", font=("Arial", 12), width=15, height=2, command=show_moves_menu)
    btn_attack.grid(row=0, column=0, padx=20, pady=15)
    
    btn_switch = tk.Button(action_frame, text="🔄 Switch Pokemon", font=("Arial", 12), width=15, height=2, command=show_switch_menu)
    btn_switch.grid(row=0, column=1, padx=20, pady=15)

def show_moves_menu() -> None:
    clear_action_frame()
    
    all_slots = [active_pokemon.firstmove, active_pokemon.secondmove, active_pokemon.thirdmove, active_pokemon.fourthmove]
    known_moves = [move for move in all_slots if move is not None]
    
    for idx, move in enumerate(known_moves):
        r = idx // 2
        c = idx % 2
        btn = tk.Button(
            action_frame, 
            text=f"{move.name}\n(Dmg: {move.damage})", 
            font=("Arial", 10), 
            width=15, 
            height=2,
            command=lambda m=move: run_turn(active_pokemon.attack(m, rattata))
        )
        btn.grid(row=r, column=c, padx=10, pady=5)
        
    btn_back = tk.Button(action_frame, text="⬅️ Back", font=("Arial", 10), width=10, command=show_main_menu)
    btn_back.grid(row=2, column=0, columnspan=2, pady=5)

def show_switch_menu() -> None:
    clear_action_frame()
    
    # Buttons are now always "normal" (clickable) so we can display errors on click!
    for idx, pokemon_obj in enumerate(pokemon_party):
        btn = tk.Button(
            action_frame,
            text=f"{pokemon_obj.name} (HP: {pokemon_obj.health}/{pokemon_obj.max_health})",
            font=("Arial", 10),
            width=20,
            command=lambda p=pokemon_obj: execute_switch(p)
        )
        btn.pack(pady=4)
        
    btn_back = tk.Button(action_frame, text="⬅️ Back", font=("Arial", 10), command=show_main_menu)
    btn_back.pack(pady=5)

def execute_switch(chosen_pokemon) -> None:
    """Checks the chosen pokemon's conditions before performing a switch."""
    global active_pokemon
    
    # ❌ CHECK 1: Is this pokemon already battling?
    if chosen_pokemon == active_pokemon:
        log_message(f"❌ {chosen_pokemon.name} is already out on the field!")
        messagebox.showwarning("Switch Error", f"{chosen_pokemon.name} is already fighting!")
        return  # Stop execution, keep switch menu open, do not lose a turn.

    # ❌ CHECK 2: Has this pokemon fainted?
    if not chosen_pokemon.is_alive():
        log_message(f"❌ {chosen_pokemon.name} has fainted and cannot be switched in!")
        messagebox.showerror("Switch Error", f"{chosen_pokemon.name} has no energy left to battle!")
        return  # Stop execution, keep switch menu open, do not lose a turn.
        
    #  SUCCESS: Perform the actual switch
    log_message(f"\n🔄 {active_pokemon.name}, return! Go, {chosen_pokemon.name}!")
    active_pokemon = chosen_pokemon
    
    # Pass empty string into run_turn, consuming the player's turn 
    # and allowing the enemy to immediately counter-attack!
    run_turn("")

# ==========================================
# WINDOW HUD DISPLAY GRAPHICS & PACKING
# ==========================================
hud_frame = tk.Frame(root, pady=10)
hud_frame.pack()

active_pokemon_label = tk.Label(hud_frame, font=("Arial", 12, "bold"), fg="blue", justify="left")
active_pokemon_label.pack(side="left", padx=30)

wild_pokemon_label = tk.Label(hud_frame, font=("Arial", 12, "bold"), fg="red", justify="right")
wild_pokemon_label.pack(side="right", padx=30)

log_text = tk.Text(root, font=("Courier", 10), state="disabled", wrap="word", bg="#f4f4f4", height=15)
log_text.pack(padx=15, pady=10, fill="both", expand=True)

action_frame = tk.Frame(root, height=120)
action_frame.pack(pady=10)

log_message(f"A wild {rattata.name} jumped out of the tall grass!\nWhat will {trainer_name} do?")
update_ui()
show_main_menu()

root.mainloop()