import streamlit as st 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


df = pd.read_csv('VillasCleaned.csv')


#title and Introduction
st.title("Discover Your Dream Villa in Riyadh")

# #Introduction
st.write("Imagine a family planning their move to the exciting city of Riyadh. They are looking for a home that fits their lifestyle, balancing cost, space, and luxury. Riyadh, with its rich culture and fast-growing development, offers many villa options to suit different family needs. Through this guide, we aim to help the family find the perfect villa in Riyadh.")

if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

s = df[~pd.isnull(df['neighbourhood'])]['neighbourhood']
chart = pd.value_counts(s).to_frame(name='data')
chart['percent'] = (chart['data'] / chart['data'].sum()) * 100
chart.index.name = 'labels'
chart = chart.reset_index().sort_values(['data', 'labels'], ascending=[False, True])
chart = chart[:100]
charts = [go.Bar(x=chart['labels'].values, y=chart['data'].values, name='Frequency')]
figure = go.Figure(data=charts, layout=go.Layout({
    'barmode': 'group',
    'legend': {'orientation': 'h'},
    'title': {'text': ' '},
    'xaxis': {'title': {'text': 'neighbourhood'}},
    'yaxis': {'title': {'text': 'Frequency'}}
}))
st.subheader('Neighbourhood Value Counts Visualization')
st.plotly_chart(figure)

st.sidebar.title("Filters")

region_options = list(df['location'].unique())
selected_region = st.sidebar.selectbox("Select Region", region_options)



neighborhood_options = list(df[df['location'] == selected_region]['neighbourhood'].unique())
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", neighborhood_options)

minprice = int(df[df['neighbourhood'] == selected_neighborhood]['price'].min())
maxprice = int(df[df['neighbourhood'] == selected_neighborhood]['price'].max())
minspace = int(df[df['neighbourhood'] == selected_neighborhood]['space'].min())
maxspace = int(df[df['neighbourhood'] == selected_neighborhood]['space'].max())

medprice = int(df[df['neighbourhood'] == selected_neighborhood]['price'].median())
medspace = int(df[df['neighbourhood'] == selected_neighborhood]['space'].median())

price_min = st.sidebar.slider("Minimum Price (SAR)", minprice - 1, maxprice, medprice//2)
price_max = st.sidebar.slider("Maximum Price (SAR)", minprice - 1, maxprice, medprice)
size_min = st.sidebar.slider("Minimum Size (sqm)", minspace - 1, maxspace, medspace//2) 
size_max = st.sidebar.slider("Maximum Size (sqm)", minspace - 1, maxspace, medspace)
kitchen_ch = st.sidebar.checkbox("Kitchen")
garage_ch = st.sidebar.checkbox("Garage")
elevator_ch = st.sidebar.checkbox("Elevator")
maidroom_ch = st.sidebar.checkbox("Maidroom")
pool_ch = st.sidebar.checkbox("Pool")
basement_ch = st.sidebar.checkbox("Basement")


filtered_df = df[(df['neighbourhood'] == selected_neighborhood) &
                    (df['price'] >= price_min) & (df['price'] <= price_max) &
                    (df['space'] >= size_min) & (df['space'] <= size_max) & (df['kitchen'] == kitchen_ch) & (df['garage'] == garage_ch)
                    & (df['elevator'] == elevator_ch) & (df['maidRoom'] == maidroom_ch) & (df['pool'] == pool_ch) & (df['basement'] == basement_ch)]


      

st.subheader(f"Neighborhoods with Villas in the Price Range of {price_min} SAR to {price_max} SAR and Size Range of {size_min} sqm to {size_max} sqm:")
st.write('To help the family in their search, we explore the villa market in Riyadh, focusing on important factors like price, size, and features. Using interactive tools and filters, we can find the best neighborhoods and villa options that meet their needs.')
# st.write(filtered_df['neighbourhood'].unique())

fig = go.Figure()

for feature in ['rooms', 'lounges', 'bathrooms']:
    fig.add_trace(go.Scatter(x=filtered_df['price'], y=filtered_df[feature],
                             mode='markers',
                            marker=dict(size=10, opacity=0.5),                 
                            name=feature))

#Update layout
fig.update_layout(title='Price vs Features',
                  xaxis_title='Price (SAR)',
                  yaxis_title='Count',
                  showlegend=True)


#Display the figure
st.plotly_chart(fig)

st.write("The family can filter villas based on their budget and the required size. This helps in narrowing down the options to those that fit their financial and spatial needs.")
st.write("By selecting different neighborhoods, the family can explore which areas offer villas within their desired price and size range.")

st.subheader("Property Age Distribution by Neighborhood")
fig = px.histogram(filtered_df, x='propertyAge', nbins=20, title=' ')

fig.update_layout(
    xaxis_title='Property Age',
    yaxis_title='Count',
    bargap=0.1,
    title_x=0.5 
) 
st.plotly_chart(fig)


st.subheader("Conclusion")
st.write("With this helpful guide, the family can confidently choose the best villa in Riyadh. By exploring different neighborhoods and comparing features and prices, they can find a home that perfectly matches their needs and preferences.")