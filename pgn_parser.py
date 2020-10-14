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
                    directions = [(0,1),(1,1),
                    (1,1),]
                    if row == 1:
                        directions.append((0,2))
                if color == 'b':
                    directions = [(0,-1),(-1,-1),
                    (1,-1),]
                    if row == 6:
                        directions.append((0,-2))
            if piece == 'R':
                directions = [(0,1),(1,1),
                (1,1),(0,-1),(-1,-1),
                (1,-1),(-1,0),(1,0)]
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
                directions = [(1,1), (1,1),
                (-1,-1), (1,-1)]
            if piece == 'C':
                directions=[(1,-2),(-1,-2),
                (2,1),(2,-1),(1,2),
                (-1,2),(-2,1),(-2,-1)]


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
                            if piece == 'P' and dir[0] != 0:
                                print(3.1)
                                return False
                            return True
                        if recursive:
                            col += dir[0]
                            row += dir[1]
                        else:
                            break
                    if current_piece[1] != color:
                        print(col,row,current_piece,color)
                        if pos2 == (col,row):
                            return True
                        else:
                            print(3.2)
                            return False
                    if current_piece[1]==color:
                        print(3.3)
                        return False
            print(3.4)
            return False

        def pgn_move(self,move,reverse=False):
            """
            Verifica que un movimiento dado en formato PGN sea valido
            y si lo es se aplica en tablero.
            Devuelve True si el movimiento pudo completarsem False de
            lo contrario
            """

            print(move)
            letras = 'abcdefgh'
            look_for_mate = False
            if move[0].islower():
                piece = 'P'
                pos1 = move[:2]
                pos2 = move[2:4]
            else:
                piece_en = move[0]
                pos1 = move[1:3]
                pos2 = move[3:5]

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

            try:
                col1 = letras.find(pos1[0])
                row1 = 8-int(pos1[1])
                col2 = letras.find(pos2[0])
                row2 = 8-int(pos2[1])
                if row1 > 7 or row2 > 7:
                    print(1)
                    return False
            except Exception as e:
                return False

            pos1 = (col1, row1)
            pos2 = (col2, row2)

            print(self.board[pos1[1]][pos1[0]][0])
            if self.board[pos1[1]][pos1[0]][0]!=piece:
                print(2)
                return False

            if self.mov_valido(pos1,pos2,piece,self.current_color):
                piece_del = self.board[pos2[1]][pos2[0]];
                self.pieces_del.append(piece_del)
                self.board[pos1[1]][pos1[0]] = '_E'
                self.board[pos2[1]][pos2[0]] = piece
                print(self.board)
            else:
                print(3)
                return False

            if look_for_mate:
                if not play.mate(self.current_color):
                    print(4)
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
        current_play = 0
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
                words = line.split(' ')
                bracket_open = False
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

                    word = word.strip('.')
                    num = is_number(word)
                    if num:
                        if num != current_play:
                            play.current_color = 'b'
                            current_play = num
                    else:
                        if play.pgn_move(word):
                            play.moves.append(word)
                            play.current_color = 'n'
                            play.current_move += 1
                        else:
                            c_move = play.current_move
                            text = (
                            f"Error leyendo movimiento {c_move}-{word} "
                            f"en {play.attr['Event']}"
                            )
                            print(text)
                            return False

        play.reset_board()
        self.plays[play.attr["Event"]] = play

        return True

    def get_play(self,name):
        return self.play[name]
