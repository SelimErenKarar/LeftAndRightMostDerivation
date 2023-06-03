
FILE_LL = "ll.txt"
FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"
liste = []
dict_ll = {}#ll tabosunu depolar
dict_lr = {}#lr tablosunu depolar
terminals = []#ll tablosundaki terminaller depolanır
nonterminals = []#ll tablosundaki nonterminaller depolanır
input_terminals = []#input stringdeki her bir terminal indexlerde depolanır
alphabeth = []#lr tabosundaki terminalleri depolar
states = []#lr tablosundaki stateler depolanır
stack = []#ll kuralı için stack

def read_file_ll():
    f = open(FILE_LL, "r", encoding='utf8')
    ct = 0
    for line in f:
        dict1 = {}
        if ct>0:
            dict1.clear()
            string = line.replace(' ', '')
            liste = string.split(";")
            for i in range(len(liste)):
                liste[i] = liste[i].strip()
            for i in range(len(terminals)):
                if i > 0 and liste[i] != '':
                    temp = liste[i].split("->")
                    dict1[terminals[i]] = temp[1]
            dict_ll[liste[0]] = dict1
            nonterminals.append(liste[0])
        elif ct==0:
            liste = line.split(";")
            for i in range(len(liste)):
                terminals.append(liste[i].strip())

        ct+=1
    f.close()

def single_terminal(input_word):            # id
    terminal =''
    for char in input_word:
        if char not in terminals:
            terminal = str(terminal + char)
            if terminal in terminals:
                input_terminals.append(terminal)
                terminal = ''
        elif char in terminals:
            input_terminals.append(char)


def list_to_str(myList):
    word =""
    for i in range(len(myList)):
        word += myList[i]
    return  word

def ll_rule():
    data = ""
    oldInp_print = ""
    NO = 1
    stack.append('$')
    non_term = nonterminals[0]
    flag = 0
    while len(input_terminals) != 0:
        term = input_terminals[0]  # inputtaki her bir terminal
        stackPrint = list_to_str(stack)
        inputPrint = list_to_str(input_terminals)
        try:
            data = dict_ll[non_term][term]
        except:
            print('{:<3}|{:<10}|{:>15}| REJECTED ({} does not have an action/step for {})'.format(NO, stackPrint, inputPrint, non_term, inputPrint[0]))
            break
        print('{:<3}|{:<10}|{:>15}| {}->{}'.format(NO, stackPrint, inputPrint, non_term, data))
        # print(NO, "|", stackPrint, "|", inputPrint, "|", non_term, "->", data)
        flag = 0
        flag2 = 0
        # stack.append(data)

        if stack[-1] != input_terminals[0]:
            if len(stack) != 1 and data != "ϵ":
                stack.pop()
            if data == "ϵ":
                stack.pop()
            elif data in terminals:
                stack.append(data)
            elif data not in terminals:
                for i in range(len(data)):
                    stack.append(data[len(data) - 1 - i])
        if stack[-1] == input_terminals[0] and stack[-1] == "$":
            NO += 1
            stackPrint = list_to_str(stack)
            print('{:<3}|{:<10}|{:>15}| ACCEPT'.format(NO, stackPrint, inputPrint))
            # print(NO, "|", stackPrint, "|", inputPrint, "|", "ACCEPT")
            flag2 = 1
        if stack[-1] == input_terminals[0]:
            NO += 1
            if flag2 == 0:
                stack[-1] = input_terminals[0]
                stackPrint = list_to_str(stack)
                print('{:<3}|{:<10}|{:>15}| Match and remove {}'.format(NO, stackPrint, inputPrint, input_terminals[0]))
                # print(NO, "|", stackPrint, "|", inputPrint, "| Match and remove", term)
            oldInp_print = list_to_str(input_terminals)
            input_terminals.pop(0)
            stack.pop()
            flag = 1
        if len(input_terminals) != 0 and stack[-1] != input_terminals[0]:
            non_term = stack[-1]
        NO += 1






