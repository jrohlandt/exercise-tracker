import sys
import os
import time
import json

storage_dir = os.path.join('~', '.local', 'share', 'exercise-tracker', 'data')
storage_dir = os.path.expanduser(storage_dir)
file_name = os.path.join(storage_dir, time.strftime('%Y-%m-%d', time.localtime()) + '.json')

if not os.path.exists(storage_dir):
    print('does not exist')
    os.makedirs(storage_dir)

exercises = [
    {'id': 1, 'name': 'Pull ups'},
    {'id': 2, 'name': 'Push ups'},
    {'id': 3, 'name': 'Squats', 'uses_weights': True},
    {'id': 4, 'name': 'Lateral lifts', 'uses_weights': True},
    {'id': 5, 'name': 'Crunches'}
]


def get_exercise(e_id):
    for e in exercises:
        if e_id == e['id']:
            return e
    return None


def clear_screen():
    os.system('clear')


def get_sets():
    sets = []
    try:
        with open(file_name, 'r') as f:
            read_data = f.read()
            if read_data:
                sets = json.loads(read_data)
    except FileNotFoundError:
        print('Creating new exercise file for today...')
        f = open(file_name, 'w')
        f.close()
        clear_screen()

    return sets


def print_summary():
    feedback = 'So far today you done: \n'

    sets = get_sets()
    sets_sums = {}
    for e_set in sets:
        e = get_exercise(e_set['exercise_id'])

        if e['id'] not in sets_sums:
            sets_sums[e['id']] = {'name': e['name'], 'reps': 0}

        sets_sums[e['id']]['reps'] += e_set['reps']

    for e_set in sets_sums.items():
        values = e_set[1]
        feedback += f" {values['reps']} {values['name']} \n"

    print(feedback)


def main():
    os.system("clear")

    args = sys.argv
    if len(args) == 2:
        if args[1] == 'status':
            print_summary()
            quit()
        elif args[1] == 'add':
            pass
        else:
            print("invalid command")
            quit()
    else:
        print("no command")
        quit()
        
    todays_sets = get_sets()
    prompt = "Choose exercise (by number):\n"
    for e in exercises:
        prompt += f"[{e['id']}] {e['name']}\n"

    e_id = input(prompt)

    selected = None
    weight = 0

    for e in exercises:
        if int(e_id) == e['id']:
            selected = e
            break

    if not selected:
        print('Invalid id selected')
        quit()

    print(f"Exercise: {selected['name']}\n")

    if 'uses_weights' in selected:
        weight = input("How much weight did you use?\n")

    reps = input("How many reps did you complete?\n")

    weight_string = f'weight: {weight}' if weight != 0 else ''
    print(f"Adding exercise {selected['name']} reps {reps} {weight_string}")

    new_set = {
        'datetime': time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime()),
        'exercise_id': selected['id'],
        'reps': int(reps),
        'weight': weight
    }
    todays_sets.append(new_set)
    sets_dump = json.dumps(todays_sets)

    with open(file_name, 'w') as f:
        f.write(sets_dump)

    print_summary()


if __name__ == "__main__":
    main()
