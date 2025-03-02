"""<!---
I hereby attest to the truth of the following facts:
1. I have not discussed the HTML, CSS, Python language code in my program with anyone other than my instructor or the teaching assistants assigned to this course.
2. I have not used HTML, CSS, Python language code obtained from another student, or any other unauthorized source, either modified or unmodified.
3. If any HTML, CSS, Python language code or documentation used in my program was obtained from another source, such as textbook or course notes, that has been clearly noted with a proper citation in the comments of my program.
-->"""

from django.db import models

# Create your models here.

class Employee(models.Model):
  name = models.CharField(max_length=21)
  id_number = models.CharField(max_length=16)
  rate = models.FloatField()
  overtime_pay = models.FloatField(null=True, default=0)
  allowance = models.FloatField(null=True, default=0)

  def getName(self):
    return self.name

  def getID(self):
    return self.id_number

  def getRate(self):
    return self.rate
  
  def getOvertime(self):
    return self.overtime_pay
  
  def resetOvertime(self):
    self.overtime_pay = 0
  
  def getAllowance(self):
    return self.allowance
  
  def __str__(self):
    return "{}: {}, Rate: {}".format(self.pk, self.id_number, self.rate)

class Payslip(models.Model):
  id_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
  month = models.CharField(max_length=10)
  date_range = models.CharField(max_length=20)
  year = models.CharField(max_length=4)
  pay_cycle = models.IntegerField()
  rate = models.FloatField()
  earnings_allowance = models.FloatField()
  deductions_tax = models.FloatField()
  deductions_health = models.FloatField()
  pag_ibig = models.FloatField()
  sss = models.FloatField()
  overtime = models.FloatField()
  total_pay = models.FloatField()

  gross_pay = models.FloatField(default=0)
  total_deductions = models.FloatField(default=0)

  def getIDNumber(self):
    return self.id_number.id_number
  
  def getMonth(self):
    return self.month
  
  def getDate_range(self):
    return self.date_range
  
  def getYear(self):
    return self.year
  
  def getPay_cycle(self):
    return self.pay_cycle
  
  def getRate(self):
    return self.rate
  
  def getCycleRate(self):
    return (self.rate/2)
  
  def getEarnings_allowance(self):
    return self.earnings_allowance
  
  def getDeductions_tax(self):
    return self.deductions_tax
  
  def getDeductions_health(self):
    return self.deductions_health
  
  def getPag_ibig(self):
    return self.pag_ibig
  
  def getSSS(self):
    return self.sss
  
  def getOvertime(self):
    return self.overtime
  
  def getTotal_pay(self):
    return self.total_pay
  
  def __str__(self):
    return "pk: {}, Employee: {}, Period: {} {}, {}, Cycle:, {}, Total Pay: {}".format(self.pk, self.id_number.id_number, self.month, self.date_range, self.year, self.pay_cycle, self.total_pay)


