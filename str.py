import streamlit as st 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
df = pd.read_csv('Data/VillasCleand.csv')


#title and Introduction
st.title("Villas in Riyadh")

# #Introduction
# st.write("Riyadh offers a diverse range of villa properties catering to various family needs and preferences.")

# #Slider for choosing price range
# st.sidebar.subheader("Choose Price Range")
# price_min = st.sidebar.slider("Minimum Price (SAR)", int(df['price'].min()), int(df['price'].max()), int(df['price'].min()))
# price_max = st.sidebar.slider("Maximum Price (SAR)", int(df['price'].min()), int(df['price'].max()), int(df['price'].max()))

# #Filter the dataframe based on selected price range
# filtered_df = df[(df['price'] >= price_min) & (df['price'] <= price_max)]

# #Display neighborhoods with villas in the selected price range
# st.subheader(f"Neighborhoods with Villas in the Price Range of {price_min} SAR to {price_max} SAR:")
# st.write(filtered_df['neighbourhood'].unique())

# #Slider for choosing size range
# st.sidebar.subheader("Choose Size Range (sqm)")
# size_min = st.sidebar.slider("Minimum Size", int(df['space'].min()), int(df['space'].max()), int(df['space'].min()))
# size_max = st.sidebar.slider("Maximum Size", int(df['space'].min()), int(df['space'].max()), int(df['space'].max()))

# #Filter the dataframe based on selected size range
# filtered_df = df[(df['space'] >= size_min) & (df['space'] <= size_max)]

# #Display neighborhoods with villas in the selected size range
# st.subheader(f"Neighborhoods with Villas in the Size Range of {size_min} sqm to {size_max} sqm:")
# st.write(filtered_df['neighbourhood'].unique())

st.write("Riyadh offers a diverse range of villa properties catering to various family needs and preferences. \
          Let's explore some insights from our villa dataset.")

st.sidebar.title("Filters")
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", df['neighbourhood'].unique())
price_min = st.sidebar.slider("Minimum Price (SAR)", int(df['price'].min()), int(df['price'].max()), int(df['price'].min()))
price_max = st.sidebar.slider("Maximum Price (SAR)", int(df['price'].min()), int(df['price'].max()), int(df['price'].max()))
size_min = st.sidebar.slider("Minimum Size (sqm)", int(df['space'].min()), int(df['space'].max()), int(df['space'].min()))
size_max = st.sidebar.slider("Maximum Size (sqm)", int(df['space'].min()), int(df['space'].max()), int(df['space'].max()))

filtered_df = df[(df['neighbourhood'] == selected_neighborhood) &
                 (df['price'] >= price_min) & (df['price'] <= price_max) &
                 (df['space'] >= size_min) & (df['space'] <= size_max)]

st.subheader(f"Neighborhoods with Villas in the Price Range of {price_min} SAR to {price_max} SAR and Size Range of {size_min} sqm to {size_max} sqm:")
st.write(filtered_df['neighbourhood'].unique())

fig = go.Figure()

for feature in ['rooms', 'lounges', 'bathrooms', 'kitchen', 'garage', 'elevator', 'maidRoom', 'pool', 'basement']:
    fig.add_trace(go.Scatter(x=filtered_df['price'], y=filtered_df[feature],
                             mode='markers',
                             marker=dict(size=filtered_df[feature]*2, opacity=0.5),
                             name=feature))

#Update layout
fig.update_layout(title='Price vs Features',
                  xaxis_title='Price (SAR)',
                  yaxis_title='Count',
                  showlegend=True)


#Display the figure
st.plotly_chart(fig)




st.subheader(f"Distribution of Features in {selected_neighborhood}")
fig = px.bar(filtered_df.drop(columns=['neighbourhood', 'location', 'price', 'square price']).sum(),
             labels={'index': 'Feature', 'value': 'Count'}, title=f"Features in {selected_neighborhood}")
st.plotly_chart(fig)
