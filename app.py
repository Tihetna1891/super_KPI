import requests

from map import *
# Sidebar inputs
start_date, end_date, time_frame = sidebar()

# Load data from the database
orders = get_orders(start_date, end_date)
products = get_product()
product_names = get_product_names()

# st.write("Products DataFrame:")
# st.write(products.head())
# st.write("Product Names DataFrame:")
# st.write(product_names.head())

products = products.merge(product_names, on='name_id')

# # Streamlit date input and time frame selection
# start_date = st.sidebar.date_input("Start date", datetime(2023, 1, 1))
# end_date = st.sidebar.date_input("End date", datetime.today())
# time_frame = st.sidebar.selectbox("Select time frame", ["Daily", "Weekly", "Monthly", "Yearly"])

# selected_date_range = st.sidebar.date_input("Select Date Range", 
#                                         value=(pd.to_datetime('today') - pd.to_timedelta(7, unit='d'), 
#                                                 pd.to_datetime('today')), 
#                                         key="date_range")

# start_date = selected_date_range[0]
# end_date = selected_date_range[1]

total_sales = calculate_total_sales(orders, products, time_frame)
order_volume = calculate_order_volume(orders, products, time_frame)
average_order_value = calculate_average_order_value(orders, products, time_frame)
fulfillment_time = calculate_fulfillment_time(orders, products, time_frame)
product_popularity_data = product_popularity(orders, products, time_frame)
# order_volume_by_status = calculate_order_volume_by_status(orders, products, time_frame)

# Summarize the most sold products
most_sold_products = total_sales.groupby('product_name')['total_sales'].sum().reset_index().sort_values(by='total_sales', ascending=False)
sorted_product_names = most_sold_products['product_name'].tolist()

# Get unique vendor names for selection
unique_vendor_names = products['vendor_name'].unique()
selected_vendors = st.sidebar.multiselect("Select vendors", unique_vendor_names, default=unique_vendor_names)

# Display products sorted by most sold
selected_products = st.sidebar.multiselect("Select products", sorted_product_names, default=sorted_product_names)

# Sidebar filters (if needed)
# unique_statuses = order_volume_by_status['status'].unique().tolist()
# selected_statuses = st.sidebar.multiselect("Select order statuses", unique_statuses, default=unique_statuses)

# filtered_order_volume_by_status = order_volume_by_status[
#     (order_volume_by_status['vendor_name'].isin(selected_vendors)) &
#     (order_volume_by_status['product_name'].isin(selected_products)) &
#     (order_volume_by_status['status'].isin(selected_statuses))
# ]

# Get unique product names for selection
# unique_product_names = products['product_name'].unique()
# selected_products = st.sidebar.multiselect("Select products", unique_product_names, default=unique_product_names)

# Filter data based on selected vendors
total_sales = total_sales[total_sales['vendor_name'].isin(selected_vendors) & (total_sales['product_name'].isin(selected_products))]
# st.write("Filtered Total Sales Data", total_sales.head())
order_volume = order_volume[order_volume['vendor_name'].isin(selected_vendors) & (order_volume['product_name'].isin(selected_products))]
average_order_value = average_order_value[average_order_value['vendor_name'].isin(selected_vendors) & (average_order_value['product_name'].isin(selected_products))]
fulfillment_time = fulfillment_time[fulfillment_time['vendor_name'].isin(selected_vendors) & (fulfillment_time['product_name'].isin(selected_products))]
product_popularity_data = product_popularity_data[product_popularity_data['vendor_name'].isin(selected_vendors) & (product_popularity_data['product_name'].isin(selected_products))]


# Streamlit dashboard
st.title('Vendor Performance KPI')
# Summary section
st.subheader("Summary")
st.markdown(f"**Total Sales:** {total_sales['total_sales'].sum():,.2f}")
st.markdown(f"**Total Orders:** {order_volume['order_count'].sum()}")
st.markdown(f"**Average Order Value:** {average_order_value['average_order_value'].mean():,.2f}")

top_products = most_sold_products.head(5)
st.markdown("**Top 5 Most Sold Products:**")
for i, row in top_products.iterrows():
    st.markdown(f"- {row['product_name']}: {row['total_sales']:,.2f}")


# # Total Sales by Vendor
# st.header('Total Sales by Vendor')
# # st.dataframe(total_sales)