def read_file_lr():
    f = open(FILE_LR, "r", encoding='utf8')
    ct = 0
    for line in f:
        tempDict = {}
        if ct > 1:
            tempDict.clear()
            string = line.replace(' ', '')
            liste = string.split(";")
            for i in range(len(liste)):
                liste[i] = liste[i].strip()
            for i in range(len(alphabeth)+1):
                if i > 0 and liste[i] != '':
                    tempDict[alphabeth[i-1]] = liste[i]
            dict_lr[liste[0][-1]] = tempDict
            states.append(liste[0][-1])
        elif ct == 1:
            liste = line.split(";")
            for i in range(len(liste)):
                if i >0 :
                    alphabeth.append(liste[i].strip())
        ct += 1

    f.close()


def lr_rule(lr_input):
    index = 0
    state = states[0]
    value = ""
    lr_inp = lr_input
    NO = 1
    state_stack = []
    state_stack.append(state)
    while True:
        string = lr_inp[index]
        try:
            value = dict_lr[state][string]
        except:
            stackPrint = list_to_str(state_stack)
            print('{:<3}|{:<15}|{:4}|{:>10}|REJECTED (State {} does not have an action/step for {})'.format(NO,stackPrint,lr_inp[index],lr_inp,state,lr_inp[index]))
            break
        if value.__contains__("_"):
            state = value[-1]
            stackPrint = list_to_str(state_stack)
            print('{:<3}|{:<15}|{:4}|{:>10}| Shift to state {}'.format(NO, stackPrint, lr_inp[index], lr_inp, state))
            # print(NO, "|", stackPrint, "|", lr_inp[index], "|", lr_inp, "| Shift to state", state)
            state_stack.append(state)
            index += 1
        elif value.__contains__("->"):
            tempValue = value.split("->")
            if len(tempValue[1]) > 1:
                lr_inp_list = list(lr_inp)
                stackPrint = list_to_str(state_stack)
                print('{:<3}|{:<15}|{:4}|{:>10}| Reverse {}'.format(NO, stackPrint, lr_inp[index], lr_inp, value))
                # print(NO, "|", stackPrint, "|", lr_inp[index], "|", lr_inp, "| Reverse", value)
                index = index - len(tempValue[1])
                for i in range(len(tempValue[1]) + 1):
                    lr_inp_list.pop()
                for i in range(len(tempValue[0])):
                    lr_inp_list.append(tempValue[0][i])
                lr_inp_list.append("$")
                lr_inp = list_to_str(lr_inp_list)
                for i in range(len(tempValue[1])):
                    state_stack.pop()
                state = state_stack[-1]
            elif len(tempValue[1]) == 1:
                lr_inp_list = list(lr_inp)
                stackPrint = list_to_str(state_stack)
                print('{:<3}|{:<15}|{:4}|{:>10}| Reverse {}'.format(NO, stackPrint, lr_inp[index], lr_inp, value))
                # print(NO, "|", stackPrint, "|", lr_inp[index], "|", lr_inp, "| Reverse", value)
                lr_inp_list[-2] = tempValue[0]
                lr_inp = list_to_str(lr_inp_list)
                index = index - 1
                for i in range(1):
                    state_stack.pop()
                state = state_stack[-1]
        else:
            stackPrint = list_to_str(state_stack)
            print('{:<3}|{:<15}|{:4}|{:>10}| ACCEPTED'.format(NO, stackPrint, lr_inp[index], lr_inp))
            # print(NO, "|", stackPrint, "|", lr_inp[index], "|", lr_inp, "| ACCEPTED")
            break
        NO += 1

def main():
    read_file_ll()  # bu fonksiyon tablodaki verileri dictionary üzerinde depolar
    read_file_lr()  # bu fonksiyon tablodaki verileri dictionary üzerinde depolar
    f = open(FILE_INPUT, "r", encoding='utf8')
    for line in f:
        string = line.replace(' ', '')
        lineList = string.split(";")
        for i in range(len(lineList)):
            lineList[i] = lineList[i].strip()
        if lineList[0] == "LL":
            print('{:<3}|{:<10}|{:<15}|{}'.format("NO","STACK","INPUT","ACTION"))
            single_terminal(lineList[1])
            ll_rule()
        elif lineList[0] == "LR":
            print('{:<3}|{:<15}|{:4}|{:<10}|{}'.format("NO","STATE STACK","READ","INPUT","ACTION"))
            lr_rule(lineList[1])



main()

