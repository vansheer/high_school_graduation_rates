import streamlit as st
import pandas as pd
import numpy as np
import folium
import pickle
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
from sklearn.impute import SimpleImputer


#read in external files
states = pd.read_csv('data/states/states_lanlon.csv')
all_districts = pd.read_csv('data/full_school_district_with_zip.csv')
original_districts = pd.read_csv('../data/dataset.csv')
state_dict = {states.loc[i][3]: states.loc[i][0] for i in range(1, states.shape[0])}

#load the prediction model
file = open("models/random_forest",'rb')
model = pickle.load(file)

#this function takes in the central lonlat coordinates of a given state and display the map
#zoom in more with smaller states, and less with larger states
def get_state_map(longitude, latitude, state):
    if state == 'Alaska':
        map = folium.Map([latitude, longitude], tiles="OpenStreetMap", zoom_start=4)
    elif state in ['Hawaii', 'Delaware', 'New Jersey', 'Connecticut', 'Massachusetts']:
        map = folium.Map([latitude, longitude], tiles="OpenStreetMap", zoom_start=8)
    elif state == 'Rhode Island':
        map = folium.Map([latitude, longitude], tiles="OpenStreetMap", zoom_start=10)
    else:
        map = folium.Map([latitude, longitude], tiles="OpenStreetMap", zoom_start=6.5)
    #folium.TileLayer('Stamen Toner').add_to(map)
    # folium_static(map)
    return map



#this function takes in the lonlat coordinates of a given school district and display the map
#@st.cache(suppress_st_warning=True)
def get_school_district_map(school_district_choice, latitude, longitude, graduation_rate_real):
    map = folium.Map([latitude, longitude], tiles="OpenStreetMap", zoom_start=13)
    folium.Marker(
        location=[latitude, longitude],
        tooltip=f"""
        In {school_district_choice.title()}<br>
        The real-world graduation rate is {round(graduation_rate_real * 100)}%
        """,
        draggable=True,
        icon=folium.Icon(icon="cloud")).add_to(map)
    folium_static(map)
    return None





#####################PAGE STARTS#####################

#ask the user to select a state
state_choice = st.selectbox(
    'Select your state:',
    states['Name']
)


