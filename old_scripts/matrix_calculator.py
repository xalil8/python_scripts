from copy import deepcopy

def matrix_sum(row1, column1, row2, column2, matrix1, matrix2):
    if row1 != row2 or column1 != column2:
        return print("ERROR")
    else:
        sum_matrix = []
        for i in range(int(row1)):
            backup_list = []
            for j in range(int(column1)):
                backup_list.append(float(matrix1[i][j]) + float(matrix2[i][j]))

            sum_matrix.append(backup_list)

        for t in range(int(row1)):
            for s in range(int(column1)):
                print(sum_matrix[t][s], end=" ")
            print(end="\n")


def multip(row1, column1, matrix1, number):
    sum_matrix = []
    for i in range(int(row1)):
        backup_list = []
        for j in range(int(column1)):
            backup_list.append(float(matrix1[i][j]) * number)

        sum_matrix.append(backup_list)

    for t in range(int(row1)):
        for s in range(int(column1)):
            print(sum_matrix[t][s], end=" ")
        print(end="\n")


def matrix_multip(row1, column1, row2, column2, matrix1, matrix2):
    sum_matrix = [[0 for i in range(int(column2))] for j in range(int(row1))]

    for i in range(int(row1)):
        for j in range(int(column2)):
            for k in range(int(column1)):
                # print(f"{sum_matrix[i][j]} = {int(sum_matrix[i][j])}+{int(matrix1[i][k])}*{int(matrix2[k][j])}")
                sum_matrix[i][j] = float(sum_matrix[i][j]) + float(matrix1[i][k]) * float(matrix2[k][j])

    for t in range(int(row1)):
        for s in range(int(column2)):
            print(float(sum_matrix[t][s]), end=" ")
        print(end="\n")


def main_diagonal():
    row1, column1 = input("Enter matrix size: > ").split()
    print("Enter matrix:")
    matrix1 = [input().split() for a in range(int(row1))]
    empty_matrix = [[0 for i in range(int(row1))] for j in range(int(column1))]

    for i in range(int(row1)):
        for j in range(int(column1)):
            empty_matrix[j][i] = matrix1[i][j]
    print("The result is:")
    for t in range(int(column1)):
        for s in range(int(row1)):
            print(float(empty_matrix[t][s]), end=" ")
        print(end="\n")


def side_diagonal():
    # 2
    row1, column1 = input("Enter matrix size: > ").split()
    print("Enter matrix:")
    matrix1 = [input().split() for a in range(int(row1))]

    empty_matrix = [[0 for i in range(int(row1))] for j in range(int(column1))]
    empty_matrix2 = [[0 for i in range(int(row1))] for j in range(int(column1))]

    for i in range(int(row1)):
        for j in range(int(column1)):
            empty_matrix[j][i] = matrix1[i][j]

    final_matrix = empty_matrix[::-1]

    for i in range(int(column1)):
        for j in range(int(row1)):
            empty_matrix2[i][j] = final_matrix[i][-1 - j]

    for t in range(int(column1)):
        for s in range(int(row1)):
            print(float(empty_matrix2[t][s]), end=" ")
        print(end="\n")


def vertical_line():
    # 3
    row1, column1 = input("Enter matrix size: > ").split()
    print("Enter matrix:")
    matrix1 = [input().split() for a in range(int(row1))]

    empty_matrix = [[0 for i in range(int(column1))] for j in range(int(row1))]

    for i in range(int(row1)):
        for j in range(int(column1)):
            empty_matrix[i][j] = matrix1[i][-1 - j]
    print("The result is:")

    for t in range(int(row1)):
        for s in range(int(column1)):
            print(float(empty_matrix[t][s]), end=" ")
        print(end="\n")


def horizontal_line():
    # 4
    row1, column1 = input("Enter matrix size: > ").split()
    print("Enter matrix:")
    matrix1 = [input().split() for a in range(int(row1))]

    empty_matrix = [[0 for i in range(int(column1))] for j in range(int(row1))]

    for i in range(int(row1)):
        empty_matrix[i] = matrix1[-1 - i]

    print("The result is:")
    for t in range(int(row1)):
        for s in range(int(column1)):
            print(float(empty_matrix[t][s]), end=" ")
        print(end="\n")


