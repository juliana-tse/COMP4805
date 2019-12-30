from datetime import datetime

def check_conflicts(result, course_list):
    week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    dict_day = {}
    for day_in_week in week: 
        course_info = []
        for i in range(len(result)):
            if result[i]['day'] == day_in_week:
                # initialize day list of dict
                course_day_info = {'course': result[i]['course_code'], 'class_code': result[i]['class_code'], 'start_time': result[i]['start_time'], 'end_time': result[i]['end_time'], 'duration': result[i]['duration'], 'day': result[i]['day']}
                course_info.append(course_day_info)
            else:
                course_info = course_info
        new_day_info = {day_in_week: course_info}
        dict_day.update(new_day_info)
    conflict_list = []
    for day_in_week in week:
        if dict_day[day_in_week] != []:
            for j in range(len(dict_day[day_in_week])):
                for k in range(len(dict_day[day_in_week])):
                    if j != k:
                        if datetime.strptime(dict_day[day_in_week][j]['start_time'], '%H:%M:%S') == datetime.strptime(dict_day[day_in_week][k]['start_time'], '%H:%M:%S'):
                            conflicts_courses = {'course_a': [dict_day[day_in_week][k]['course'], dict_day[day_in_week][k]['class_code'], dict_day[day_in_week][k]['start_time'], dict_day[day_in_week][k]['end_time'], dict_day[day_in_week][k]['day']], 'course_b': [
                                dict_day[day_in_week][j]['course'], dict_day[day_in_week][j]['class_code'], dict_day[day_in_week][j]['start_time'], dict_day[day_in_week][j]['end_time'], dict_day[day_in_week][j]['day']]}
                            conflict_list.append(conflicts_courses)
                        elif datetime.strptime(dict_day[day_in_week][j]['end_time'], '%H:%M:%S') == datetime.strptime(dict_day[day_in_week][k]['end_time'], '%H:%M:%S'):
                            conflicts_courses = {'course_a': [dict_day[day_in_week][k]['course'], dict_day[day_in_week][k]['class_code'], dict_day[day_in_week][k]['start_time'], dict_day[day_in_week][k]['end_time'], dict_day[day_in_week][k]['day']], 'course_b': [
                                dict_day[day_in_week][j]['course'], dict_day[day_in_week][j]['class_code'], dict_day[day_in_week][j]['start_time'], dict_day[day_in_week][j]['end_time'], dict_day[day_in_week][j]['day']]}
                            conflict_list.append(conflicts_courses)
                        elif datetime.strptime(dict_day[day_in_week][j]['start_time'], '%H:%M:%S') < datetime.strptime(dict_day[day_in_week][k]['start_time'], '%H:%M:%S') and datetime.strptime(dict_day[day_in_week][j]['end_time'], '%H:%M:%S') > datetime.strptime(dict_day[day_in_week][k]['start_time'], '%H:%M:%S'):
                            conflicts_courses = {'course_a': [dict_day[day_in_week][k]['course'], dict_day[day_in_week][k]['class_code'], dict_day[day_in_week][k]['start_time'], dict_day[day_in_week][k]['end_time'], dict_day[day_in_week][k]['day']], 'course_b': [
                                dict_day[day_in_week][j]['course'], dict_day[day_in_week][j]['class_code'], dict_day[day_in_week][j]['start_time'], dict_day[day_in_week][j]['end_time'], dict_day[day_in_week][j]['day']]}
                            conflict_list.append(conflicts_courses)
                        else:
                            conflict_list = conflict_list
        else:
            continue 
    unique_conflict_list = conflict_list
    for m in conflict_list:
        for u in unique_conflict_list:
            if m['course_a'] == u['course_b'] and m['course_b'] == u['course_a']:
                unique_conflict_list.remove(m)
            else:
                continue
    return unique_conflict_list
