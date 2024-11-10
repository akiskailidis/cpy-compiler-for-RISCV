#Directed by Kailidis Kyrillos

import sys

MAX_LENGTH = 30 #Max Character Length

linenum = 1

#function that reads the file
f = open(sys.argv[1], 'r')

#Lexical Analyzer    
def lex():
    global linenum
    while True:
        ch = f.read(1)
        
        if ch == '':
            return '', "eoftk"
        if ch.isspace():
            
            if ch == '\n':
                linenum = linenum + 1
            
        #Identifier
        elif ch.isalpha():
            temp = ch
            ch  = f.read(1)
            while ch != '':
                if (ch.isalpha() or ch.isdigit()) and (len(temp)<=MAX_LENGTH):
                    temp = temp + ch
                    ch  = f.read(1)
                else:
                    
                    break
                
            
            f.seek(f.tell() - 1, 0)

            #Keywords
            if (temp == 'return')or(temp == 'print')or(temp == 'def')or(temp == 'main')or(temp == 'global')or(temp == 'if')or(temp == 'else')or(temp == 'while')or(temp == 'not')or(temp == 'and')or(temp == 'or'):
                return temp, "keyword"
            else:
                return temp, "id"
            
        #Digits
        elif ch.isdigit():
            temp = ''
            while len(temp) <= MAX_LENGTH and ch.isdigit():
                temp = temp + ch
                ch  = f.read(1)
            f.seek(f.tell() - 1, 0)
            return temp, "number"
        
        #relOperations
        elif ch == '=':
            ch  = f.read(1)
            if ch == '=':
                temp = '=='
                return temp, "relOperation"
            else:
                f.seek(f.tell() - 1, 0)
                temp = '='
                return temp, "assignment"
        elif ch == '>':
            ch  = f.read(1)
            if ch == '=':
                temp = '>='
                return temp, "relOperation"
            else:
                f.seek(f.tell() - 1, 0)
                temp = '>'
                return temp, "relOperation"
        elif ch == '<':
            ch  = f.read(1)
            if ch == '=':
                temp = '<='
                return temp, "relOperation"
            else:
                f.seek(f.tell() - 1, 0)
                temp = '<'
                return temp, "relOperation"
        elif ch == '!':
            ch  = f.read(1)
            if ch == '=':
                temp = '!='
                return temp, "relOperation"
            else:
                temp = ch
                return temp, "ERROR"
                    
        #Arithmetic operations
        elif (ch == '+')or(ch == '-'):
            return ch, "addOperation"
        elif ch == '*' or ch == '%':
            return ch, "mulOperation"
            
        elif ch == '/':
            ch  = f.read(1)
            if ch == '/':
                temp = '//'
                return temp, "mulOperation"
            else:
                temp = ch
                return temp, "ERROR"

        #Delimiters
        elif (ch == ':')or(ch == ','):
            return ch, "delimiter"
            
        #Group symbols
        elif (ch == '(')or(ch == ')'):
            return ch, "groupsymbol"
        elif ch == '#':
            ch  = f.read(1)
            if (ch == '{') or (ch == '}'):
                temp = '#' + ch
                return temp, "groupsymbol"
            elif ch.isalpha():
                temp = '#' + ch
                ch  = f.read(1)
                temp = temp + ch
                ch  = f.read(1)
                temp = temp + ch
                if temp == '#int' or temp == '#def':
                    return temp, "keyword"
                else:
                    return temp, "ERROR"
            elif ch == '#':
                inComments = True
                while inComments == True:
                    ch = f.read(1)
                    if ch == '#':
                        ch = f.read(1)
                        if ch == '#':
                            inComments = False
                        elif ch == '':
                            return ch, "ERROR"
                    elif ch == '':
                        return ch, "ERROR"
            else:
                return ch, "ERROR"
    

