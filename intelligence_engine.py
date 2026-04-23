import re

CATEGORY_KEYWORDS = {
    "Network Link Analysis": ["link", "links"],
    "Interface Analysis": ["interface", "port"],
    "Node Analysis": ["node", "nodename"],
    "Domain Analysis": ["domain"],
    "Time Series Data": ["week", "day", "month"],
    "Pattern Search": ["pattern", "keyword"],
    "Assignment Operations": ["assign"],
}


def split_words(name: str):

    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', name)

    return [w.lower() for w in words]


def clean_parameter_name(param):

    if not param:
        return param

    name = param.lower()

    prefixes = ["p_", "i_", "arg_", "input_", "param_"]

    for p in prefixes:
        if name.startswith(p):
            name = name[len(p):]

    name = name.replace("name", "_name")
    name = name.replace("names", "_names")

    name = re.sub(r'[^a-z0-9]+', "_", name)

    name = name.strip("_")

    return name


def categorize_procedure(proc_name):

    name = proc_name.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            if keyword in name:
                return category

    return "General Database Procedure"



def generate_description(proc_name, params):

    words = split_words(proc_name)

    base_sentence = " ".join(words)

    base_sentence = base_sentence.capitalize()

    cleaned_params = [clean_parameter_name(p) for p in params]

    if cleaned_params:

        param_sentence = ", ".join(cleaned_params)

        description = f"{base_sentence}. Accepts parameters: {param_sentence}."

    else:

        description = f"{base_sentence}."

    return description



def build_procedure_metadata(proc_name, params):

    category = categorize_procedure(proc_name)

    description = generate_description(proc_name, params)

    cleaned_params = [clean_parameter_name(p) for p in params]

    return {
        "name": proc_name,
        "category": category,
        "description": description,
        "parameters": cleaned_params
    }