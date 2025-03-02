"""<!---
I hereby attest to the truth of the following facts:
1. I have not discussed the HTML, CSS, Python language code in my program with anyone other than my instructor or the teaching assistants assigned to this course.
2. I have not used HTML, CSS, Python language code obtained from another student, or any other unauthorized source, either modified or unmodified.
3. If any HTML, CSS, Python language code or documentation used in my program was obtained from another source, such as textbook or course notes, that has been clearly noted with a proper citation in the comments of my program.
-->"""

from django.apps import AppConfig


class PayrollAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payroll_app'