#if user selects a state from the menu, 
if state_choice != 'Select your state':
    #pop:
    '**Select a school district from the menu**'

    #read in the address file of the selected state, and display a drop menu of all school districts of this state
    school_districts = pd.read_csv(f'data/states/zip/{state_dict[state_choice]}.csv', dtype={'MZIP': 'object'})
    school_district_choice = st.selectbox('Select your school district', school_districts['NAME'])


    #if user selects a school district from the menu, get the zipcode of the district and call geopy for lanlon coordinates
    if school_district_choice != 'Select your school district':
        zipcode = school_districts.loc[school_districts['NAME']==school_district_choice]['MZIP'].values[0]
        district_id = school_districts.loc[school_districts['NAME']==school_district_choice]['LEAID'].values[0]
        graduation_rate_real = school_districts.loc[school_districts['NAME']==school_district_choice]['Graduation Rate'].values[0]
        geolocator = Nominatim(user_agent="project5 GA")
        location = geolocator.geocode({'postalcode': zipcode})
        this_district = all_districts.loc[all_districts['leaid']==district_id]
        
        


        #if lanlon coordinates obtained, call get_school_district_map function to display the map of the district
        try: 
            get_school_district_map(school_district_choice, location.latitude, location.longitude, graduation_rate_real)
            
        #otherwise prompt 'No such address' (or something nice we can discuss later)
        except:
            'No such address'

        

        #diaplay features
        old = original_districts.loc[original_districts['LEAID']==district_id]
        features = old[['TFEDREV', 'TSTREV', 'TLOCREV', 'Z33', 'Z34']]
        features.rename(columns={'TFEDREV':'Federal Revenue', 
            'TSTREV': 'State Revenue', 
            'TLOCREV': 'Local Revenue', 
            'Z33': 'Teacher Salaries',
            'Z34': 'Employee Benefits'}, inplace=True)

        #change the display format of currency values
        for col in features.columns:
            features[col] = features[col].apply(lambda x: "${:,.2f}k".format((x/1000))) 

        st.table(features)                                                                                             
        #user select input
        df = original_districts.loc[original_districts['LEAID']==district_id]
        


        #set sliders for key features
        side_menu = st.checkbox('Would you like to play around?')
        if side_menu:
            #change Total Federal Revenue
            min_tfedrev = int(df['TFEDREV'].values[0])
            max_tfedrev = int(df['TFEDREV'].values[0]*2)
            tfedrev = st.sidebar.slider('Total Federal Revenue', min_value=min_tfedrev, max_value=max_tfedrev, step=round(min_tfedrev/5))
            df['TFEDREV'] = tfedrev

            #change Salaries - support service - instructional staff
            min_v14 = int(df['TSTREV'].values[0])
            max_v14 = int(df['TSTREV'].values[0]*2)
            tstrev = st.sidebar.slider('Total State Revenue', min_value=min_v14, max_value=max_v14, step=round(min_v14/5))
            df['TSTREV'] = tstrev

            #change Total Local Revenue
            min_tlocrev = int(df['TLOCREV'].values[0])
            max_tlocrev = int(df['TLOCREV'].values[0]*2)
            tlocrev = st.sidebar.slider('Total Local Revenue', min_value=min_tlocrev, max_value=max_tlocrev, step=round(min_tlocrev/5))
            df['TLOCREV'] = tlocrev

            #change Teacher Salaries - support service - instructional staff
            min_z33 = int(df['Z33'].values[0])
            max_z33 = int(df['Z33'].values[0]*2)
            z33 = st.sidebar.slider('Total Teacher Salaries', min_value=min_z33, max_value=max_z33, step=round(min_z33/5))
            df['Z33'] = z33


            #change Employee Benefits
            min_z34 = int(df['Z34'].values[0])
            max_z34 = int(df['Z34'].values[0]*2)
            tz34 = st.sidebar.slider('Total Employee Benefits', min_value=min_z34, max_value=max_z34, step=round(min_z34/5))
            df['Z34'] = tz34

            
            #prepare the school district row for prediction
            df.columns = df.columns.str.lower()
            df.set_index('leaid', inplace=True)
            num_cols = df.drop(columns=['name', 'stabbr', 'agchrt', 'v33', 'graduation rate']).columns
            no_pop = df[df['v33'] <= 0].index
            df.drop(no_pop, inplace=True)
            for col in num_cols:
                df[col] = df[col] / df['v33']
            df[num_cols] = np.where(df[num_cols] <= 0, 0, np.log(df[num_cols]))
            # df[num_cols] = df[num_cols].replace(0, np.nan)
            # imputer = SimpleImputer(strategy='mean')
            # df[num_cols] = imputer.fit_transform(df[num_cols])
            df['graduation rate'] = np.where(df['graduation rate'] >= .95, .95,
                                    np.where(df['graduation rate'] <= .05, .05, 
                                            df['graduation rate']))
            #school district row prepared



            #make and display prediction
            X = df[['2', '3', 'tfedrev', 'tstrev', 'a13', 't06', 'a11', 'u30', 'totalexp', 't40', 
                'v93', 'z33', 'z35', 'z36', 'z38', 'z37', 'v11', 'v13', 'v17', 'v37', 'v10', 
                'v12', 'v14', 'v18', 'v24', 'v38', 'w01', 'w31', 'w61', '_19h', '_21f', '_41f', 
                '_61v']]
            pred = model.predict(X)[0]
            #print(df)


            #write out two graduation rates to the screen
            st.write(f'For {school_district_choice.title()}:')
            st.write(f"""
            The **real-world** graduation rate of is **{round(graduation_rate_real * 100)}%**
            """)
            st.write(f'The **predicted** graduation rate is **{round(pred * 100)}%**')
            

            


    #if user doesn't select a school district from the menu, call get_state_map function to display the map of the state 
    else:
        longitude = states.loc[states['Name']==state_choice]['Longitude']
        latitude = states.loc[states['Name']==state_choice]['Latitude']
        get_state_map(longitude, latitude, state_choice)