# sales_chart = alt.Chart(total_sales).mark_bar().encode(
#     x='date:T',
#     y='total_sales:Q',
#     color='vendor_name:N',
#     tooltip=['vendor_name', 'date', 'total_sales']
# ).interactive().properties(title='Total Sales Over Time')
# st.altair_chart(sales_chart, use_container_width=True)

# # Order Volume by Vendor
# st.header('Order Volume by Vendor')
# # st.dataframe(order_volume)

# volume_chart = alt.Chart(order_volume).mark_bar().encode(
#     x=alt.X('date:T', title='Date' if time_frame == 'Daily' else 'Time Frame'),
#     y='order_count:Q',
#     color='vendor_name:N',
#     tooltip=['vendor_name', 'date', 'order_count']
# ).interactive().properties(title='Order Volume Over Time')
# st.altair_chart(volume_chart, use_container_width=True)

# # Average Order Value by Vendor
# st.header('Average Order Value by Vendor')
# # st.dataframe(average_order_value)

# aov_chart = alt.Chart(average_order_value).mark_bar().encode(
#     x='date:T',
#     y='average_order_value:Q',
#     color='vendor_name:N',
#     tooltip=['vendor_name', 'date', 'average_order_value']
# ).interactive().properties(title='Average Order Value Over Time')
# st.altair_chart(aov_chart, use_container_width=True)
# # Total Sales by Vendor
# st.header('Total Sales by Vendor')
# st.dataframe(total_sales)

# sales_chart = alt.Chart(total_sales).mark_line().encode(
#     x='date:T',
#     y='total_sales:Q',
#     color='vendor_id:N',
#     tooltip=['vendor_id', 'date', 'total_sales']
# ).interactive().properties(title='Total Sales Over Time')
# st.altair_chart(sales_chart, use_container_width=True)

# # Order Volume by Vendor

# st.dataframe(order_volume)
total_sales['vendor_product'] = total_sales['vendor_name'] + ' - ' + total_sales['product_name']
st.header('Total sales by Vendor')
# st.write("Total Sales Data for Chart", total_sales)
st.markdown("""
### Total Sales
This metric calculates the total revenue generated from sales over a specified period. It is calculated by summing the sales revenue for each product sold.
""")
sales_chart = alt.Chart(total_sales).mark_line().encode(
    x='date:T',
    y='total_sales:Q',
    color='vendor_product:N',
    tooltip=['vendor_name','product_name', 'date', 'total_sales']
).interactive().properties(title='Total Sales Over Time').facet(
    column=alt.Column('vendor_name:N', header=alt.Header(labelAngle=-90, titleOrient='top'))
)
# .facet(
#     column='vendor_name:N'
# )
st.altair_chart(sales_chart, use_container_width=True)
# Loop through each selected vendor and create separate charts
for vendor in selected_vendors:
    st.subheader(f'Total Sales for {vendor}')
    vendor_data = total_sales[total_sales['vendor_name'] == vendor]
    
    if not vendor_data.empty:
        vendor_data['vendor_product'] = vendor_data['product_name']
        
        sales_chart = alt.Chart(vendor_data).mark_line().encode(
            x='date:T',
            y='total_sales:Q',
            color='vendor_product:N',
            tooltip=['vendor_name', 'product_name', 'date', 'total_sales']
        ).interactive().properties(
            title=f'Total Sales Over Time for {vendor}'
        )
        
        st.altair_chart(sales_chart, use_container_width=True)
    else:
        st.write(f"No data available for {vendor}")

total_sales['vendor_product'] = total_sales['vendor_name'] + ' - ' + total_sales['product_name']
st.header('Order Volume by Vendor')
st.markdown("""
### Order Volume
This metric measures the total number of COMPLETED orders placed over a specified period. It indicates the quantity of products sold.
""")
volume_chart = alt.Chart(order_volume).mark_line().encode(
    x=alt.X('date:T', title='Date' if time_frame == 'Daily' else 'Time Frame'),
    y='order_count:Q',
    color='vendor_name:N',
    tooltip=['vendor_name','product_name', 'date', 'order_count']
).interactive().properties(title='Order Volume Over Time')
st.altair_chart(volume_chart, use_container_width=True)

# st.markdown("""
# ### Order Volume by Status
# This metric measures the total number of orders placed over a specified period, categorized by their status (COMPLETED, FAILED, PENDING). It helps understand the distribution of order statuses.
# """)