#Syntactical Analyzer
class Syntax:
    def __init__(self):
        
        self.symbol_table = SymbolTable()
        self.int_code = Intcode(self.symbol_table)
            
    def get_token(self):
        return lex()
    
    def syntax(self):
        return self.startRule()
        
    def startRule(self):
        tk = self.get_token()
        tk = self.declarations(tk)
        tk = self.def_main_part(tk)
        tk = self.call_main_part(tk)
        
    def def_main_part(self, tk):
        while tk[0] == "def":
            tk = self.def_main_function(tk)
        return tk
    
    def def_main_function(self, tk):
        if tk[0] == "def":
            tk = self.get_token()
            if tk[1] == 'id':
                name = tk[0]
                self.symbol_table.addEntity(name, "function")
                self.symbol_table.addScope(name)
                tk = self.get_token()
                if tk[0] == "(":
                    tk = self.get_token()
                    tk = self.id_list(tk, "parameter")
                    
                    if tk[0] == ")":
                        tk = self.get_token()
                        if tk[0] == ":":
                            tk = self.get_token()
                            if tk[0] == "#{":
                                tk = self.get_token()
                                tk = self.declarations(tk)
                                tk = self.def_main_part(tk)
                                tk = self.global_decl(tk)
                                
                                starting_quad = self.int_code.nextquad()
                                self.int_code.genquad("begin_block", name, "_", "_")
                                tk = self.statements(tk)
                                
                                if tk[0] == "#}":
