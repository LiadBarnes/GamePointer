import json
import keyboard
import pyautogui
from threading import Lock


def check_mouse():
    while True:
        print(pyautogui.position())


class Decorator:
    def __init__(self):
        self.mutex = Lock()

    def wrap(self):
        def decorate(func):
            def call(*args, **kwargs):
                self.mutex.acquire(1)
                result = func(*args, **kwargs)
                self.mutex.release()
                return result

            return call

        return decorate


class Myjson:
    w = Decorator()

    def __init__(self, file_path):
        self.file = file_path

    @Decorator.wrap(w)
    def get(self, key=False):
        with open(self.file, encoding='utf8') as json_file:
            data = json.load(json_file)
            if not key:
                return data
            elif key in data:
                return data[key]
            return None

    @Decorator.wrap(w)
    def set(self, key, value):
        with open(self.file) as json_file:
            data = json.load(json_file)
            data[key] = value
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile)

    @Decorator.wrap(w)
    def add_to_list(self, key, value, uniqeList=False):
        with open(self.file) as json_file:
            data = json.load(json_file)
            if uniqeList:
                if value not in data[key]:
                    data.setdefault(key, []).append(value)
                else:
                    return None
            else:
                data.setdefault(key, []).append(value)

        # Save JSON file
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile)

    @Decorator.wrap(w)
    def delVal(self, key):
        with open(self.file) as json_file:
            data = json.load(json_file)
            data.pop(key, None)

        with open(self.file, 'w') as outfile:
            json.dump(data, outfile)

    @Decorator.wrap(w)
    def dump(self, data):
        # Save JSON file
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile)

    @Decorator.wrap(w)
    def CompareMasterJson(self, slaveFile):
        master = self.get()
        slaveFile.dump(list(set(slaveFile.get()) - set(master)))


class tennis_game:
    def __init__(self, lineup):
        self.lineup_name = lineup
        self.lineups_json = Myjson('jsons/Line_ups.json')
        self.lineup_dict = self.lineups_json.get(lineup)

        self.Agility = self.lineup_dict['skills']['Agility']
        self.Stamina = self.lineup_dict['skills']['Stamina']
        self.Serve_skills = self.lineup_dict['skills']['Serve']
        self.Volley = self.lineup_dict['skills']['Volley']
        self.Forehand = self.lineup_dict['skills']['Forehand']
        self.Backhand = self.lineup_dict['skills']['Backhand']
        self.right_handed = True

        self.shot_dict = self.lineup_dict['shot']
        self.serve_dict = self.lineup_dict['serve']
        self.mouse_offset = Myjson('jsons/Offsets.json').get(self.lineup_dict['mouse_offset'])


    def listener(self, Keyboard):
        while True:  # making a loop
            key = keyboard.read_key()
            if key in Keyboard:
                command = Keyboard[key].split('_')

                if command[0] in ['Shot', 'Serve']:
                    method = getattr(self, command[0], lambda: 'Invalid')
                    # Passing 'Direction' to specific shot command
                    method(command[1])

                elif command[0] == 'Power':
                    self.Power(*command[1:])

                else:  # escape or function with no params
                    method = getattr(self, Keyboard[key], lambda: 'Invalid')
                    method()

    def drag(self, x_offset, power):
        # Move to mouse offset
        pyautogui.moveTo(*self.mouse_offset)

        # Drag mouse as specific shot
        pyautogui.drag(x_offset, power, 0.11, button='left')

    def Shot(self, Direction):
        self.drag(self.shot_dict[Direction], self.shot_dict['Power'])

    def Serve(self, Direction):
        self.drag(self.serve_dict[Direction], self.serve_dict['Power'])

    def Power(self, Operator, shot_type):
        shot = getattr(self, f'{shot_type}_dict', lambda: 'Invalid')
        shot['Power'] += 5 if Operator == 'inc' else -5
        print(shot['Power'])

    def Esc(self):
        self.lineup_dict['shot'] = self.shot_dict
        self.lineup_dict['serve'] = self.serve_dict

        json = self.lineups_json.get()
        json[self.lineup_name] = self.lineup_dict
        self.lineups_json.dump(json)
        exit(0)
