import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def plt_scattering_diagram(df):
    x = df['EV/EBITDA']
    y = df['долг/EBITDA']
    rad = df['Капит-я  млрд руб']
    labels = df['Название']
    plt.scatter(x, y, s=rad, alpha=0.3)
    for i in range(len(x)):
        plt.annotate(labels[i], (x[i], y[i]), fontsize=12, ha='center', va='center')
    plt.xlabel('EV/EBITDA')
    plt.ylabel('долг/EBITDA')
    plt.grid(True)
    plt.show()

def plt_info(df, info='P/E'):
    plt.bar(df['Тикер'], df[info], color='skyblue')
    plt.title(info)
    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()
    plt.show()

def import_report(url: str): 
    with requests.Session() as session:
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, features="lxml")
            table = soup.find_all('table')
            if table:
                df = pd.read_html(str(table))[0]
                # erase OMZZ
                df.drop(0, inplace=True) 
                df.reset_index(drop=True, inplace=True)
                head = ['Название', 'Тикер']
                info = ['Капит-я  млрд руб', 'Выручка', 'Чистая прибыль', 'P/E', 'P/S', 'P/B', 'долг/EBITDA', 'EV/EBITDA']
                df = df[head + info]
                # converting specified columns to numeric format (float)
                df[info] = df[info].replace({' ': ''}, regex=True)
                df[info] = df[info].apply(pd.to_numeric, errors='coerce')
                df['ROE'] = df['Чистая прибыль'] / df['Капит-я  млрд руб']
                df['ROS'] = df['Чистая прибыль'] / df['Выручка']
                df['Graham coefficient(P/E * P/B)'] = df['P/E'] * df['P/B']
                return df
            else:
                 raise ValueError('Table was not found on the page')
        else:
             raise ValueError(f'Error loading the page: {response.status_code}')

def main():
    url = "https://smart-lab.ru/q/shares_fundamental2/?type=MSFO"
    df = import_report(url)
    plt_info(df[:20], 'P/E')

if __name__ == '__main__':
    main()