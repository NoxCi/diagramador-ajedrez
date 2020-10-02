import dearpygui.core as dpg
from PIL import Image
import pickle
import copy
import os

class Board():

    def __init__(self, pieces = list()):
        self.puting_piece = False
        self.current_selection = -1
        self.piece_color = 'b'
        self.pieces = pieces
        self.size = 320
        self.piece_size = 40

    def draw_board(self):
        dpg.clear_drawing('canvas')
        board = Image.new('RGB',(320,320))
        for row in range(8):
            for colum in range(8):
                piece = self.pieces[row][colum]
                piece = '' if piece == '_E' else piece
                x = self.piece_size*colum
                y = self.piece_size*row
                if (-1)**(row+colum) == 1: # fondo blanco
                    im = Image.open(self.piece_p(str(piece)+'b'))
                else: # fondo negro
                    im = Image.open(self.piece_p(str(piece)+'n'))
                board.paste(im,(x,y))

        board.save('tmp.jpg')
        dpg.draw_image('canvas','tmp.jpg',[0,320])
        # os.remove("tmp.jpg")

    def change_box(self,piece_name, position):
        if piece_name:
            self.pieces[position[1]][position[0]] = piece_name+self.piece_color
        else:
            self.pieces[position[1]][position[0]] = '_E'

        self.draw_board()

    def get_board_position(self,m_position):
        if self.size < m_position[0] or self.size < m_position[1]:
            return

        pos = (int((m_position[0]-10)//40), int((m_position[1]+10)//40))
        return pos

    def piece_p(self,name):
        path = 'images/piezas-ajedrez/'
        return path + name + '.jpg'

    def get_marroquin_row(self,row):
        str = ''
        m_p = ''
        for colum in range(8):
            piece = self.pieces[row][colum]

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
            if (-1)**(row+colum) == (-1): # fondo negro
                if piece == '_E':
                    m_p = '+'
                m_p = m_p.upper()

            str += m_p
        return str

    def save_board(self):
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
                     ['Pb','Pb','Pb','Pb','Pb','_E','Pb','Pb'],
                     ['Tb','Cb','Ab','Db','Rb','Ab','Cb','Tb']]

    def mouse_click_callback(sender,data):
        nonlocal c_board

        if data == 0 and c_board.puting_piece:
            m_position = dpg.get_mouse_pos()
            position = c_board.get_board_position(m_position)

            if not position:
                return

            if c_board.current_selection == dpg.mvKey_1:
                c_board.change_box('P', position) # put peon
            if c_board.current_selection == dpg.mvKey_2:
                c_board.change_box('T', position) # put toker
            if c_board.current_selection == dpg.mvKey_3:
                c_board.change_box('C', position) # put horse
            if c_board.current_selection == dpg.mvKey_4:
                c_board.change_box('A', position) # put bishop
            if c_board.current_selection == dpg.mvKey_5:
                c_board.change_box('D', position) # put queen
            if c_board.current_selection == dpg.mvKey_6:
                c_board.change_box('R', position) # put king
            if c_board.current_selection == dpg.mvKey_D:
                c_board.change_box(None,position) # remove


        if data == 1:
            if c_board.piece_color == 'b':
                c_board.piece_color = 'n'
                dpg.set_value("color", "Negro")
            else:
                 c_board.piece_color = 'b'
                 dpg.set_value("color", "Blanco")

    def key_press_callback(sender, data):
        nonlocal c_board

        if c_board.current_selection == data:
            c_board.current_selection = -1
            c_board.puting_piece = False
            dpg.set_value("accion", "Sin seleccionar")
            dpg.set_value("pieza", "Sin seleccionar")
            return

        if 48 < data and data < 55:
            dpg.set_value("accion", "Añadiendo Pieza")
        if data == dpg.mvKey_1:
            dpg.set_value("pieza", "Peon")
        if data == dpg.mvKey_2:
            dpg.set_value("pieza", "Torre")
        if data == dpg.mvKey_3:
            dpg.set_value("pieza", "Caballo")
        if data == dpg.mvKey_4:
            dpg.set_value("pieza", "Alfil")
        if data == dpg.mvKey_5:
            dpg.set_value("pieza", "Reina")
        if data == dpg.mvKey_6:
            dpg.set_value("pieza", "Rey")
        if data == dpg.mvKey_D:
            dpg.set_value("accion", "Eliminando Pieza")
            dpg.set_value("pieza", "Sin seleccionar")

        c_board.puting_piece = True
        c_board.current_selection = data

    def load_callback(sender, data):
        def apply_selected_file(sender, data):
            nonlocal c_board
            inp = open(data[1],'rb')
            load_board = pickle.load(inp)
            inp.close()
            c_board = load_board
            c_board.draw_board()

        dpg.open_file_dialog(callback=apply_selected_file, extensions=".sv")

    def save_callback(sender, data):
        nonlocal c_board

        c_board.save_board()

    def save_image_callback(sender,data):
        nonlocal c_board
        c_board.save_board_image()

    def clean_callback(sender, data):
        nonlocal c_board
        nonlocal empty_board
        c_board.pieces = copy.deepcopy(empty_board)
        c_board.draw_board()

    def deafult_board_callback(sender, data):
        nonlocal c_board
        nonlocal initial_board
        c_board.pieces = copy.deepcopy(initial_board)
        c_board.draw_board()

    def close(sender,data):
        try:
            os.remove("tmp.jpg")
        except Exception as e:
            pass

    controles =(
        "Controles\n"
        "1 : Peon\n"
        "2 : Torre\n"
        "3 : Caballo\n"
        "4 : Alfil\n"
        "5 : Reina\n"
        "6 : Rey\n"
        "D : Eliminar\n"
        "Click Derecho : Cambiar color"
    )

    c_board = Board(pieces = copy.deepcopy(empty_board))
    dpg.set_main_window_size(540,560)
    dpg.set_main_window_title('Diagramador')
    dpg.set_main_window_resizable(False)
    dpg.set_exit_callback(close)
    dpg.add_drawing("canvas", width=c_board.size,height=c_board.size)
    dpg.add_image('board_img','',source=c_board.piece_p('Abb'))
    dpg.add_same_line()
    dpg.add_text(controles)
    dpg.add_button("Cargar", callback=load_callback)
    dpg.add_button("Guardar", callback=save_callback)
    dpg.add_same_line()
    dpg.add_input_text("Nombre de Archivo", width=250, source='save_name')
    dpg.add_button("Guardar Imagen", callback=save_image_callback)
    dpg.add_same_line()
    dpg.add_input_text("Nombre de Imagen", width=250, source='save_img_name')
    dpg.add_button("Limpiar tablero", callback=clean_callback)
    dpg.add_button("Tablero por defecto", callback=deafult_board_callback)
    dpg.add_label_text("Accion", value='Sin seleccionar', source="accion")
    dpg.add_label_text("Pieza", value='Sin seleccionar', source="pieza")
    dpg.add_label_text("Color", value='Blanco', source="color")
    c_board.draw_board()

    dpg.set_key_press_callback(key_press_callback)
    dpg.set_mouse_click_callback(mouse_click_callback)

    dpg.start_dearpygui()

if __name__ == '__main__':
    main()
