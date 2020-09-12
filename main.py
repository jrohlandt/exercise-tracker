import os
import time
import json
import datetime

# print(time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime()))
# quit()
exercises = [
    {'id': 1, 'name': 'Pull ups'},
    {'id': 2, 'name': 'Push ups'},
    {'id': 3, 'name': 'Squats', 'uses_weights': True}
]


def get_exercise(e_id):
    for e in exercises:
        if e_id == e['id']:
            return e
    return None


def clear_screen():
    os.system('clear')


def main():
    os.system("clear")

    todays_sets = []
    file_name = os.path.join('.', 'data', str(datetime.date.today()) + '.json')
    # file_name = './data/' + str(datetime.date.today()) + '.json'
    try:
        with open(file_name, 'r') as f:
            read_data = f.read()
            if read_data:
                todays_sets = json.loads(read_data)
    except FileNotFoundError:
        print('Creating new exercise file for today...')
        f = open(file_name, 'w')
        f.close()
        clear_screen()

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

    time.sleep(1)

    feedback = 'So far today you done: \n'
    
    with open(file_name) as f:
        sets = f.read()
        sets = json.loads(sets)

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


if __name__ == "__main__":
    main()