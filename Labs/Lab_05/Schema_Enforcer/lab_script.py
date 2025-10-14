#!usr/bin/python3

# Imports
import json
import pandas as pd

# Start of Task 1
def __get_lists(student_id_list, major_list, GPA_list, is_cs_major_list, credits_taken_list):
    lists = []

    for i in range(5):
        lists.append([student_id_list[i], major_list[i], GPA_list[i], is_cs_major_list[i], credits_taken_list[i]])
    
    return lists

def __write_delim(f, is_last_element):
    if is_last_element:
        f.write('\n')
    else:
        f.write(',')

def __write_line(f, list):
    for i in range(len(list)):
        entry = list[i]
        is_string = (type(entry) == str)
        is_last_element = (i == len(list) - 1)

        f.write(str(entry))
        __write_delim(f, is_last_element)

def __create_csv(): # Task 1 Main
    student_id_list = [0, 1, 2, 3, 4]
    major_list = ['Computer Science', 'Data Science', 'Computer Science', 'Chemistry', 'Physics']
    gpa_list = [2.7, 4, 3.5, 3.2, 3]
    is_cs_major_list = ['Yes', 'No', 'Yes', 'No', 'No']
    credits_taken_list = ['15.5', '12', '14.5', '15', '13']

    lists = __get_lists(student_id_list, major_list, gpa_list, is_cs_major_list, credits_taken_list)

    with open('/workspaces/DS-2002-F25/Labs/Lab_05/Schema_Enforcer/raw_survey_data.csv', 'w') as f:
        f.write('student_id,major,GPA,is_cs_major,credits_taken\n')
        for list in lists:
            __write_line(f, list)
# End of Task 1

# Start of Task 2
def __get_json_object(course_id_list, section_list, title_list, level_list, instructor_list):
    json_object = []

    for i in range(4):
        json_object.append({
            'course_id': course_id_list[i],
            'section': section_list[i],
            'title': title_list[i],
            'level': level_list[i],
            'instructors': instructor_list[i]
        })
    
    return json_object

def __create_json(): # Task 2 Main   
    course_id_list = ['DS2002', 'DS2003', 'CS3205', 'CS3710']
    section_list = ['001', '002', '001', '002']
    title_list = ['Data Science Systems', 'Communicating with Data', 'HCI in Software Development', 'Intro to Cybersecurity']
    level_list = [200, 200, 300, 300]
    instructor_list = [
        [{'name': 'Austin Rivera', 'role': 'Primary'}, {'name': 'Heywood Williams-Tracy', 'role': 'TA'}],
        [{'name': 'Antonios Mamalakis', 'role': 'Primary'}, {'name': 'Hayeon Chung', 'role': 'TA'}],
        [{'name': 'Panagiotis Apostolellis', 'role': 'Primary'}, {'name': 'Zebanai Melaku', 'role': 'TA'}],
        [{'name': 'Angela Orebaugh', 'role': 'Primary'}]
    ]
    
    json_object = __get_json_object(course_id_list, section_list, title_list, level_list, instructor_list)

    with open('/workspaces/DS-2002-F25/Labs/Lab_05/Schema_Enforcer/raw_course_catalog.json', 'w') as f:
        f.write(json.dumps(json_object))
# End of Task 2

# Start of Task 3
def __enforce_boolean(df):
    pd.set_option('future.no_silent_downcasting', True)
    df['is_cs_major'] = df['is_cs_major'].replace('Yes', True)
    df['is_cs_major'] = df['is_cs_major'].replace('No', False)
    return df

def __clean_csv(): # Task 3 Main
    df = pd.read_csv('/workspaces/DS-2002-F25/Labs/Lab_05/Schema_Enforcer/raw_survey_data.csv')
    df = __enforce_boolean(df)
    df = df.astype({'GPA': 'float64', 'credits_taken': 'float64'})
    df.to_csv('/workspaces/DS-2002-F25/Labs/Lab_05/Schema_Enforcer/clean_survey_data.csv')
# End of Task 3

# Start of Task 4
def __normalize_json(): # Task 4 Main
    with open('/workspaces/DS-2002-F25/Labs/Lab_05/Schema_Enforcer/raw_course_catalog.json', 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data, record_path=['instructors'], meta=['course_id', 'title', 'level'])
    df.to_csv('/workspaces/DS-2002-F25/Labs/Lab_05/Schema_Enforcer/clean_course_catalog.csv')
# End of Task 4

def main():
    __create_csv() # Task 1
    __create_json() # Task 2
    __clean_csv() # Task 3
    __normalize_json() # Task 4

if __name__ == '__main__':
    main()