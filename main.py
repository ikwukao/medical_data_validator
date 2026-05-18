# Import Python's built-in regular expression module.
# This is used for validating structured string patterns
# such as patient IDs and visit IDs.
import re


# =========================================================
# SAMPLE MEDICAL RECORD DATASET
# =========================================================
# This list simulates records that could come from:
# - a database
# - an API
# - a CSV/JSON file
# - a hospital management system
#
# Each dictionary represents a single patient record.
# =========================================================
medical_records = [
    {
        'patient_id': 'P1001',
        'age': 34,
        'gender': 'Female',
        'diagnosis': 'Hypertension',
        'medications': ['Lisinopril'],
        'last_visit_id': 'V2301',
    },
    {
        'patient_id': 'p1002',
        'age': 47,
        'gender': 'male',
        'diagnosis': 'Type 2 Diabetes',
        'medications': ['Metformin', 'Insulin'],
        'last_visit_id': 'v2302',
    },
    {
        'patient_id': 'P1003',
        'age': 29,
        'gender': 'female',
        'diagnosis': 'Asthma',
        'medications': ['Albuterol'],
        'last_visit_id': 'v2303',
    },
    {
        'patient_id': 'p1004',
        'age': 56,
        'gender': 'Male',
        'diagnosis': 'Chronic Back Pain',
        'medications': ['Ibuprofen', 'Physical Therapy'],
        'last_visit_id': 'V2304',
    }
]


# =========================================================
# RECORD VALIDATION FUNCTION
# =========================================================
# This function validates the individual fields
# of a single patient record.
#
# It checks:
# - data types
# - string patterns
# - minimum allowed values
# - accepted enumerations
#
# The function returns a list of invalid field names.
# =========================================================
def find_invalid_records(
    patient_id,
    age,
    gender,
    diagnosis,
    medications,
    last_visit_id
):

    # -----------------------------------------------------
    # Dictionary containing validation rules for each field
    #
    # Each key maps to a Boolean expression.
    # If the expression evaluates to False,
    # that field is considered invalid.
    # -----------------------------------------------------
    constraints = {

        # Validate patient ID:
        # - Must be a string
        # - Must start with "p" followed by digits
        # - re.IGNORECASE allows both uppercase/lowercase
        #
        # Examples:
        # P1001 -> valid
        # p5002 -> valid
        # PX100 -> invalid
        'patient_id': (
            isinstance(patient_id, str)
            and re.fullmatch(r'p\d+', patient_id, re.IGNORECASE)
        ),

        # Validate age:
        # - Must be an integer
        # - Must be 18 or older
        'age': (
            isinstance(age, int)
            and age >= 18
        ),

        # Validate gender:
        # - Must be a string
        # - Must match either "male" or "female"
        # - lower() ensures case-insensitive comparison
        'gender': (
            isinstance(gender, str)
            and gender.lower() in ('male', 'female')
        ),

        # Validate diagnosis:
        # - Must be a string
        # - OR can be None
        #
        # This allows nullable diagnosis fields.
        'diagnosis': (
            isinstance(diagnosis, str)
            or diagnosis is None
        ),

        # Validate medications:
        # - Must be a list
        # - Every item inside the list must be a string
        #
        # all() ensures every condition evaluates to True.
        'medications': (
            isinstance(medications, list)
            and all([isinstance(i, str) for i in medications])
        ),

        # Validate last visit ID:
        # - Must be a string
        # - Must follow the format "v" + digits
        #
        # Examples:
        # V2301 -> valid
        # v9002 -> valid
        # visit12 -> invalid
        'last_visit_id': (
            isinstance(last_visit_id, str)
            and re.fullmatch(r'v\d+', last_visit_id, re.IGNORECASE)
        )
    }

    # -----------------------------------------------------
    # Return all invalid field names
    #
    # Dictionary comprehension breakdown:
    #
    # key   -> field name
    # value -> validation result (True/False)
    #
    # Only fields that fail validation are returned.
    # -----------------------------------------------------
    return [
        key
        for key, value in constraints.items()
        if not value
    ]


# =========================================================
# MAIN DATASET VALIDATOR
# =========================================================
# This function validates:
# 1. The outer data structure
# 2. Each record structure
# 3. Required dictionary keys
# 4. Individual field values
#
# Returns:
# - True  -> if all records are valid
# - False -> if any validation fails
# =========================================================
def validate(data):

    # -----------------------------------------------------
    # Ensure the provided dataset is iterable
    # and structured as either:
    # - a list
    # - a tuple
    # -----------------------------------------------------
    is_sequence = isinstance(data, (list, tuple))

    if not is_sequence:
        print('Invalid format: expected a list or tuple.')
        return False

    # -----------------------------------------------------
    # Validation state tracker
    #
    # If any validation fails, this becomes True.
    # -----------------------------------------------------
    is_invalid = False

    # -----------------------------------------------------
    # Define the exact set of required keys
    # expected in every patient record.
    #
    # Using a set makes equality comparison easy.
    # -----------------------------------------------------
    key_set = set([
        'patient_id',
        'age',
        'gender',
        'diagnosis',
        'medications',
        'last_visit_id'
    ])

    # -----------------------------------------------------
    # Iterate through every record in the dataset
    #
    # enumerate() provides:
    # - index      -> record position
    # - dictionary -> current patient record
    # -----------------------------------------------------
    for index, dictionary in enumerate(data):

        # -------------------------------------------------
        # Ensure each record is a dictionary
        # -------------------------------------------------
        if not isinstance(dictionary, dict):

            print(
                f'Invalid format: expected a dictionary at position {index}.'
            )

            is_invalid = True
            continue

        # -------------------------------------------------
        # Validate dictionary keys
        #
        # The record must contain:
        # - all required keys
        # - no extra keys
        # -------------------------------------------------
        if set(dictionary.keys()) != key_set:

            print(
                f'Invalid format: {dictionary} '
                f'at position {index} has missing and/or invalid keys.'
            )

            is_invalid = True
            continue

        # -------------------------------------------------
        # Validate individual field values
        #
        # **dictionary unpacks the dictionary values
        # into named function parameters.
        # -------------------------------------------------
        invalid_records = find_invalid_records(**dictionary)

        # -------------------------------------------------
        # Print detailed validation errors
        #
        # Each invalid field is displayed together with:
        # - the field name
        # - the invalid value
        # - the record index
        # -------------------------------------------------
        for key in invalid_records:

            # Retrieve the invalid value
            val = dictionary[key]

            print(
                f"Unexpected format '{key}: {val}' "
                f'at position {index}.'
            )

            # Mark dataset as invalid
            is_invalid = True

    # -----------------------------------------------------
    # Final validation result
    # -----------------------------------------------------
    if is_invalid:
        return False

    print('Valid format.')
    return True


# =========================================================
# EXECUTE THE MAIN VALIDATION FUNCTION
# =========================================================
# Pass the medical_records dataset into the validate()
# function and display the final validation result.
# =========================================================

result = validate(medical_records)

print(result)
