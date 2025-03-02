"""<!---
I hereby attest to the truth of the following facts:
1. I have not discussed the HTML, CSS, Python language code in my program with anyone other than my instructor or the teaching assistants assigned to this course.
2. I have not used HTML, CSS, Python language code obtained from another student, or any other unauthorized source, either modified or unmodified.
3. If any HTML, CSS, Python language code or documentation used in my program was obtained from another source, such as textbook or course notes, that has been clearly noted with a proper citation in the comments of my program.
-->"""

from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .models import Payslip
from django.contrib import messages 

# Create your views here.

overtime = 0

def employee(request):
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/employee.html', {'employees':employee_objects})

def create_employee(request):
    employee_objects = Employee.objects.all()
    if request.method == "POST":
        nuName = request.POST.get('nuName')
        nuID = request.POST.get('nuID')
        nuRate = request.POST.get('nuRate')
        nuAllowance = request.POST.get('nuAllowance')

        # Check if required fields are not empty
        if not (nuName and nuID and nuRate and nuAllowance):
            messages.info(request, 'All fields are required.')
            return redirect('create_employee')
        else:
            # Check if employee with given ID already exists
            if Employee.objects.filter(id_number=nuID).exists():
                messages.info(request, 'Employee with this ID already exists.')
                return redirect('create_employee')

            # Create the employee object
            Employee.objects.create(name=nuName, id_number=nuID, rate=nuRate, allowance=nuAllowance)
            messages.success(request, 'Employee has been created.')
            return redirect('employee')

    return render(request, 'payroll_app/create_employee.html', {'employees': employee_objects})

def update_employee(request, pk):
    if request.method == "POST":
        newname = request.POST.get('nuName')
        newid = request.POST.get('nuID')
        newrate = request.POST.get('nuRate')
        newallowance = request.POST.get('nuAllowance')

        # Check if required fields are not empty
        if not (newname and newrate and newallowance):
            messages.info(request, 'All fields are required.')
            return redirect('update_employee', pk=pk)

        else:
            # Check if employee with given ID already exists (excluding the current employee being updated)
            if Employee.objects.filter(id_number=newid).exclude(pk=pk).exists():
                messages.info(request, 'Employee with this ID already exists.')
                return redirect('update_employee', pk=pk)

            # Update the employee object
            Employee.objects.filter(pk=pk).update(name=newname, rate=newrate, allowance=newallowance)
            messages.success(request, 'Employee has been updated.')
            return redirect('employee')
    else:
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, 'payroll_app/update_employee.html', {'employee': employee})
    
def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    messages.info(request, 'Employee has been deleted.')
    return redirect('employee')

def add_overtime(request, pk):
    global overtime
    if(request.method=="POST"):
        overtimehours = float(request.POST.get('OvertimeHours'))
        rate = Employee.objects.get(pk=pk).rate
        overtime += float((rate / 160) * 1.5 * overtimehours)
        Employee.objects.filter(pk=pk).update(overtime_pay=overtime)
        return redirect('employee')
    else:
        return redirect('employee')
    
def payslips(request):
    payslip_objects = Payslip.objects.all()
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/payslips.html', {'payslips':payslip_objects, 'employees': employee_objects})