#                                    
                                    self.int_code.genquad("end_block", name, "_", "_")
                                    
            
                                    #delete the Scope
                                    self.symbol_table.updateEntity(name, starting_quad);
                                    firstFinalQuad = self.symbol_table.firstFinalQuad
                                    self.int_code.quadsFinal = self.int_code.quads[firstFinalQuad:]
                                    self.symbol_table.deleteScope(self.int_code.quadsFinal)
                                    tk = self.get_token()
                                    
                                    return tk
                                else:
                                    print("def_main_function(): #} not closed", linenum)
                                    sys.exit()
                            else:
                                print("def_main_function(): #{ expected ", linenum)
                                sys.exit()

                        else:
                            print("def_main_function() error: expect ':'", linenum)
                            sys.exit()
                    else:
                        print("def_main_function() error: expect ')'", linenum)
                        sys.exit()

                else:
                    print("def_main_function()error: expect '('", linenum)
                    sys.exit()
            else:
                print("def_main_function() expect an id: the name of the function", linenum)
                sys.exit()
        else:
            print("def_main_function(): expect the word 'def'", linenum)
            sys.exit()

    

    def declarations(self, tk):
        
        while tk[0] == "#int":
            tk = self.get_token()
            tk = self.id_list(tk, "variable")
            
        return tk
    
    def global_decl(self, tk):
        
        while tk[0] == "global":
            tk = self.get_token()
            tk = self.id_list(tk, "global_variable")
            
        return tk
    
    def declaration_line(self):
        tk = self.get_token()
        
        if tk[0] == "#int":
            self.id_list("variable")
        else:
            print("declaration_line(tk): #int expected", linenum)

    def statement(self, tk):
        
        if (tk[0] == "print") or (tk[0]=="return") or (tk[1]=="id"):
            tk = self.simple_statement(tk)
        elif(tk[0]=="while") or (tk[0]=="if"):
            tk = self.structured_statement(tk)
        else:
            print("statement() error: expected a keyword or an id", linenum)
        
        return tk
    
    def statements(self, tk):
        
        while (tk[1] == "id") or (tk[1]=="keyword"):
            tk = self.statement(tk)
            
        return tk

    def simple_statement(self, tk):
        if tk[1] == "id":
            tk = self.assignment_stat(tk)
        elif tk[0] == "print":
            tk = self.print_stat(tk)
        elif tk[0] == "return":
            tk = self.return_stat(tk)
        else:
            print("simple_statement() error: neither assignment nor print nor return", linenum)
        return tk

    def structured_statement(self, tk):
        if tk[0] == "if":
            tk = self.if_stat(tk)
        elif tk[0] == "while":
            tk = self.while_stat(tk)
        else:
            print("structured_statement() error: neither if nor while", linenum)
            
        return tk

    def assignment_stat(self, tk):
        
        if tk[1] == "id":
            name = tk[0]            
            tk = self.get_token()
            
            if tk[0] == "=":
                tk = self.get_token()
                if tk[0] == "int":
                    tk = self.get_token()
                    
                    if tk[0] == "(":
                        tk = self.get_token()
                        if tk[0] == "input":
                            tk = self.get_token()
                            if tk[0] == "(":
                                tk = self.get_token()
                                if tk[0] == ")":
                                    tk=self.get_token()
                                    if tk[0] == ")":
                                        tk=self.get_token()
                                        return tk 
                                    else:
                                        print("assignment_stat() error: ')' expected", linenum)
                                        sys.exit()
                                else:
                                    print("assignment_stat() error: ')' expected", linenum)
                                    sys.exit()
                           
                            else:
                                print("assignment_stat() error: '(' expected", linenum)
                                sys.exit()
                        else:
                            print("assignment_stat() error: 'input' expected", linenum)
                            sys.exit()
                    else:
                        print("assignment stat: '(' expected", linenum)
                        sys.exit()

                elif (tk[1] == "number") or (tk[1]=="id") or (tk[1] == "addOperation") or (tk[0] == '('):
                    
                    tk = self.expression(tk)
                    eplace = tk[2]
                    self.int_code.genquad(":=", eplace, "_", name)
                    return tk
                
                else:
                    print("assignment_stat() error: 'int' or '(' expected", linenum)
                    sys.exit()
            else:
                print("assignment_stat() error: '=' expected", linenum)
                sys.exit()
        else:
            print("assignment_stat error: an id expected", linenum)
                

    def print_stat(self, tk):
       
        if tk[0] == "print":
            tk = self.get_token()
            if tk[0] == "(":
                tk = self.get_token()
                tk = self.expression(tk)
                eplace = tk[2]
                
                if tk[0] == ")":
                    
                    tk=self.get_token()
                    
                    self.int_code.genquad("out", eplace, "_", "_")
                    return tk
                else:
                    print("print_stat() error: ')' expected", linenum)
                    sys.exit()
            else:
                print("print_stat() error: '(' expected", linenum)
                sys.exit()
        else:
            print("print_stat() error: 'print' expected", linenum)
            sys.exit()

    def return_stat(self, tk):
        if tk[0] == "return":
            tk = self.get_token()
            tk = self.expression(tk)
            eplace = tk[2]
            self.int_code.genquad("retv", eplace, "_", "_")
            return tk[0], tk[1]
        else:
            print("return_stat(): 'return' expected", linenum)
            sys.exit(0)


    def if_stat(self, tk):
        tk = self.get_token()
        tk = self.condition(tk)
        
        b = [tk[2], tk[3]]
        if tk[0] == ":":
            tk = self.get_token()
            self.int_code.backpatch(b[0], self.int_code.nextquad())  # b[0] == B.true
            if tk[0] == "#{":
                tk = self.get_token()
                
                tk = self.statements(tk)
                ifList = self.int_code.makelist(self.int_code.nextquad())
                self.int_code.genquad("jump", "_", "_", "_")
                self.int_code.backpatch(b[1], self.int_code.nextquad())
                
                if tk[0] == "#}":
                    tk = self.get_token()
                    
                else:
                    print("if_stat(): '#}' expected", linenum)
                    sys.exit()
            else:
                tk = self.statement(tk)
                ifList = self.int_code.makelist(self.int_code.nextquad())
                self.int_code.genquad("jump", "_", "_", "_")
                self.int_code.backpatch(b[1], self.int_code.nextquad())
                
        else:
            print("if_stat(): ':' expected", linenum)
            sys.exit(0)
            
        while tk[0] == "elif":
            tk = self.get_token()
            
            tk = self.condition(tk)
            b = [tk[2], tk[3]]
            if tk[0] == ":":
                tk = self.get_token()
                self.int_code.backpatch(b[0], self.int_code.nextquad())  # b[0] == B.true
                if tk[0] == "#{":
                    tk = self.get_token()
                    
                    tk = self.statements(tk)
                    
                    ifL = self.int_code.makelist(self.int_code.nextquad())
                    self.int_code.genquad("jump", "_", "_", "_")
                    ifList = self.int_code.merge(ifList, ifL)
                    self.int_code.backpatch(b[1], self.int_code.nextquad())
                    
                    if tk[0] == "#}":
                        tk = self.get_token()
                        
                    else:
                        print("if_stat()(elif): '#}' expected", linenum)
                        sys.exit(0)
                else:
                    tk = self.statement(tk)
                    
                    ifL = self.int_code.makelist(self.int_code.nextquad())
                    self.int_code.genquad("jump", "_", "_", "_")
                    ifList = self.int_code.merge(ifList, ifL)
                    self.int_code.backpatch(b[1], self.int_code.nextquad())
            else:
                print("if_stat(): ':' expected", linenum)
                sys.exit()
        
        if tk[0] == "else":
            tk = self.get_token()
            if tk[0] == ":":
                tk = self.get_token()
                if tk[0] == "#{":
                    tk = self.get_token()
                    
                    tk = self.statements(tk)
                    
                    if tk[0] == "#}":
                        tk = self.get_token()
                        
                    else:
                        print("if_stat(): '#}' expected", linenum)
                        sys.exit()
                else:
                    tk = self.statement(tk)
            else:
                print("if_stat()(else): ':' expected", linenum)
                sys.exit()
        self.int_code.backpatch(ifList, self.int_code.nextquad())
        return tk[0], tk[1]
    
    def while_stat(self, tk):
        tk = self.get_token()
        
        condition_start_quad = self.int_code.nextquad()
        tk = self.condition(tk)
        
        b = [tk[2], tk[3]]
        if tk[0] == ":":
            tk = self.get_token()
            self.int_code.backpatch(b[0], self.int_code.nextquad())  # b[0] == B.true
            if tk[0] == "#{":
                tk = self.get_token()
                
                tk = self.statements(tk)

                self.int_code.genquad("jump", "_", "_", condition_start_quad)
                self.int_code.backpatch(b[1], self.int_code.nextquad())
                
                if tk[0] == "#}":
                    tk = self.get_token()
                    return tk
                else:
                    print("while_stat(): '#}' expected", linenum)
                    sys.exit()
            else:
                self.int_code.backpatch(b[0], self.int_code.nextquad())  # b[0] == B.true

                tk = self.statement(tk)
                
                self.int_code.genquad("jump", "_", "_", condition_start_quad)
                self.int_code.backpatch(b[1], self.int_code.nextquad())
                return tk
                
        else:
            print("while_stat(): ':' expected", linenum)
            sys.exit(0)
        

    

    def id_list(self, tk, idtype):
        if tk[1] == "id":
            self.symbol_table.addEntity(tk[0], idtype)
            tk = self.get_token()
            while tk[0] == ",":
                tk = self.get_token()
                if tk[1] != "id":
                    print("id_list() error: id expected", linenum)
                    exit(0)
                self.symbol_table.addEntity(tk[0], idtype)
                tk = self.get_token()
        else:
            print("id_list() error: id expected", linenum)
            exit(0)
        
        return tk

    def expression(self, tk):
        tk = self.optional_sign(tk)
        tk = self.term(tk)
        
        t1place = tk[2]
        op = tk[0]
        
        if tk[1] == "addOperation":
            while tk[1] == "addOperation":
                op = tk[0]
                tk = self.get_token()
                
                tk = self.term(tk)
                t2place = tk[2]
                
                w = self.int_code.newtemp()
                self.int_code.genquad(op, t1place, t2place, w)
                t1place = w
            return tk[0], tk[1], t1place
        else:
            return tk[0], tk[1], t1place

    def term(self, tk):
        tk = self.factor(tk)
        f1place = tk[2]
        
        op = tk[0]
        if tk[1] == "mulOperation":
            
            while tk[1] == "mulOperation":
                op = tk[0]
                tk = self.get_token()
                
                tk = self.factor(tk)
                f2place = tk[2]
                w = self.int_code.newtemp()
                self.int_code.genquad(op, f1place, f2place, w)
                f1place = w
            return tk[0], tk[1], f1place
        else:
            return tk[0], tk[1], f1place
        
    def factor(self, tk):
        
        fplace = tk[0]
        if tk[1] == "number":            
            tk = self.get_token()
            
            return tk[0], tk[1], fplace
        elif tk[0] == "(":
            tk = self.get_token()
            exp = self.expression(tk)
            
            if exp[0] == ")":
                tk = self.get_token()
                print("par", tk[0], tk[1], exp[2])
                return tk[0], tk[1], exp[2]
            else:
                print("factor(): ')' expected", linenum)
                sys.exit(0)
        elif tk[1] == "id":
            
            tk = self.get_token()
           
            idtailb = self.idtail(tk, fplace)
           
            return idtailb
        else:
            print("factor() error: number, id or '(' expected", linenum)
            sys.exit()

    def idtail(self, tk, fplace):
        idtk = fplace
        if tk[0] == "(":
            tk = self.get_token()
           
            returnb = self.actual_par_list(tk, idtk)
            
            tk = [returnb[0], returnb[1]]
            if tk[0] == ")":
                tk = self.get_token()
                
                return tk[0], tk[1], returnb[2]
            else:
                print("idtail(): ')' expected", linenum)
                sys.exit(0)
        else:
            return tk[0], tk[1], fplace

    def actual_par_list(self, tk, assign):
        
        tk = self.expression(tk)
        a = tk[2]
        
        self.int_code.genquad("par", a, "CV", "_")
        
        if tk[0] == ",":
            while tk[0] == ",":
                tk = self.get_token()
                tk = self.expression(tk)
                b = tk[2]
                self.int_code.genquad("par", b, "CV", "_")
                
            ntemp = self.int_code.newtemp()
            self.int_code.genquad("par", ntemp, "RET", "_")
            self.int_code.genquad("call", assign, "_", "_")
            return tk[0],tk[1], ntemp
        else:
            ntemp = self.int_code.newtemp()
            self.int_code.genquad("par", ntemp, "RET", "_")
            self.int_code.genquad("call", assign, "_", "_")
            return tk[0],tk[1], ntemp

    def optional_sign(self, tk):
        
        if tk[1] == "addOperation":
            op = tk[0]
            tk = self.get_token()
            
            return op+tk[0], tk[1]
        else:
            return tk

    def condition(self, tk):
        b = []
        tk = self.bool_term(tk)
        b = [tk[2], tk[3]]
        
        if tk[0] == "or":
            while tk[0] == "or":
                tk = self.get_token()
                self.int_code.backpatch(b[1], self.int_code.nextquad()) #b[1] == B.false
                tk = self.bool_term(tk)
                q2 = [tk[2], tk[3]]
                b[0] = self.int_code.merge(b[0], q2[0]) #b[0] == B.true and q2[0] == Q2.true
                b[1] = q2[1]    #B.false = Q2.false
                
        return tk[0], tk[1], b[0], b[1]

    def bool_term(self, tk):
        q = []
        tk = self.bool_factor(tk)
        q = [tk[2], tk[3]]
        
        if tk[0] == "and":
            while tk[0] == "and":
                tk = self.get_token()
                self.int_code.backpatch(q[0], self.int_code.nextquad()) #symplhrwsh oswn tetradwn boroun na symplhrwthoun mesa ston kanona
                tk = self.bool_factor(tk)
                r2 = [tk[2], tk[3]]
                q[1] = self.int_code.merge(q[1], r2[1])
                q[0] = r2[0]    #Q.true = R2.true
        return tk[0], tk[1], q[0], q[1]

    def bool_factor(self, tk):
        r = []
        
        if tk[0] == "not":
            tk = self.get_token()
            tk = self.expression(tk)
            e1place = tk[2]
            
            relop = tk[0]
            if tk[1] == "relOperation":
                tk = self.get_token()
                tk = self.expression(tk)
                e2place = tk[2]
                
                r.append(self.int_code.makelist(self.int_code.nextquad()))   #r.true
                self.int_code.genquad(relop, e1place, e2place, "_")
                r.append(self.int_code.makelist(self.int_code.nextquad()))   #r.false
                
                self.int_code.genquad("jump", "_", "_", "_")
                return tk[0], tk[1], r[1], r[0] 
            else:
                print("bool_factor() error: relOperation expected", linenum)
                exit(0)
        else:
            tk = self.expression(tk)
            e1place = tk[2]
            
            relop = tk[0]
            if tk[1]=="relOperation":
                tk = self.get_token()
                tk = self.expression(tk)
                e2place = tk[2]
                
                
                r.append(self.int_code.makelist(self.int_code.nextquad()))   #r.true
                self.int_code.genquad(relop, e1place, e2place, "_")
                r.append(self.int_code.makelist(self.int_code.nextquad()))   #r.false
                
                self.int_code.genquad("jump", "_", "_", "_")
                return tk[0], tk[1], r[0], r[1] 
            else:
                print("bool_factor() error: relOperation expected", linenum)
                sys.exit(0)

    
    def call_main_part(self, tk):
        self.int_code.genquad("begin_block", "main", "_", "_")
        if tk[0] == "#def":
            tk = self.get_token()
            if tk[0] == "main":
                tk = self.get_token()
                tk = self.declarations(tk)
                tk = self.statements(tk)
                self.int_code.genquad("halt", "_", "_", "_")
                self.int_code.genquad("end_block", "main", "_", "_")
                firstFinalQuad = self.symbol_table.firstFinalQuad
                self.int_code.quadsFinal = self.int_code.quads[firstFinalQuad:]
                self.symbol_table.deleteScope(self.int_code.quadsFinal)
                return True
            else:
                print("call_main_part(): 'main' expected", linenum)
                sys.exit(0)
        else:
            print("call_main_part() error: '#def' expected", linenum)
            sys.exit(0)




