# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5)

table = st.dataframe(data=ingredients_list, use_container_width=True)

if ingredients_list:

    for fruit in ingredients_list:
        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
        ingredients_string = ''
        ingredients_string = ' - '.join(ingredients_list)
        st.write(ingredients_string)
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
                values """ +  f"('{ingredients_string}', '{smoothie_name}')"
        
        #st.write(my_insert_stmt)
        
        time_to_insert = st.button('Submit Order')
        
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered! {smoothie_name}', icon="✅")

