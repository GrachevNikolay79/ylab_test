import tkinter as tk

from engine import BasicEngine, WinType, CellState


class GameWindow:

    def __init__(self, engine: BasicEngine):
        self.engine = engine
        self.x_size, self.y_size = self.engine.get_size()
        self.root = tk.Tk()
        self.buttons = []
        self.fg_x_color = 'DarkOrange3'
        self.fg_o_color = 'SeaGreen'
        self.__create_widgets()
        self.game_over = False
        self.active = False

    def run(self):
        self.active = False
        self.root.mainloop()
        pass

    def __create_widgets(self):
        top_frame = tk.Frame(master=self.root)
        tk.Label(master=top_frame, text="(X) Philip J. Fry ", fg=self.fg_x_color).pack(side='left')
        tk.Label(master=top_frame, text="(O) Bender Bending Rodriguez", fg=self.fg_o_color).pack(side='right')
        top_frame.pack()

        gf = tk.Frame(master=self.root)
        for x in range(self.x_size):
            gf.columnconfigure(x, minsize=40)

        for y in range(self.y_size):
            gf.rowconfigure(y, minsize=30)
            for x in range(self.x_size):
                tb = tk.StringVar(value=".")

                b = tk.Button(gf, textvariable=tb, overrelief="solid", relief="solid",
                              command=self.wrap_cell_on_click(x, y))
                b.grid(row=y, column=x, sticky="ew")
                self.buttons.append((b, tb))
        gf.pack()

    def cell_on_click(self, x, y, man=False):
        if man:
            res = self.engine.turn(x, y, CellState.X)
        else:
            res = self.engine.turn(x, y, CellState.O)

        if res is not None:
            btn = self.buttons[x + y * self.x_size]
            if res == CellState.X:
                btn[0]['fg'] = self.fg_x_color
            else:
                btn[0]['fg'] = self.fg_o_color
            btn[1].set(value=res)

            win, user, line = self.engine.check_win(x, y)
            if win == WinType.Draw:
                self.__draw()
            elif win == WinType.Continue:
                if man:
                    self.engine.think(self.cell_on_click)
            else:
                self.__win(user, line)


    def wrap_cell_on_click(self, x: int, y: int):
        def func():
            if self.game_over:
                self.root.destroy()
                return
            self.cell_on_click(x, y, True)

        return func

    def __win(self, user, line):
        self.game_over = True
        self.__highlight_loose_line(line)
        slave = tk.Toplevel(self.root)

        if user == CellState.O:
            u_name = "Bender Bending Rodriguez"
            fg = self.fg_o_color
        else:
            u_name = "Philip J. Fry"
            fg = self.fg_x_color

        win_text = " {} WIN! \n Congratulations! ".format(u_name)
        tk.Button(slave, text=win_text, command=self.__end_game, fg=fg).pack()
        slave.transient(self.root)
        slave.grab_set()
        slave.focus_set()
        slave.wait_window()

    def __highlight_loose_line(self, line):
        l, x1, y1, x2, y2 = line
        if x2 > x1:
            dx = 1
        elif x2 == x1:
            dx = 0
        else:
            dx = -1

        if y2 > y1:
            dy = 1
        elif y2 == y1:
            dy = 0
        else:
            dy = -1

        for i in range(l):
            pos = (x1 + dx * i) + (y1 + dy * i) * self.x_size
            b = self.buttons[pos][0]
            b['fg'] = 'gold'
            b['bg'] = 'blue4'

    def __end_game(self):
        self.root.destroy()

    def __draw(self):
        self.game_over = True
        win_text = " Draw! \n There are no winners!"
        slave = tk.Toplevel(self.root)
        tk.Button(slave, text=win_text, command=self.__end_game, justify='center').pack()
        slave.transient(self.root)
        slave.grab_set()
        slave.focus_set()
        slave.wait_window()
