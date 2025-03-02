"""<!---
I hereby attest to the truth of the following facts:
1. I have not discussed the HTML, CSS, Python language code in my program with anyone other than my instructor or the teaching assistants assigned to this course.
2. I have not used HTML, CSS, Python language code obtained from another student, or any other unauthorized source, either modified or unmodified.
3. If any HTML, CSS, Python language code or documentation used in my program was obtained from another source, such as textbook or course notes, that has been clearly noted with a proper citation in the comments of my program.
-->"""

"""
URL configuration for Lazapee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employee, name='employee'),
    path('create_employee', views.create_employee, name='create_employee'),
    path('update_employee/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('add_overtime/<int:pk>/', views.add_overtime, name='add_overtime'),
    path('payslips', views.payslips, name='payslips'),
    path('submit_payslip/<int:pk>/', views.submit_payslip, name='submit_payslip'),
    path('view_payslip1/<int:pk>/', views.view_payslip, name='view_payslip1'),
    path('view_payslip2/<int:pk>/', views.view_payslip, name='view_payslip2'),
]
