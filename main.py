#Pauliina Hippula
#Secure Programming, Exercise Work

import sys

def read_file(filename):
    try:
        file = open(filename, "r")
        rows = []
        for row in file:
            rows.append(row)
        file.close()
        return rows
    except IOError:
        print("Error: Reading of file failed.")

def find_sql_queries(code):
    sql_indices = []
    for i in range(len(code)):
        if "pg_query" in code[i]:
            sql_indices.append(i)
    return sql_indices

def search_wulnerabilities(search_area):
    return True
  




def main():
    code = read_file(sys.argv[1])
    sql_indices = find_sql_queries(code)
    wulnerabilities= []        
    for i in range(len(sql_indices)):
        if i == 0:
            if search_wulnerabilities(code[0:(sql_indices[i] + 1)]):
                wulnerabilities.append(code[sql_indices[i]])
        else:
            if search_wulnerabilities(code[sql_indices[i -1], sql_indices[i + 1]]):
                wulnerabilities.append(code[sql_indices[i]])
    for row in wulnerabilities:
        print("It seems it is a Sql injection risk in row", row, sep="\n")
  
main()