#Intermediate Code
class Intcode:
    def __init__(self, symbol_table):
        self.quads = []                     # quads table
        self.quadsFinal = []                # final quads table
        self.nquad = 0                      # number of quads already created
        self.ntemp = 0                      # number of temp variables so far
        self.symbol_table = symbol_table
        
    #returns the number of the next quad to be produced
    def nextquad(self):
        return self.nquad

    #creates the next quad
    def genquad(self, op, x=None, y=None, z=None):
        quad = (op, x, y, z)
        self.quads.append(quad)
        self.nquad = self.nquad + 1
        return quad

   #creates and returns a new temp 
    def newtemp(self):
        self.ntemp = self.ntemp + 1
        temp = f"T_{self.ntemp}"
        self.symbol_table.addEntity(temp, "temp_variable")
        return temp

    #creates an empty list
    def emptylist(self):
        return []

    #creates a list containing only "x"
    def makelist(self, x):
        return [x]

    #merges two lists and returns them
    def merge(self, list1, list2):
        return list1 + list2

    #visits the quads one by one and completes them with the label z
    def backpatch(self, list1, z):
        
        for i in range(len(list1)):
            listq = list(self.quads[list1[i]])
            listq[3] = z
            self.quads[list1[i]] = tuple(listq)

    def printquads(self):
        o = open(sys.argv[1] + ".int", "w")                                 # Write the results in a file
        for i in range(len(self.quads)):
            k = i
            #print(k, ":", self.quads[i])
            o.write(str(k) + ":" + str(self.quads[i]) + "\n")
        

