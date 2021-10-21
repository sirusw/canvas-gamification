import requests
import re
from requests.auth import HTTPBasicAuth
import math

# TODO: Error handling:
#  - input error
#  - api not available
user = 'ourinsou@gmail.com'
pw = 'wlsgss12184'
java_submission_url = 'http://127.0.0.1:8000/api/java-submission/'
parsons_submission_url = 'http://127.0.0.1:8000/api/parson-submission/'
javaSub_list = []
unary_op_list = ["-", "++", "--", "!", "~"]
binary_op_list = ["+", "-", "*", "/", "%", "!=", "<", "<=", ">", ">=", "==", "^", "||", "|",
                  "&&", "&", "+=", "-=", "*=", "/=", "%=", "&=", "^=", "="]


class JavaSub:
    def __init__(self, pk, uqj_id, q_id, u_id, ans_file, lines, blank_lines, comment_lines, import_lines, cc, method,
                 operator, operand, operator_list, operand_list):
        self.pk = pk
        self.uqj_id = uqj_id
        self.q_id = q_id
        self.u_id = u_id
        self.ans_file = ans_file
        self.lines = lines
        self.blank_lines = blank_lines
        self.comment_lines = comment_lines
        self.import_lines = import_lines
        self.cc = cc
        self.method = method
        self.operator = operator
        self.operand = operand
        self.operator_list = operator_list
        self.operand_list = operand_list


def request_api(url, username, password):
    return requests.get(url, auth=HTTPBasicAuth(username, password))


def get_submission_dict(url, username, password):
    r = request_api(url, username, password)
    r = r.json()
    print('Success')
    return r


def init():
    print('Fetching java submissions... ', end="")
    java_submission_dict = get_submission_dict(java_submission_url, user, pw)
    print('Success')
    print('Fetching parsons submissions... ', end="")
    parsons_submission_dict = get_submission_dict(parsons_submission_url, user, pw)
    print('Success')
    print('Done.')
    return {'java_sub': java_submission_dict, 'parsons_sub': parsons_submission_dict}


def num_lines(string):
    return string.count('\n') + 1


def num_blank_lines(string):
    temp_list = string.split("\n")
    num = 0
    for i in temp_list:
        if i.isspace():
            num += 1
    return num


def num_comment_lines(string):
    temp_list = string.split("\n")
    num = 0
    for i in temp_list:
        tmp = i.strip()
        if len(tmp) >= 2:
            if tmp[0] == "/" and tmp[1] == "/":
                num += 1

    return num


def num_import(string):
    temp_list = string.split("\n")
    num = 0
    for i in temp_list:
        if 'import' in i:
            num += 1

    return num


def calc_cc(string):
    num = 1
    num += string.count('if')
    num += string.count('while')
    num += string.count('for')
    num += string.count('case')
    num += string.count('&&')
    num += string.count('||')
    return num


def num_method(string):
    pattern = "(\n|\t| )(?!new|private|public)[\w]+\[?\]?(<?[\w]+?>?) +[\w]+ ?\((\w+ \w+\[\])?"
    num = len(re.findall(pattern, string))
    return num


def num_op(string):
    lines = string.split("\n")
    operator = 0
    operand = 0
    operator_list = []
    operand_list = []

    print("////////////////////////////////////////")
    for line in lines:
        words = line.split(" ")
        if "import" in line:
            continue
        if line.strip()[0:2] == '//':
            continue
        for i in range(len(words)):
            for bi in binary_op_list:
                if bi in words[i] and len(re.findall("^-[\w]+", words[i])) == 0:
                    print("########")
                    print(words)
                    print("bi")
                    print("########")

                    if bi not in operator_list:
                        operator_list.append(bi)
                    if bi == words[i] and 0 < i < len(words) - 1:
                        prev = words[i - 1]
                        nxt = words[i + 1]
                        if prev not in operand_list:
                            operand_list.append(prev)
                        if nxt not in operand_list:
                            operand_list.append(nxt)
                    else:
                        split = words[i].split(bi)
                        for op in split:
                            if op not in operand_list:
                                operand_list.append(op)

                    operator += 1
                    operand += 2
                    break
            for uni in unary_op_list:
                pattern_exception = uni + "="

                pattern_exception2 = "[^a-zA-Z\d\s]="
                neg_sign = len(re.findall("^-[\w]+", words[i]))
                rep = len(re.findall(pattern_exception2, words[i]))
                if uni in words[i] and neg_sign > 0 and pattern_exception not in words[i] and rep == 0:
                    print("########")
                    print(words)
                    print("########")

                    if uni not in operator_list:
                        operator_list.append(uni)
                    split = words[i].split(uni)
                    for op in split:
                        if op != "" and op not in operand_list:
                            operand_list.append(op)

                    operator += 1
                    operand += 1
                    print(re.findall("^-[\w]+", words[i]))
                    break

    return [operator, operand, operator_list, operand_list]


