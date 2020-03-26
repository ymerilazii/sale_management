from django.shortcuts import render, redirect
from .forms import EndOfDay, ExpenseAdd
from nitishop.models import Total, Budget
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear

### MAIN PAGE####
def index(request):
    results = Total.objects.order_by('-date')[:10]
    return render(request,'index.html',{'data':results})

##CALCULATION SALES###
def calc_page(request):
    if request.method == 'POST':
        form = EndOfDay(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            t1 = Total()
            b_u = Budget.objects.filter(id=1)
            up = Budget.objects.last()
            if Total.objects.filter(date=clean['f_date']):
                overwrite = Total.objects.filter(date=clean['f_date'])
                a = float(Total.objects.get(date=clean['f_date']).cashbox) + float(clean['f_cashbox'])
                b = float(Total.objects.get(date=clean['f_date']).withdraw) + float(clean['f_withdraw'])
                c = a - b
                d = a -float(Total.objects.order_by('-date')[1].remain)
                f = d*0.2
                e = f -20.00
                overwrite.update(cashbox=a)
                overwrite.update(withdraw=b)
                overwrite.update(remain=c)
                overwrite.update(sale=d)
                overwrite.update(profit=f)
                overwrite.update(neto=e)
                #BUDGET
                temp_cash = float(clean['f_cashbox'])
                temp_with = float(clean['f_withdraw'])
                b_u.update(total_sale=float(up.total_sale)+float(up.budget) +temp_cash)
                b_u.update(total_profit=float(up.total_profit)+float(up.total_profit)+(temp_cash-temp_with))
                b_u.update(total_neto=float(up.total_neto)+float(up.total_profit)+(temp_cash-temp_with)*0.2)
                b_u.update(budget=float(up.budget)+temp_cash)
            else:
                t1.date = clean['f_date']
                t1.cashbox = clean['f_cashbox']
                t1.withdraw = clean['f_withdraw']
                t1.remain = t1.cashbox - t1.withdraw
                t1.sale = float(t1.cashbox) - float(Total.objects.order_by('-date')[0].remain)
                t1.profit = float(t1.sale*0.2)
                t1.neto = float(t1.profit-20.00)
                t1.expense = float(0.00)
                t1.save()
                b_u.update(total_sale=float(up.total_sale )+float(t1.sale))
                b_u.update(total_profit=float(up.total_profit)+float(t1.profit))
                b_u.update(total_neto=float(up.total_neto)+float(t1.neto))
                b_u.update(budget=float(up.budget)+float(t1.sale))
            return redirect('/')
    else:
        form = EndOfDay()
    results = Total.objects.order_by('-date')[:8]
    return render(request, 'calc.html',{'form':form,'data':results})


### EXPENSE PAGE ####
def expense_page(request):
    if request.method == 'POST':
        form = ExpenseAdd(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            overwrite = Total.objects.filter(date=clean['f_date'])
            overwrite.update(expense=clean['f_expense'])
            b_u = Budget.objects.filter(id=1)
            up = Budget.objects.last()
            b_u.update(total_expense=up.total_expense+clean['f_expense'])
            b_u.update(budget=up.budget-clean['f_expense'])
            return redirect('/')
    else:
        form = ExpenseAdd()
    results = Total.objects.order_by('-date')[:8]
    return render(request, 'expense.html',{'form':form,'data':results})


#STATISTIC PAGE#
def statistics_page(request):
    def getList(var,val):
        generate = Total.objects.annotate(month=TruncMonth('date'),year=TruncYear('date')).values('month','year').annotate(c=Sum(var)).values('month','year','c')
        a = []
        for i in generate:
            a.append(i)
        if var == 'cashbox':
            #return a[val](0).month
            return a[val]['month'].month
        else:
            return round(a[val]['c'],2)

    sale_sum = getList('sale',-1)
    profit_sum = getList('profit',-1)
    neto_sum = getList('neto',-1)
    withdraw_sum = getList('withdraw',-1)
    expense_sum = getList('expense',-1)
    sale_sum1 = getList('sale',-2)
    profit_sum1 = getList('profit',-2)
    neto_sum1 = getList('neto',-2)
    withdraw_sum1 = getList('withdraw',-2)
    expense_sum1 = getList('expense',-2)

    def switchcase(i):
        switcher = {
            1:'Janar',
            2:'Shkurt',
            3:'Mars',
            4:'Prill',
            5:'Maj',
            6:'Qershor',
            7:'Korrik',
            8:'Gusht',
            9:'Shtator',
            10:'Tetor',
            11:'Nentor',
            12:'Dhjetor',
        }
        return switcher.get(i,"Muaj i paidentifikuar")

    date_name = switchcase(getList('cashbox', -1))
    date_name1 = switchcase(getList('cashbox', -2))
    context = {
        'this_date':date_name,
        'prev_date':date_name1,
        'sale':sale_sum,
        'profit':profit_sum,
        'neto':neto_sum,
        'withdraw':withdraw_sum,
        'expense':expense_sum,
        'sale1':sale_sum1,
        'profit1':profit_sum1,
        'neto1':neto_sum1,
        'withdraw1':withdraw_sum1,
        'expense1':expense_sum1,
    }
    return render(request,'statistics.html',context)


#TOTAL PAGE#
def total_page(request):
    t = Budget.objects.last()
    context = {
        'budget':t.budget,
        'sale':t.total_sale,
        'profit':t.total_profit,
        'neto':t.total_neto,
        'expense':t.total_expense,
    }

    return render(request, 'total.html',context)