import streamlit as st
# st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
# Custom CSS for background image
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://img.freepik.com/free-vector/city-road-traffic-urban-landscape-intersection-with-city-cars-street-crosswalk-with-lights-background_80590-7646.jpg?size=626&ext=jpg");
        background-size: cover;
    }
    .sidebar .sidebar-content {
        background: url("https://img.freepik.com/free-vector/city-road-traffic-urban-landscape-intersection-with-city-cars-street-crosswalk-with-lights-background_80590-7646.jpg?size=626&ext=jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    try:
        st.markdown('<h1 style="color: #CFD4D7; text-align: center;">TRAFFICANALYZER 🚗</h1>', unsafe_allow_html=True)
        st.markdown('<h6 style="color: #CFD4D7; text-align: center;">Get your area traffic trends here</h6>', unsafe_allow_html=True)
        traffic_data = pd.read_csv("traffic.csv")
        st.write(traffic_data)
        
        # Descriptive Statistics
        st.markdown("<h3 style='text-align: center;'>Descriptive Statistics</h3>", unsafe_allow_html=True)
        st.write(traffic_data.describe())
        st.write(traffic_data.describe(include='object'))

        # Data Preprocessing
        st.markdown("<h3 style='text-align: center;'>Data Preprocessing</h3>", unsafe_allow_html=True)
        st.write(f"Before dropping: {traffic_data.shape[0]}")
        traffic_data.drop_duplicates(keep="first", inplace=True) 
        st.write(f"After dropping: {traffic_data.shape[0]}")
        if traffic_data.isnull().sum().sum() == 0:
            st.write('No missing values in train')
        else:
            traffic_data.fillna(method='ffill', inplace=True)
        traffic_data['DateTime'] = pd.to_datetime(traffic_data['DateTime'])
        traffic_data["Year"] = traffic_data['DateTime'].dt.year  
        traffic_data["Month"] = traffic_data['DateTime'].dt.month  
        traffic_data["Date_no"] = traffic_data['DateTime'].dt.day  
        traffic_data["Hour"] = traffic_data['DateTime'].dt.hour  

        # Data Visualization
        st.markdown("<h3 style='text-align: center;'>Data Visualization</h3>", unsafe_allow_html=True)

        # Histogram of Vehicles column
        st.markdown("<h4 style='text-align: center;'>Histogram of Vehicles Column</h4>", unsafe_allow_html=True)
        plt.hist(traffic_data['Vehicles'], bins=30)
        st.pyplot()

        # Time Series Plot
        st.markdown("<h4 style='text-align: center;'>Time Series Plot</h4>", unsafe_allow_html=True)
        st.line_chart(traffic_data.set_index('DateTime')['Vehicles'])

        # Line plot of traffic volume over time
        st.markdown("<h4 style='text-align: center;'>Line Plot of Traffic Volume Over Time</h4>", unsafe_allow_html=True)
        traffic_data_resampled = traffic_data.set_index('DateTime').resample('D').mean()
        st.line_chart(traffic_data_resampled['Vehicles'])

        # Boxplots to compare traffic volumes across different junctions
        st.markdown("<h4 style='text-align: center;'>Boxplots of Traffic Volume by Junction</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.boxplot(traffic_data['Vehicles'], patch_artist=True)
        st.pyplot(fig)

        # Identifying peak traffic hours
        st.markdown("<h4 style='text-align: center;'>Peak Traffic Hours</h4>", unsafe_allow_html=True)
        traffic_data['HourOfDay'] = traffic_data['DateTime'].dt.hour
        traffic_data['DayOfWeek'] = traffic_data['DateTime'].dt.day_name()
        hourly_traffic = traffic_data.groupby('HourOfDay')['Vehicles'].mean().reset_index()

        # Aggregate data to find mean traffic volume for each day of the week
        weekly_traffic = traffic_data.groupby('DayOfWeek')['Vehicles'].mean().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ).reset_index()

        # Plotting the hourly traffic volume
        st.markdown("<h4 style='text-align: center;'>Hourly Traffic Volume</h4>", unsafe_allow_html=True)
        st.bar_chart(hourly_traffic.set_index('HourOfDay'))

    except FileNotFoundError:
        st.write("File not found. Please make sure the file path is correct.")
    except ValueError as ve:
        st.write(f"An error occurred: {ve}")

if __name__ == "__main__":
    main()
