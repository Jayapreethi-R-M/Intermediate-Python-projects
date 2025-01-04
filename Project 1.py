# initialize and main game loop

def main_game(game_info, map_data, npc):
    c_loc = game_info['start']
    inv = []
    disc_path = {}
    disc_obj = {}
    talk2_to_npc = {}

    print(f"Welcome to {game_info['name']}!")
    print(f"Goal: {game_info['goal']}")

    while True:
        print(f"\nYou are {map_data[c_loc]['desc']}")
        show_obj(c_loc, map_data, disc_obj)
        show_npc(c_loc, npc)

        cmd = input("What next? ").strip().lower()
        if cmd == 'exit':
            print("Thanks for playing!")
            break
        elif cmd.startswith('move '):
            dir = cmd.split()[1]
            c_loc = move(c_loc, dir, map_data, game_info)
        elif cmd == 'inv':
            print(f"Inventory: {inv}")
        elif cmd == 'goal':
            print(f"Goal: {game_info['goal']}")
        elif cmd.startswith('take '):
            take_obj(c_loc, cmd.split()[1], inv, map_data, disc_obj)
        elif cmd.startswith('drop '):
            drop_obj(c_loc, cmd.split()[1], inv, map_data)
        elif cmd == 'search':
            search_loc(c_loc, map_data, disc_path, disc_obj)
        elif cmd.startswith('talk '):
            npc_name = cmd.split()[1]
            talk_to_npc(c_loc, npc_name, npc, talk2_to_npc)
        else:
            print("Invalid command. Please use valid player commands.")

        if check_win_condition(game_info, map_data, inv):
            print("Congratulations! You've won the game!")
            break

# search location for hidden object or path

def search_loc(c_loc, map_data, disc_path, disc_obj):
    if 'hiddenobj' in map_data[c_loc] and c_loc not in disc_obj:
        hidden_obj = map_data[c_loc]['hiddenobj']
        print(f"You found a {hidden_obj}!")
        map_data[c_loc].setdefault('obj', []).append(hidden_obj)
        disc_obj[c_loc] = hidden_obj
        del map_data[c_loc]['hiddenobj']

    if 'hiddenpath' in map_data[c_loc] and c_loc not in disc_path:
        print(f"You found a hidden path!")
        disc_path[c_loc] = map_data[c_loc]['hiddenpath']

# movement and override

def move(c_loc, dir, map_data, game_info):
    x_size = game_info['xsize']
    y_size = game_info['ysize']

    if f'r_{dir}' in map_data[c_loc]:
        return map_data[c_loc][f'r_{dir}']

    c_row = (c_loc - 1) // x_size
    c_col = (c_loc - 1) % x_size

    new_row = c_row
    new_col = c_col

    if dir == "north":
        new_row = c_row - 1
    elif dir == "south":
        new_row = c_row + 1
    elif dir == "east":
        new_col = c_col + 1
    elif dir == "west":
        new_col = c_col - 1
    elif dir == "path" and 'hiddenpath' in map_data[c_loc]:
        return map_data[c_loc]['hiddenpath']

    new_row = (new_row + y_size) % y_size
    new_col = (new_col + x_size) % x_size
    n_loc = new_row * x_size + new_col + 1

    return n_loc

# show object at the location

def show_obj(c_loc, map_data, disc_obj):
    if 'obj' in map_data[c_loc]:
        if map_data[c_loc]['obj']:
            print(f"There is {', '.join(map_data[c_loc]['obj'])} here.")

# put the object into inv

def take_obj(c_loc, obj, inv, map_data, disc_obj):
    if obj in map_data[c_loc].get('obj', []):
        inv.append(obj)
        map_data[c_loc]['obj'].remove(obj)
        print(f"You took the {obj}.")
    elif c_loc in disc_obj and obj == map_data[c_loc].get('hiddenobj', ''):
        inv.append(obj)
        del disc_obj[c_loc]
    else:
        print(f"That object is not here.")

# drop the object

def drop_obj(c_loc, obj, inv, map_data):
    if obj in inv:
        inv.remove(obj)
        map_data[c_loc].setdefault('obj', []).append(obj)
    else:
        print(f"You don't have {obj} in your inventory.")

# check for winning condition and end game loop

def check_win_condition(game_info, map_data, inv):
    goal_loc = game_info['goalloc']
    goal_obj = game_info['goalobj']

    if goal_obj in map_data[goal_loc].get('obj', []):
        return True
    return False

# advanced functions - talk to the npc keep track of the conversation

def talk_to_npc(c_loc, npc_name, npc, talk2_to_npc):
    npc_name = npc_name.capitalize()

    if npc_name in npc and npc[npc_name]['loc'] == c_loc:
        if npc_name not in talk2_to_npc:
            print(npc[npc_name]['first_talk'])
            talk2_to_npc[npc_name] = True
        else:
            print(npc[npc_name]['second_talk'])
    else:
        print(f"There is no one named {npc_name} here to talk to.")


def show_npc(c_loc, npc):
    present_npc = [n for n, data in npc.items() if data['loc'] == c_loc]
    if present_npc:
        print(f"You see {', '.join(present_npc)} here.")

# read the configuration file

def read_config(file_name):
    game_info = {}
    map_data = {}
    npc = {}

    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line == "---":
                continue

            key, value = map(str.strip, line.split(':'))

            if key.startswith("game_"):
                game_info[key.split('_')[1]] = int(value) if value.isdigit() else value
            elif key == "r_id":
                c_rm = int(value)
                map_data[c_rm] = {}
            elif key == "r_obj":
                map_data[c_rm].setdefault('obj', []).append(value)
            elif key.startswith("r_"):
                map_data[c_rm][key.split('_')[1]] = int(value) if value.isdigit() else value
            elif key.startswith("npc_"):
                npc_name, npc_attr = key.split('_')[1:]
                if npc_name not in npc:
                    npc[npc_name] = {'loc': None, 'first_talk': None, 'second_talk': None}
                if npc_attr == "loc":
                    npc[npc_name]['loc'] = int(value)
                elif npc_attr == "1":
                    npc[npc_name]['first_talk'] = value
                elif npc_attr == "2":
                    npc[npc_name]['second_talk'] = value

    return game_info, map_data, npc

# run main game

game_info, map_data, npc = read_config('game1.txt')
main_game(game_info, map_data, npc)

