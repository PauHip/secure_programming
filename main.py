#Pauliina Hippula
#Secure Programming, Exercise Work

import sys
from phpanalyser import PhpAnalyser

def read_file(filename):
    try:
        file = open(filename, "r")
        rows = []
        for row in file:
            rows.append(row.encode())
        file.close()
        #print("Found", len(rows), "rows")
        return rows
    except IOError:
        print("Error: Reading of file failed.")
        
def create_analyser(filename):
    #print(filename[-4:])
    if filename[-4:] == ".php":
        return PhpAnalyser()
    else:
        print("Error: Unknown file type.")
        return  None

def main():
    code = read_file(sys.argv[1])
    analyser = create_analyser(sys.argv[1])
    if analyser != None:
        #print("Code read, found", len(code), "rows")
        sql_indices = analyser.find_sql_queries(code)
        #print("Indices passed, found", len(sql_indices))
        wulnerabilities= []        
        for i in range(len(sql_indices)):
            #print("inside", i)
            if i == 0:
                #print("i = 0")
                if analyser.is_sql_wulnerable(code[0:(sql_indices[i] + 1)]):
                    #print("Wulnerability found")
                    wulnerabilities.append(code[sql_indices[i]])
                    #print("...and added")
            else:
                if analyser.is_sql_wulnerable(code[sql_indices[i -1], sql_indices[i + 1]]):
                    #print("Wulnerability found")
                    wulnerabilities.append(code[sql_indices[i]])
                    #print("...and added")
        #print("Outside")
    if wulnerabilities == []:
        print("It seems all is well.")
    else:
        for row in wulnerabilities:
            print("It seems it is a Sql injection risk in row", row.decode(), sep="\n")

main()