# def find_position(scores, names):
#     """function to return position of student from their score """
#     score_copy = scores.copy()  #
#     tempt = [0] * len(scores)
#     print(score_copy, tempt)
#     for value in range(len(score_copy)):
#         try:
#             max_ = max(score_copy)
#         except ValueError:  # list has reach it end due to multiple same value
#             break
#         count = score_copy.count(max_)
#         if count > 1:
#             index_list = []
#             for counter in range(count):
#                 try:
#                     _ = scores.index(max_)
#                 except ValueError:  # list has reach it end due to multiple same value
#                     break
#                 if counter == 0:
#                     index_list.append(scores.index(max_, _))
#                 else:
#                     index_list.append(scores.index(max_, _) + 1)
#                 scores.remove(max_)
#                 print(score_copy)
#             for i in index_list:
#                 tempt[i] = value
#             # index2 = scores.index(max_, index1 + 1)
#             # tempt[index1] = value
#             # tempt[index2] = value
#             # score_copy.remove(max_)
#             print(index_list)
#             print(score_copy)
#             # a.remove(max_)
#         else:
#             index = scores.index(max_)
#             tempt[index] = value
#             score_copy.remove(max_)
#     return tempt
#
#
# result = find_position(q, "dama")
# print(result)
import random

score1 = {
    "michael":
        {
            "math": {"test1": 10, "test2": 10, 'assignment': 10, "exam": 70}
        },
    "Gabriel":
        {
            "math": {"test1": 10, "test2": 10, 'assignment': 10, "exam": 70}
        },
    "Patrick":
        {
            "math": {"test1": 10, "test2": 10, 'assignment': 10, "exam": 70}
        }
}
b = {'Michael Yohanna Dama':
         {'English': {'assignment': '10', 'test1': '8', 'test2': '9', 'exam': '66'}},
     'Gabriel Peter':
         {'English': {'assignment': '6', 'test1': '8', 'test2': '9', 'exam': '70'}},
     'Willy Sam': {'English': {'assignment': '9', 'test1': '8', 'test2': '9', 'exam': '55'}}}