class Entity:
    def __init__(self, name, etype, offset):
        self.name = name
        self.etype= etype
        self.offset = offset
        self.framelength = None
        self.starting_quad = None
        self.par = []

class Scope:
    def __init__(self, name, nestinglevel):
        self.symtable = {}
        self.name = name
        self.nestinglevel = nestinglevel
        self.enoffset = 12
        
    def addEntity(self, name, etype):
        if name in self.symtable:
            print("addEntity(): ", name, " already in symtable ", linenum)
            sys.exit(0)
        offset = 0
        if etype != "function" and etype != "global_variable":
            offset = self.enoffset
            self.enoffset += 4            
        entity = Entity(name, etype, offset)
        self.symtable[name] = entity
    
    def updateEntity(self, name, starting_quad, framelength):
        entity = self.symtable[name]
        entity.framelength = framelength
        entity.starting_quad = starting_quad
        
class SymbolTable:
    def __init__(self):
        self.quads = []
        self.scopes = [Scope("main", 0)]
        self.nquad = 0
        self.firstFinalQuad = 0                             # tracks the first quad in final code
        self.outfileS = open(sys.argv[1] + ".sym", "w")
        self.outfile = open(sys.argv[1] + ".asm", "w")
        self.outfile.write(".data\n")
        self.outfile.write("str_nl: .asciz \"\\n\"\n")
        self.outfile.write(".text\n")
        self.outfile.write("j Lmain\n")
        
        
    def addEntity(self, name, etype):
        self.scopes[-1].addEntity(name, etype)
        

    def addScope(self, name):
        nestinglevel = len(self.scopes)
        self.scopes.append(Scope(name, nestinglevel))

    def deleteScope(self, quads):
        self.printTable()
        
        
        self.quads = quads
        self.firstFinalQuad = self.firstFinalQuad + len(quads)
        
        self.toFinal()
        
        self.scopes.pop()
    
    def gnlvcode(self, v):
        search = self.searchEntity(v)
        if search[0].etype == "function":
            print("call_main_part(): function was not expected", linenum)
            sys.exit(0)
            
        offset = search[0].offset
        nestingLevel1 = search[2]
        nestingLevel = len(self.scopes) - 1
        
        
        self.outfile.write("lw t0, -4(sp)\n")
        for i in range(nestingLevel - nestingLevel1 - 1):
            self.outfile.write("lw t0, -4(t0)\n")
        
        
        self.outfile.write("addi t0, t0, -" +str(offset) + "\n")
    
    def loadvr(self, v, r):
        if v.isdigit() or v[0] == '+' or v[0] == '-':
            self.outfile.write("li " + str(r) +  ", " + str(v) + "\n")
        else:
            search = self.searchEntity(v)
            if search[0].etype == "function":
                print("call_main_part(): function was not expected", linenum)
                sys.exit(0)
                
            offset = search[0].offset
            nestingLevel1 = search[2]
            nestingLevel = len(self.scopes) - 1
            
            if nestingLevel == nestingLevel1: 
                self.outfile.write("lw " + r +  ", -" + str(offset) + "(sp)\n")
            elif nestingLevel1 == 0: 
                self.outfile.write("lw " + r +  ", -" + str(offset) + "(gp)\n")
            else:
                self.gnlvcode(v)
                self.outfile.write("lw " + r +  ", 0(t0)\n")


    def storerv(self, r, v):
        search = self.searchEntity(v)
        if search[0].etype == "function":
            print("call_main_part(): function was not expected", linenum)
            sys.exit(0)
            
        offset = search[0].offset
        nestingLevel1 = search[2]
        nestingLevel = len(self.scopes) - 1
        
        if nestingLevel == nestingLevel1:
            self.outfile.write("sw " + r +  ", -" + str(offset) + "(sp)\n")
        elif nestingLevel1 == 0:
            self.outfile.write("sw " + r +  ", -" + str(offset) + "(gp)\n")
        else:
            self.gnlvcode(v)
            self.outfile.write("sw " + r +  ", 0(t0)\n") 
    
    def toFinal(self):
        parOffset = 12  # Offset for parameters in the stack frame

        for i in range(len(self.quads)):
            k = self.nquad  # Current quad number
            self.nquad = self.nquad + 1  # Increment quad counter

            # Write the label for the current quad
            self.outfile.write("L" + str(k) + ":\n")

            # Handle different types of quads
            if self.quads[i][0] == "jump":
                # Unconditional jump
                self.outfile.write("j L" + str(self.quads[i][3]) + "\n")
            
            elif self.quads[i][0] == "=":
                # Conditional jump if equal
                self.loadvr(self.quads[i][1], "t1")  # Load first operand into t1
                self.loadvr(self.quads[i][2], "t2")  # Load second operand into t2
                self.outfile.write("beq t1, t2 L" + str(self.quads[i][3]) + "\n")
            
            elif self.quads[i][0] == "<>":
                # Conditional jump if not equal
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("bne t1, t2 L" + str(self.quads[i][3]) + "\n")
            
            elif self.quads[i][0] == ">":
                # Conditional jump if greater than
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("bgt t1, t2 L" + str(self.quads[i][3]) + "\n")
            
            elif self.quads[i][0] == "<":
                # Conditional jump if less than
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("blt t1, t2 L" + str(self.quads[i][3]) + "\n")
            
            elif self.quads[i][0] == ">=":
                # Conditional jump if greater than or equal
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("bge t1, t2 L" + str(self.quads[i][3]) + "\n")
            
            elif self.quads[i][0] == "<=":
                # Conditional jump if less than or equal
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("ble t1, t2 L" + str(self.quads[i][3]) + "\n")
            
            elif self.quads[i][0] == ":=":
                # Assignment
                self.loadvr(self.quads[i][1], "t1")  # Load the value into t1
                self.storerv("t1", self.quads[i][3])  # Store the value from t1
            
            elif self.quads[i][0] == "+":
                # Addition
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("add t1, t1, t2\n")
                self.storerv("t1", self.quads[i][3])
            
            elif self.quads[i][0] == "-":
                # Subtraction
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("sub t1, t1, t2\n")
                self.storerv("t1", self.quads[i][3])
            
            elif self.quads[i][0] == "*":
                # Multiplication
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("mul t1, t1, t2\n")
                self.storerv("t1", self.quads[i][3])
            
            elif self.quads[i][0] == "/":
                # Division
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("div t1, t1, t2\n")
                self.storerv("t1", self.quads[i][3])
            
            elif self.quads[i][0] == "%":
                # Modulo
                self.loadvr(self.quads[i][1], "t1")
                self.loadvr(self.quads[i][2], "t2")
                self.outfile.write("rem t1, t1, t2\n")
                self.storerv("t1", self.quads[i][3])
            
            elif self.quads[i][0] == "retv":
                # Return value
                self.loadvr(self.quads[i][1], "t1")
                self.outfile.write("lw t0, -8(sp)\n")
                self.outfile.write("sw t1, 0(t0)\n")
            
            elif self.quads[i][0] == "inp":
                # Input
                self.outfile.write("li a7, 5\n")
                self.outfile.write("ecall\n")
                self.storerv("a0", self.quads[i][1])
            
            elif self.quads[i][0] == "out":
                # Output
                self.loadvr(self.quads[i][1], "a0")
                self.outfile.write("li a7, 1\n")
                self.outfile.write("ecall\n")
                self.outfile.write("la a0, str_nl\n")
                self.outfile.write("li a7, 4\n")
                self.outfile.write("ecall\n")
            
            elif self.quads[i][0] == "halt":
                # Halt
                self.outfile.write("li a0, 0\n")
                self.outfile.write("li a7, 93\n")
                self.outfile.write("ecall\n")
            
            elif self.quads[i][0] == "begin_block":
                # Begin block
                if self.quads[i][1] == "main":
                    self.outfile.write("Lmain:\n")
                    framelenth = self.scopes[0].enoffset
                    self.outfile.write("addi sp, sp, " + str(framelenth) + "\n")
                    self.outfile.write("mv gp, sp\n")
                else:
                    self.outfile.write("sw ra, 0(sp)\n")
            
            elif self.quads[i][0] == "end_block":
                # End block
                if self.quads[i][1] != "main":
                    self.outfile.write("lw ra, 0(sp)\n")
                    self.outfile.write("jr ra\n")
            
            elif self.quads[i][0] == "par":
                # Parameter handling
                if parOffset == 12:
                    for j in range(i + 1, len(self.quads)):
                        if self.quads[j][0] == "call":
                            search = self.searchEntity(self.quads[j][1])
                            if search[0].etype != "function":
                                print("toMain: function was expected", linenum)
                                sys.exit(0)
                            framelength = search[0].framelength
                            self.outfile.write("addi s0, sp, " + str(framelength) + "\n")
                
                if self.quads[i][2] == "CV":
                    # CV
                    self.loadvr(self.quads[i][1], "t0")
                    self.outfile.write("sw t0, -" + str(parOffset) + "0(s0)\n")
                    parOffset = parOffset + 4
                else:
                    # Reference parameter
                    search = self.searchEntity(self.quads[i][1])
                    offset = search[0].offset
                    self.outfile.write("addi t0, sp, -" + str(offset) + "\n")
                    self.outfile.write("sw t0, -8(s0)\n")
            
            elif self.quads[i][0] == "call":
                # Function call
                parOffset = 12
                self.outfile.write("sw sp, -4(s0)\n")
                search = self.searchEntity(self.quads[i][1])
                if search[0].etype != "function":
                    print("toMain: function was expected", linenum)
                    sys.exit(0)
                framelength = search[0].framelength
                starting_quad = search[0].starting_quad
                self.outfile.write("addi sp, sp, " + str(framelength) + "\n")
                self.outfile.write("jal L" + str(starting_quad) + "\n")
                self.outfile.write("addi sp, sp, -" + str(framelength) + "\n")

        self.quads = []  # Clear the quads after translation

        
    def updateEntity(self, name, starting_quad):
        scope = self.scopes[-1]
        framelength = scope.enoffset

        scope = self.scopes[-2]
        scope.updateEntity(name, starting_quad, framelength)
        return None

    def searchEntity(self, name):
        # Reverse the list of scopes to start searching from the innermost scope
        revscopes = reversed(self.scopes)
        
        # Iterate over each scope in reverse order
        for i in revscopes:
            # Check if the entity with the given name exists in the current scope's symbol table
            if name in i.symtable:
                # If the entity is a global variable, return it from the global scope (scope 0)
                if i.symtable[name].etype == "global_variable":
                    i = self.scopes[0]
                    return i.symtable[name], i.name, 0
                else:
                    # Return the entity along with its name and nesting level
                    return i.symtable[name], i.name, i.nestinglevel
        
        # If the entity was not found in any scope, print an error message and exit
        print("searchEntity() error: variable " + str(name) + " not in SymbolTable", linenum)
        exit(0)


    def printTable(self):
        for i in self.scopes:
            #print the current scope
            self.outfileS.write("\n")                                           #Write the results in a file
            self.outfileS.write(f"{i.name, i.nestinglevel, i.enoffset}")
            
            self.outfileS.write("\n")
            for j in i.symtable:
                #print the entities in the current scope
                if i.symtable[j].etype == "function":
                    self.outfileS.write(i.symtable[j].name + ":" + i.symtable[j].etype + "/framelength=" + str(i.symtable[j].framelength) +  ", starting_quad=" + str(i.symtable[j].starting_quad) +  "\n")
                else:
                    self.outfileS.write(i.symtable[j].name + ":" + i.symtable[j].etype +  "/offset=" + str(i.symtable[j].offset) + "\n")


            
def main():
    if len(sys.argv) < 2:
        print("ERROR: You should give at least two arguments!!!")
    else:
        
        syn = Syntax()
        syn.syntax()
        syn.int_code.printquads()
        syn.symbol_table.printTable()

# Call main()
main()
