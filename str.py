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
chart = chart[:20]
charts = [go.Bar(x=chart['labels'].values, y=chart['data'].values, name='Frequency')]
figure = go.Figure(data=charts, layout=go.Layout({
    'barmode': 'group',
    'legend': {'orientation': 'h'},
    'title': {'text': 'neighbourhood Value Counts'},
    'xaxis': {'title': {'text': 'neighbourhood'}},
    'yaxis': {'title': {'text': 'Frequency'}}
}))
st.subheader('Neighbourhood Value Counts Visualization')
st.plotly_chart(figure)

st.write("The chart shows the mix of old and new neighborhoods. New sections feature modern villas, while established areas see long-term residents moving out. Infrastructure is improving with new amenities and services for the growing population. This combination of tradition and innovation makes the area attractive to potential buyers.")

st.sidebar.title("Filters")

region_options = list(df['location'].unique())
selected_region = st.sidebar.selectbox("Select Region", region_options)



neighborhood_options = list(df[df['location'] == selected_region]['neighbourhood'].unique())
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", neighborhood_options)

minprice = int(df[df['neighbourhood'] == selected_neighborhood]['price'].min()) - 1
maxprice = int(df[df['neighbourhood'] == selected_neighborhood]['price'].max())
minspace = int(df[df['neighbourhood'] == selected_neighborhood]['space'].min()) - 1
maxspace = int(df[df['neighbourhood'] == selected_neighborhood]['space'].max())

medprice = int(df[df['neighbourhood'] == selected_neighborhood]['price'].median())
medspace = int(df[df['neighbourhood'] == selected_neighborhood]['space'].median())

price_range = st.sidebar.slider("Price (SAR)", minprice, maxprice, (minprice, maxprice))
size_range = st.sidebar.slider("Size (sqm)", minspace, maxspace, (minspace, maxspace)) 
furnished_ch = st.sidebar.checkbox("Furnished")
garage_ch = st.sidebar.checkbox("Garage")
elevator_ch = st.sidebar.checkbox("Elevator")
maidroom_ch = st.sidebar.checkbox("Maid Room")
driver_ch = st.sidebar.checkbox("Driver Room")
pool_ch = st.sidebar.checkbox("Pool")
basement_ch = st.sidebar.checkbox("Basement")


filtered_df = df[(df['neighbourhood'] == selected_neighborhood) &
                    (df['price'] >= price_range[0]) & (df['price'] <= price_range[1]) &
                    (df['space'] >= size_range[0]) & (df['space'] <= size_range[1]) & 
                    (df['furnished'] == furnished_ch) & (df['garage'] == garage_ch) & 
                    (df['elevator'] == elevator_ch) & (df['maidRoom'] == maidroom_ch) & 
                    (df['pool'] == pool_ch) & (df['basement'] == basement_ch) & 
                    (df['driverRoom'] == driver_ch)]


      

st.subheader(f"Neighborhoods with Villas in the Price Range of {price_range[0]:,} SAR to {price_range[1]:,} SAR and Size Range of {size_range[0]:,} sqm to {size_range[1]:,} sqm")
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
fig = px.histogram(filtered_df, x='propertyAge', nbins=45, title=' ')

fig.update_layout(
    xaxis_title='Property Age',
    yaxis_title='Count',
    bargap=0.1,
    title_x=0.5,
) 
st.plotly_chart(fig)

st.write('As we explore the age of the villa, we notice a distinct pattern. In older neighbourhoods, there\'s a prevalence of villas reflecting the longstanding history and heritage of these areas. Conversely, in newer neighbourhoods, the trend is different, with villas predominantly younger than the age of the villa in older neighbourhoods.')


st.subheader("Conclusion")
st.write("With this helpful guide, the family can confidently choose the best villa in Riyadh. By exploring different neighborhoods and comparing features and prices, they can find a home that perfectly matches their needs and preferences.")