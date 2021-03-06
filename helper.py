import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64

def load_telco():
    # Read data
    telco = pd.read_csv('data/telcochurn.csv')
    
    # Adjust dtypes
    catcol = telco.select_dtypes('object').columns
    telco[catcol] = telco[catcol].apply(lambda x: x.astype('category'))
    
    # Tenure Months to grouping categories
    def grouping_tenure(telco) :
        if telco["tenure_months"] <= 12 :
            return "< 1 Year"
        elif (telco["tenure_months"] > 12) & (telco["tenure_months"] <= 24 ):
            return "1-2 Year"
        elif (telco["tenure_months"] > 24) & (telco["tenure_months"] <= 48) :
            return "2-4 Year"
        elif (telco["tenure_months"] > 48) & (telco["tenure_months"] <= 60) :
            return "4-5 Year"
        else:
            return "> 5 Year"
        
    telco["tenure_group"] = telco.apply(lambda telco: grouping_tenure(telco), axis = 1)
    
    # Adjust category order
    tenure_group = ["< 1 Year", "1-2 Year", "2-4 Year", "4-5 Year", "> 5 Year"]
    telco["tenure_group"] = pd.Categorical(telco["tenure_group"], categories = tenure_group, ordered=True)
    
    return(telco)

def table_churn(data):
    table = pd.crosstab(
        data['churn_label'],
        columns = 'percent',
        normalize = True
    )*100
    return(table)

def plot_phone(data):
    
    # ---- Phone Service Customer

    phonesrv = pd.crosstab(
        data['phone_service'], data['churn_label'], normalize=True
    )*100

    ax = phonesrv.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Phone Service Customer')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_internet(data):

    # ---- Internet Service Customer
    isp = pd.crosstab(
        data['internet_service'], data['churn_label'], normalize=True
    )*100

    ax = isp.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Internet Service Customer')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_churn(data):
    
    # ---- Churn Rate by Tenure Group
    task10 = (pd.crosstab(data['tenure_group'], data['churn_label'], normalize=True)*100).round(2)

    ax = task10.plot(kind = 'bar', color=['#53a4b1','#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Tenure Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_cltv(data):

    # ---- Average Lifetime Value by Tenure
    b = pd.crosstab(data['tenure_months'], [data['churn_label']], values=data['cltv'], aggfunc='mean')

    ax = b.plot(color=['#333333','#b3b3b3'], figsize=(8, 6),style = '.--')

    # Plot Configuration
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.title('Average Lifetime Value by Tenure')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_arpu_internet_tenure(data):
    # ARPU Internet by Tenure
    b = pd.crosstab(data['tenure_months'], [data['internet_service']], values=data['monthly_charges'], aggfunc='mean', normalize=False).iloc[:,0:2]
    aj = b.plot(color=['#cf3232','#329dcf'], figsize=(8, 6),style = '.--')
    
    # Plot Configuration
    aj.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.xticks(rotation = 360)
    plt.legend(['DSL', 'Fiber Optic'],fancybox=True,shadow=True)
    plt.title('Internet Service Customer')


    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_arpu_phone_tenure(data):
    # ARPU Internet by Tenure
    c = pd.crosstab(data['tenure_months'], [data['phone_service']], values=data['monthly_charges'], aggfunc='mean', normalize=False).loc[:,['Multiple Lines', 'Single Line']]
    az = c.plot(color=['#cf3232','#329dcf'], figsize=(8, 6),style = '.--')
    
    # Plot Configuration
    az.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.xticks(rotation = 360)
    plt.legend(['Multiple Lines', 'Single Line'],fancybox=True,shadow=True)
    plt.title('Phone Service Customer')


    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_arpu_phone_single(data):
    c = pd.crosstab(data['tenure_months'], [data['phone_service'], data['churn_label']], values=data['monthly_charges'], aggfunc='mean', normalize=False).loc[:,['Single Line']]
    aj = c.plot(color=['#ffbdbd','#cf3232', '#bde8fc', '#329dcf'], figsize=(8, 6),style = '.-')

    aj.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.xticks(rotation = 360)
    plt.legend(['Active', 'Churned', 'Single Line', 'Single Line (Churned)'],fancybox=True,shadow=True)
    plt.title('Phone Single Line')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_arpu_phone_multi(data):
    c = pd.crosstab(data['tenure_months'], [data['phone_service'], data['churn_label']], values=data['monthly_charges'], aggfunc='mean', normalize=False).loc[:,['Multiple Lines']]
    aj = c.plot(color=['#ffbdbd','#cf3232', '#bde8fc', '#329dcf'], figsize=(8, 6),style = '.-')

    aj.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.xticks(rotation = 360)
    plt.legend(['Active', 'Churned', 'Single Line', 'Single Line (Churned)'],fancybox=True,shadow=True)
    plt.title('Phone Multiple Lines')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_arpu_inet_fo(data):
    c = pd.crosstab(data['tenure_months'], [data['internet_service'], data['churn_label']], values=data['monthly_charges'], aggfunc='mean', normalize=False).loc[:,['Fiber optic']]
    ad = c.plot(color=['#bde8fc', '#329dcf'], figsize=(8, 6),style = '.-')

    ad.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.xticks(rotation = 360)
    plt.legend(['Active', 'Churned', 'Single Line', 'Single Line (Churned)'],fancybox=True,shadow=True)
    plt.title('Internet Fiber Optic')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_arpu_dsl(data):
    d = pd.crosstab(data['tenure_months'], [data['internet_service'], data['churn_label']], values=data['monthly_charges'], aggfunc='mean', normalize=False).loc[:,['DSL']]
    an = d.plot(color=['#bde8fc', '#329dcf'], figsize=(8, 6),style = '.-')

    an.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.xticks(rotation = 360)
    plt.legend(['Active', 'Churned'],fancybox=True,shadow=True)
    plt.title('Internet DSL')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    return(result)

