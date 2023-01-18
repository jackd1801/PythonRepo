import pandas as pd
def cpi_data(file):
    level = ["Urban", "Rural", "All Rwanda"]
    df_list=[]
    for i in level:
            df = pd.read_excel(file, sheet_name=i, skiprows=3)
            df = df.rename(columns={"Unnamed: 0": "Province", "Unnamed: 1": "U_R", "Unnamed: 2": "COICOP", "Unnamed: 3": "Index"})
            df = df.drop([0,19])
            df['Index']=df['Index'].str.replace('v', '')
            df['Index']=df['Index'].str.strip()
            df = df.melt(id_vars=['Province', 'U_R', 'COICOP', 'Index', 'Weights'], var_name='Date', value_name='CPI')
            df['Month']=df['Date'].dt.month_name(locale='English')
            df['Level']=i
            df_list.append(df)
    cpi = pd.concat(df_list)
    return(cpi)