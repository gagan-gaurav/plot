import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
	page_title = "Sales Dashboard",
	page_icon = ":bar_chart:",
	layout = "wide"
	)

df = pd.read_excel(
	io = 'sp.xlsx',
	engine = 'openpyxl',
	sheet_name = 'Sales',
	skiprows = 3,
	usecols = 'B:R',
	nrows = 1000,
)

# st.dataframe(df)

st.sidebar.header("please filter here")
city = st.sidebar.multiselect(
	"select the city",
	options=df["City"].unique(),
	default=df["City"].unique(),
)

customer_type = st.sidebar.multiselect(
	"select the customer type",
	options=df["Customer_type"].unique(),
	default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
	"select the Gender",
	options=df["Gender"].unique(),
	default=df["Gender"].unique(),
)

df_selection = df.query(
	"City == @city & Customer_type == @customer_type & Gender == @gender"
)

# st.dataframe(df_selection)

## -- main page ---

st.title(":bar_chart: sales dashboard")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
average_rating  = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
	st.subheader("Total Sales:")
	st.subheader(f"Us ${total_sales:,}")

with middle_column:
	st.subheader("Average Rating:")
	st.subheader(f"{average_rating}{star_rating}")

with right_column:
	st.subheader("Average Sales Per Transaction:")
	st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

sales_by_product_line = (
	df_selection.groupby(by = ["Product line"]).sum()[["Total"]].sort_values(by = "Total")
)
# st.dataframe(df_selection)

fig_product_sales= px.bar(
	sales_by_product_line,
	x = "Total",
	y = sales_by_product_line.index,
	orientation = "h",
	title = "<b> sales by produc line </b>",
	color_discrete_sequence = ["#0083B8"] * len(sales_by_product_line),
	template = "plotly_white",
)

st.plotly_chart(fig_product_sales)

