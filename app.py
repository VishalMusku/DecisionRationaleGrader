# import streamlit as st
# import pandas as pd
# from preprocess import process_excel  # Import preprocess function
# from grading import grade_messages  # Import grading function


# # Streamlit interface
# st.title("Rationale Grading ")

# # Upload Excel file 
# uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])


# if uploaded_file is not None:
#     # Step 1: Preprocess the uploaded file
#     st.write("Processing the uploaded file...")
    
#     # Preprocess the Excel file and return a DataFrame
#     preprocessed_data = process_excel(uploaded_file)
    
#     # Display the preprocessed data (optional)
#     st.write("Preprocessed Data:")
    
#     st.dataframe(preprocessed_data)
    
#     # Step 2: Grade the messages using LLM
#     if st.button("Run Grading"):
#         st.write("Grading messages with LLM...")
        
#         # Pass the preprocessed data to the grading function
#         graded_data = grade_messages()
        
#         # Display the graded results
#         st.write("Grading Results:")
#         st.dataframe(graded_data)
        
#         # Option to download results
#         st.download_button(
#             label="Download Grading Results",
#             data=graded_data.to_excel(index=False, engine='openpyxl'),
#             file_name="graded_results.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

import streamlit as st
import pandas as pd
from preprocess import process_excel  # Import preprocess function
from grading import grade_messages  # Import grading function

# Streamlit interface configuration
st.set_page_config(page_title="Rationale Grading", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f7f9fc;  /* Light background for a modern look */
        font-family: 'Arial', sans-serif;  /* Readable font */
    }
    .title {
        color: #2c3e50;  /* Dark color for the title */
        font-size: 2.5em;  /* Large font for title */
        text-align: center;
        margin: 30px 0;
    }
    .header {
        color: #2980b9;  /* Color for headers */
        font-size: 1.5em;
        margin: 15px 0;
        text-align: left;
    }
    .container {
        margin: 20px auto;  /* Center the container */
        padding: 20px;
        border-radius: 10px;
        background-color: white;  /* White background for containers */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
    }


    .stButton {
    
     
        border-radius: 0px;  /* Rounded corners */
        transition: background-color 0.3s;  /* Smooth transition for hover */
    }
    
    
  
    .stFileUploader {
        background-color: #2980b9;  /* File uploader button color */
        color: white;  /* White text */
        border-radius: 5px;  /* Rounded corners */
    }
    .stFileUploader:hover {
        background-color: #1f639d;  /* Darker blue on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Application title
st.markdown('<h1 class="title">Rationale Grading</h1>', unsafe_allow_html=True)

# # Create a sidebar layout for file upload and buttons
# st.sidebar.header("Actions")

# Upload Excel file 
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Step 1: Preprocess the uploaded file
    st.sidebar.write("Processing the uploaded file...")

    # Preprocess the Excel file and return a DataFrame
    preprocessed_data = process_excel(uploaded_file)

    # Display the preprocessed data (optional)
    st.subheader("Preprocessed Data:")
    st.dataframe(preprocessed_data)

    # Step 2: Grade the messages using LLM
    if st.sidebar.button("Run Grading"):
        st.sidebar.write("Grading messages with LLM...")

        # Pass the preprocessed data to the grading function
        graded_data = grade_messages()

        # Display the graded results
        st.subheader("Grading Results:")
        st.dataframe(graded_data)

        # Option to download results
        st.sidebar.download_button(
            label="Download Grading Results",
            data=graded_data.to_excel(index=False, engine='openpyxl'),
            file_name="graded_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.sidebar.info("Please upload an Excel file to get started.")
