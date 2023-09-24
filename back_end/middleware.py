def prepare_scores(score_list, subject):
    """function to prepare scores for further processing
        param1: dict
        param2: str

        value: [['Dama Michael Yohanna', 'JSS 1', '10', '', '10'],
                ['Williams Dama Yohanna', 'JSS 1', '10', '10', ''],
                """
    dict_value = {}
    for value in score_list:
        dict_value[value[0]] = {subject: {"first_ca": value[2],
                                          "second_ca": value[3],
                                          "exam": value[4],
                                          "total":0
                                          }
                                }
    print(dict_value)
    # print(find_total_score_per_subject(dict_value))


def find_total_score_per_subject(param_dict):
    """function to find student total score
        param: dict
        value: {
                "michael":
                {
                    "math": {"test1": 10, "test2": 10, 'assignment': 10, "exam": 70}
                },
                "
        {'Dama Michael Yohanna':
            {'English': {'first_ca': '60', 'second_ca': '0', 'exam': '0', 'tota l': 0}
        },
    }"""
    a = {}
    for key in param_dict:
        # for inner_key in param_dict[key]:
        a[key] = sum(param_dict[key].values())
        param_dict[key]['total'] = sum(param_dict[key].values())

    return a, param_dict


def find_total_score_all_subject(param_dict):
    """function to find student total score
        param: dict
        value:
                {
                    "michael": {"math": 10, "english": 10, 'chemistry': 10, "example": 70}
                },

    }"""
    a = {}
    for key in param_dict:
        # for inner_key in param_dict[key]:
        a[key] = sum(param_dict[key].values())

    return a


def find_position(position_dict):
    """Find students position given their names and score
        param: dict
        value: {"michael": 10, "gabriel": 20, "patrick": 13, "willy": 10}"""
    sorted_dict = sorted(position_dict.items(), key=lambda x: x[1], reverse=True)
    final_dict = dict(sorted_dict)
    position_dict = {}
    position = 1
    former = None
    for index, key in enumerate(final_dict):
        if final_dict[key] == former:
            position_dict[key] = position + 1
        else:
            position_dict[key] = index + 1
            former = final_dict[key]
            position = index
    return position_dict


score = {"michael": 10, "gabriel": 20, "patrick": 13, "willy": 10, "john": 17, "alice": 9, "anthony": 10}
# print(find_position(score))
