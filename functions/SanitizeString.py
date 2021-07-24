import re

def sanitize_email(email):
    if len(email) < 1: raise ValueError('All fields must be filled')

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.match(regex, email)):
        return email
 
    else:
        raise ValueError('Wrong Email Format')


def sanitize_general_string(str):
    if len(str) < 1: raise ValueError('All fields must be filled')

    return str