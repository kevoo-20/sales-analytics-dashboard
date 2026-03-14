import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load data
df = pd.read_csv("sales_data.csv")

df["revenue"] = df["quantity"] * df["price"]
df["date"] = pd.to_datetime(df["date"])

# KPIs
total_revenue = df["revenue"].sum()
total_orders = df["order_id"].count()
avg_order = round(df["revenue"].mean(),2)

# Charts
sales_by_product = df.groupby("product")["revenue"].sum().reset_index()
fig_product = px.bar(sales_by_product, x="product", y="revenue", title="Revenue by Product")

monthly = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().reset_index()
monthly["date"] = monthly["date"].astype(str)
fig_month = px.line(monthly, x="date", y="revenue", markers=True, title="Monthly Revenue Trend")

region = df.groupby("region")["revenue"].sum().reset_index()
fig_region = px.bar(region, x="region", y="revenue", title="Revenue by Region")

category = df.groupby("category")["revenue"].sum().reset_index()
fig_category = px.pie(category, values="revenue", names="category", title="Category Share")

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Sales Analytics Dashboard", style={"textAlign":"center"}),

    html.Div([
        html.Div([
            html.H3("Total Revenue"),
            html.H2(f"${total_revenue}")
        ], className="card"),

        html.Div([
            html.H3("Total Orders"),
            html.H2(total_orders)
        ], className="card"),

        html.Div([
            html.H3("Average Order Value"),
            html.H2(f"${avg_order}")
        ], className="card"),
    ], style={"display":"flex","justifyContent":"space-around"}),

    dcc.Graph(figure=fig_product),
    dcc.Graph(figure=fig_month),
    dcc.Graph(figure=fig_region),
    dcc.Graph(figure=fig_category)

])
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)