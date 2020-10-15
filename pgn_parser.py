from utils import is_number

class Parser:
    class Play:
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
            self.pieces_del = [] # se guarda la pieza que se elimino en dado movimiento
            self.current_move = 0
            self.current_color = 'b'

        def next_position(self):
            pass

        def previews_position(self):
            pass

        def mov_valido(self,pos1,pos2,piece,color):
            col = pos1[0]
            row = pos1[1]
            recursive = False
            if piece == 'P':
                if color == 'n':
                    directions = [(0,1),(-1,1),
                    (1,1),]
                    if row == 1:
                        directions.append((0,2))
                if color == 'b':
                    directions = [(0,-1),(-1,-1),
                    (1,-1),]
                    if row == 6:
                        directions.append((0,-2))
            if piece == 'R':
                directions = [(0,1),(-1,1),
                (1,1),(0,-1),(-1,-1),
                (1,-1),(-1,0),(1,0)]
                if col == 4 and row == 7 and color == 'b':
                    directions.append((2,0))
                    directions.append((-3,0))
                if col == 4 and row == 0 and color == 'n':
                    directions.append((2,0))
                    directions.append((-3,0))
            if piece == 'D':
                recursive = True
                directions = [(0,1),(1,1),
                (1,1),(0,-1),(-1,-1),
                (1,-1),(-1,0),(1,0)]
            if piece == 'T':
                recursive=True
                directions = [(0,1),(0,-1),
                (-1,0),(1,0)]
            if piece == 'A':
                recursive = True
                directions = [(1,1), (-1,1),
                (-1,-1), (1,-1)]
            if piece == 'C':
                directions=[(1,-2),(-1,-2),
                (2,1),(2,-1),(1,2),
                (-1,2),(-2,1),(-2,-1)]


            for dir in directions:
                col = pos1[0]+dir[0]
                row = pos1[1]+dir[1]

                print((col,row),dir,sep=', ')
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
                                if dir == (-3,0):
                                    lib1 = self.board[7][3] == '_E';
                                    lib2 = self.board[7][2] == '_E';
                                    if lib1 and lib2:
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
                                if dir == (-3,0):
                                    lib1 = self.board[0][3] == '_E';
                                    lib2 = self.board[0][2] == '_E';
                                    if lib1 and lib2:
                                        return True, -1
                                    else:
                                        break # enroque
                            if piece == 'P' and dir[0] != 0:
                                print(4.1)
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
                            print(4.2)
                            break
                        if pos2 == (col,row):
                            return True, 0
                        else:
                            print(4.3)
                            break
                    if current_piece[1]==color:
                        print(4.4)
                        break
            print(4.5)
            return False, 0

        def pgn_move(self,move,reverse=False):
            """
            Verifica que un movimiento dado en formato PGN sea valido
            y si lo es se aplica en tablero.
            Devuelve True si el movimiento pudo completarsem False de
            lo contrario
            """

            print(self.current_move//2+1,move)

            if move == 'O-O-O' or move == 'O-O':
                piece = 'R'
                if color == 'b':
                    pos1 = 'e1'
                    if move == 'O-O-O':
                        pos2 = 'b1'
                    else:
                        pos2 = 'g1'
                else:
                    pos1 = 'e8'
                    if move == 'O-O-O':
                        pos2 = 'b8'
                    else:
                        pos2 = 'g8'
            else:
                letras = 'abcdefgh'
                look_for_mate = False
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

                if move[-1] == '+':
                    look_for_mate = True
                    move = move[:-1]

                if '-' in move:
                    move_ = move.split('-')
                    pos1 = move_[0]
                    pos2 = move_[0]
                elif 'x' in move:
                    move_ = move.split('x')
                    pos1 = move_[0]
                    pos2 = move_[0]
                else:
                    pos1 = move[:2]
                    pos2 = move[2:]

            try:
                col1 = letras.find(pos1[0])
                row1 = 8-int(pos1[1])
                col2 = letras.find(pos2[0])
                row2 = 8-int(pos2[1])
                if row1 > 7 or row2 > 7:
                    print(1)
                    return False
            except Exception as e:
                print(2)
                return False

            pos1 = (col1, row1)
            pos2 = (col2, row2)

            if self.board[pos1[1]][pos1[0]][0]!=piece:
                print(3)
                return False

            valido, enroque = self.mov_valido(pos1,pos2,piece,self.current_color)
            if valido:
                if not enroque:
                    piece_del = self.board[pos2[1]][pos2[0]];
                    self.pieces_del.append(piece_del)
                    self.board[pos1[1]][pos1[0]] = '_E'
                    self.board[pos2[1]][pos2[0]] = piece+self.current_color
                else:
                    piece_del = self.board[pos2[1]][pos2[0]+enroque];
                    self.pieces_del.append(piece_del)
                    self.board[pos1[1]][pos1[0]] = 'T'+self.current_color
                    self.board[pos2[1]][pos2[0]+enroque] = piece+self.current_color
                self.print_board()
            else:
                print(4)
                return False

            if look_for_mate:
                if not play.mate(self.current_color):
                    print(5)
                    return False

            return True

        def reset_board(self):
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
        self.plays = {} # Play dict

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
        play = self.Play()
        reading_play = False
        current_move = 0
        for line in file:
            line = line.strip(' \n')

            if len(line) == 0:
                continue

            if line[0] == '[' and reading_play:
                reading_play = False
                play.reset_board()
                self.plays[play.attr["Event"]] = play
                play = self.Play()

            if line[0] == '[':
                line = line.strip('[]')
                line = line.strip(' ')
                attr, value = get_attr_val(line)
                print(attr,value)
                play.attr[attr] = value

            if line[0] == '1':
                reading_play = True

            if reading_play:
                bracket_open = False
                words = line.split(' ')
                for word in words:
                    if bracket_open:
                        if word[-1] == '}':
                            bracket_open = False
                        continue

                    if word[0] == '{':
                        bracket_open = True
                        continue
                    if word[0] in ['$!?']:
                        continue

                    move = word.slit('.')
                    num = is_number(move[0])
                    if num:
                        move = move[1]
                        if num != current_move:
                            play.current_color = 'b'
                            current_move = num
                    else:
                        move = move[0]
                    if play.pgn_move(move):
                        play.moves.append(move)
                        play.current_color = 'n'
                        play.current_move += 1
                        move = ''
                    else:
                        c_move = play.current_move//2 +1
                        text = (
                        f"Error leyendo movimiento {c_move}-{word} "
                        f"en {play.attr['Event']}"
                        )
                        print(text)
                        return False
                    else:
                        move += char


        play.reset_board()
        self.plays[play.attr["Event"]] = play

        return True

    def get_play(self,name):
        return self.play[name]
