import tkinter as tk
from tkinter import messagebox
import math
from typing import List, Tuple, Optional


class Connect4Game:
    def __init__(self):
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.MARGIN = 20
        self.BOARD_PADDING = 15
        self.ANIMATION_SPEED = 8

        self.COLORS = {
            'background': '#2c2444',
            'board': '#39334d',
            'cell_empty': '#252233',
            'cell_border': '#5a4d7a',
            'red': '#c62128',
            'red_inner': '#8b1a1f',
            'yellow': '#f8ff0c',
            'yellow_inner': '#e6b800',
            'suggestion': '#00d2d3',
            'text': '#ffffff',
            'button': '#5a4d7a',
            'button_hover': '#6c5ce7'
        }

        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.suggested_col = None
        self.animating = False
        self.ai_player = None
        self.game_started = False

        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Puissance 4 - IA")
        self.root.configure(bg=self.COLORS['background'])
        self.root.resizable(False, False)

        window_width = self.COLS * self.CELL_SIZE + 2 * self.MARGIN + 2 * self.BOARD_PADDING
        window_height = self.ROWS * self.CELL_SIZE + 4 * self.MARGIN + 150 + 2 * self.BOARD_PADDING
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        main_frame = tk.Frame(self.root, bg=self.COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        title_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        title_frame.pack(pady=(0, 20))

        title = tk.Label(title_frame, text="PUISSANCE 4",
                         font=('Arial', 24, 'bold'),
                         fg=self.COLORS['text'], bg=self.COLORS['background'])
        title.pack()

        self.choice_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        self.choice_frame.pack(pady=(0, 20))

        choice_label = tk.Label(self.choice_frame, text="Choisissez la couleur de l'IA:",
                                font=('Arial', 14, 'bold'),
                                fg=self.COLORS['text'], bg=self.COLORS['background'])
        choice_label.pack(pady=(0, 10))

        button_choice_frame = tk.Frame(self.choice_frame, bg=self.COLORS['background'])
        button_choice_frame.pack()

        self.red_ai_button = tk.Button(button_choice_frame, text="IA ROUGE",
                                       font=('Arial', 12, 'bold'),
                                       bg=self.COLORS['red'],
                                       fg=self.COLORS['text'],
                                       activebackground='#8b1a1f',
                                       activeforeground=self.COLORS['text'],
                                       relief='flat', padx=20, pady=8,
                                       command=lambda: self.start_game(1))
        self.red_ai_button.pack(side='left', padx=10)

        self.yellow_ai_button = tk.Button(button_choice_frame, text="IA JAUNE",
                                          font=('Arial', 12, 'bold'),
                                          bg=self.COLORS['yellow'],
                                          fg='#333333',
                                          activebackground='#e6b800',
                                          activeforeground='#333333',
                                          relief='flat', padx=20, pady=8,
                                          command=lambda: self.start_game(2))
        self.yellow_ai_button.pack(side='left', padx=10)

        self.info_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        self.info_frame.pack(pady=(0, 10))

        self.player_label = tk.Label(self.info_frame, text="Choisissez la couleur de l'IA pour commencer",
                                     font=('Arial', 14, 'bold'),
                                     fg=self.COLORS['text'], bg=self.COLORS['background'])
        self.player_label.pack()

        self.suggestion_label = tk.Label(self.info_frame, text="",
                                         font=('Arial', 12),
                                         fg=self.COLORS['suggestion'], bg=self.COLORS['background'])
        self.suggestion_label.pack()

        canvas_width = self.COLS * self.CELL_SIZE + 2 * self.BOARD_PADDING
        canvas_height = self.ROWS * self.CELL_SIZE + 2 * self.BOARD_PADDING

        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height,
                                bg=self.COLORS['board'], highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)

        button_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        button_frame.pack(pady=10)

        self.reset_button = tk.Button(button_frame, text="NOUVELLE PARTIE",
                                      font=('Arial', 12, 'bold'),
                                      bg=self.COLORS['button'],
                                      fg=self.COLORS['text'],
                                      activebackground=self.COLORS['button_hover'],
                                      activeforeground=self.COLORS['text'],
                                      relief='flat', padx=20, pady=8,
                                      command=self.reset_game)
        self.reset_button.pack()

        self.draw_board()

    def start_game(self, ai_color):
        self.ai_player = ai_color
        self.game_started = True
        self.choice_frame.pack_forget()
        self.update_display()
        if self.ai_player == self.current_player:
            self.calculate_suggestion()

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(self.ROWS):
            for col in range(self.COLS):
                x1 = col * self.CELL_SIZE + 5 + self.BOARD_PADDING
                y1 = row * self.CELL_SIZE + 5 + self.BOARD_PADDING
                x2 = x1 + self.CELL_SIZE - 10
                y2 = y1 + self.CELL_SIZE - 10

                if self.board[row][col] == 0:
                    color = self.COLORS['cell_empty']
                    self.canvas.create_oval(x1, y1, x2, y2,
                                            fill=color, outline='',
                                            width=1, tags=f"cell_{row}_{col}")
                elif self.board[row][col] == 1:
                    self.draw_red_token(x1, y1, x2, y2)
                else:
                    self.draw_yellow_token(x1, y1, x2, y2)

        if (self.suggested_col is not None and self.current_player == self.ai_player
                and not self.game_over and self.game_started):
            self.draw_suggestion_arrow()

    def draw_red_token(self, x1, y1, x2, y2):
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        radius = (x2 - x1) // 2

        self.canvas.create_oval(x1, y1, x2, y2,
                                fill=self.COLORS['red'], outline='',
                                tags="red_token")

        inner_radius = radius * 0.85
        inner_x1 = center_x - inner_radius
        inner_y1 = center_y - inner_radius
        inner_x2 = center_x + inner_radius
        inner_y2 = center_y + inner_radius

        self.canvas.create_oval(inner_x1, inner_y1, inner_x2, inner_y2,
                                fill=self.COLORS['red_inner'], outline='',
                                tags="red_token_inner")

        self.draw_star(center_x, center_y, 12, '#c62128')

    def draw_yellow_token(self, x1, y1, x2, y2):
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        radius = (x2 - x1) // 2

        self.canvas.create_oval(x1, y1, x2, y2,
                                fill=self.COLORS['yellow'], outline='',
                                tags="yellow_token")

        inner_radius = radius * 0.85
        inner_x1 = center_x - inner_radius
        inner_y1 = center_y - inner_radius
        inner_x2 = center_x + inner_radius
        inner_y2 = center_y + inner_radius

        self.canvas.create_oval(inner_x1, inner_y1, inner_x2, inner_y2,
                                fill=self.COLORS['yellow_inner'], outline='',
                                tags="yellow_token_inner")

        self.draw_star(center_x, center_y, 12, '#f8ff0c')

    def draw_star(self, center_x, center_y, size, color):
        star_points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                x = center_x + size * math.cos(angle - math.pi / 2)
                y = center_y + size * math.sin(angle - math.pi / 2)
            else:
                x = center_x + (size * 0.4) * math.cos(angle - math.pi / 2)
                y = center_y + (size * 0.4) * math.sin(angle - math.pi / 2)
            star_points.extend([x, y])

        self.canvas.create_polygon(star_points, fill=color,
                                   outline='', tags="star")

    def draw_animated_token(self, center_x, center_y, player):
        if player == 1:

            outer_circle = self.canvas.create_oval(
                center_x - 30, center_y - 30,
                center_x + 30, center_y + 30,
                fill=self.COLORS['red'], outline='white', width=2,
                tags="animated_piece"
            )

            inner_radius = 30 * 0.85
            inner_circle = self.canvas.create_oval(
                center_x - inner_radius, center_y - inner_radius,
                center_x + inner_radius, center_y + inner_radius,
                fill=self.COLORS['red_inner'], outline='',
                tags="animated_piece"
            )

            star_points = []
            for i in range(10):
                angle = i * math.pi / 5
                if i % 2 == 0:
                    x = center_x + 12 * math.cos(angle - math.pi / 2)
                    y = center_y + 12 * math.sin(angle - math.pi / 2)
                else:
                    x = center_x + (12 * 0.4) * math.cos(angle - math.pi / 2)
                    y = center_y + (12 * 0.4) * math.sin(angle - math.pi / 2)
                star_points.extend([x, y])

            star = self.canvas.create_polygon(star_points, fill='#c62128',
                                              outline='', tags="animated_piece")

            return [outer_circle, inner_circle, star]

        else:
            outer_circle = self.canvas.create_oval(
                center_x - 30, center_y - 30,
                center_x + 30, center_y + 30,
                fill=self.COLORS['yellow'], outline='white', width=2,
                tags="animated_piece"
            )

            inner_radius = 30 * 0.85
            inner_circle = self.canvas.create_oval(
                center_x - inner_radius, center_y - inner_radius,
                center_x + inner_radius, center_y + inner_radius,
                fill=self.COLORS['yellow_inner'], outline='',
                tags="animated_piece"
            )

            star_points = []
            for i in range(10):
                angle = i * math.pi / 5
                if i % 2 == 0:
                    x = center_x + 12 * math.cos(angle - math.pi / 2)
                    y = center_y + 12 * math.sin(angle - math.pi / 2)
                else:
                    x = center_x + (12 * 0.4) * math.cos(angle - math.pi / 2)
                    y = center_y + (12 * 0.4) * math.sin(angle - math.pi / 2)
                star_points.extend([x, y])

            star = self.canvas.create_polygon(star_points, fill='#f8ff0c',
                                              outline='', tags="animated_piece")

            return [outer_circle, inner_circle, star]

    def draw_suggestion_arrow(self):
        if self.suggested_col is None:
            return

        col = self.suggested_col
        x_center = col * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_PADDING

        arrow_points = [
            x_center, self.BOARD_PADDING - 10,
                      x_center - 15, self.BOARD_PADDING - 25,
                      x_center - 8, self.BOARD_PADDING - 25,
                      x_center - 8, self.BOARD_PADDING - 35,
                      x_center + 8, self.BOARD_PADDING - 35,
                      x_center + 8, self.BOARD_PADDING - 25,
                      x_center + 15, self.BOARD_PADDING - 25
        ]

        self.canvas.create_polygon(arrow_points, fill=self.COLORS['suggestion'],
                                   outline='white', width=2, tags="suggestion_arrow")

        self.animate_suggestion_arrow()

    def animate_suggestion_arrow(self):
        if not hasattr(self, '_arrow_scale'):
            self._arrow_scale = 1.0
            self._arrow_direction = 0.05

        self._arrow_scale += self._arrow_direction
        if self._arrow_scale >= 1.2:
            self._arrow_direction = -0.05
        elif self._arrow_scale <= 0.8:
            self._arrow_direction = 0.05

        self.canvas.delete("suggestion_arrow")
        if (self.suggested_col is not None and self.current_player == self.ai_player
                and not self.game_over and self.game_started):
            col = self.suggested_col
            x_center = col * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_PADDING
            size = 15 * self._arrow_scale

            arrow_points = [
                x_center, self.BOARD_PADDING - 10,
                          x_center - size, self.BOARD_PADDING - 25,
                          x_center - size * 0.5, self.BOARD_PADDING - 25,
                          x_center - size * 0.5, self.BOARD_PADDING - 35,
                          x_center + size * 0.5, self.BOARD_PADDING - 35,
                          x_center + size * 0.5, self.BOARD_PADDING - 25,
                          x_center + size, self.BOARD_PADDING - 25
            ]

            self.canvas.create_polygon(arrow_points, fill=self.COLORS['suggestion'],
                                       outline='white', width=2, tags="suggestion_arrow")

        if (not self.game_over and self.current_player == self.ai_player
                and self.game_started):
            self.root.after(50, self.animate_suggestion_arrow)

    def on_hover(self, event):
        if self.game_over or self.animating or not self.game_started:
            return

        col = (event.x - self.BOARD_PADDING) // self.CELL_SIZE
        if 0 <= col < self.COLS:
            self.canvas.delete("hover")
            if self.is_valid_move(col):
                x_center = col * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_PADDING
                y_center = self.BOARD_PADDING - 5

                if self.current_player == 1:
                    self.canvas.create_oval(x_center - 25, y_center - 25,
                                            x_center + 25, y_center + 25,
                                            fill=self.COLORS['red'], outline='white', width=2,
                                            stipple='gray25', tags="hover")

                    inner_radius = 25 * 0.85
                    self.canvas.create_oval(x_center - inner_radius, y_center - inner_radius,
                                            x_center + inner_radius, y_center + inner_radius,
                                            fill=self.COLORS['red_inner'], outline='',
                                            stipple='gray25', tags="hover")

                    star_points = []
                    for i in range(10):
                        angle = i * math.pi / 5
                        if i % 2 == 0:
                            x = x_center + 10 * math.cos(angle - math.pi / 2)
                            y = y_center + 10 * math.sin(angle - math.pi / 2)
                        else:
                            x = x_center + (10 * 0.4) * math.cos(angle - math.pi / 2)
                            y = y_center + (10 * 0.4) * math.sin(angle - math.pi / 2)
                        star_points.extend([x, y])

                    self.canvas.create_polygon(star_points, fill='#c62128',
                                               outline='', stipple='gray25', tags="hover")

                else:
                    self.canvas.create_oval(x_center - 25, y_center - 25,
                                            x_center + 25, y_center + 25,
                                            fill=self.COLORS['yellow'], outline='white', width=2,
                                            stipple='gray25', tags="hover")

                    inner_radius = 25 * 0.85
                    self.canvas.create_oval(x_center - inner_radius, y_center - inner_radius,
                                            x_center + inner_radius, y_center + inner_radius,
                                            fill=self.COLORS['yellow_inner'], outline='',
                                            stipple='gray25', tags="hover")

                    star_points = []
                    for i in range(10):
                        angle = i * math.pi / 5
                        if i % 2 == 0:
                            x = x_center + 10 * math.cos(angle - math.pi / 2)
                            y = y_center + 10 * math.sin(angle - math.pi / 2)
                        else:
                            x = x_center + (10 * 0.4) * math.cos(angle - math.pi / 2)
                            y = y_center + (10 * 0.4) * math.sin(angle - math.pi / 2)
                        star_points.extend([x, y])

                    self.canvas.create_polygon(star_points, fill='#f8ff0c',
                                               outline='', stipple='gray25', tags="hover")

    def on_click(self, event):
        if self.game_over or self.animating or not self.game_started:
            return

        col = (event.x - self.BOARD_PADDING) // self.CELL_SIZE
        if 0 <= col < self.COLS and self.is_valid_move(col):
            self.make_move(col)

    def is_valid_move(self, col: int) -> bool:
        return 0 <= col < self.COLS and self.board[0][col] == 0

    def make_move(self, col: int) -> bool:
        if not self.is_valid_move(col):
            return False

        row = -1
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r][col] == 0:
                row = r
                break

        if row == -1:
            return False

        self.animate_piece_drop(row, col)
        return True

    def animate_piece_drop(self, target_row: int, col: int):
        self.animating = True
        self.canvas.delete("hover")

        x_center = col * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_PADDING
        start_y = self.BOARD_PADDING - self.CELL_SIZE // 2
        end_y = target_row * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_PADDING

        animated_pieces = self.draw_animated_token(x_center, start_y, self.current_player)

        def animate_step(current_y, velocity=0):
            gravity = 0.7
            damping = 0.45

            velocity += gravity
            current_y += velocity

            if current_y >= end_y:
                current_y = end_y
                if abs(velocity) < 1:
                    self.canvas.delete("animated_piece")
                    self.board[target_row][col] = self.current_player
                    self.draw_board()
                    self.check_winner()
                    self.switch_player()
                    self.animating = False
                    return
                else:
                    velocity = -velocity * damping

            for piece in animated_pieces:
                coords = self.canvas.coords(piece)
                if len(coords) == 4:
                    width = coords[2] - coords[0]
                    height = coords[3] - coords[1]
                    self.canvas.coords(piece,
                                       x_center - width / 2, current_y - height / 2,
                                       x_center + width / 2, current_y + height / 2)
                else:
                    star_points = []
                    for i in range(10):
                        angle = i * math.pi / 5
                        if i % 2 == 0:
                            x = x_center + 12 * math.cos(angle - math.pi / 2)
                            y = current_y + 12 * math.sin(angle - math.pi / 2)
                        else:
                            x = x_center + (12 * 0.4) * math.cos(angle - math.pi / 2)
                            y = current_y + (12 * 0.4) * math.sin(angle - math.pi / 2)
                        star_points.extend([x, y])
                    self.canvas.coords(piece, *star_points)

            self.root.after(16, lambda: animate_step(current_y, velocity))

        animate_step(start_y)

    def check_winner(self):
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and
                        self.board[row][col] == self.board[row][col + 1] ==
                        self.board[row][col + 2] == self.board[row][col + 3]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    return

        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if (self.board[row][col] != 0 and
                        self.board[row][col] == self.board[row + 1][col] ==
                        self.board[row + 2][col] == self.board[row + 3][col]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    return

        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and
                        self.board[row][col] == self.board[row + 1][col + 1] ==
                        self.board[row + 2][col + 2] == self.board[row + 3][col + 3]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    return

        for row in range(self.ROWS - 3):
            for col in range(3, self.COLS):
                if (self.board[row][col] != 0 and
                        self.board[row][col] == self.board[row + 1][col - 1] ==
                        self.board[row + 2][col - 2] == self.board[row + 3][col - 3]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    return

        if all(self.board[0][col] != 0 for col in range(self.COLS)):
            self.game_over = True
            self.winner = 0

    def switch_player(self):
        if not self.game_over:
            self.current_player = 3 - self.current_player
            self.update_display()
            if self.current_player == self.ai_player:
                self.calculate_suggestion()
            else:
                self.suggested_col = None
                self.suggestion_label.config(text="")
        else:
            self.show_game_over()

    def update_display(self):
        if self.game_over or not self.game_started:
            return

        if self.current_player == 1:
            player_text = "Tour du joueur Rouge"
            if self.ai_player == 1:
                player_text += " (IA)"
            self.player_label.config(text=player_text, fg=self.COLORS['red'])
        else:
            player_text = "Tour du joueur Jaune"
            if self.ai_player == 2:
                player_text += " (IA)"
            self.player_label.config(text=player_text, fg=self.COLORS['yellow'])

    def show_game_over(self):
        if self.winner == 1:
            message = "🎉 Le joueur Rouge a gagné! 🎉"
            if self.ai_player == 1:
                message = "🤖 L'IA Rouge a gagné! 🤖"
            color = self.COLORS['red']
        elif self.winner == 2:
            message = "🎉 Le joueur Jaune a gagné! 🎉"
            if self.ai_player == 2:
                message = "🤖 L'IA Jaune a gagné! 🤖"
            color = self.COLORS['yellow']
        else:
            message = "🤝 Match nul! 🤝"
            color = self.COLORS['text']

        self.player_label.config(text=message, fg=color)
        self.suggestion_label.config(text="")

        self.root.after(500, lambda: messagebox.showinfo("Fin de partie", message))

    def reset_game(self):
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.suggested_col = None
        self.animating = False
        self.ai_player = None
        self.game_started = False

        self.choice_frame.pack(pady=(0, 20), after=self.info_frame)

        self.player_label.config(text="Choisissez la couleur de l'IA pour commencer",
                                 fg=self.COLORS['text'])
        self.suggestion_label.config(text="")
        self.draw_board()

    def calculate_suggestion(self):
        if self.game_over or self.current_player != self.ai_player or not self.game_started:
            self.suggested_col = None
            self.suggestion_label.config(text="")
            return

        best_col = self.get_best_move()
        self.suggested_col = best_col

        if best_col is not None:
            color_name = "Rouge" if self.ai_player == 1 else "Jaune"
            self.suggestion_label.config(
                text=f"💡 Suggestion IA {color_name}: Colonne {best_col + 1}",
                fg=self.COLORS['suggestion']
            )
        else:
            self.suggestion_label.config(text="")

    def get_best_move(self, depth: int = 6) -> Optional[int]:
        _, best_col = self.minimax(self.board, depth, -math.inf, math.inf, True)
        return best_col

    def minimax(self, board: List[List[int]], depth: int, alpha: float,
                beta: float, maximizing: bool) -> Tuple[float, Optional[int]]:

        winner = self.check_winner_board(board)
        if winner == 1:
            return 1000 + depth, None
        elif winner == 2:
            return -1000 - depth, None
        elif self.is_board_full(board) or depth == 0:
            return self.evaluate_board(board), None

        best_col = None

        if maximizing:
            max_eval = -math.inf
            for col in self.get_valid_moves(board):
                new_board = self.make_move_copy(board, col, 1)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            return max_eval, best_col

        else:
            min_eval = math.inf
            for col in self.get_valid_moves(board):
                new_board = self.make_move_copy(board, col, 2)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            return min_eval, best_col

    def evaluate_board_for_ai(self, board: List[List[int]]) -> float:
        ai_score = self.evaluate_windows(board, self.ai_player)
        opponent_score = self.evaluate_windows(board, 3 - self.ai_player)

        center_col = self.COLS // 2
        center_bonus = 0
        for row in range(self.ROWS):
            if board[row][center_col] == self.ai_player:
                center_bonus += 6
            elif board[row][center_col] == (3 - self.ai_player):
                center_bonus -= 6

        return ai_score - opponent_score + center_bonus

    def get_valid_moves_ordered(self, board: List[List[int]]) -> List[int]:
        valid_moves = self.get_valid_moves(board)
        center_col = self.COLS // 2

        def move_priority(col):
            return abs(col - center_col)

        return sorted(valid_moves, key=move_priority)

    def evaluate_board(self, board: List[List[int]]) -> float:
        score = 0

        center_col = self.COLS // 2
        for row in range(self.ROWS):
            if board[row][center_col] == 1:
                score += 6
            elif board[row][center_col] == 2:
                score -= 6

        score += self.evaluate_windows(board, 1) - self.evaluate_windows(board, 2)

        return score

    def evaluate_windows(self, board: List[List[int]], player: int) -> float:
        score = 0

        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                window = [board[row][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                window = [board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, player)

        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        for row in range(self.ROWS - 3):
            for col in range(3, self.COLS):
                window = [board[row + i][col - i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

    def evaluate_window(self, window: List[int], player: int) -> float:
        score = 0
        opponent = 3 - player

        player_count = window.count(player)
        empty_count = window.count(0)
        opponent_count = window.count(opponent)

        if player_count == 4:
            score += 100
        elif player_count == 3 and empty_count == 1:
            score += 10
        elif player_count == 2 and empty_count == 2:
            score += 2

        if opponent_count == 3 and empty_count == 1:
            score -= 80

        return score

    def get_valid_moves(self, board: List[List[int]]) -> List[int]:
        return [col for col in range(self.COLS) if board[0][col] == 0]

    def make_move_copy(self, board: List[List[int]], col: int, player: int) -> List[List[int]]:
        new_board = [row[:] for row in board]

        for row in range(self.ROWS - 1, -1, -1):
            if new_board[row][col] == 0:
                new_board[row][col] = player
                break

        return new_board

    def check_winner_board(self, board: List[List[int]]) -> Optional[int]:
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if (board[row][col] != 0 and
                        board[row][col] == board[row][col + 1] ==
                        board[row][col + 2] == board[row][col + 3]):
                    return board[row][col]

        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if (board[row][col] != 0 and
                        board[row][col] == board[row + 1][col] ==
                        board[row + 2][col] == board[row + 3][col]):
                    return board[row][col]

        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if (board[row][col] != 0 and
                        board[row][col] == board[row + 1][col + 1] ==
                        board[row + 2][col + 2] == board[row + 3][col + 3]):
                    return board[row][col]

        for row in range(self.ROWS - 3):
            for col in range(3, self.COLS):
                if (board[row][col] != 0 and
                        board[row][col] == board[row + 1][col - 1] ==
                        board[row + 2][col - 2] == board[row + 3][col - 3]):
                    return board[row][col]

        return None

    def is_board_full(self, board: List[List[int]]) -> bool:
        return all(board[0][col] != 0 for col in range(self.COLS))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = Connect4Game()
    game.run()