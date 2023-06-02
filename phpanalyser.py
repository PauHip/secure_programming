from analyser_base import Analyser_base

class PhpAnalyser(Analyser_base):

    def __init__(self):
        Analyser_base.__init__(self)
        self.__chars_to_del = [' '.encode(), ','.encode(), '.'.encode(), '('.encode(), ')'.encode(), '"'.encode(), '>'.encode(), ';'.encode(), "\n".encode(), '$'.encode(), '-'.encode(), "'".encode()] #This is for finding starts and ends of the variables that must be bound.
    
    #This function finds all Php code so that the code that is not in Php format doesn't go to the analysis.
    def find_php_code(self, code):
        php_code = []
        php_open = False
        for row in code:
            if "<?php".encode() in row:
                php_open = True 
                #The row is added later because we need to add it always when the Php tag is open so it avoids repetition to do it only once.
            if "?>".encode() in row and php_open:
                php_open = False
                php_code.append(row)
                continue
            if php_open:
                php_code.append(row)
        return php_code
    
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
            for char in possible_var:
                if char.encode() not in self.__chars_to_del:
                    var += char
                else:
                    if var.encode() not in variable_list:
                        variable_list.append(var.encode())
                    var = ""
                    break
        return variable_list

    #This function finds which variable was bound in the binding clause.
    def __find_bound_var(self, row):
        start_index = row.index(':'.encode()) + 1 #Bounded var starts with colon.
        var = ""
        decoded_row = row.decode() #Again needed for comparisons.
        for i in range(start_index, len(row)):
            if decoded_row[i].encode() == "'".encode():
                var = row[start_index : i]
                break
        return var
    
    #This function finds Sql queries from the code.
    def find_sql_queries(self, code):
        query_indices = []
        inside_query = False
        query_starting_index = -1
        for i in range(len(code)):
            if '"'.encode() not in code[i]:
                continue #We are either middle of the query or then there isn't Sql query.
            if  self.__contains_sql_oper(code[i]):
                if code[i].count('"'.encode()) == 2: #Starts and ends in this row.
                    query_indices.append(i)
                    continue
                if inside_query:
                    inside_query = False #One quote and open query means that it closes now.
                    query_indices.append(query_starting_index)
                else:
                    inside_query = True #One quote and closed query means that a new query starts.
                    query_starting_index = i
        return query_indices

    #This function checks if the given query has Sql wulnerable.
    def is_sql_wulnerable(self, search_area):
        can_be_unwulnerable = False
        variables_to_bind = []
        bound_var_count = 0
        for i in range(len(search_area)):
            if "prepare(".encode() in search_area[i]:
                can_be_unwulnerable = True
            if ':'.encode() in search_area[i] and can_be_unwulnerable: #Found some variable that is bound in somewhere else and we are inside the query.
                possible_variables = search_area[i].split(':'.encode())
                #Searching starts at index 1 because bound var starts with colon so the first index has no variables.
                variables_to_bind = self.__search_variables(possible_variables[1:], variables_to_bind)
            if ("bindParam(".encode() in search_area[i]) and can_be_unwulnerable: #Bind clause inside the query
                if self.__find_bound_var(search_area[i]) in variables_to_bind:
                    bound_var_count += 1
        if bound_var_count < len(variables_to_bind) or (not can_be_unwulnerable): #no prepare clause or all parameters aren't bound.
            return True
        return False