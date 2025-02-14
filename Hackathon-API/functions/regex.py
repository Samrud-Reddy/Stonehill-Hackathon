import re
from fastapi import HTTPException

num_pattern = re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})')
id_pattern = re.compile(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}')

def validate_login(phone_number: str, upi_id: str):
    
    number_result = num_pattern.match(phone_number)
    id_result = id_pattern.match(upi_id)
    
    if number_result is None:
        raise HTTPException(status_code=404, detail="Invalid Indian phone number!")
    elif id_result is None:
        raise HTTPException(status_code=404, detail="Invalid UPI ID!")
    else:
        return True
        