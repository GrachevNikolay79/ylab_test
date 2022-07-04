from engine import Engine, WinType
from game_window import GameWindow

if __name__ == "__main__":

    engine = Engine(10, 10)
    gw = GameWindow(engine)
    gw.run()

    # while True:
    #     if engine.get_map().check_for_empty_cells():
    #         x, y = engine.think()
    #         win, user, line = engine.check_win(x, y)
    #         if win == WinType.Draw:
    #             print('Ничья')
    #             break
    #         elif win == WinType.Win_X:
    #             print("Победа X")
    #             break
    #         elif win == WinType.Win_O:
    #             print("Победа O")
    #             break
    #     else:
    #         print('Ничья')
    #         break
    #
    # engine.get_map().print_map()
