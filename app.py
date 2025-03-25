import streamlit as st
import pandas as pd 
import plotly.express as px
import io

# Apply Dark mode theme
st.markdown("""
   <style>
            body{
              background-color :#121212;
              color:white;
            
            }
            .sttextinput,.stSelectbox,.stRadio,.stButton{
              color : white !important;
            }
   </style>
""",unsafe_allow_html=True)

# App Title
st.title("📊 CSV & Excel Data Analyzer")

#sidebar navigation
st.sidebar.header("⚙️ Features")
feature = st.sidebar.radio("Select an Option ",["Upload file","Data Cleaning","Data Grouping","Visualization","Download"])

#file uploader (section)
st.sidebar.subheader("📂 Upload File")
uploaded_file =st.sidebar.file_uploader("Upload CSV or Excel file",type=["csv","xlsx"])

if uploaded_file:
    try:
        #read file
        with st.spinner("Loading file..."):
            if uploaded_file.name.endswith('csv'):
                df =pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.sidebar.success("File Uploaded Successfully ! ✅")

        #Display Data Preview
        with st.expander("🔍 View Data Preview"):
           st.write(df.head())

### ----Data Cleaning ---- ###
        if feature == "Data Cleaning":
          st.subheader("🛠️ Data Cleaning")

          #Remove Duplicates
          if st.button("Remove Duplicates"):
              df = df.drop_duplicates()
              st.success("✅ Duplicates Removed !")

           #covert datatype
          columns_to_covert = st.selectbox("Select a column to covert type",df.columns)
          Dtype = st.radio("Convert to",["Numeric","string","Categorical"])
          if st.button("Convert Data Type "):
              if Dtype == "Numeric":
                  df[columns_to_covert] =pd.to_numeric(df[columns_to_covert], errors="coerce") 
              elif Dtype == "Categorical":
                  df[columns_to_covert] = df[columns_to_covert].astype("category")
              else:
                  df[columns_to_covert] = df[columns_to_covert].astype("string")
              st.success(f"✅ {columns_to_covert} coverted to {Dtype}")

          #Noramlize Data
          columns_to_Normalize = st.selectbox("Select column to normalize :",df.select_dtypes(include=["number"]).columns)
          st.success(f"✅ {columns_to_Normalize} Normalized !")

### ------Data Grouping -----###
        elif feature == "Data Grouping":
            st.subheader("📊 Data Grouping ")

            columns_to_group = st.selectbox("Select column to group",df.columns)
            Aggregation = st.radio("Aggregation Methods:",["sum","mean","count"])
            if Aggregation == "sum":
                gropued_df = df.groupby(columns_to_group).sum()
            elif Aggregation == "mean":
                gropued_df = df.groupby(columns_to_group).mean()
            else:
                gropued_df = df.groupby(columns_to_group).count()
            st.success(f" ✅ Data Grouped by {columns_to_group} using {Aggregation}")
            st.write(gropued_df)
        
### ------Data Visualization ------###
        elif feature == "Visualization":
            st.subheader("📈 Data Visualization")

            Chart_type = st.selectbox("Select Chart type:",['Bar chart','Line chart','Pie chart','Histogram'])
            x_column = st.selectbox("Select X-axis Column",df.columns)
            y_column  = st.selectbox("Select Y-axis column",df.select_dtypes(include=["number"]).columns)

            if st.button("Generate Chart"):
                st.success(" ✅ Chart generated")
                if Chart_type == 'Bar chart':
                    fig=px.bar(df,x=x_column,y=y_column,title=f"{Chart_type} of {y_column} by {x_column}")
                elif Chart_type == 'Line chart':
                    fig = px.line(df,x=x_column,y=y_column,title=f"{Chart_type} of {y_column} by {x_column}")
                elif Chart_type == 'Pie chart':
                    fig = px.pie(df, names=x_column, values=y_column, title=f"{Chart_type} of {y_column}")
                else:
                    fig= px.histogram(df,x=y_column,nbins=20,title=f"{Chart_type} of {y_column} ")
                st.plotly_chart(fig)

        ##----Download file --- 
        elif feature == 'Download':
            st.subheader("📥 Download Processed File")
            file_format= st.selectbox("Select File format",["CSV","Excel"])
            
            if file_format =="CSV":
                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button(label="Download CSV" ,data=csv_data,file_name="Processed_data.csv",mime='text/csv')
            else:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer,engine="xlsxwriter") as writer:
                    df.to_excel(writer,index=False)
                    writer.close()
                    st.download_button(label="Download Excel",data=buffer,file_name="processed_data.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                


    except Exception as e:
        st.error(f"⚠️ Errors: {e}")            