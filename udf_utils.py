import re
from datetime import datetime


def extract_file_name(file_content):
    file_content = file_content.strip()
    position = file_content.split('\n')[0]
    return position
    

def extract_position(file_content):
    file_content = file_content.strip()
    position = file_content.split('\n')[0]
    return position

def extract_class_code(file_content):
    try:
        classcode_match = re.search(r'Class Code:)\s+(\d+)', file_content)
        classcode = classcode_match.group(2) if classcode_match else None
        return classcode
    except Exception as e:
        raise ValueError(f'Error extracting class node: {e}')

def extract_start_date(file_content):
    try:
        opendate_match = re.search(r'(Open [Dd]ate: )\s+(\d\d-\d\d-\d\d)', file_content)
        start_date = datetime.strptime(opendate_match.group(2), '%m-%d-%y') if opendate_match else None
        return start_date 
    except Exception as e:
        raise ValueError (f'Error extracting start date: {e}')

def extract_end_date(file_content):
    enddate_match = re.search(
        r'JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOMBER|NOVEMBER|DECEMBER)\s\d{1,2},\s\d{4}',
        file_content)
    enddate = enddate_match.group() if enddate_match else None
    enddate = datetime.strptime(enddate, '%B %d %Y') if enddate else None
    return enddate

def extract_salary():
    try:
        salary_pattern = r'\$(d{1,3}(?:,\d{3}+).+tb.+\$(\d{1,3}(?:,\d{3})+)(?:\s+and\s+\$(\d{1,3}(?:,\d{3})+)\s+to\s+\$(\d{1,3}(?:,\d{3})+)))?'
        

def extract_requirements():
    pass

def extract_notes():
    pass

def extract_duties():
    pass

def extract_selection():
    pass

def extract_experience_length():
    pass

def extract_eduation_length():
    pass

def extract_appication_location():
    pass