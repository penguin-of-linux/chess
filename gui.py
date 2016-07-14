import sdl2
import sdl2.ext
import time
import figures


class Render:
    def __init__(self):
        """
        Создание инструментов pysdl2 для рисовашек
        """
        try:
            print("Grafics initializing... ", end = '')
            sdl2.ext.init()
            self.BLACK_COLOR = sdl2.ext.Color(128, 128, 128)
            self.WHITE_COLOR = sdl2.ext.Color(192, 192, 192)
            self.window = sdl2.ext.Window("Lite Chess 1.0", size = (512, 512))
            self.window.show()
        
            self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
            self.renderer = sdl2.ext.SoftwareSpriteRenderSystem(self.window)

            self.board = self.factory.create_software_sprite((512, 512))
            self.board.surface = sdl2.sdlimage.IMG_Load(b"board.png")

            self.sprites = dict()
            temp_dict = {
                -6 : "black_king",
                -5 : "black_queen",
                -4 : "black_tower",
                -3 : "black_elf",
                -2 : "black_horse",
                -1 : "black_pawn",
                0 : "green_frame",
                1 : "white_pawn",
                2 : "white_horse",
                3 : "white_elf",
                4 : "white_tower", 
                5 : "white_queen",
                6 : "white_king"
            }

            for i in range(-6, 7, 1):
                    self.sprites[i] = self.factory.create_software_sprite((64, 64))
                    self.sprites[i].surface = sdl2.sdlimage.IMG_Load((temp_dict[i] + ".png").encode("utf-8"))

            print("done")
        except Exception as exception:
            print("error: ", end = '')
            print(exception)
            exit()

    def init_board(self, board):
        """
        Рисование начальнго положения доски
        """
        self.window.refresh()
        self.renderer.render(self.board, 0, 0)
        for i in range(0, 8, 1):
            for j in range(0, 8, 1):
                if isinstance(board[j][i], figures.Figure):
                    self.renderer.render(self.sprites[board[j][i].ID], i * 64, j * 64)
                    pass
    def update_board(self, coords, board):
        """
        Обновление картинки одной клетки
        """
        background = self.WHITE_COLOR if (coords[0] + coords[1]) % 2 == 0 else self.BLACK_COLOR
        sdl2.ext.fill(self.window.get_surface(), background, (coords[0] * 64 + 2, coords[1] * 64, 60, 60)) # Кривая доска

        if isinstance(board[coords[1]][coords[0]], figures.Figure):
            self.renderer.render(self.sprites[board[coords[1]][coords[0]].ID], coords[0] * 64, coords[1] * 64)

        self.window.refresh()

    def get_coords_by_click(self):
        """
        Возвращает координаты клетки, на которую тыкнули мышкой
        """
        while True:
            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    return (event.button.x // 64, event.button.y // 64)

    #def wait_for_event(self):
        

    def draw_frame(self, coords):
        """
        Рисуем рамку вокруг клетки (на данном мемонте всего-лишь подчеркивание выбранной фигуры)
        """
        self.renderer.render(self.sprites[0], coords[0] * 64 + 1, coords[1] * 64 - 1)
        self.window.refresh()