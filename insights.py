def generate_insights(df):
    insights = []

    top_product = df.groupby("Product")["Total_Sales"].sum().idxmax()
    insights.append(f"Top product is {top_product}")

    top_region = df.groupby("Region")["Total_Sales"].sum().idxmax()
    insights.append(f"Best region is {top_region}")

    avg = df["Total_Sales"].mean()
    if avg < 20000:
        insights.append("Sales are below expected level")
    elif avg>20000:
        insights.append("sales are above your benchmark that you have given")

    return insights