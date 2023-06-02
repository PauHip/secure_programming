#Pauliina Hippula
#Secure Programming, Exercise Work

import sys
from phpanalyser import PhpAnalyser

#This function reads the file and returns its content.
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
        print("Error: Reading of file", filename, "failed.")
        return None
    except MemoryError:
        print("Error with memory.")
        return None
 
 #This function takes the filename and code and returns the analyser class based on the filetype, as well as the code which is needed because
# PhpAnalyser has to search the Php parts of it so that only them can be used.
def create_analyser(filename, code):
    #print(filename[-4:])
    analyser = None
    if filename[-4:] == ".php":
        analyser = PhpAnalyser()
        #original_code = code
        code = analyser.find_php_code(code)
        #print("Codes are the same:", code == original_code, "new code:", code)
    else:
        print("Error: Unknown file type in the file ", filename, ".", sep="")
    return  analyser, code

#Main function calls different functions and handles and prints the results.
def main():
    if len(sys.argv) != 2:
        print("Error: Wrong amount of parameters")
        return
    original_code = read_file(sys.argv[1])
    if original_code != None:
        analyser, php_code = create_analyser(sys.argv[1], original_code)
        print("Main codes the same:", php_code == original_code, "code:", php_code)
        if analyser != None:
            #print("Code read, found", len(code), "rows")
            sql_indices = analyser.find_sql_queries(php_code)
            #print("Indices passed, found", len(sql_indices))
            wulnerabilities= []        
            print("Length:", len(sql_indices))
            for i in range(len(sql_indices)):
                print("inside", i)
                is_wulnerable = False
                #print(code[sql_indices[i]])
                #We want to take the query but also things after it,
                # that is, before the next query appears, because we have to study parameter bindings as well.
                if i == len(sql_indices) - 1:
                    print("Last index")
                    is_wulnerable = analyser.is_sql_wulnerable(php_code[sql_indices[i]:])
                    print("wulnerable:", is_wulnerable)            
                elif i == 0:
                    print("i = 0")
                    is_wulnerable = analyser.is_sql_wulnerable(php_code[0:(sql_indices[1])])
                    print("wulnerable:", is_wulnerable)
                    #print("Wulnerability found")
                    #wulnerabilities.append(php_code[sql_indices[i]])
                    #print("...and added")
                else:
                    print("Middle index")
                    is_wulnerable = analyser.is_sql_wulnerable(php_code[sql_indices[i] : sql_indices[i + 1]])
                    print("wulnerable:", is_wulnerable)
                if is_wulnerable:
                    print("Wulnerability found")
                    wulnerabilities.append(php_code[sql_indices[i]])
                    #print("...and added")
            #print("Outside")
            if wulnerabilities == []:
                print("It seems all is well.")
            else:
                latest_code_index = 0 #In case there is more similar rows we must know which row to choose when searching the row number.
                for row in wulnerabilities:
                    latest_code_index += original_code[latest_code_index :].index(row) + 1
                    print("It seems it is a Sql injection risk in the Sql query starting on row ", latest_code_index, "\n", row.decode(), sep="")

main()