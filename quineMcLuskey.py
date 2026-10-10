minterms = [0, 1, 2, 4, 6, 8, 9, 11, 13, 15]

def boolToBin(boolList):
    return ''.join(['-' if bit is None else str(int(bit)) for bit in boolList])

def SOPTerm(binBools, terms = ['A', 'B', 'C', 'D']):
    return ''.join([f"{var}{"'" if not bit else ''}" for var, bit in zip(terms, binBools) if bit is not None])

def printColumn(column):
    for i in range(len(column)):
        if column[i]:
            print(i, end = '')
            for j in column[i]:
                print(f"\t{boolToBin(j)}")
                
def compare(x, y):
    return sum([a != b for a, b in zip(x, y)]) == 1 and all([(a == None) == (b == None) for a, b in zip(x, y)])

def combine(x, y):
    return tuple([a if a == b else None for a, b in zip(x, y)])

def quineMcLuskey(decMinterms):
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

    for columnI in range(len(columns)):
        print(f"Column {columnI+1}\n")
        printColumn(columns[columnI])
        print("\n")

    print("Prime Implicants:\n")
    for i in primeImplicants:
        print(boolToBin(i))
    print("\n")

    print(f"F = {' + '.join([SOPTerm(i) for i in primeImplicants])}")
    

quineMcLuskey(minterms)
