

#imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the app
st.set_page_config(page_title=" 💿Data sweeper", layout='wide')
st.title("💿Data sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

#uplload the
if uploaded_files is not None and len(uploaded_files) > 0:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")    
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.getbuffer().nbytes / 1024:.2f} KB") 

        st.write("🔍Preview the Head of the Dataframe")
        st.dataframe(df.head())

        #  Data Cleaning options 
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed successfully!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    
                    if len(numeric_cols) > 0:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing values have been filled successfully!")

                        # ✅ Debugging: Check if missing values are gone
                        st.write("Missing Values Count After Cleaning:")
                        st.write(df.isnull().sum())
                    else:
                        st.write("⚠ No numeric columns found for missing value filling.")

        # Choose Specific columns to Keep or Convert
        st.subheader("🎯Select Columns to Convert")
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]  # ✅ Fixed this line! (Keeping only selected columns)

        # Create Some Visualizations
        st.subheader("📊 Data visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the File -> CSV to Excel
        st.subheader("🔄Conversion Options")
        conversion_types = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name} "):
            buffer = BytesIO()
            if conversion_types == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_types == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"⬇️Download {file_name} as {conversion_types}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )  

# SUCCESULLY ALL FILES  ARE PROCEEDS HERE
st.success("🎉 All files processed successfully!")





