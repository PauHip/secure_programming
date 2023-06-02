class Analyser_base:
    def __init__(self):    
        self.possible_opers = ["select", "insert into", "drop", "create table", "alter table", "alter column", "delete from", "update"]
    
    def find_sql_queries(self, code):
        return None
    def is_sql_wulnerable(self, search_area):
        return None