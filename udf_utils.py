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

def extract_salary(file_content):
    try:
        salary_pattern = r'\$(d{1,3}(?:,\d{3}+).+tb.+\$(\d{1,3}(?:,\d{3})+)(?:\s+and\s+\$(\d{1,3}(?:,\d{3})+)\s+to\s+\$(\d{1,3}(?:,\d{3})+)))?'
        salary_match = re.search(salary_pattern, file_content)

        if salary_match:
            salary_start = float(salary_match.group(1).replace(',',''))
            salary_end = float(salary_match.group(4).replace(',','')) if salary_match.group(4) \
                else float(salary_match.group(2).replace(',', ''))
        else:
            salary_start, salary_end = None, None
        
        return salary_start, salary_end
    except Exception as e:
        raise ValueError(f'Error extracting salary: {str(e)}')


def extract_requirements(file_content):
    try:
        requirements_match = re.search(r'(REQUIREMENTS?/\s?MINIMUM QUALIFICATIONS?)(.*)(PROCESS NOTES)' file_content,
                                       re.DOTALL)
        req = requirements_match.group(2).strip() if requirements_match else None
    except Exception as e:
        raise ValueError(f'Error extracting requirements:  {str(e)}')
        

def extract_notes(file_content):
    try:
        notes_match = re.search(r'(NOTES?):(.*)(?=DUTIES)', file_content, re.DOTALL | re.IGNORECASE)
        notes = notes_match.group(2).strip() if notes_match else None
        return notes
    except Exception as e:
        raise ValueError(f'Error extracting notes: {str(e)}')

def extract_duties(file_content):
    try:
        duties_match = re.search(r'(DUTIES):(.*?)(REQ[A-Z])', file_content, re.DOTALL)
        duties = duties_match.group(2).strip() if duties_match else None
        return duties
    except Exception as e:
        raise ValueError(f'Error extracting duties: {str(e)}')

def extract_selection():
    try:
        selection_match = re.search(r'')
    except Exception as e:
        raise ValueError(f'Error extracting selection: {str(e)}')

def extract_experience_length():
    pass

def extract_eduation_length():
    pass

def extract_appication_location():
    pass