def transpose():
    key1 = 1
    while key:
        print("1. Main diagonal",
              "2. Side diagonal",
              "3. Vertical line",
              "4. Horizontal line",
              "0. Exit", sep="\n")

        key1 = int(input("Your Choice > "))

        if key1 == 1:
            main_diagonal()
            break
        elif key1 == 2:
            side_diagonal()
            break
        elif key1 == 3:
            vertical_line()
            break

        elif key1 == 4:
            horizontal_line()
            break


def smaller_matrix(original_matrix, row, column):
    new_matrix = deepcopy(original_matrix)
    new_matrix.remove(original_matrix[row])
    for i in range(len(new_matrix)):
        new_matrix[i].pop(column)
    return new_matrix


def determinant_cal(matrix):
    num_rows = len(matrix)
    for row in matrix:
        if len(row) != num_rows:
            print("not a square matrix.")
            return None
    if len(matrix) == 2:
        simple_determinant = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return simple_determinant
    elif len(matrix) == 1:
        return matrix[0][0]
    else:
        # cofactor expression
        answer = 0
        num_columns = num_rows
        for j in range(num_columns):
            cofactor = (-1) ** (0 + j) * matrix[0][j] * determinant_cal(smaller_matrix(matrix, 0, j))
            answer += cofactor
        return answer
def transposeMatrix(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

key = 1
while key:

    print("1. Add matrices",
          "2. Multiply matrix by a constant",
          "3. Multiply matrices",
          "4. Transpose matrix",
          "5. Calculate a determinant",
          "6. Inverse matrix",
          "0. Exit", sep="\n")
    key = int(input("Your Choice > "))

    if key == 1:
        row1, column1 = input("Enter size of first matrix: > ").split()
        print("Enter first matrix:")
        matrix1 = [input().split() for a in range(int(row1))]

        row2, column2 = input("Enter size of second matrix: > ").split()
        matrix2 = [input().split() for a in range(int(row2))]
        print("Enter second matrix:")
        matrix_sum(row1, column1, row2, column2, matrix1, matrix2)

    elif key == 2:
        row1, column1 = input("Enter size of matrix: > ").split()
        print("Enter matrix:")
        matrix1 = [input().split() for a in range(int(row1))]
        print("Enter constant: >")
        constant = int(input())
        multip(row1, column1, matrix1, constant)

    elif key == 3:

        row1, column1 = input("Enter size of first matrix: > ").split()
        print("Enter first matrix:")
        matrix1 = [input().split() for a in range(int(row1))]

        row2, column2 = input("Enter size of second matrix: > ").split()
        print("Enter second matrix:")
        matrix2 = [input().split() for a in range(int(row2))]

        if int(column1) != int(row2):
            print("you cant multiply these 2 matrix")
        else:
            matrix_multip(row1, column1, row2, column2, matrix1, matrix2)

    elif key == 4:
        transpose()

    elif key == 5:

        row1, column1 = input("Enter matrix size: > ").split()
        my_matrix = [[0 for i in range(int(column1))] for j in range(int(row1))]
        print("Enter matrix:")
        matrix1 = [input().split() for a in range(int(row1))]
        for i in range(int(row1)):
            for j in range(int(column1)):
                my_matrix[i][j] = float(matrix1[i][j])

        print("The result is:")
        print(determinant_cal(my_matrix))

    elif key == 6:
        row1, column1 = input("Enter matrix size: > ").split()
        my_matrix = [[0 for i in range(int(column1))] for j in range(int(row1))]
        print("Enter matrix:")
        matrix1 = [input().split() for a in range(int(row1))]
        for i in range(int(row1)):
            for j in range(int(column1)):
                my_matrix[i][j] = float(matrix1[i][j])

        print("The result is:")
        result = getMatrixInverse(my_matrix)
        for t in range(int(row1)):
            for s in range(int(column1)):
                print(result[t][s], end=" ")
            print(end="\n")
    else:
        pass
