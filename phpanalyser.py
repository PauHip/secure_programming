from analyser_base import Analyser_base

class PhpAnalyser(Analyser_base):

    def __init__(self):
        Analyser_base.__init__(self)
        self.__chars_to_del = [' '.encode(), ','.encode(), '.'.encode(), '('.encode(), ')'.encode(), '"'.encode(), '<'.encode(), '>'.encode(), '='.encode(), '/'.encode(), ';'.encode(), "\n".encode(), '$'.encode(), '-'.encode(), "'".encode()] #This is for finding variables that must be bound.
        self.__multichar_comment_marks = ["//".encode(), "/*".encode(), "*/".encode()]
        print("Chars to del:", self.__chars_to_del)
    
   
    def __contains_comment_marks(self, row):
        stripped_row = row.strip()
        #We have to  remove the possible space between the php tag
        # and the code and the tag itself, because of searching the comment marks.
        if stripped_row[0:5] == "<?php".encode():
            print("Php tag found")
            stripped_row = stripped_row[5:].strip()
        if stripped_row.decode()[0].encode() == "#".encode():
            return True
        for mark in self.__multichar_comment_marks:
            if mark in row:
                return True
        return False
   
    #This function removes the rows that are commented away and aren't
    # therefore part of the code to be analysed.
    def __remove_comments(self, code):
        print("Finding comments")
        print("Contains comment mark", self.__contains_comment_marks("<?php test?>".encode()))
        comment_open = False
        for row in code:
            if comment_open and (not "*/".encode() in row):
                print("Comment open")
                print("Remove", row)
                code.remove(row)
                continue
            #For some reason, we can't directly compare one character
            # of the encoded row to the encoded character, so we have to decode the row and encode the character.
            if self.__contains_comment_marks:
                print("Comment found")
                if "/*".encode() in row:
                    comment_open = True
                if "*/".encode() in row:
                    comment_open = False
                print("Removing", row)
                code.remove(row) #This row is removed without depending if the comment is multiline or not.
        return code

    #This function finds all Php code so that the code that is not in Php format doesn't go to the analysis.
    def find_php_code(self, code):
        php_code = []
        php_open = False
        #print("Comment test:", self.__remove_comments(["//test".encode()]))
        #print("Original:", code)
        for row in code:
            if "<?php".encode() in row:
                print("Php found")
                php_open = True 
                #The row is added later because we need to add it always when the Php tag is open so it avoids repetition to do it only once.
            if "?>".encode() in row and php_open:
                print("Php closed")
                php_open = False
                php_code.append(row)
                continue
            print("Checking if php is open or closed")
            if php_open:
                print("Php was open")                
                php_code.append(row)
            print("Php open question passed")
        print("Code:", php_code)
        return code
        #return self.__remove_comments(php_code)
    
    #This function checks if the row contains  Sql operations so that we can decide where the Sql clauses are.
    def __contains_sql_oper(self, row):
        for oper in self.possible_opers:
            if oper.encode() in row.lower():
                return True
        return False
    
    #This function removes the characters at the start of the possible variable that must be bounded when using query parameterization.
    def __find_var_start(self, var):
        if var.decode()[0].encode() in self.__chars_to_del:
            return self.__find_var_start(var[1:]) #continues until it finds first character that can start the variable.
        return var

    #This function finds all variables that have to be bound if the query parameterization is used right.
    def __search_variables(self, splitted_command, variable_list):
        var = ""
        for possible_var in splitted_command:
            #We must decode this so that we can add its characters to the variable and compare characters.
            possible_var = self.__find_var_start(possible_var).decode()
            print("found possible var:", possible_var)
            for char in possible_var:
                print(str(char), end=" ")
                if char.encode() not in self.__chars_to_del:
                    var += char
                else:
                    print("Variable cutted")
                    print("Var:", var)
                    if var.encode() not in variable_list:
                        variable_list.append(var.encode())
                    var = ""
                    break
        return variable_list

    #This function finds which variable was bound in the binding clause.
    def __find_bound_var(self, row):
        print("Bound var:", row)
        start_index = row.index(':'.encode()) + 1 #Bounded var starts with colon.
        print("Start index", start_index)
        var = ""
        decoded_row = row.decode() #Again needed for comparisons.
        print("varchars: ", end="")
        for i in range(start_index, len(row)):
            print(row[i], end=" ")
            if decoded_row[i].encode() == "'".encode():
                var = row[start_index : i]
                break
        return var
    
    #This function finds Sql queries from the code.
    def find_sql_queries(self, code):
        print("Inside the code found function")
        query_indices = []
        inside_query = False
        query_starting_index = -1
        #print(code)
        for i in range(len(code)):
            print("Inside founding loop")
            if '"'.encode() not in code[i]:
                print("no quotes found")                
                continue #We are either middle of the query or then there isn't Sql query.
            if  self.__contains_sql_oper(code[i]):
                print("One found", code[i])
                if code[i].count('"'.encode()) == 2: #Starts and ends in this row.
                    query_indices.append(i)
                    print("Index added")
                    print("Two quotes found")
                    continue
                print("Studying if the quotes are open")
                if inside_query:
                    print("Quotes open")
                    inside_query = False #One quote and open query means that it closes now.
                    query_indices.append(query_starting_index)
                    print("Index added")
                else:
                    print("Quotes were closed")
                    inside_query = True #One quote and closed query means that a new query starts.
                    query_starting_index = i
                    print("Query starting index", query_starting_index)
        return query_indices

    #This function checks if the given query has Sql wulnerable.
    def is_sql_wulnerable(self, search_area):
        print("Inside wuln func")
        print(search_area[0])
        can_be_unwulnerable = False
        variables_to_bind = []
        bound_var_count = 0
        for i in range(len(search_area)):
            print("Inside the loop", i)
            if "prepare(".encode() in search_area[i]:
                print("Prepare found")
                can_be_unwulnerable = True
            if ':'.encode() in search_area[i] and can_be_unwulnerable: #Found some variable that is bound in somewhere else and we are inside the query.
                print("Colon found")
                possible_variables = search_area[i].split(':'.encode())
                #print("Possible vars:", possible_variables)
                variables_to_bind = self.__search_variables(possible_variables[1:], variables_to_bind) #Searching starts at index 1 because bound var starts with colon so the first index has no variables.
                print("Vars found:", variables_to_bind)
            if ("bindParam(".encode() in search_area[i]) and can_be_unwulnerable: #Bind clause inside the query
                print("Bind clause found")
                if self.__find_bound_var(search_area[i]) in variables_to_bind:
                    bound_var_count += 1
                    print("Bound var count added")
        if bound_var_count < len(variables_to_bind) or (not can_be_unwulnerable): #no prepare clause or all parameters aren't bound.
            print("concluded to be wulnerable")
            return True
        return False