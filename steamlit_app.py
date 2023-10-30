import snowflake.connector
import streamlit
import pandas
import requests
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('🐔Breakfast Menu')
streamlit.text('🥣Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🍞Hard Boiled Egg')
streamlit.text('🥑Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#need to correct indez 
my_fruit_list = my_fruit_list.set_index('Fruit')

#Put in a multiselect to pick the fruit
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#Header Fruit Advice
def get_fruityvice_data(this_fruit_choice): 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())#create function to normalize json
    # Creates dataframe of normalized fruit.
    return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")
try:  
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLERROR as e:
  streamlit.error()
    
#streamlit.write('The user entered ', fruit_choice)

#new section to display API response

#streamlit.text(fruityvice_response)


streamlit.header("The fruit load contains:")
#Snowflake-related functions


#def get_fruit_load_list():
   # with my_cnx.cursor() as my_cur:
   # my_cur.execute("SELECT * FROM fruit_load_list")   
    #return my_cur.fetchall()

#Add a button to load the fruit

def insert_row_snowflake(new_fruit):
    with my cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return 'Thanks for adding ' + "New Fruit"

add_my_fruit = streamlit.text_input('What fruit would you like information about?')
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function=insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

#streamlit.text("The fruit load list contains:")
#streamlit.dataframe(my_data_row)

streamlit.stop()





