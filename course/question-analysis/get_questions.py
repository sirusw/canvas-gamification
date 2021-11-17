import requests
from requests.auth import HTTPBasicAuth

# TODO: Error handling:
#  - input error
#  - api not available

user = 'ourinsou@gmail.com'
pw = 'Wlsgss12184'

java_url = 'https://gamification.ok.ubc.ca/api/java-question/'
parson_url = 'https://gamification.ok.ubc.ca/api/parsons-question/'
mcq_url = 'https://gamification.ok.ubc.ca/api/multiple-choice-question/'


def request_api(url, username, password):
    return requests.get(url, auth=HTTPBasicAuth(username, password))


def get_question_dict(url, username, password):
    r = request_api(url, username, password)
    r = r.json()
    result_dict = r['results']
    next = r['next']
    while 1:
        if next is None:
            break
        else:
            temp = request_api(next, username, password)
            temp = temp.json()
            result_dict += temp['results']
            next = temp['next']
    return result_dict


def get_all_question_dict(username, password):
    print("Fetching java questions... ", end="")
    java_dict = get_question_dict(java_url, username, password)
    if java_dict is not None:
        print('Success')
    print("Fetching parson questions... ", end=""),
    parson_dict = get_question_dict(parson_url, username, password)
    if parson_dict is not None:
        print('Success')
    print("Fetching multiple choice questions... ", end=""),
    mcq_dict = get_question_dict(mcq_url, username, password)
    if mcq_dict is not None:
        print('Success')
    q_dict = {'java_dict': java_dict, 'parson_dict': parson_dict, 'mcq_dict': mcq_dict}
    return q_dict


def init():
    question_dict = get_all_question_dict(user, pw)
    print('Done')
    return question_dict


def main():
    question_dict = init()
    print('Number of java questions: ' + str(len(question_dict['java_dict'])))
    print('Number of parson questions: ' + str(len(question_dict['parson_dict'])))
    print('Number of multiple choice questions: ' + str(len(question_dict['mcq_dict'])))


if __name__ == "__main__":
    main()