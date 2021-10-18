import requests
import re
from requests.auth import HTTPBasicAuth

# TODO: Error handling:
#  - input error
#  - api not available
user = 'ourinsou@gmail.com'
pw = 'wlsgss12184'
java_submission_url = 'http://127.0.0.1:8000/api/java-submission/'
parsons_submission_url = 'http://127.0.0.1:8000/api/parson-submission/'
javaSub_list = []


class JavaSub:
    def __init__(self, uqj_id, q_id, u_id, ans_file, lines, blank_lines, comment_lines, import_lines, cc, method):
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
    pattern = "(?!new|private|public)[\w]+\[?\]?(<?[\w]+?>?) +[\w]+ ?\((\w+ \w+\[\])?"
    num = len(re.findall(pattern, string))
    return num


def code_analysis(sub_dict):
    lines = 0
    blank_lines = 0
    comment_lines = 0
    import_lines = 0
    cc = 0
    method = 0
    for string in sub_dict.values():
        lines += num_lines(string)
        blank_lines += num_blank_lines(string)
        comment_lines += num_comment_lines(string)
        import_lines += num_import(string)
        cc += calc_cc(string)
        method += num_method()

    return [lines, blank_lines, comment_lines, import_lines, cc, method]


def main():
    submission_dict = init()
    java_dict = submission_dict['java_sub']
    java_sub = java_dict['results']
    # java_answer_file = java_sub['answer_files']
    parsons_dict = submission_dict['parsons_sub']
    parsons_sub = parsons_dict['results'][0]

    for i in range(len(java_sub)):
        ans_file = java_sub[i]['answer_files']
        tmp = code_analysis(ans_file)
        uqj = java_sub[i]['uqj']
        sub = JavaSub(uqj['id'], uqj['question_id'], uqj['user'], ans_file, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5])
        javaSub_list.append(sub)

    for s in javaSub_list:
        print("UQJ id: " + str(s.uqj_id) + "\nQuestion id: " + str(s.q_id) + "\nUser id: " + str(
            s.u_id) + "\nNumber of lines: " + str(s.lines)
              + "\nNumber of blank lines: " + str(s.blank_lines) + "\nNumber of comment lines: " + str(s.comment_lines)
              + "\nNumber of imports: " + str(s.import_lines) + "\nCyclomatic complexity: " + str(s.cc)
              +  "\nNumber of methods: " + str(s.method))
        print("==========================")


if __name__ == "__main__":
    main()
