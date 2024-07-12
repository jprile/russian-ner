import re

class Annotation():

    def __init__(self, ann):
        self.terms = []
        self.relations = []

        self.__terms_to_names = {} # maps terms to names, used privately

        self.names = [] # List of tuples (name, start_col, end_col)
        self.org_alt_name_pairs = [] # Pairs of name lists. Example: ([<original_name>], [<alternate_name>])
        self.parse(ann)        

    def parse(self, ann):
        lines = ann.split('\n')

        # Separate terms from relations (T and R)
        for line in lines:
            if(line != ""):
                cols = re.split(r"[ \t]+", line)
                term = cols[0]
                type = cols[1]

                if(term[0] == "T"):
                    if(type == "PERSON"):
                        self.terms.append(cols)

                elif(term[0] == "R"):
                    if(type == "ALTERNATIVE_NAME"):
                        self.relations.append(cols)

        for term in self.terms:
            term_number = term[0]
            start_char = term[2]
            end_char = term[3]
            name = []
            for i in range (4, len(term)):
                name.append(term[i])

            self.__terms_to_names.update({term_number: name})
            self.names.append((name, start_char, end_char))
        
        for relation in self.relations:
            arg1 = relation[2]
            i1 = arg1.find(":")
            arg2 = relation[3]
            i2 = arg2.find(":")

            original_term = arg1[i1+1:len(arg1)]
            alternate_term = arg2[i2+1:len(arg2)]

            original_name = self.__terms_to_names[original_term]
            alternate_name = self.__terms_to_names[alternate_term]

            # Insert this pair into the map, indexed on the alternate name
            self.org_alt_name_pairs.append((original_name, alternate_name))

            # Add tuples for transitive relationships (e.g. if we have A-->A' and  A'-->A'', then add A-->A'')
            # for org_alt_name_pair in self.org_alt_name_pairs:
            #     A, B = org_alt_name_pair

            #     # A-->B  
            #     # original_name-->alternate_name

            #     # If, B == original_name, then we can add A-->alternate_name by transitivity

            #     if(B == original_name):
            #         # Then add in this transitive relationship
            #         self.org_alt_name_pairs.append((A, alternate_name))
                    
            #     # Otherwise, if A == alternate_name, then we can add original_name --> B by transitivity
            #     elif(A == alternate_name):
            #         self.org_alt_name_pairs.append((original_name, B))

    def get_alt_names(self, name: []):
        '''
        Given the input name, return all known aliases of that name
        '''
        alt_names = []
        for org_alt_name_pair in self.org_alt_name_pairs:
            original_name, alt_name = org_alt_name_pair
            if(name == original_name):
                alt_names.append(alt_name)

        return alt_names
