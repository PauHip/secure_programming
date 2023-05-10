from analyser_base import Analyser_base

class PhpAnalyser(Analyser_base):

#    def __init(self, code):
#        Analyser_base.__init__(code)

    def __contains_sql_oper(self, row):
        for oper in self.possible_opers:
            if oper.encode() in row:
                return True
        return False

    def __search_variables(splitted_command):
        variables = []
        chars_to_del = [' '.encode(), ','.encode(), '.'.encode(), '('.encode(), ')'.encode(), '"'.encode(), '<'.encode(), '>'.encode(), '=',encode(), '/'.encode()]
        for possible_var in splitted_command:
            if possible_var[0] in chars_to_del:
                possible_var = possible_var[1:]
            for char in possible_var:
                if char in chars_to_del:
                    variables.append(possible_var)
        return variables

    def __find_bound_var(self, row):
        start_index = row.index(':'.encode())
        var = ""
        for i in range(start_index, len(row)):
            if row[i] == "'".encode():
                break
            else:
                var += row[i]
        return var
    
    def find_sql_queries(self, code):
        #print("Inside the code found function")
        query_indices = []
        are_quotes_open = False
        query_starting_index = -1
        #print(code[0])
        for i in range(len(code)):
            #print("Inside founding loop")
            if  self.__contains_sql_oper(code[i]):
                #print("One found")
                if '"'.encode() not in code[i]:
                    continue
                    #print("no quotes found")
                else:
                    if code[i].count('"'.encode()) == 2:
                        query_indices.append(i)
                        #print("Two quotes found")
                    else:
                        #print("Studying if the quotes are open")
                        if are_quotes_open:
                            #print("Quotes open")
                            are_quotes_open = False
                            query_indices.append(query_starting_index)
                        else:
                            #print("Quotes were closed")
                            are_quotes_open = True
                            query_starting_index = i
        return query_indices

    def is_sql_wulnerable(self, search_area):
        #print("Inside wuln func")
        can_be_unwulnerable = False
        variables_to_bind = []
        bound_var_count = 0
        for i in range(len(search_area) - 1):
            if "prepare(".encode() in search_area[i]:
                can_be_unwulnerable = True
                possible_variables = search_area[i].split(':'.encode())
                variables_to_bind = self.__search_variables(possible_variables[1:])
            elif ("bindParam(".encode() in search_area[i]) and can_be_unwulnerable:
                if self.__find_bound_var(search_area[i]) in variables_to_bound:
                    bound_var_count += 1
            else:
                continue
                if bound_param_count == len(variables_to_bind):
                    return False        
        return True