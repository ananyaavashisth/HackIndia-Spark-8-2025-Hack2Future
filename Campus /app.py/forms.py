def autofill_form(form_type, user_info):
    # Dummy implementation
    if form_type.lower() == "kyc":
        return f"KYC form filled for {user_info.get('name', 'User')}."
    return "Form autofill not supported for this type yet."