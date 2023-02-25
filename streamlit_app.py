# imports
import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# funcs
def get_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

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
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit for information.")
  else:
#     back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

# snowflake integration
if streamlit.button('Get Fruit List:'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load()
  streamlit.dataframe(my_data_rows)
  
streamlit.stop()
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * FROM fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("Fruit list contains:")
# streamlit.dataframe(my_data_rows)

# new_fruit = streamlit.text_input('What fruit would you like to add?')
# streamlit.write('Thanks for adding ', new_fruit)

# my_cur.execute("insert into fruit_load_list values ('from streamlit')")
