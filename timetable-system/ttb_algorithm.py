week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

for course in course_list:
    for day in week:
        dict_day = []
        if result[course][day] == day:
            # initialize day list of dict
            course_day_info = {'course': result[course], 'class_code': result[class_code], 'start_time': result[start_time], 'end_time': result[end_time], 'duration': result[duration]}
            dict_day.append(course_day_info)
        return dict_day

for i in range(len(week)):
    conflict_list = []
    for j in range(len(dict_day)):
        if dict_day[i][start_time] == dict_day[j][start_time]:
            conflicts_courses = {dict_day[i][course], dict_day[j][course]}
            conflict_list.append(conflicts_courses)
        elif dict_day[i][end_time] == dict_day[j][end_time]:
            conflicts_courses = {dict_day[i][course], dict_day[j][course]}
            conflict_list.append(conflicts_courses)
        elif dict_day[i][start_time] < dict_day[j][start_time] && dict_day[i][end_time] > dict_day[j][start_time]:
            conflicts_courses = {dict_day[i][course], dict_day[j][course]}
            conflict_list.append(conflicts_courses)
        else:
            return True