# # Create and display the chart
# heatmap = alt.Chart(filtered_order_volume_by_status).mark_line().encode(
#     x=alt.X('date:T', title='Order Status'),
#     y=alt.Y('status:N', title='Status'),
#     color='vendor_name:N',
#     # color=alt.Color('order_volume:Q', title='Order Volume', scale=alt.Scale(scheme='viridis')),
#     tooltip=['vendor_name', 'product_name', 'status', 'order_volume']
# ).facet(
#     facet='product_name:N',
#     columns=4
# ).properties(
   
#     title='Order Volume by Status'
   
# )

# st.altair_chart(heatmap, use_container_width=True)

# # Average Order Value by Vendor
st.header('Average Order Value by Vendor')
st.markdown("""
### Average Order Value
This metric calculates the average revenue per order. It is calculated by dividing the total sales revenue by the number of orders.
""")
aov_chart = alt.Chart(average_order_value).mark_line().encode(
    x='date:T',
    y='average_order_value:Q',
    color='vendor_name:N',
    tooltip=['vendor_name','product_name', 'date', 'average_order_value']
).interactive().properties(title='Average Order Value Over Time')
st.altair_chart(aov_chart, use_container_width=True)


st.header('Fulfillment Time by Vendor')
st.markdown("""
### Fulfillment Time
This metric measures the average time taken to fulfill orders from the time they are placed to the time they are delivered. It indicates the efficiency of the fulfillment process.
""")
fulfillment_time_chart = alt.Chart(fulfillment_time).mark_line().encode(
    x=alt.X('time_frame:T', title='Date' if time_frame == 'Daily' else 'Time Frame'),
    y='fulfillment_time:Q',
    color='vendor_name:N',
    tooltip=['vendor_name','product_name', 'fulfillment_time']
).interactive().properties(title='Fulfillment Time by Vendor')
st.altair_chart(fulfillment_time_chart, use_container_width=True)

st.header('Product Popularity by Vendor')
st.markdown("""
### Product Popularity
This metric measures the popularity of each product based on the number of units sold. It helps identify the best-selling products.
""")
product_popularity_data_chart = alt.Chart(product_popularity_data).mark_line().encode(
    x=alt.X('time_frame:T', title='Date' if time_frame == 'Daily' else 'Time Frame'),
    y='product_popularity:Q',
    color='vendor_name:N',
    # tooltip=['vendor_name','product_name','product_popularity']
).interactive().properties(title='Product Popularity by Vendor')
st.altair_chart(product_popularity_data_chart, use_container_width=True)
# Calculate metrics
# return_rate = calculate_return_rate(orders, products, time_frame)

# customer_satisfaction = calculate_customer_satisfaction(orders,products, time_frame)
# stock_alerts_data = stock_alerts(orders, products, time_frame)


# # Visualization functions
# def create_line_chart(df, x_col, y_col, z_col,tool,title):
#     chart = alt.Chart(df).mark_line().encode(
#         x=x_col,
#         y=y_col,
#         color=z_col,
#         tooltip=tool
#     ).properties(
#         title=title
#     )
#     return chart

# # Display metrics


# st.subheader("Return Rate")
# st.altair_chart(create_line_chart(return_rate, 'time_frame', 'return_rate','vendor_name',['vendor_name','product_name','date','return rate'],'Return Rate by Vendor'))

# st.subheader("Fulfillment Time")
# st.altair_chart(create_line_chart(fulfillment_time, 'time_frame', 'fulfillment_time','vendor_name', ['vendor_name','product_name','date','Fulfillment Time by Vendor'],'Fulfillment Time by Vendor'))

# st.subheader("Customer Satisfaction")
# st.altair_chart(create_bar_chart(customer_satisfaction, 'vendor_name', 'average_satisfaction', 'Customer Satisfaction by Vendor'))

# st.subheader("Stock Alerts")
# st.altair_chart(create_bar_chart(stock_alerts_data, 'time_frame', 'stock_alert_count','vendor_name', 'Stock Alerts by Vendor'))

# st.subheader("Product Popularity")
# st.altair_chart(create_line_chart(product_popularity_data, 'time_frame', 'total_quantity_sold','vendor_name',['vendor_name','product_name','date','Product Popularity by Vendor'], 'Product Popularity by Vendor'))
