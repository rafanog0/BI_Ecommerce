import pandas as pd
import streamlit as st
import random
from streamlit_folium import st_folium
import folium
import matplotlib.pyplot as plt
from datetime import datetime

def order_count_region(df):
    # Dicionário de estados para região
    estado_para_regiao = {
        'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
        'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
        'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste', 'DF': 'Centro-Oeste',
        'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
        'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
    }
    
    # Mapear as regiões para números
    regiao_para_codigo = {
        'Norte': "N",
        'Nordeste': "NE",
        'Centro-Oeste': "CO",
        'Sudeste': "SE",
        'Sul': "S"
    }

    # Função para converter estado em código numérico
    def estado_para_codigo(estado):
        regiao = estado_para_regiao.get(estado, None)
        if regiao:
            return regiao_para_codigo[regiao]
        else:
            return None  # Para estados que não estão no dicionário

    # Aplicar a conversão no DataFrame
    df['region'] = df['customer_state'].apply(estado_para_codigo)

    resultado = df.groupby('region')['order_id'].sum().reset_index()
    resultado.columns = ['region', 'order_count_region']
    # resultado.to_csv("./region.csv", index=False)
    print(resultado.head(60))

    return resultado

def client_count_region(df):
    # Dicionário de estados para região
    estado_para_regiao = {
        'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
        'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
        'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste', 'DF': 'Centro-Oeste',
        'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
        'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
    }
    
    # Mapear as regiões para números
    regiao_para_codigo = {
        'Norte': "N",
        'Nordeste': "NE",
        'Centro-Oeste': "CO",
        'Sudeste': "SE",
        'Sul': "S"
    }

    # Função para converter estado em código numérico
    def estado_para_codigo(estado):
        regiao = estado_para_regiao.get(estado, None)
        if regiao:
            return regiao_para_codigo[regiao]
        else:
            return None  # Para estados que não estão no dicionário

    # Aplicar a conversão no DataFrame
    df['region'] = df['customer_state'].apply(estado_para_codigo)

    resultado = df.groupby('region')['client_count'].sum().reset_index()
    resultado.columns = ['region', 'clients_region']
    # resultado.to_csv("./region.csv", index=False)

    return resultado

def client_count_state(df):
    state_counts = df.groupby('customer_state').size()
    state_counts_df = state_counts.reset_index(name='client_count')
    # print(state_counts_df)
    return state_counts_df



def plot_clients_per_region(df, start_date, end_date):
    df = df[(df['register_date'] >= pd.Timestamp(start_date)) & (df['register_date'] <= pd.Timestamp(end_date))]
    # df.to_csv("./dataframe.csv", index=False)

    df = client_count_state(df)
    df = client_count_region(df)

    fig = plt.figure(figsize=(16,9))
    plt.style.use("ggplot")
    plt.bar(x = df["region"], height = df["clients_region"], width = 0.8)
    plt.xlabel("Region")
    plt.ylabel("Client Count")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    return fig



# def plot_sales_per_region(df):
#     df = df.groupby('customer_state')['order_total'].sum().reset_index()
#     df = client_count_region(df)
#     fig = plt.figure(figsize=(16,9))
#     plt.style.use("ggplot")
#     plt.bar(x = df["region"], height = df["order_total"], width = 0.8)
#     plt.xlabel("Region")
#     plt.ylabel("Sales")
#     plt.grid(True, which='both', linestyle='--', linewidth=0.5)
#     return fig

def plot_amount_of_orders_per_region(df):
    fig = plt.figure(figsize=(16,9))
    plt.style.use("ggplot")
    plt.bar(x = df["region"], height = df["order_count_region"], width = 0.8)
    plt.xlabel("Region")
    plt.ylabel("Amount of Orders")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    return fig

def main_page():
    st.markdown("# Ecommerce")
    st.sidebar.markdown("# Region Insights")
    st.write("## General Overview")
    st.write("This page contains general insights about this Ecommerce.")
    st.markdown('---')
    customers_df = pd.read_csv("./real_data/Customers_data_registered.csv", dtype = {'customer_zip_code_prefix': str})
    orders_df = pd.read_csv("./real_data/Orders_data.csv")

    customers_df['register_date'] = pd.to_datetime(customers_df['register_date'])

    start_date = st.date_input('Enter start date', value = datetime(2024,3,1))
    end_date = st.date_input('Enter end date')

    st.pyplot(plot_clients_per_region(customers_df, start_date, end_date))

    # st.markdown('---')
    # st.write("## Region Insights")  
    # region = st.selectbox("Select a region", ["Nordeste", "Sudeste", "Centro-Oeste", "Sul", "Norte"])
    # st.write(f"## {region}")

    # join the customer data with the order data to get the total orders per region
    customers_df = pd.merge(customers_df, orders_df, on = 'customer_id', how = 'inner')
    customers_df['order_delivered_customer_date'] = pd.to_datetime(customers_df['order_delivered_customer_date'])
    customers_df = customers_df[(customers_df['order_delivered_customer_date'] >= pd.Timestamp(start_date)) & (customers_df['order_delivered_customer_date'] <= pd.Timestamp(end_date))]
    #group the data by region and count the total orders per region 
    region_df = customers_df.groupby('customer_state')['order_id'].count().reset_index()
    region_df = order_count_region(region_df)
    # print(region_df.head(30))
    # print(len(region_df))

    # print(region_df.head(20))
    st.pyplot(plot_amount_of_orders_per_region(region_df))
    
    



def nordeste_page():
    st.write("Nordeste")

def sul_page():
    st.write("Sul")

def sudeste_page():
    st.write("Sudeste")

def centrooeste_page():
    st.write("Centro-Oeste")

def norte_page():
    st.write("Norte")


page_names_to_funcs = {
    "Ecommerce": main_page,
    "Nordeste": nordeste_page,
    "Sudeste": sudeste_page,
    "Centro-Oeste": centrooeste_page,
    "Sul": sul_page,
    "Norte": norte_page,
}

logo_path = './static/idp_logo.png'


st.sidebar.image(image = logo_path, width = 64)
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()