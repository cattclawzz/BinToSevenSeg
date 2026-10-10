minterms = [0, 1, 2, 4, 6, 8, 9, 11, 13, 15]

def boolToBin(boolList):
    return ''.join(['-' if bit is None else str(int(bit)) for bit in boolList])

def SOPTerm(binBools, terms):
    return ''.join([f"{var}{"'" if not bit else ''}" for var, bit in zip(terms, binBools) if bit is not None])

def printColumn(column):
    for i in range(len(column)):
        if column[i]:
            print(i, end = '')
            for j in column[i]:
                print(f"\t{boolToBin(j)}")
                
def compare(x, y):
    return sum([a != b for a, b in zip(x, y)]) == 1 and all([(a is None) == (b is None) for a, b in zip(x, y)])

def combine(x, y):
    return tuple([a if a == b else None for a, b in zip(x, y)])

def quineMcLuskey(decMinterms, terms = ['A', 'B', 'C', 'D'], debug = False):
    binMinterms = [tuple([bool(j == '1') for j in bin(i)[2:].rjust(4, '0')]) for i in decMinterms]
    dictName = {i:False for i in binMinterms}
    column1 = [[j for j in binMinterms if sum(j) == i] for i in range(5)]

    columns = [column1]
    while True:
        columnTemp = []
        for i in range(len(columns[-1])-1):
            column2Temp = []
            for j in columns[-1][i+1]:
                for k in columns[-1][i]:
                    if compare(j,k):
                        column2Temp.append(combine(j,k))
                        dictName[j], dictName[k] = True, True
                        dictName[combine(j,k)] = False
            columnTemp.append(column2Temp)
        if not any(columnTemp):
            break
        else:
            columns.append(columnTemp)

    primeImplicants = set([i for i in dictName if not dictName[i]])

    if debug:
        for columnI in range(len(columns)):
            print(f"Column {columnI+1}\n")
            printColumn(columns[columnI])
            print("\n")

        print("Prime Implicants:\n")
        for i in primeImplicants:
            print(boolToBin(i))
        print("\n")

        print(f"F = {' + '.join([SOPTerm(i, terms) for i in primeImplicants])}")

    return ' + '.join([SOPTerm(i, terms) for i in primeImplicants])
    

binToSevenSeg = [
    [0, 2, 3, 5, 6, 7, 8, 9, 10, 12, 14, 15],   # A
    [0, 1, 2, 3, 4, 7, 8, 9, 10, 13],           # B
    [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13],    # C
    [0, 2, 3, 5, 6, 8, 9, 11, 12, 13, 14],      # D
    [0, 2, 6, 8, 10, 11, 12, 13, 14, 15],       # E
    [0, 4, 5, 6, 8, 9, 10, 11, 12, 14],         # F
    [2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15],  # G
] #Minterms

segments = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for segment, i in zip(segments, binToSevenSeg):
    print(f"{segment} = {quineMcLuskey(i, terms = ['P', 'Q', 'R', 'S'])}")
