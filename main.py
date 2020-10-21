import dearpygui.core as dpg
from dearpygui.simple import menu_bar, menu, window
from PIL import Image, ImageDraw
import math
import pickle
import copy
import os
from utils import recta
from pgn_parser import Parser

class Board:

    def __init__(self, board = list()):
        self.current_selection = -1
        self.piece_color = 'b'
        self.board = board
        self.piece_size = 80
        self.size = self.piece_size*8
        self.lines = []
        self.colored_boxes = [[None,None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None,None]]
        self.step = 0
        self.drawing_color = [0,0,0]
        self.reading_pgn = False

    def draw_board(self):
        """
        Dibuja el tablero pegando las piezas en una imagen vacia
        """
        p_size = self.piece_size
        dpg.clear_drawing('canvas')
        board = Image.new('RGB',(self.size,self.size))
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                piece = '' if piece == '_E' else piece
                x = p_size*col
                y = p_size*row
                if (-1)**(row+col) == 1: # fondo blanco
                    im = Image.open(self.piece_p(str(piece)+'b'))

                else: # fondo negro
                    im = Image.open(self.piece_p(str(piece)+'n'))
                im = im.resize((p_size,p_size))

                # color boxes
                color = self.colored_boxes[row][col]
                if color:
                    size = (self.piece_size,self.piece_size)
                    im_color = Image.new('RGB',size,color)
                    im = Image.blend(im, im_color, 0.5)
                board.paste(im,(x,y))

        # draw lines
        im_arrows = Image.new('RGB',(self.size,self.size),'rgb(255,255,255)')
        draw = ImageDraw.Draw(im_arrows)
        for line in self.lines:
            init = line[0]
            end = line[1]
            draw.line([init,end],width=p_size//8,fill=line[2])
            # agregar flecha
            x = end[0]
            y = end[1]
            d = 30
            if x == init[0]:
                x0 = x
                if y-init[1] < 0:
                    y0 = y+d
                else:
                    y0 = y-d
            else:
                m, f = recta(init,end)
                c = math.sqrt(d**2/(1+m**2))
                if x-init[0] < 0:
                    x0 = x+c
                else:
                    x0 = x-c
                y0 = f(x0)

            vector = (x0-x,y0-y)
            v_x = vector[0]
            v_y = vector[1]

            rad = math.pi / 4
            x_ = v_x*math.cos(rad) - v_y*math.sin(rad)
            y_ = v_x*math.sin(rad) + v_y*math.cos(rad)
            arrow_1 = (int(x_+x),int(y_+y))

            rad = (-1)*(math.pi / 4)
            x_ = v_x*math.cos(rad) - v_y*math.sin(rad)
            y_ = v_x*math.sin(rad) + v_y*math.cos(rad)
            arrow_2 = (int(x_+x),int(y_+y))

            draw.line([end,arrow_1],width=p_size//8,fill=line[2])
            draw.line([end,arrow_2],width=p_size//8,fill=line[2])

        board = Image.blend(board,im_arrows,0.3)
        board.save('tmp.jpg')
        dpg.draw_image('canvas','tmp.jpg',[0,self.size])

    def change_box(self,piece_name, position):
        """
        Cambia el valor de casilla en la posicion dada por el
        valor dado
        """
        row = position[1]
        col = position[0]
        if piece_name:
            self.board[row][col] = piece_name+self.piece_color
        else:
            self.board[row][col] = '_E'

    def get_board_position(self,m_position):
        """
        Comvierte las coordenadas dadas a una posicion del
        tablero dde 8x8
        """
        v1 = m_position[0] < 0 or self.size < m_position[0]
        v2 = m_position[1] < 0 or self.size < m_position[1]
        if v1 or v2:
            return

        pos = (int((m_position[0]-10)//self.piece_size),
               int((m_position[1]+10)//self.piece_size))
        return pos

    def piece_p(self,name):
        """
        Duelve el path  de la imagen de la pieza dada
        """
        path = 'images/piezas-ajedrez/'
        return path + name + '.jpg'

    def get_marroquin_row(self,row):
        """
        Comvierte el renglon dado del tablero a texto
        para fuente Marroquin
        """
        str = ''
        m_p = ''
        for col in range(8):
            piece = self.board[row][col]

            if piece == '_E':
                m_p = ' '
            elif piece == 'Pb':
                m_p = 'p'
            elif piece == 'Pn':
                m_p = 'o'
            elif piece == 'Tb':
                m_p = 'r'
            elif piece == 'Tn':
                m_p = 't'
            elif piece == 'Cb':
                m_p = 'n'
            elif piece == 'Cn':
                m_p = 'm'
            elif piece == 'Ab':
                m_p = 'b'
            elif piece == 'An':
                m_p = 'v'
            elif piece == 'Db':
                m_p = 'q'
            elif piece == 'Dn':
                m_p = 'w'
            elif piece == 'Rb':
                m_p = 'k'
            elif piece == 'Rn':
                m_p = 'l'
            if (-1)**(row+col) == (-1): # fondo negro
                if piece == '_E':
                    m_p = '+'
                m_p = m_p.upper()

            str += m_p
        return str

    def save_board(self):
        """
        Guardar el tablero en texto para fuente Marroquin,
        y serializa el tablero
        """

        str = '!""""""""#\n'
        for row in range(8):
            str += '$'
            str += self.get_marroquin_row(row)
            str += '%\n'
        str += '/(((((((()'

        name = dpg.get_value('save_name')
        if len(name) == 0:
            out = open('save.mrq', 'w')
            out.write(str)
            out.close()

            out = open('save.sv','wb')
            pickle.dump(self,out)
            out.close()
        else:
            out = open(name+'.mrq', 'w')
            out.write(str)
            out.close()

            out = open(name+'.sv','wb')
            pickle.dump(self,out)
            out.close()

    def save_board_image(self):
        """
        Guarda la imagen del tablero copiando el contenido
        del archivo tmp.jps
        """
        board = Image.open('tmp.jpg')
        name = dpg.get_value('save_img_name')
        if len(name) == 0:
            board.save('img_save.jpg')
        else:
            board.save(name+'.jpg')


def main():
    empty_board = [['_E','_E','_E','_E','_E','_E','_E','_E'],
                   ['_E','_E','_E','_E','_E','_E','_E','_E'],
                   ['_E','_E','_E','_E','_E','_E','_E','_E'],
                   ['_E','_E','_E','_E','_E','_E','_E','_E'],
                   ['_E','_E','_E','_E','_E','_E','_E','_E'],
                   ['_E','_E','_E','_E','_E','_E','_E','_E'],
                   ['_E','_E','_E','_E','_E','_E','_E','_E'],
                   ['_E','_E','_E','_E','_E','_E','_E','_E']]
    initial_board = [['Tn','Cn','An','Dn','Rn','An','Cn','Tn'],
                     ['Pn','Pn','Pn','Pn','Pn','Pn','Pn','Pn'],
                     ['_E','_E','_E','_E','_E','_E','_E','_E'],
                     ['_E','_E','_E','_E','_E','_E','_E','_E'],
                     ['_E','_E','_E','_E','_E','_E','_E','_E'],
                     ['_E','_E','_E','_E','_E','_E','_E','_E'],
                     ['Pb','Pb','Pb','Pb','Pb','Pb','Pb','Pb'],
                     ['Tb','Cb','Ab','Db','Rb','Ab','Cb','Tb']]

    def mouse_click_callback(sender,data):
        nonlocal c_board

        if data == 0 and c_board.current_selection != -1:
            m_position = dpg.get_mouse_pos()
            position = c_board.get_board_position(m_position)

            if not position:
                return

            if c_board.current_selection == 0:
                c_board.change_box('P', position) # put peon
            elif c_board.current_selection == 1:
                c_board.change_box('T', position) # put toker
            elif c_board.current_selection == 2:
                c_board.change_box('C', position) # put horse
            elif c_board.current_selection == 3:
                c_board.change_box('A', position) # put bishop
            elif c_board.current_selection == 4:
                c_board.change_box('D', position) # put queen
            elif c_board.current_selection == 5:
                c_board.change_box('R', position) # put king
            elif c_board.current_selection == 6:
                c_board.change_box(None,position) # remove
            elif c_board.current_selection == 7:
                # draw arrow
                size = c_board.piece_size
                c = size//2
                position = (position[0]*size+c,position[1]*size+c)
                if c_board.step == 0:
                    c_board.lines.append([(),(),''])
                    c_board.lines[-1][0] = position
                elif c_board.step == 1:
                    c_board.lines[-1][1] = position
                    color = dpg.get_value('drawing_color')
                    r = int(color[0])
                    g = int(color[1])
                    b = int(color[2])
                    color = 'rgb({},{},{})'.format(r,g,b)
                    c_board.lines[-1][2] = color

                c_board.step = (c_board.step+1)%2

                if c_board.step == 1:
                    return

            elif c_board.current_selection == 8:
                # delete arrow
                size = c_board.piece_size
                c = size//2
                position = (position[0]*size+c,position[1]*size+c)
                for i in range(len(c_board.lines)):
                    line = c_board.lines[i]
                    if position == line[0] or position == line[1]:
                        c_board.lines.remove(line)
                        break
            elif c_board.current_selection == 9:
                # color box
                color = dpg.get_value('drawing_color')
                r = int(color[0])
                g = int(color[1])
                b = int(color[2])
                color = 'rgb({},{},{})'.format(r,g,b)
                col = position[0]
                row = position[1]
                c_board.colored_boxes[row][col] = color
            elif c_board.current_selection == 10:
                # discolor box
                col = position[0]
                row = position[1]
                c_board.colored_boxes[row][col] = None

            c_board.draw_board()

        if data == 1:
            if c_board.piece_color == 'b':
                c_board.piece_color = 'n'
                dpg.set_value('color_piece', "Negro")
            else:
                 c_board.piece_color = 'b'
                 dpg.set_value('color_piece', "Blanco")

    def key_press_callback(sender, data):
        nonlocal c_board
        if data == dpg.mvKey_Right:
            if c_board.reading_pgn:
                pars.current_match.next_position()
                c_board.draw_board()
            else:
                return

        if data == dpg.mvKey_Left:
            if c_board.reading_pgn:
                pars.current_match.previews_position()
                c_board.draw_board()
            else:
                return

        if data == dpg.mvKey_Escape :
            c_board.current_selection = -1
            c_board.reading_pgn = False
            dpg.set_value("accion", "Sin seleccionar")
            dpg.set_value("pieza", "Sin seleccionar")
            return

    def load_callback(sender, data):
        def file_callback(sender, data):
            nonlocal c_board
            file = open(data[1],'rb')
            load_board = pickle.load(file)
            file.close()
            c_board = load_board
            c_board.draw_board()

        dpg.open_file_dialog(callback=file_callback, extensions=".sv")

    def save_callback(sender, data):
        nonlocal c_board

        c_board.save_board()

    def save_image_callback(sender,data):
        nonlocal c_board
        c_board.save_board_image()

    def clean_callback(sender, data):
        nonlocal c_board
        nonlocal empty_board
        c_board.reading_pgn = False
        c_board.board = copy.deepcopy(empty_board)
        c_board.lines = []
        c_board.colored_boxes = [[None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None]]
        c_board.draw_board()

    def default_board_callback(sender, data):
        nonlocal c_board
        nonlocal initial_board
        c_board.reading_pgn = False
        c_board.board = copy.deepcopy(initial_board)
        c_board.lines = []
        c_board.colored_boxes = [[None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None]]
        c_board.draw_board()

    def close(sender,data):
        try:
            os.remove("tmp.jpg")
        except Exception as e:
            pass

    def pgn_reader(sender,data):

        def load_match(sender,data):
            nonlocal pars
            nonlocal c_board
            coords = dpg.get_table_selections(sender)
            dpg.delete_item('Partidas')
            dpg.delete_item('Lista de Partidas')
            i = coords[0][0]
            match = pars.matches[i]
            pars.current_match = match
            c_board.board = match.board
            c_board.reading_pgn = True
            dpg.set_value('accion','Leyendo partida PGN')
            dpg.set_value('pieza','Sin seleccionar')
            c_board.draw_board()

        def close_callback(sender,data):
            dpg.delete_item('Partidas')
            dpg.delete_item('Lista de Partidas')

        def file_callback(sender, data):
            nonlocal c_board
            nonlocal pars

            pars = Parser()
            pars.get_plays(data[0]+'/'+data[1])

            # Lista de partidas cargadas--------------------------------TODO
            dpg.add_window('Lista de Partidas',on_close=close_callback)
            colums = set()
            for match in pars.matches:
                for att in match.attr:
                    colums.add(att)
            colums = list(colums)
            # colums.sort()
            dpg.add_table("Partidas", colums, callback=load_match)

            rows = list()
            for match in pars.matches:
                row = list()
                for colum in colums:
                    row.append(match.attr[colum])

                rows.append(row)

            for row in rows:
                dpg.add_row("Partidas", row)

            dpg.end()

        dpg.open_file_dialog(callback=file_callback, extensions=".pgn")

    def control_button(sender,data):
        nonlocal c_board;
        c_board.reading_pgn = False

        add_arr = c_board.current_selection == 7
        if add_arr and c_board.step == 1:
            c_board.lines.pop()
            c_board.step = 0

        if sender == 'Peon':
            c_board.current_selection = 0
            dpg.set_value("accion", "Añadiendo Pieza")
            dpg.set_value("pieza", "Peon")
        elif sender == 'Torre':
            c_board.current_selection = 1
            dpg.set_value("accion", "Añadiendo Pieza")
            dpg.set_value("pieza", "Torre")
        elif sender == 'Caballo':
            c_board.current_selection = 2
            dpg.set_value("accion", "Añadiendo Pieza")
            dpg.set_value("pieza", "Caballo")
        elif sender == 'Alfil':
            c_board.current_selection = 3
            dpg.set_value("accion", "Añadiendo Pieza")
            dpg.set_value("pieza", "Alfil")
        elif sender == 'Reina':
            c_board.current_selection = 4
            dpg.set_value("accion", "Añadiendo Pieza")
            dpg.set_value("pieza", "Reina")
        elif sender == 'Rey':
            c_board.current_selection = 5
            dpg.set_value("accion", "Añadiendo Pieza")
            dpg.set_value("pieza", "Rey")
        elif sender == 'Eliminar Pieza':
            c_board.current_selection = 6
            dpg.set_value("accion", "Eliminando Pieza")
            dpg.set_value("pieza", "Sin seleccionar")
        elif sender == 'Añadir flecha':
            c_board.current_selection = 7
            dpg.set_value("accion", "Añadiendo flecha")
            dpg.set_value("pieza", "Sin seleccionar")
        elif sender == 'Eliminar flecha':
            c_board.current_selection = 8
            dpg.set_value("accion", "Eliminando flecha")
            dpg.set_value("pieza", "Sin seleccionar")
        elif sender == 'Colorear casilla':
            c_board.current_selection = 9
            dpg.set_value("accion", "Coloreando casilla")
            dpg.set_value("pieza", "Sin seleccionar")
        elif sender == 'Descolorear casilla':
            c_board.current_selection = 10
            dpg.set_value("accion", "Descolorando casilla")
            dpg.set_value("pieza", "Sin seleccionar")

    c_board = Board(board = copy.deepcopy(empty_board))
    pars = Parser()

    main_width = c_board.size+220
    main_height= c_board.size+240
    dpg.set_main_window_size(main_width, main_height)
    dpg.set_main_window_title('Diagramador')
    dpg.set_main_window_resizable(False)
    dpg.set_exit_callback(close)

    with menu_bar('Menu bar'):
        with menu('Archivo'):
            dpg.add_menu_item("Guardar", callback=save_callback)
            dpg.add_menu_item("Guardar Imagen", callback=save_image_callback)
            dpg.add_menu_item("Cargar tablero", callback=load_callback)
        with menu('Herramientas'):
            dpg.add_menu_item("Leer archivo PGN", callback=pgn_reader)
        with menu('Color'):
            dpg.add_color_edit3('Seleccion de Color',source='drawing_color')

    dpg.add_drawing("canvas", width=c_board.size,height=c_board.size)
    dpg.add_image('board_img','',source=c_board.piece_p('Abb'))
    dpg.add_same_line()

    controles =(
        "\nControles\n"
        "Click Derecho : Cambiar color de pieza\n\n"
        "Flecha derecha: Mostrar siguiente jugada PGN\n\n"
        "Flecha izquierda: Mostrar la jugada PGN previa\n\n"
    )
    dpg.add_child('controls',height=c_board.size)
    dpg.add_button('Peon',callback=control_button)
    dpg.add_button('Torre',callback=control_button)
    dpg.add_button('Caballo',callback=control_button)
    dpg.add_button('Alfil',callback=control_button)
    dpg.add_button('Reina',callback=control_button)
    dpg.add_button('Rey',callback=control_button)
    dpg.add_button('Eliminar Pieza',callback=control_button)
    dpg.add_button('Añadir flecha',callback=control_button)
    dpg.add_button('Eliminar flecha',callback=control_button)
    dpg.add_button('Colorear casilla',callback=control_button)
    dpg.add_button('Descolorear casilla',callback=control_button)
    dpg.add_text(controles)
    dpg.end()

    dpg.set_value('drawing_color',[0,0,0])
    name = "Nombre de Archivo"
    dpg.add_input_text(name, width=250, source='save_name')
    name = "Nombre de Imagen"
    dpg.add_input_text(name, width=250, source='save_img_name')
    dpg.add_button("Limpiar tablero", callback=clean_callback)
    name = "Tablero por defecto"
    dpg.add_button(name, callback=default_board_callback)

    name = "Acción"
    dpg.add_label_text(name, default_value='Sin seleccionar', source="accion")
    dpg.add_label_text("Pieza", default_value='Sin seleccionar', source="pieza")
    dpg.add_label_text("Color de pieza", default_value='Blanco', source='color_piece')
    c_board.draw_board()

    dpg.set_key_press_callback(key_press_callback)
    dpg.set_mouse_click_callback(mouse_click_callback)

    dpg.start_dearpygui()

if __name__ == '__main__':
    main()
    # pars = Parser()
    # pars.get_plays('reference/Kasparovs_Game_short.pgn')
