import copy, time

def main():
    loop = True
    matrix = []

    # matrix size
    dim = input(f"Enter matrix size(integer): ")
    if not dim.isdigit():
        print(Error.InvalidInteger.msg)
        return True
    elif dim == '1':
        print(Error.InvalidSize.msg)
        return True

    # rows input
    rows = int(dim)
    len_ = rows
    for r in range(1, rows + 1):
        invalid = True
        while invalid:
            eq = input(f"Please Enter Row {r}: ").strip(' ')
            if ' ' in eq and eq.count(' ') == len_ - 1 and all([True if isfloat(n) else False for n in eq.split(' ')]):
                e = []
                for n in eq.split(' '):
                    e.append(float(n))
                matrix.append(e)
                invalid = False
            else:
                print(Error.InvalidRowInput.msg(len_))

    # instance of a matrix
    m = SquareMatrix(matrix, rows)

    # OPERATION LOOP
    while 1:
        print(f'{"-" * 40}\n\n'
               'Your Matrix: ')
        m.print_(matrix)
        op = input("Choose operation: ------------------\n"
                    "1. Solve Determinant (cofactor method)\n"
                    "2. Solve Determinant (upper triangular method)\n"
                    "3. Find Cofactor\n"
                    "4. Enter new Matrix\n"
                    "5. Exit Program\n\n"
                    "Choice: ")
        if op == '1':
            print(f'\n{"-" * 40}')
            print(f'\n{"-" * 40}\n'
                   'FINAL ANSWER (DETERMINANT):\n'
                  f'det(matrix) =', simplify(m.determinant()), end='\n\n')

        elif op == '2':
            print(f'{"-" * 40}\n'
                    'FINAL ANSWER (DETERMINANT):\n'
                   f'det(matrix) =', simplify(m.det_shortcut()), end='\n\n')

        elif op == '3':
            cof = input('Enter cofactor (i, j) seperated by space: ')
            if ' ' in cof and cof.count(' ') == 1 and all([True if n.isdecimal() else False for n in cof.split(' ')]):
                cof = [int(s) for s in cof.split(' ')]
                row, col = tuple(cof)
                print(f'{"-" * 40}\n'
                      'FINAL ANSWER (COFACTOR):\n'
                      f'det(cof(matrix({row}, {col})) = {m.cofactor(row, col)}', end='\n\n')

            else:
                print(Error.InvalidCofactor.msg)
                
        elif op == '4':
            return True
        
        elif op == '5':
            return False
        else:
            print(Error.InvalidChoice.msg)
            time.sleep(1)
            continue
        time.sleep(2)
    return loop

class SquareMatrix:
    def __init__(self, matrix, dim):
        self.init = matrix
        self.dim = dim
        self.matrix = self.init

    # determinant of 2x2
    def solve_2x2(self):
        m = self.matrix
        a = m[0][0]; d = m[-1][-1]
        b = m[0][-1]; c = m[-1][0]
        ad = a * d; bc = b * c        
        ans = ad - bc

        print(f'det(matrix) = ({a})({d})-({b})({c})')
        print(f'det(matrix) = ({ad})-({bc})')
        print(f'det(matrix) = {simplify(ans)}')
        return ans
    
    # cofactor of a matrix
    def cofactor(self, row, col):
        cof = []; i = 1
        for r in self.init:
            rows = []; j = 1
            if i != row:
                for v in r:
                    if j != col: 
                        rows.append(v)
                    j += 1
                cof.append(rows)
            i += 1
        
        m = SquareMatrix(cof, self.dim - 1)
        determinant = m.determinant()
        print('\ncof(matrix(i, j)):')
        self.print_(cof)
        return determinant

    # solve using cofactors
    def determinant(self):
        d = None
        if self.dim == 2:
            d = self.solve_2x2()
        else:
            matrix = self.init
            multiplier = 0
            
            mults = []; i = 0
            for c in matrix[0]:
                multiplier = c
                if i % 2 == 1:
                    multiplier *= -1
                i += 1
                mults.append(multiplier)

            matrices = []
            for col in range(self.dim):
                reduced = []
                for r in matrix[1:]:
                    row = []
                    current = 0
                    for c in r:
                        if col != current:
                            row.append(c)
                        current += 1
                    reduced.append(row)
                matrices.append(reduced)
            
            prods = []; i = 0
            for reduced in matrices:
                  dim = self.dim - 1
                  print('multiplier: ', mults[i])
                  reduced_matrix = SquareMatrix(reduced, dim)
                  print('reduced:')
                  reduced_matrix.print_(reduced)

                  prod = reduced_matrix.determinant() * mults[i]
                  prods.append(prod)
                  i += 1

            d = sum(prods)
            p = ['('+str(simplify(n))+')'for n in prods]
            print(f'\ndet += {"+".join(p).strip("+")}', end = '')
        return d

    # solve using upper triangular 
    def det_shortcut(self):
        matrix = copy.deepcopy(self.init)
        determinant = 1

        for x in range(len(matrix)):
            for y in range(x + 1, len(matrix)):
                row = SquareMatrix.new_row(matrix[x], matrix[y][x], x)
                for z in range(len(row)):
                    matrix[y][z] += row[z]
        
        for x in range(len(matrix)):
            determinant *= matrix[x][x]
        
        print(f'{"-" * 40}')
        print(f'Upper triangle matrix form:')
        self.print_(matrix)
        return determinant

    @staticmethod
    def new_row(row, num, index):
        new_row = row[:]
        multiplier = 0
        for x in range(len(row)):
            if row[x] == 0:
                multiplier = 0
            if x == index:
                if row[x] == 0:
                    multiplier = 0
                else:
                    multiplier = -num / row[x]
            new_row[x] *= multiplier
        return new_row

    def print_(self, matrix):
        current = 0
        str_ = ""
        
        for r in matrix:
            for n in r:
                if float(n) == int(n):
                    length = len(str(int(n)))
                else:
                    length = len("%.3f" %(n))
                if length > current: 
                    current = length 
        length = current + 2
    
        for r in matrix:
            s = "|"
            for n in r:        
                if int(n) == float(n):
                    s += str(int(n)).center(length)
                else:
                    s += str("%.3f" %(n)).center(length)
            s += "|"
            str_ += s.center(length * (self.dim + 1)) + '\n'
        print(str_)
        
class Error:
    class InvalidInteger:
        msg = 'ERROR: Matrix size should be a POSITIVE INTEGER'
    class InvalidSize:
        msg = 'ERROR: Matrix size should NOT be 1'
    class InvalidRowInput:
        @staticmethod
        def msg(len_):
            return f'ERROR: Please enter {len_} numbers'
    class InvalidCofactor:
        msg = 'ERROR: Cofactor must be within the Matrix\' range'
    class InvalidChoice:
        msg = 'ERROR: Please enter from 1-5 only'

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def simplify(n):
    if int(n) == 0 and float(abs(n)) == int(n):
        n = 0
    elif float(n) == int(n):
        n = int(n)
    else:
        n = float("{0:.3f}".format(n))
    return n

if __name__ == '__main__':
    loop = True
    while loop:
        loop = main()