def submit_payslip(request, pk):
    if(request.method=="POST"):
        employee_return = []
        if request.POST.get('payrollFor') == "All": ## Here we will get all payslips
            payrollfor = "All"
            idnum = Employee.objects.values_list('pk', flat=True)
            for x in list(idnum):
                employee_return.append(get_object_or_404(Employee, pk=x))
                
        else: ## For use in getting the payslip of one person
            payrollfor = int(request.POST.get('payrollFor')) # Gets the employee ID number
            employee_return = get_object_or_404(Employee, id_number=payrollfor)
            
            rate = employee_return.rate/2
            earnings_allowance = employee_return.allowance
            overtime = employee_return.overtime_pay
            
            # calculations
            deductions_health = rate * 2 * 0.04
            pag_ibig = 100
            sss = rate * 2 * 0.045
            deductions_tax_1 = ((rate) + earnings_allowance + overtime - pag_ibig)*0.2
            total_pay_1 = ((rate) + earnings_allowance + overtime - pag_ibig)- deductions_tax_1
            deductions_tax_2 = ((rate) + earnings_allowance + overtime - deductions_health - sss)*0.2
            total_pay_2 = ((rate) + earnings_allowance + overtime - deductions_health - sss) - deductions_tax_2

            gross_pay = (rate) + earnings_allowance + overtime
            total_deductions1 = deductions_tax_1 + pag_ibig
            total_deductions2 = deductions_tax_2 + deductions_health + sss

        month = request.POST.get('payrollMonth') # Gets the month
        year = int(request.POST.get('payrollYear')) # Gets the year
        cycle = int(request.POST.get('payrollCycle')) # Gets the payroll cycle (1 or 2)
        
        payslip_duplicate= 0
        all_payslip_1 = []

        month31 = ["January", "March", "May", "July", "August", "October", "December"]
        month30 = ["April", "June", "September", "November"]
        month28 = ["February"]
        
        if payrollfor == "All": # Process used to get payslips when selecting 'All employees'

            for employee in employee_return:
                emp_pk = employee.pk
                
                rate = (employee.rate)/2
                earnings_allowance = employee.allowance
                overtime = employee.overtime_pay
                
                # calculations
                deductions_health = rate * 2 * 0.04
                pag_ibig = 100
                sss = rate * 2 * 0.045
                deductions_tax_1 = ((rate) + earnings_allowance + overtime - pag_ibig)*0.2
                total_pay_1 = ((rate) + earnings_allowance + overtime - pag_ibig)- deductions_tax_1
                deductions_tax_2 = ((rate) + earnings_allowance + overtime - deductions_health - sss)*0.2
                total_pay_2 = ((rate) + earnings_allowance + overtime - deductions_health - sss) - deductions_tax_2

                gross_pay = (rate) + earnings_allowance + overtime
                total_deductions1 = deductions_tax_1 + pag_ibig
                total_deductions2 = deductions_tax_2 + deductions_health + sss


                if Payslip.objects.filter(id_number=employee, month=month, year=year, pay_cycle=cycle).exists():
                    payslip_duplicate += 1
                    message = ('%(payslip_duplicate)s duplicate/s found for this period. No payslip generated for duplicates.') % {'payslip_duplicate': payslip_duplicate}
            
                else:
                    message = ('Payslips have been created.')    
                    if cycle == 1:
                        date_range = month + " 1-15" 
                        
                        # Payslip data is stored in a list and that list is stored in another list.
                        # Once all payslip data are collected, payslip objects will be created 
                        all_payslip_1.append([employee, month, date_range, year, cycle, rate, earnings_allowance, deductions_tax_1, deductions_health, pag_ibig, sss, overtime, total_pay_1, total_deductions1, gross_pay])
            
                        Employee.objects.filter(pk=emp_pk).update(overtime_pay=0) # This resets the overtime pay

                    
                    else: # cycle 2

                        if month in month31:
                                date_range = month + " 16-31"
                                all_payslip_1.append([employee, month, date_range, year, cycle, rate, earnings_allowance, deductions_tax_2, deductions_health, pag_ibig, sss, overtime, total_pay_2, total_deductions2, gross_pay])
                            
                        elif month in month30:
                            date_range = month + " 16-30"
                            all_payslip_1.append([employee, month, date_range, year, cycle, rate, earnings_allowance, deductions_tax_2, deductions_health, pag_ibig, sss, overtime, total_pay_2, total_deductions2, gross_pay])

                        elif month in month28:
                            if year % 4 == 0:
                                date_range = month + " 16-29"
                                all_payslip_1.append([employee, month, date_range, year, cycle, rate, earnings_allowance, deductions_tax_2, deductions_health, pag_ibig, sss, overtime, total_pay_2, total_deductions2, gross_pay])

                            else:
                                date_range = month + " 16-28"
                                all_payslip_1.append([employee, month, date_range, year, cycle, rate, earnings_allowance, deductions_tax_2, deductions_health, pag_ibig, sss, overtime, total_pay_2, total_deductions2, gross_pay])
                        
                        Employee.objects.filter(pk=emp_pk).update(overtime_pay=0)

            # Create payslip objects
            for x in all_payslip_1:
                Payslip.objects.create(id_number= x[0], month=x[1], date_range=x[2], year=x[3], pay_cycle=x[4], rate=x[5], earnings_allowance=x[6], deductions_tax=x[7], deductions_health=x[8], pag_ibig=x[9], sss=x[10], overtime=x[11], total_pay=x[12], total_deductions =x[13], gross_pay = x[14])
                
            messages.info(request, message)
            return redirect('payslips')

        else:  # for single payslips
            
            if Payslip.objects.filter(id_number=employee_return, month=month, year=year, pay_cycle=cycle).exists():
                messages.info(request, 'Payslip already exists. No payslip generated.')
                return redirect('payslips')
            
            else:

                if cycle == 1:
                    # if month find 31 or 30

                    date_range = month + " 1-15" 
                    
                    # Create payslip object
                    Payslip.objects.create(id_number=employee_return, month=month, date_range=date_range, year=year, pay_cycle=cycle, rate=rate, earnings_allowance = earnings_allowance, deductions_tax=deductions_tax_1, deductions_health=deductions_health, pag_ibig=pag_ibig, sss=sss, overtime=overtime, total_pay=total_pay_1, gross_pay = gross_pay, total_deductions = total_deductions1)
                    messages.success(request, 'Payslip has been created.')
                    Employee.objects.filter(pk=employee_return.pk).update(overtime_pay=0)
                    return redirect('payslips')
                
                else: # cycle 2

                    if month in month31:
                        date_range = month + " 16-31"
                    
                    elif month in month30:
                        date_range = month + " 16-30"

                    elif month in month28:
                        if year % 4 == 0:
                            date_range = month + " 16-29"
                        else:
                            date_range = month + " 16-28"

                    # Create payslip object
                    Payslip.objects.create(id_number=employee_return, month=month, date_range=date_range, year=year, pay_cycle=cycle, rate=rate, earnings_allowance = earnings_allowance, deductions_tax=deductions_tax_2, deductions_health=deductions_health, pag_ibig=pag_ibig, sss=sss, overtime=overtime, total_pay=total_pay_2, gross_pay = gross_pay, total_deductions = total_deductions2)
                    messages.success(request, 'Payslip has been created.')
                    Employee.objects.filter(pk=employee_return.pk).update(overtime_pay=0)
                    return redirect('payslips')
    else:
        return redirect('payslips')

def view_payslip(request, pk):
    d = get_object_or_404(Payslip, pk=pk)
    if d.pay_cycle == 2:
        return render(request, "payroll_app/view_payslip2.html", {'d':d})
    elif d.pay_cycle == 1:
        return render(request, "payroll_app/view_payslip1.html", {'d':d})

