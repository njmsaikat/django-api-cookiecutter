import re
import sys

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
DB_NAME = "{{ cookiecutter.db_name }}"

if not re.match(r"^[a-z][a-z0-9-]*$", PROJECT_SLUG):
    print(f"ERROR: project_slug '{PROJECT_SLUG}' must be lowercase letters, digits and hyphens, starting with a letter.")
    sys.exit(1)

if not re.match(r"^[a-z][a-z0-9_]*$", DB_NAME):
    print(f"ERROR: db_name '{DB_NAME}' must be lowercase letters, digits and underscores, starting with a letter.")
    sys.exit(1)
