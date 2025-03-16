import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Load Data
df = pd.read_csv('coaster_db_clean.csv')

# Streamlit UI
st.set_page_config(page_title='Roller Coaster EDA', layout='wide')
st.title('🎢 Roller Coaster Exploratory Data Analysis')

# Sidebar Filters
st.sidebar.header('Filters')
years = st.sidebar.multiselect('Select Years:', df['Year_Introduced'].dropna().unique())

df_filtered = df[df['Year_Introduced'].isin(years)] if years else df

# Bar Chart - Top 10 Years Coasters Introduced
year_counts = df['Year_Introduced'].value_counts().head(10)
fig_bar = px.bar(year_counts, x=year_counts.index, y=year_counts.values,
                 title='🎢 Top 10 Years Coasters Introduced',
                 labels={'x': 'Year Introduced', 'y': 'Count'},
                 color=year_counts.values, color_continuous_scale='blues')
st.plotly_chart(fig_bar, use_container_width=True)

# Histogram - Speed Distribution
fig_hist = px.histogram(df, x='Speed_mph', nbins=20,
                        title='📊 Coaster Speed Distribution (mph)',
                        labels={'Speed_mph': 'Speed (mph)'},
                        color_discrete_sequence=['#FF5733'])
st.plotly_chart(fig_hist, use_container_width=True)

# KDE Plot - Speed
fig_kde = ff.create_distplot([df['Speed_mph'].dropna()], ['Speed'], show_hist=False, curve_type='kde')
st.plotly_chart(fig_kde, use_container_width=True)

# Scatter Plot - Speed vs. Height
fig_scatter = px.scatter(df_filtered, x='Speed_mph', y='Height_ft',
                         title='📍 Coaster Speed vs. Height',
                         labels={'Speed_mph': 'Speed (mph)', 'Height_ft': 'Height (ft)'},
                         color='Year_Introduced', size='Inversions',
                         color_continuous_scale='viridis')
st.plotly_chart(fig_scatter, use_container_width=True)

# Correlation Heatmap
df_corr = df[['Speed_mph', 'Height_ft', 'Inversions', 'Gforce']].corr()
fig_heatmap = px.imshow(df_corr, text_auto=True, title='🔥 Correlation Heatmap')
st.plotly_chart(fig_heatmap, use_container_width=True)

# Bar Chart - Average Speed by Location
location_speeds = df.groupby('Location')['Speed_mph'].agg(['mean', 'count']).query('count >= 10').sort_values('mean')
fig_location = px.bar(location_speeds, x=location_speeds.index, y='mean',
                      title='📌 Average Coaster Speed by Location',
                      labels={'index': 'Location', 'mean': 'Average Speed (mph)'},
                      color='mean', color_continuous_scale='blues', orientation='h')
st.plotly_chart(fig_location, use_container_width=True)

st.markdown('🚀 **Enjoy exploring the thrilling world of roller coasters!**')

