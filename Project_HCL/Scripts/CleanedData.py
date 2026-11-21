#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df=pd.read_csv(r"C:\Project_HCL\Hospital_Revenue_Performance_RAW_Data.csv")


# In[3]:


df


# In[4]:


df['Age'] = df['Age'].replace("35 yrs", np.nan)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df.loc[(df['Age'] < 1) | (df['Age'] > 80), 'Age'] = np.nan
df['Age'].value_counts()


# In[5]:


df['Age'] = df['Age'].replace(np.nan , df['Age'].mode()[0])


# In[6]:


df['Age'].value_counts()


# In[7]:


df['Age'].isnull().sum()


# In[8]:


gender_map = {
    'm': 'Male',
    'male': 'Male',
    'f': 'Female',
    'female': 'Female'
}


# In[9]:


df['Gender'] = df['Gender'].astype(str).str.strip().str.lower().map(gender_map)


# In[10]:


df = df.dropna(subset=['Patient_ID'])


# In[11]:


df


# In[12]:


df["Department"].value_counts()


# In[13]:


dept_map = {
    # General Medicine
    'general medicine': 'General Medicine',
    'gen med': 'General Medicine',

    # Emergency & Critical Care
    'emergency & critical care': 'Emergency & Critical Care',
    'emergency/critical care': 'Emergency & Critical Care',
    'er & cc': 'Emergency & Critical Care',

    # Pediatrics
    'pediatrics': 'Pediatrics',
    'paediatrics': 'Pediatrics',

    # Obstetrics & Gynecology
    'obstetrics & gynecology': 'Obstetrics & Gynecology',
    'obs & gynae': 'Obstetrics & Gynecology',
    'obg': 'Obstetrics & Gynecology',

    # Gastroenterology
    'gastroenterology': 'Gastroenterology',
    'gastroentrology': 'Gastroenterology', # typo
    'gastro': 'Gastroenterology',

    # Orthopedics
    'orthopedics': 'Orthopedics',
    'orthopaedics': 'Orthopedics',
    'ortho': 'Orthopedics',

    # Oncology
    'oncology': 'Oncology',
    'oncolgy': 'Oncology', # typo

    # Nephrology
    'nephrology': 'Nephrology',
    'nephrolgy': 'Nephrology', # typo

    # Neurology
    'neurology': 'Neurology',
    'nuerology': 'Neurology', # typo

    # Cardiology
    'cardiology': 'Cardiology',
    'cardio': 'Cardiology'
}


# In[14]:


df['Department'] = df['Department'].astype(str).str.strip().str.lower().replace(dept_map)


# In[15]:


print(df['Department'].value_counts())


# In[16]:


df["Admission_Type"].value_counts()


# In[17]:


df['Admission_Type'] = df['Admission_Type'].str.strip().str.title()


# In[18]:


mapping = {
    'Elective': 'Elective',
    'Emergency': 'Emergency',
    '-': 'Unknown'  # Or None / pd.NA depending on your needs
}


# In[19]:


df['Admission_Type'] = df['Admission_Type'].map(mapping).fillna('Unknown')


# In[20]:


print(df['Admission_Type'].value_counts())


# In[21]:


df['Admission_Type'] = df['Admission_Type'].replace('Unknown',df['Admission_Type'].mode()[0])


# In[22]:


print(df['Admission_Type'].value_counts())


# In[23]:


df


# In[24]:


d1 = pd.to_datetime(df['Admission_Date'], errors= 'coerce', format='%d-%m-%Y')
df['Admission_Date'] = df['Admission_Date'].replace(np.nan,df['Admission_Date'].mode()[0])


# In[25]:


df["Admission_Date"].isnull().sum()


# In[26]:


df['Admission_Date'].value_counts()


# In[27]:


df['Admission_Date'] = pd.to_datetime(df['Admission_Date'], format='mixed', dayfirst=False)


# In[28]:


df['Admission_Date'].value_counts()


# In[30]:


df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"], format="mixed", errors="coerce"
).dt.strftime("%Y-%m-%d")


# In[31]:


df['Discharge_Date'].value_counts()


# In[32]:


df['Discharge_Date'] = df['Discharge_Date'].replace(np.nan,df['Discharge_Date'].mode()[0])


# In[33]:


df


# In[34]:


df['Length_of_Stay_Days'].value_counts()


# In[35]:


df["Length_of_Stay_Days"] = (
    df["Length_of_Stay_Days"].astype(str).str.replace(" days", "", regex=False).str.strip()
)
df["Length_of_Stay_Days"] = pd.to_numeric(df["Length_of_Stay_Days"], errors="coerce")
df["Length_of_Stay_Days"] = df["Length_of_Stay_Days"].abs()
df["Length_of_Stay_Days"] = df["Length_of_Stay_Days"].fillna(df["Length_of_Stay_Days"].median())
df['Length_of_Stay_Days'].value_counts()


# In[36]:


df['Ward_Type'].value_counts()


# In[37]:


df["Ward_Type"] = (
    df["Ward_Type"]
    .str.strip()
    .str.lower()
    .replace({
        "semi private": "semi-private",
        "semiprivate": "semi-private"
    })
)

df["Ward_Type"] = df["Ward_Type"].str.title().replace({"Icu": "ICU"})


# In[38]:


df['Ward_Type'].value_counts()


# In[39]:


df['Attending_Doctor_ID'].value_counts()


# In[40]:


df["Attending_Doctor_ID"] = df["Attending_Doctor_ID"].str.strip().str.upper()
df['Attending_Doctor_ID'].value_counts()


# In[41]:


df['Attending_Doctor_ID'] = df['Attending_Doctor_ID'].replace(np.nan,df['Attending_Doctor_ID'].mode()[0])
df['Attending_Doctor_ID'].value_counts()


# In[42]:


df['Attending_Doctor_ID'].isnull().sum()


# In[43]:


df['Payer_Type'].value_counts()


# In[44]:


df["Payer_Type"] = df["Payer_Type"].str.strip().str.lower()

payer_map = {
    "private insurance": "Private Insurance",
    "pvt insurance": "Private Insurance",
    "insurance": "Private Insurance",
    "self-pay": "Self-Pay",
    "self pay": "Self-Pay",
    "cash": "Self-Pay",
    "corporate": "Corporate",
    "corp": "Corporate",
    "government scheme": "Government Scheme",
    "govt scheme": "Government Scheme",
}

df["Payer_Type"] = df["Payer_Type"].replace(payer_map)

# 3. Fill any missing (NaN) values
df["Payer_Type"] = df["Payer_Type"].fillna("Unknown")


# In[45]:


df['Payer_Type'].value_counts()


# In[46]:


df['Outcome'].value_counts()


# In[47]:


df["Outcome"] = df["Outcome"].str.strip().str.lower()

outcome_map = {
    "recovered": "Recovered",
    "improved": "Improved",
    "lama": "LAMA",
    "left against medical advice": "LAMA",
    "referred": "Referred",
    "referred to higher centre": "Referred",
}

df["Outcome"] = df["Outcome"].replace(outcome_map)


# In[48]:


df['Outcome'] = df['Outcome'].replace(np.nan,df['Outcome'].mode()[0])


# In[49]:


df['Outcome'].value_counts()


# In[50]:


df


# In[51]:


df.to_csv(r"C:\Project_HCL\Hospital_Revenue_Performance_RAW_Data_clean.csv", index=False)


# In[ ]:




