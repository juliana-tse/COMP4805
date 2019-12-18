def check_course_conflicts(result):
    conflict_list = []
    for j in range(len(result)):
        for k in range(len(result)):
            if j != k:
                if result[j]['timeslot'] == result[k]['timeslot'] and result[j]['course_nature'] == result[k]['course_nature']:
                    conflicts_courses = {'course_a': [result[k]['course'], result[k]['class_code']], 'course_b': [result[j]['course'], result[j]['class_code']]}
                    conflict_list.append(conflicts_courses)
                elif result[j]['timeslot'] == result[k]['timeslot'] and result[j]['instructor'] == result[k]['instructor']:
                    conflicts_courses = {'course_a': [result[k]['course'], result[k]['class_code']], 'course_b': [
                        result[j]['course'], result[j]['class_code']]}
                    conflict_list.append(conflicts_courses)
                else:
                    conflict_list = conflict_list
    unique_conflict_list = conflict_list
    for m in conflict_list:
        for u in unique_conflict_list:
            # if m != u:
            print('m', m)
            print('u', u)
            if m['course_a'] == u['course_b'] and m['course_b'] == u['course_a']:
                unique_conflict_list.remove(m)
                print('remove')
            else:
                print('append')
                continue
    print(conflict_list)
    print('unique', unique_conflict_list)
    # for m in conflict_list:
    #     if m not in unique_conflict_list:
    #         unique_conflict_list.append(m)
    return unique_conflict_list
