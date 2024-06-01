# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fuits you want in your smoothie."""
)

smoothie_name = st.text_input("Client Name", "")
st.write("The name on the smoothie will be: ", smoothie_name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5)

# table = st.dataframe(data=ingredients_list, use_container_width=True)

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + " "
        ingredients_string = ingredients_string.strip()
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit,' is ', search_on, '.')
        
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        st.subheader(f'{fruit} nutritional info')
        st.stop()
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values """ +  f"('{ingredients_string}', '{smoothie_name}')"
        
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {smoothie_name}', icon="✅")

