# CONFIGURASI #
import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
# END #

# Fungsi Haversine untuk hitung jarak #
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    return 6371 * c
# END #

# Load Dataset #
@st.cache_data
def load_data():
    customers = pd.read_csv("customers_dataset.csv")
    orders = pd.read_csv("orders_dataset.csv", parse_dates=["order_purchase_timestamp","order_delivered_customer_date"])
    order_items = pd.read_csv("order_items_dataset.csv")
    order_payments = pd.read_csv("order_payments_dataset.csv")
    order_reviews = pd.read_csv("order_reviews_dataset.csv")
    products = pd.read_csv("products_dataset.csv")
    product_cat = pd.read_csv("product_category_name_translation.csv")
    sellers = pd.read_csv("sellers_dataset.csv")
    geolocation = pd.read_csv("geolocation_dataset.csv")
    
    # join product-cat
    products = products.merge(product_cat, how="left",
                              left_on="product_category_name",
                              right_on="product_category_name")
    return customers, orders, order_items, order_payments, order_reviews, products, sellers, geolocation

customers, orders, order_items, order_payments, order_reviews, products, sellers, geolocation = load_data()
# END #

# Sidebar #
st.sidebar.title("📊 E-Commerce Data Analysis")
menu = st.sidebar.radio("Pilih Menu:", [
    "EDA",
    "Customers & Sellers",
    "Products",
    "Orders & Revenue",
    "Payments",
    "Reviews",
    "Geolocation",
    "RFM Segmentation"
])
# END #