def code_analysis(sub_dict):
    lines = 0
    blank_lines = 0
    comment_lines = 0
    import_lines = 0
    cc = 0
    method = 0
    operator = 0
    operand = 0
    operator_list = []
    operand_list = []
    for string in sub_dict.values():
        lines += num_lines(string)
        blank_lines += num_blank_lines(string)
        comment_lines += num_comment_lines(string)
        import_lines += num_import(string)
        cc += calc_cc(string)
        method += num_method(string)
        op_list = num_op(string)
        operator += op_list[0]
        operand += op_list[1]
        operator_list.append(op_list[2])
        operand_list.append(op_list[3])
    return [lines, blank_lines, comment_lines, import_lines, cc, method, operator, operand, operator_list, operand_list]



def fetch():
    submission_dict = init()
    java_dict = submission_dict['java_sub']
    java_sub = java_dict['results']
    # java_answer_file = java_sub['answer_files']
    parsons_dict = submission_dict['parsons_sub']
    parsons_sub = parsons_dict['results'][0]
    result = ''

    for i in range(len(java_sub)):
        ans_file = java_sub[i]['answer_files']
        res = code_analysis(ans_file)
        uqj = java_sub[i]['uqj']
        sub = JavaSub(java_sub[i]['pk'], uqj['id'], uqj['question_id'], uqj['user'], ans_file, res[0], res[1], res[2],
                      res[3], res[4], res[5], res[6], res[7], res[8], res[9])
        javaSub_list.append(sub)
    
    for s in javaSub_list:
        unique_operator = sum(len(y) for y in s.operator_list)
        unique_operand = sum(len(x) for x in s.operand_list)
        vocab = unique_operator + unique_operand
        size = s.operator + s.operand
        vol = size * math.log2(vocab)
        difficulty = unique_operator / 2 + s.operand / unique_operand
        effort = vol * difficulty
        error = vol / 3000
        test_time = effort / 18
        result += "PK: " + str(s.pk) + "\nUQJ id: " + str(s.uqj_id) + "\nQuestion id: " + str(s.q_id) + "\nUser id: " + str(
            s.u_id) + "\nNumber of lines: " + str(s.lines)
              + "\nNumber of blank lines: " + str(s.blank_lines) + "\nNumber of comment lines: " + str(s.comment_lines)
              + "\nNumber of imports: " + str(s.import_lines) + "\nCyclomatic complexity: " + str(s.cc)
              + "\nNumber of methods: " + str(s.method) + "\nNumber of operators: " + str(s.operator)
              + "\nNumber of operands: " + str(s.operand)
              + "\nNumber of unique operators: " + str(sum(len(y) for y in s.operator_list))
              + "\nNumber of unique operands: " +  str(sum(len(x) for x in s.operand_list))
              + "\nOperators: " + str(s.operator_list)
              + "\nOperands: " + str(s.operand_list)
              + "\nVocabulary: " + str(vocab)
              + "\nSize: " + str(size)
              + "\nVolume: " + str(round(vol, 2))
              + "\nDifficulty: " + str(difficulty)
              + "\nEffort: " + str(round(effort, 2))
              + "\nError: " + str(round(error, 5))
              + "\nTest time:" + str(round(test_time, 3))
        res += "--------------------------"
        for ans in s.ans_file.values():
            result += ans
            result += "--------------------------"
        result += "=========================================="
    return result



