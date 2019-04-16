import zlib
import encodings

class Test:
    def __init__(self, board):
        self.board = board

a = Test("[[{'card': Card('Blue', 'DtL-T-DtR', 2), 'img': None}, {'card': Card('Blue', 'T', 1-3), 'img': None}, {'card': Card('Blue', 'T-B', 1-3), 'img': None}, {'card': Card('Blue', 'DtL-T-DtR-R-DbR-B-DbL-L', 4), 'img': None}, {'card': Card('Blue', 'DtL-DtR-DbR-DbL', 1-3), 'img': None}], [{'card': Card('Blue', 'DtL-DtR', 1-3), 'img': None}, {'card': Card('Blue', 'R-DbR-B-DbL-L', 4), 'img': None}, {'card': Card('Red', 'L-T-R', 1-3), 'img': None}, {'card': Card('Blue', 'L-T-R-B', 1-3), 'img': None}, {'card': Card('Red', 'L-T-R', 3), 'img': None}], [{'card': Card('Red', 'T-B', 1), 'img': None}, {'card': Card('Red', 'DtL-DtR', 1-3), 'img': None}, {'card': Card('Blue', 'L-T-R-B', 2), 'img': None}, {'card': Card('Red', 'L-R', 4), 'img': None}, {'card': Card('Red', 'DtL-T-DtR-R-DbR-B-DbL-L', 3), 'img': None}], [{'card': Card('Blue', 'DtL-DtR-DbR-DbL', inf), 'img': None}, {'card': Card('Red', 'DtL-T-DtR-R-DbR-B-DbL-L', 3), 'img': None}, {'card': Card('Red', 'T', 1), 'img': None}, {'card': Card('Blue', 'L-R', 4), 'img': None}, {'card': Card('Red', 'T-B', 1), 'img': None}], [{'card': Card('Blue', 'L-T-R-B', 2), 'img': None}, {'card': Card('Red', 'R-DbR-B-DbL-L', 1-3), 'img': None}, {'card': Card('Blue', 'T-B', 1), 'img': None}, {'card': Card('Blue', 'T-B', 3), 'img': None}, {'card': Card('Red', 'DtL-DtR-DbR-DbL', 2), 'img': None}], [{'card': Card('Blue', 'L-T-R', 2), 'img': None}, {'card': Card('Blue', 'L-T-R', 2), 'img': None}, {'card': Card('Red', 'DtL-DtR', 3), 'img': None}, {'card': Card('Red', 'DtL-T-DtR', 1-2), 'img': None}, {'card': Card('Blue', 'T-B', 1), 'img': None}], [{'card': Card('Red', 'DtL-DtR', 4), 'img': None}, {'card': Card('Blue', 'DtL-T-DtR', 1), 'img': None}, {'card': Card('Blue', 'DtL-T-DtR-R-DbR-B-DbL-L', 3), 'img': None}, {'card': Card('Red', 'DtL-DtR-DbR-DbL', 1), 'img': None}, {'card': Card('Red', 'DtL-T-DtR-R-DbR-B-DbL-L', 1-2), 'img': None}], [{'card': Card('Red', 'DtL-DtR', 1), 'img': None}, {'card': Card('Red', 'DtL-DtR-DbR-DbL', 1-3), 'img': None}, {'card': Card('Red', 'L-T-R-B', 1-2), 'img': None}, {'card': Card('Red', 'L-R', 2), 'img': None}, {'card': Card('Red', 'DtL-T-DtR-R-DbR-B-DbL-L', 1-2), 'img': None}]]"
)

r = a.encode()
f = zlib.compress()


print(f)