
import argparse
import pandas as pd

from re import A
from dateutil import rrule

def weeks_between(start_date, end_date):
    weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
    return weeks.count()


def get_environment():
    """Get environment via command line args.
    If '--prod' is passed as a command line argument, it will run the production environment. Otherwise, it will run the development
        environment.
    Returns:
        db (str): Environment to run. "dbprod" if production. "dbdev" otherwise.
    """
    parser = argparse.ArgumentParser(description='Define environment')
    parser.add_argument('--prod', action="store_true")
    args = parser.parse_args()

    if args.prod:
        db = "dbprod"
    else:
        db = "dbdev"

    return db

def find_matches(df_students, df_projects):
    """
    Finds matches between projects and students
    Parameters:
        projects (pandas DataFrame)
        students (pandas DataFrame)
    Returns:
        matches (pandas DataFrame): a dataframe of matches
    """
    
    df_matches = pd.DataFrame(columns = ["student", "project"])
    df_matches = df_matches.set_index("student")

    for student_index, student_row in df_students.iterrows():
        student = student_row["id"]
        student_start_date = student_row["start_date"]
        student_end_date = student_row["end_date"]
        student_skills = student_row["school"]

        project_list = []

        for project_index, project_row in df_projects.iterrows():
            project = project_row["id"]
            project_start_date = project_row["start_date"]
            project_end_date = project_row["end_date"]
            project_skills = project_row["skills"]

            # Condition 1: dates match
            if (student_start_date <= project_start_date) and (student_end_date >= project_end_date):
                dates_match = True
            else:
                dates_match = False

            # Condition 2: skills match 
            if student_skills == project_skills:
                skills_match = True
            else:
                skills_match = False

            # Add to dataframe
            if dates_match and skills_match:
                project_list.append(project)
        
        df_matches.loc[student, "project"] = project_list
    
    return df_matches