from utils import is_number, chess_position, chess_directions

class Parser:
    class Match:
        def __init__(self):
            self.board = [['Tn','Cn','An','Dn','Rn','An','Cn','Tn'],
                          ['Pn','Pn','Pn','Pn','Pn','Pn','Pn','Pn'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['Pb','Pb','Pb','Pb','Pb','Pb','Pb','Pb'],
                          ['Tb','Cb','Ab','Db','Rb','Ab','Cb','Tb']]
            self.attr = {}
            self.moves = []
            self.pieces_del = {} # se guarda la pieza que se elimino en dado movimiento
            self.current_move = 0
            self.current_color = 'b'

        def next_position(self):
            if not self.current_move < len(self.moves) :
                return

            move = self.moves[self.current_move]
            print(move)
            self.pgn_move(move)
            self.current_color = 'n' if self.current_color == 'b' else 'b'
            size = len(self.moves)
            self.current_move += 1

        def previews_position(self):
            if not self.current_move > 0:
                return

            self.current_move -= 1
            self.current_color = 'n' if self.current_color == 'b' else 'b'
            move = self.moves[self.current_move]
            self.pgn_move(move, reverse=True)

        def find_pos1(self, move, color, piece):
            """
            Encuentra la posicion inicial de un moviemto PGN en formato
            corto
            """
            col1 = None
            row1 = None
            letras = 'abcdefgh'

            if len(move) == 3:
                if is_number(move[0]):
                    row1 = move[0]
                else:
                    col1 = move[0]

            pos2 = move[-2:]
            try:
                if col1 != None:
                    col1 = letras.find(col1)
                if row1 != None:
                    row1 = 8-int(row1)
                col2 = letras.find(pos2[0])
                row2 = 8-int(pos2[1])
                if row2 > 7:
                    return
            except Exception as e:
                return

            pos2 = (col2,row2)
            if row1 != None:
                for col in range(8):
                    if self.board[row1][col] == piece+color:
                        valido, _ = self.mov_valido((col,row1),pos2,piece,color)
                        if valido:
                            return chess_position(col,row1)

            for row in range(8):
                if col1 != None:
                    if self.board[row][col1] == piece+color:
                        valido, _ = self.mov_valido((col1,row),pos2,piece,color)
                        if valido:
                            return chess_position(col1,row)
                else:
                    for col in range(8):
                        if self.board[row][col] == piece+color:
                            valido, _ = self.mov_valido((col,row),pos2,piece,color)
                            if valido:
                                return chess_position(col,row)

        def mov_valido(self,pos1,pos2,piece,color):
            """
            Checa que el moviemto dado se valido respecto al color y pieza
            dada
            """

            col = pos1[0]
            row = pos1[1]

            directions, recursive = chess_directions(piece, color, col, row)

            for dir in directions:
                col = pos1[0]+dir[0]
                row = pos1[1]+dir[1]

                while True:
                    if col < 0 or 7 < col:
                        break
                    if row < 0 or 7 < row:
                        break
                    current_piece = self.board[row][col]
                    if current_piece == '_E':
                        if pos2 == (col,row):
                            if piece == 'R' and pos1 == (4,7) and color == 'b': # enroque
                                if dir == (2,0):
                                    lib1 = self.board[7][5] == '_E';
                                    if lib1:
                                        return True, 1
                                    else:
                                        break
                                if dir == (-2,0):
                                    lib1 = self.board[7][3] == '_E';
                                    if lib1:
                                        return True, -1
                                    else:
                                        break # enroque
                            if piece=='R' and pos1 == (4,0) and color == 'n': # enroque
                                if dir == (2,0):
                                    lib1 = self.board[0][5] == '_E';
                                    if lib1:
                                        return True, 1
                                    else:
                                        break
                                if dir == (-2,0):
                                    lib1 = self.board[0][3] == '_E';
                                    if lib1:
                                        return True, -1
                                    else:
                                        break # enroque
                            if piece == 'P' and dir[0] != 0:
                                # print('Peon - Mov diagonal a casilla vacia')
                                break
                            return True, 0
                        if recursive:
                            col += dir[0]
                            row += dir[1]
                            continue
                        else:
                            break
                    if current_piece[1] != color:
                        if piece == 'P' and dir[0] == 0:
                            # print('Peon - Mov frontal a casilla ocupada por color opuesto')
                            break
                        if pos2 == (col,row):
                            return True, 0
                        else:
                            # print('No es casilla objetivo')
                            break
                    if current_piece[1]==color:
                        # print('Casilla ocupada por pieza del mismo color')
                        break
            # print('No se encontro posicion valida')
            return False, 0

        def pgn_move(self,move,reverse=False):
            """
            Verifica que un movimiento dado en formato PGN sea valido
            y si lo es se aplica en tablero.
            Devuelve True si el movimiento pudo completarsem False de
            lo contrario
            """

            print(self.current_move//2+1,move)
            letras = 'abcdefgh'
            p_names = {'P':'',
                       'R':'K',
                       'D':'Q',
                       'T':'R',
                       'A':'B',
                       'C':'N',}
            look_for_mate = False
            is_enroque = False

            if move[-1] == '+':
                move = move[:-1]
                look_for_mate = True

            if move in ['O-O-O','O-O']:
                move_ = move
                is_enroque = True
                piece = 'R'
                if self.current_color == 'b':
                    move = 'e1'
                    if move_ == 'O-O-O':
                        move += 'c1'
                    else:
                        move += 'g1'
                else:
                    move = 'e8'
                    if move_ == 'O-O-O':
                        move += 'c8'
                    else:
                        move += 'g8'
            else:
                if move[0].islower():
                    piece = 'P'
                else:
                    piece_en = move[0]
                    move = move[1:]

                    if piece_en == 'K':
                        piece = 'R'
                    elif piece_en == 'Q':
                        piece = 'D'
                    elif piece_en == 'R':
                        piece = 'T'
                    elif piece_en == 'B':
                        piece = 'A'
                    elif piece_en == 'N':
                        piece = 'C'

            if '-' in move:
                move_ = move.split('-')
                pos1 = move_[0]
                pos2 = move_[1]
            elif 'x' in move:
                move_ = move.split('x')
                pos2 = move_[1]
                if not reverse and len(move_[0]) < 2:
                    move = ''.join(move_)
                    pos1 = self.find_pos1(move,self.current_color,piece)
                    self.moves[self.current_move] = p_names[piece]+pos1+pos2
                else:
                    pos1 = move_[0]
            else:
                pos2 = move[-2:]
                if not reverse and len(move) < 4:
                    pos1 = self.find_pos1(move,self.current_color,piece)
                    self.moves[self.current_move] = p_names[piece]+pos1+pos2
                else:
                    pos1 = move[:2]

            if not pos1:
                print(f'pos2 invalida: {move[:2]}')
                return False



            if pos1+pos2 in ['e1g1','e1c1','e8g8','e8c8']:
                is_enroque = True
                if pos2[0] == 'c':
                    enroque = 0
                else:
                    enroque = 7
                piece = 'R'
            try:
                col1 = letras.find(pos1[0])
                row1 = 8-int(pos1[1])
                col2 = letras.find(pos2[0])
                row2 = 8-int(pos2[1])
                if row1 > 7 or row2 > 7:
                    print('El valor de los renglones es mayor a 8')
                    return False
            except Exception as e:
                print('Letras de columas no validas')
                return False

            pos1 = (col1, row1)
            pos2 = (col2, row2)

            if reverse:
                piece_del = self.pieces_del[self.current_move]
                self.board[pos2[1]][pos2[0]] = piece_del
                self.board[pos1[1]][pos1[0]] = piece+self.current_color
                if is_enroque:
                    T = 'T'+self.current_color
                    self.board[pos1[1]][enroque] = T
                return True

            if self.board[pos1[1]][pos1[0]][0]!=piece:
                print('La pieza no esta en la posicion inicial dada')
                return False

            valido, enroque = self.mov_valido(pos1,pos2,piece,self.current_color)
            if valido:
                piece_del = self.board[pos2[1]][pos2[0]];
                self.pieces_del[self.current_move] = piece_del
                self.board[pos1[1]][pos1[0]] = '_E'
                self.board[pos2[1]][pos2[0]] = piece+self.current_color
                if enroque:
                    self.board[pos1[1]][pos1[0]+enroque] = 'T'+self.current_color
                    if enroque < 0:
                        self.board[pos1[1]][0] = '_E'
                    else:
                        self.board[pos1[1]][7] = '_E'

                self.print_board()
            else:
                print(f'El moviemto {move} no es valido')
                return False

            if look_for_mate:
                if not self.mate(self.current_color):
                    print(5)
                    return False

            return True

        def reset_board(self):
            self.current_color = 'b'
            self.current_move = 0
            self.board = [['Tn','Cn','An','Dn','Rn','An','Cn','Tn'],
                          ['Pn','Pn','Pn','Pn','Pn','Pn','Pn','Pn'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['_E','_E','_E','_E','_E','_E','_E','_E'],
                          ['Pb','Pb','Pb','Pb','Pb','Pb','Pb','Pb'],
                          ['Tb','Cb','Ab','Db','Rb','Ab','Cb','Tb']]

        def print_board(self):
            string = '8: '+str(self.board[0])+'\n'
            string += '7: '+str(self.board[1])+'\n'
            string += '6: '+str(self.board[2])+'\n'
            string += '5: '+str(self.board[3])+'\n'
            string += '4: '+str(self.board[4])+'\n'
            string += '3: '+str(self.board[5])+'\n'
            string += '2: '+str(self.board[6])+'\n'
            string += '1: '+str(self.board[7])+'\n'
            string += '      a     b     c     d     e     f     g     h '
            print(string)

        def mate(self, color):
            return True

    def __init__(self):
        self.matches = [] # Match dict
        self.current_match = self.Match()

    # excluir los ultimos datos de las partidas "0-1", "1/2-1/2"
    def get_plays(self,pgn_input):
        """
        Obtiene las jugadas dado un archivo en formato PGN
        """
        def get_attr_val(attr_val):
            attr = ''
            val = ''
            found_quote = False
            for c in attr_val:
                if c == '"' and found_quote:
                    return attr, val
                if c == '"':
                    found_quote = True
                    continue
                if found_quote:
                    val += c
                if not found_quote and c != ' ':
                    attr += c

        file = open(pgn_input,'r')
        match = self.Match()
        reading_play = False
        current_play = 0
        for line in file:
            line = line.strip(' \n')

            if len(line) == 0:
                continue

            if line[0] == '[' and reading_play:
                reading_play = False
                match.reset_board()
                self.matches.append(match)
                match = self.Match()

            if line[0] == '[':
                line = line.strip('[]')
                line = line.strip(' ')
                attr, value = get_attr_val(line)
                print(attr,value)
                match.attr[attr] = value

            if line[0] == '1':
                reading_play = True

            if reading_play:
                comment_open = False
                words = line.split(' ')
                for word in words:
                    if comment_open:
                        if word[-1] in '})':
                            comment_open = False
                        continue

                    if word[0] in '{(':
                        comment_open = True
                        continue

                    if word[0] in '$!?':
                        continue

                    move = word.split('.')
                    num = is_number(move[0])
                    if num:
                        move = move[1]
                        if num != current_play:
                            match.current_color = 'b'
                            current_play = num
                    else:
                        move = move[0]
                    if not move: # espacio enfrente numero de jugada
                        continue
                    if '-1' in move or '-0' in move: # resultado
                        continue
                    match.moves.append(move)
                    if match.pgn_move(move):
                        match.current_color = 'n'
                        match.current_move += 1
                    else:
                        text = (
                        f"Error leyendo "
                        f"movimiento {current_play}: {move} "
                        f"en partida {len(self.matches)}"
                        )
                        print(text)
                        return False

        match.reset_board()
        self.matches.append(match)

        return True

    def get_play(self,name):
        return self.match[name]
