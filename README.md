📊 E-Commerce Data Analysis Dashboard
=====================================
📂 Dataset

Menggunakan dataset publik Brazilian E-Commerce (Olist), yang berisi:

- customers_dataset.csv → informasi pelanggan

- orders_dataset.csv → detail order (status, waktu, pengiriman)

- order_items_dataset.csv → produk per order

- order_payments_dataset.csv → metode & nilai pembayaran

- order_reviews_dataset.csv → ulasan pelanggan

- products_dataset.csv & product_category_name_translation.csv → detail produk & kategori

- sellers_dataset.csv → informasi penjual

- geolocation_dataset.csv → data lokasi pelanggan & penjual

🧭 Methodology
==============
- Data Collection → Menggabungkan beberapa dataset Olist.

- Data Preprocessing → cleaning, handling missing values, parsing tanggal, join tabel.

- Exploratory Data Analysis (EDA) → menghitung statistik deskriptif & membuat visualisasi distribusi.

- Trend Analysis → order & revenue bulanan.

- Segmentation (RFM) → mengukur Recency, Frequency, Monetary untuk klasifikasi pelanggan.

- Visualization & Dashboard → membuat dashboard interaktif dengan Streamlit dan Plotly.

- Business Insight → menarik kesimpulan & rekomendasi strategi.

💡 Key Insights
===============
- Customer: Mayoritas berasal dari São Paulo.

- Products: Produk terpopuler adalah bed_bath_table dan health_beauty.

- Orders & Revenue: Lonjakan order terjadi pada Nov 2017 → peak season belanja.

- Payments: Lebih dari 70% transaksi menggunakan kartu kredit.

- Reviews: Didominasi rating 5⭐ → tingkat kepuasan pelanggan cukup tinggi.

- RFM Segmentation: Identifikasi Best Customers dan At Risk Customers → peluang retargeting.

📈 Sample Visualizations
========================
- Order Status Distribution → bar chart status pesanan (delivered, canceled, shipped, dll).

- Monthly Revenue Trend → line chart perkembangan penjualan.

- Top Product Categories → bar chart kategori produk terpopuler.

- Customer vs Seller Map → peta persebaran geografis (Pydeck).

- Customer Segmentation (RFM) → pie chart & bar chart distribusi segmen pelanggan.

🏆 Project Level
================
- Intermediate–Advanced

- Cocok untuk portfolio Data Analyst / Business Analyst.

- Menggunakan data real-world (>100k records).

- Menggabungkan EDA, Data Visualization, Customer Segmentation, dan Dashboarding.

⚙️ Tech Stack
=============
- Python → data preprocessing & analisis

- Pandas, NumPy → manipulasi data

- Plotly Express, Pydeck → visualisasi interaktif

- Streamlit → dashboard & deployment

GitHub → source code & dokumentasi

