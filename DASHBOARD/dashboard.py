import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as mtick
import datetime as dt
sns.set(style='dark')

# menyiapkan data all_data
all_df = pd.read_csv('all_data.csv')

# menyiapkan produk yang paling banyak dan sedikit dijual
def create_product_count_df(df):
    product_counts = df.groupby('product_category_name_english')['product_id'].count().reset_index()
    sorted_df = product_counts.sort_values(by='product_id', ascending=False)
    return sorted_df

# menyiapkan kota yang memiliki seller dan customer paling banyak
def create_city_customer_df(df):
    city_customer = all_df.customer_city.value_counts().sort_values(ascending=False).rename_axis('City').reset_index(name='Number of Customers') 
    return city_customer
def create_city_seller_df(df):
    city_seller = all_df.seller_city.value_counts().sort_values(ascending=False).rename_axis('City').reset_index(name='Number of Sellers')
    return city_seller


    # menyiapkan komponen filter
min_date = pd.to_datetime(all_df['order_approved_at']).dt.date.min()
max_date = pd.to_datetime(all_df['order_approved_at']).dt.date.max()

# menyiapkan side bar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Streamlit-logo-primary-colormark-darktext.png")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Span',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) &
                (all_df["order_approved_at"] <= str(end_date))]

# menyiapkan berbagai dataframe
product_count_df = create_product_count_df(main_df)
city_customer_df = create_city_customer_df(main_df)
city_seller_df = create_city_seller_df(main_df)

#   Membuat judul
st.title(' E-Commerce Public Dataset :star:')

# Membuat produk yang paling banyak dan sedikit terjual
st.header('Most & Least Product')
col1, col2 = st.columns(2)
with col1:
    most = product_count_df['product_id'].max()
    st.metric('Highest orders', value=most)
with col2:
    low = product_count_df['product_id'].min()
    st.metric('Lowest Order', value=low )

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name_english", hue="product_category_name_english", data=product_count_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=35)
ax[0].set_title("Products with the highest sales", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)

sns.barplot(x="product_id", y="product_category_name_english", hue="product_category_name_english", data=product_count_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=35)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Products with the lowest sales", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)

plt.suptitle("Most and Least Sold Products", fontsize=58)
st.pyplot(fig)

# Membuat kota dengan customer & seller terbanyak
st.header('City With Most Customers and Sellers.')
tab1, tab2 = st.tabs(['Customer', 'Sellers'])
with tab1:
    st.subheader('Most Customers City')
    top_5_cities_customer = city_customer_df.head(5)
    plt.figure(figsize=(10, 6))
    colors = ["#72BCD4" if city == top_5_cities_customer['City'].iloc[0] else "#D3D3D3" for city in top_5_cities_customer['City']]
    sns.barplot(x="Number of Customers", y="City", data=top_5_cities_customer, hue=top_5_cities_customer['City'], palette=colors, legend=False)
    plt.xlabel('Number of Customers')
    plt.ylabel('City')
    plt.title('Top 5 Cities with the Most Customers', fontsize=20)
    st.pyplot(plt)
with tab2:
    st.subheader('Most Sellers City')
    top_5_cities = city_seller_df.head(5)
    plt.figure(figsize=(10, 6))
    colors = ["#72BCD4" if city == top_5_cities['City'].iloc[0] else "#D3D3D3" for city in top_5_cities['City']]
    sns.barplot(x="Number of Sellers", y="City", data=top_5_cities, hue=top_5_cities['City'], palette=colors, legend=False)
    plt.xlabel('Number of Sellers')
    plt.ylabel('City')
    plt.title('Top 5 Cities with the Most Sellers', fontsize=20)
    st.pyplot(plt)
