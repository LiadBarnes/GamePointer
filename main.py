from classes import Myjson, tennis_game


line_up = 'Volley'
Player = tennis_game(line_up)
Keyboard = Myjson('jsons/Keyboard.json').get()

Player.listener(Keyboard)

