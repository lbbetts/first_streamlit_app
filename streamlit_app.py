# imports
import streamlit 
import pandas
import requests
import snowflake.connector

# testing menu items
streamlit.title("My Parents' New Healthy Diner") 

streamlit.header("Breakfast Faves")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach and Rocket Smoothie")
streamlit.text("🐔 Hardboiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

# more advanced streamlit features; data display
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Strawberries', 'Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# APIs
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# formats fruityvice data
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# displays fruityvice in dataframe
streamlit.dataframe(fruityvice_normalized)

# snowflake integration
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("Fruit list contains:")
streamlit.text(my_data_row)