# Menu EDA #
if menu == "EDA":
    st.title("📊 Exploratory Data Analysis")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customers", customers["customer_unique_id"].nunique())
    col2.metric("Orders", orders["order_id"].nunique())
    col3.metric("Sellers", sellers["seller_id"].nunique())
    col4.metric("Products", products["product_id"].nunique())
    
    status_counts = orders["order_status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    fig = px.bar(status_counts, x="status", y="count", title="Order Status Distribution")
    st.plotly_chart(fig, use_container_width=True)
# END #

# Customers & Sellers #
elif menu == "Customers & Sellers":
    st.title("👥 Customers & Sellers Analysis")
    
    cust_state = customers["customer_state"].value_counts().reset_index().head(10)
    cust_state.columns = ["state", "count"]
    fig = px.bar(cust_state, x="state", y="count", title="Top 10 Customer States")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Total Sellers: " + str(sellers["seller_id"].nunique()))
# END #

# Products #
elif menu == "Products":
    st.title("📦 Products Analysis")
    order_products = order_items.merge(products, on="product_id", how="left")
    top_cat = order_products["product_category_name_english"].value_counts().reset_index().head(10)
    top_cat.columns = ["category", "count"]
    fig = px.bar(top_cat, x="category", y="count", title="Top 10 Product Categories")
    st.plotly_chart(fig, use_container_width=True)
# END #

# Orders & Revenue #
elif menu == "Orders & Revenue":
    st.title("📈 Orders & Revenue Trend")
    orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M")
    
    monthly_orders = orders.groupby("order_month")["order_id"].count().reset_index()
    monthly_orders["order_month"] = monthly_orders["order_month"].astype(str)
    
    monthly_revenue = order_payments.merge(orders, on="order_id")
    monthly_revenue = monthly_revenue.groupby(monthly_revenue["order_purchase_timestamp"].dt.to_period("M"))["payment_value"].sum().reset_index()
    monthly_revenue["order_purchase_timestamp"] = monthly_revenue["order_purchase_timestamp"].astype(str)
    
    tab1, tab2 = st.tabs(["📦 Orders", "💰 Revenue"])
    with tab1:
        fig = px.line(monthly_orders, x="order_month", y="order_id", markers=True, title="Monthly Orders")
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        fig = px.line(monthly_revenue, x="order_purchase_timestamp", y="payment_value", markers=True, title="Monthly Revenue")
        st.plotly_chart(fig, use_container_width=True)
# END #

# Payments #
elif menu == "Payments":
    st.title("💳 Payments Analysis")
    payment_types = order_payments["payment_type"].value_counts().reset_index()
    payment_types.columns = ["payment_type", "count"]
    fig = px.bar(payment_types, x="payment_type", y="count", title="Payment Method Distribution")
    st.plotly_chart(fig, use_container_width=True)
# END #

# Reviews #
elif menu == "Reviews":
    st.title("⭐ Reviews Analysis")
    review_dist = order_reviews["review_score"].value_counts().sort_index().reset_index()
    review_dist.columns = ["review_score", "count"]
    fig = px.bar(review_dist, x="review_score", y="count", title="Review Score Distribution")
    st.plotly_chart(fig, use_container_width=True)
# END #

# Geolocation #
elif menu == "Geolocation":
    st.title("🌍 Geolocation Analysis")
    st.write("Jumlah data geo:", geolocation.shape[0])
    
    geo_state = geolocation["geolocation_state"].value_counts().reset_index().head(10)
    geo_state.columns = ["state", "count"]
    fig = px.bar(geo_state, x="state", y="count", title="Top 10 States by Geolocation")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Customer vs Seller Map (Sample)")
    cust_geo = customers.merge(geolocation, how="left", left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix")
    seller_geo = sellers.merge(geolocation, how="left", left_on="seller_zip_code_prefix", right_on="geolocation_zip_code_prefix")
    
    map_data = pd.concat([
        cust_geo[["geolocation_lat","geolocation_lng"]].sample(200).assign(type="Customer"),
        seller_geo[["geolocation_lat","geolocation_lng"]].sample(200).assign(type="Seller")
    ])
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position=["geolocation_lng","geolocation_lat"],
        get_radius=2000,
        get_color=["type == 'Customer' ? 0 : 255","type == 'Customer' ? 0 : 0","type == 'Customer' ? 255 : 0"],
        pickable=True
    )
    view_state = pdk.ViewState(latitude=-15, longitude=-47, zoom=3)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
# END #

# RFM Segmentation #
elif menu == "RFM Segmentation":
    st.title("📊 RFM Segmentation")
    df_merge = order_items.merge(order_payments, on="order_id", how="inner")
    df_merge = df_merge.merge(orders[["order_id","order_purchase_timestamp","customer_id"]], 
                              on="order_id", how="left")
    
    snapshot_date = orders["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm = df_merge.groupby("customer_id").agg({
        "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
        "order_id": "count",
        "payment_value": "sum"
    }).reset_index()
    rfm.columns = ["customer_id","Recency","Frequency","Monetary"]
    
    # Buat skor per quartile
    rfm["R_quartile"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
    rfm["F_quartile"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
    rfm["M_quartile"] = pd.qcut(rfm["Monetary"].rank(method="first"), 4, labels=[1,2,3,4])
    
    rfm["RFM_Score"] = rfm.R_quartile.astype(str) + rfm.F_quartile.astype(str) + rfm.M_quartile.astype(str)
    
    # Segmentasi sederhana
    def segment_customer(row):
        if row["RFM_Score"] in ["444","443","434","344"]:
            return "Best Customers"
        elif row["R_quartile"] == "4" and row["F_quartile"] in ["3","4"]:
            return "Loyal Customers"
        elif row["R_quartile"] in ["2","3"] and row["F_quartile"] in ["2","3","4"]:
            return "Potential Loyalist"
        elif row["R_quartile"] == "1":
            return "At Risk"
        else:
            return "Others"
    
    rfm["Segment"] = rfm.apply(segment_customer, axis=1)
    
    st.write("📌 RFM Sample")
    st.dataframe(rfm.head())
    
    # Visualisasi distribusi segmen
    seg_counts = rfm["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment","Count"]
    
    st.subheader("📊 Customer Segments Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(seg_counts, x="Segment", y="Count", title="Customer Segments")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.pie(seg_counts, names="Segment", values="Count", title="Customer Segments Pie Chart")
        st.plotly_chart(fig, use_container_width=True)
# END #