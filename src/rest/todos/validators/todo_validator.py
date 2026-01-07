#is input validation even a thing in django? I coudn't find something useful like zod sorry
def validate_input(data: dict):
    if "title" not in data or not isinstance(data["title"], str):
        return False, "Missing or invalid 'title'"
    return True, None