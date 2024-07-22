import re

def extract_fields(input_string):
    fields = ["incident_type", "perpInd", "perpOrg", "target", "victim", "weapon"]
    pattern = r'{}: ([^,]+(?:, [^,]+)*)'

    extracted_data = {}
    
    for field in fields:
        regex = pattern.format(re.escape(field))
        match = re.search(regex, input_string)
        if match:
            extracted_data[field] = [item.strip() for item in match.group(1).split(',')]
        else:
            extracted_data[field] = None

    return extracted_data

# Example usage
input_string = "incident_type: attack, PerpInd: None, PerpOrg: venezuelan army, Target: None, Victim: jose antonio aregua, justo pastor ceballos, Weapon: None"
print(extract_fields(input_string))