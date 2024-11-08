import streamlit as st
import requests
import models
import pandas as pd
import plotly.express as pl
from datetime import datetime
import math

st.title('Welcome To Store Page')


# will use the key_var variable to change through pages with streamlit sessions
key_var = 'sign_or_log'

if key_var not in st.session_state:
    st.session_state[key_var] = 'Sign Up'

if 'userId' not in st.session_state:
    st.session_state['userId'] = None

the_col1,the_col2 = st.columns(2)


# if the user is logged the log out and home button will appear
if st.session_state['userId']:
    with the_col1:
        if st.sidebar.button('Log Out'):
            st.session_state[key_var] = 'Log In'
            st.session_state['shopSearched'] = None
            st.session_state['userId'] = None
    with the_col2:
        if st.sidebar.button('Home'):
            st.session_state[key_var] = 'Home'
            st.session_state['shopSearched'] = None



# there i will create a function
# which will tell the avg rating for this store
# based on user's rating's
def average_rating(the_id:int):
    the_url = f'http://127.0.0.1:8111/avgRating/{the_id}'
    response = requests.get(the_url)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['success'] == 'True':
            get_the_ratings = json_response['rating']
            only_rating = 0
            for rating in get_the_ratings:
                only_rating += rating[-1]
            average_rating = only_rating/len(get_the_ratings)
            return average_rating
        else:
            st.error('Not Rated By Any')
    else:
        st.write(response.text)

# take users who ordered in an store more than once
def users_who_ordered(the_store):
    the_number_dict = {}
    user_with_more_than_one = []
    the_url = f'http://127.0.0.1:8111/mostOrdersUsers/{the_store}'
    the_response = requests.get(the_url)
    into_json_data = the_response.json()['users']
    for user in into_json_data:
        if user[-3] not in the_number_dict:
            the_number_dict[user[-3]] = 1
        else:
            the_number_dict[user[-3]] += 1

    for user_ordered in the_number_dict:
        if the_number_dict[user_ordered] > 1:
            user_with_more_than_one.append(user_ordered)

    return len(user_with_more_than_one)




# get current points of a user for every store
def current_points(the_store_id,the_user_id):
    the_url = f'http://127.0.0.1:8111/getPoints'
    the_model_data = models.gettingPoints(user_id=the_user_id,store_id=the_store_id)
    the_response = requests.post(the_url,json=the_model_data.dict())
    if the_response.status_code == 200:
        into_json_response = the_response.json()
        if into_json_response['success'] == 'True':
            the_points = into_json_response['data'][3]
            st.sidebar.text(f'Points: {the_points}/50')
            # IF THE USER HAS ACHIEVED 50 POINTS ON
            # AN PARTICULAR STORE GO ON AND
            # GIVE THEM A RANDOM PRODUCT
            if the_points >= 50:
                st.sidebar.success('Congrats You Achieved 50 Points Now You Get A Product For Free!')
                the_url_random_product = f'http://127.0.0.1:8111/randomProduct/{the_store_id}'
                response_product = requests.get(the_url_random_product)
                into_json = response_product.json()
                if into_json['success'] == 'True':
                    the_product = into_json['data'][1]
                    st.session_state['Product Free'] = the_product
                    st.session_state['Product Free Price'] = into_json['data'][-1]
                    st.session_state[key_var] = 'Product For Free'
                else:
                    st.sidebar.write(into_json['success'])

        else:
            st.sidebar.text('Points: 0/50')
    else:
        st.error(the_response.text)


if 'shopSearched' in st.session_state:
    # if we have searched a shop and found results
    if st.session_state['shopSearched']:
        the_shop_id = st.session_state['shopSearched']
        the_user_id = st.session_state['userId']
        # get the average rating
        the_average = average_rating(the_shop_id)
        if the_average:
            st.sidebar.text(f'The Average Rating {round(the_average,2)}/10')
            # get the current points also
            current_points(the_shop_id,the_user_id)

# function to compare two stores
def comparing_two_stores(store1,store2):
    the_user_id = st.session_state['userId']
    # check if store exists
    def looking_for_store(store_inside):
        if store_inside:
            the_array_with_stores = []
            the_data = None
            the_url_request = f'http://127.0.0.1:8111/allShops/{the_user_id}'
            the_response = requests.get(the_url_request)
            into_json = the_response.json()
            if into_json['success'] == 'True':
                the_data = into_json['data']
                for data in the_data:
                    if store_inside == data[2]:
                        the_array_with_stores.append(data)
                        break
                if len(the_array_with_stores) == 0:
                    st.error('One Of Stores Name Is Wrong')
                    return
            return the_array_with_stores

    # get the stores
    the_store_1 = looking_for_store(store1)
    the_store_2 = looking_for_store(store2)

    if the_store_1 and the_store_2:
        the_store_1_id = the_store_1[0][0]
        the_store_2_id = the_store_2[0][0]

        st.session_state['firstStoreId'] = the_store_1_id
        st.session_state['secondStoreId'] = the_store_2_id

        st.session_state['firstStoreName'] = store1
        st.session_state['secondStoreName'] = store2

        st.session_state[key_var] = 'Comparing'



        # masi te konfirmojm qe ekzistojn te dyja stores
        # atehere shkojm edhe e bojm vizualizimin e te dhenave per keto stores

# get the number of orders for a particular store
def get_orders(the_store_id):
    the_url = f'http://127.0.0.1:8111/eachOrder/{the_store_id}'
    the_response = requests.get(the_url)
    into_json = the_response.json()['data']
    the_number_of_orders = len(into_json)
    return the_number_of_orders

# adding to cart the product that we want from a particular store
def addToCart(all_product_names_ids,product=None):
    if st.button('Add To Cart', key=f'my_button{product[3]}'):
        product_id_ordering = all_product_names_ids[product[4]]
        products_ordered_by_id.append(product_id_ordering)
        the_store_id = st.session_state['shopSearched']
        the_user_id = st.session_state['userId']
        current_date_time = datetime.now()
        date_time_without_microseconds = current_date_time.replace(microsecond=0)
        date_time_to_string = date_time_without_microseconds.strftime("%Y-%m-%d %H:%M:%S")
        the_data_ready = models.productOrder(product_id=product_id_ordering, store_id=the_store_id,
                                             user_ordering=the_user_id, order_address='',order_date=date_time_to_string)
        the_url = 'http://127.0.0.1:8111/addToCart'
        the_response = requests.post(the_url, json=the_data_ready.dict())
        if the_response.status_code == 200:
            into_json = the_response.json()
            if into_json['success'] == 'True':
                st.success('Added')
                # now add to the cart
        else:
            st.error('Wrong Response')


# an reusable function which will make a functional search bar through the whole project
def search_bar():
    [the_search_part] = st.columns(1)
    with the_search_part:
        [search_bar] = st.columns(1)
        the_store_the_id = {}
        with search_bar:
            the_search_input = st.sidebar.text_input('Search Shops')
            the_user_id = st.session_state['userId']

            # requesting to get all shops excluding the shop's of the user who is searching
            the_url = f'http://127.0.0.1:8111/allShops/{the_user_id}'
            the_response = requests.get(the_url)
            if the_response.status_code == 200:
                into_json = the_response.json()
                if into_json['success'] == 'True':
                    the_data = into_json['data']
                    for store in the_data:
                        # this dictionarie will have as a key the store name
                        # and as a value the store id to make it easier to access
                        # the store id through the store name
                        the_store_the_id[store[2]] = store[0]

            if st.sidebar.button('Search'):
                the_input_value = the_search_input
                # if the input value matches any key in the dictionarie
                if the_input_value in the_store_the_id:
                    # now saving to sessions the id of the shop we searched
                    st.session_state['shopSearched'] = the_store_the_id[the_input_value]
                    # saving the shop name
                    st.session_state['shopName'] = the_input_value
                    # and changing the page to Search Shop
                    st.session_state[key_var] = 'Search Shop'
                else:
                    st.sidebar.error('No Shop Named Like That')



products_ordered_by_id = []


# function that will handle all the visualization for every store
# and also the process of viewing the cart of products you added
def visualizing_data(the_shop_id):
            # a request to take data about the store
            the_url_to_request = f'http://127.0.0.1:8111/shopData/{the_shop_id}'
            the_user_id = st.session_state['userId']
            response = requests.get(the_url_to_request)
            the_owner = False
            if response.status_code == 200:
                into_json = response.json()
                if into_json['success'] == 'True':
                    all_product_names_ids = {}
                    all_shop_data = into_json['data']
                    all_categories = []
                    product_prices = []
                    all_products = []
                    for user in all_shop_data:
                        if user[1] == the_user_id:
                            the_owner = True

                    for product in all_shop_data:
                        if product[1] != the_user_id:
                            all_product_names_ids[product[4]] = product[3]
                            product_name_column, product_dump, product_price_column, product_order = st.columns(4)
                            with product_name_column:
                                st.text(f'Product Name:{product[4]}')
                            with product_price_column:
                                st.text(f'Price:{product[7]}$')

                            with product_order:
                                addToCart(all_product_names_ids,product)
                        all_categories.append(product[-1])
                        all_products.append(product[4])
                        product_prices.append(product[7])

                    # an option to view the cart i
                    if not the_owner:
                        [view_cart_column] = st.columns(1)
                        with view_cart_column:
                            if st.button('View Cart'):
                                st.session_state['productIdOrdered'] = products_ordered_by_id
                                st.session_state[key_var] = 'Confirm Order'
                        # making the lists ready for future data sets

                    # visualizing data about the store

                    # Top 3 Categories

                    top_3_categories = {
                        'products':all_products,
                        'categories':all_categories
                    }
                    into_df = pd.DataFrame(top_3_categories)

                    [the_column2] = st.columns(1)

                    with the_column2:
                        colors = ['#008080','#FF6F61','#FFD700']
                        the_values = into_df['categories'].value_counts().head(3)
                        reseting_index = the_values.reset_index()
                        reseting_index.columns = ['categories','Products']
                        figure = pl.pie(reseting_index,names='categories',values='Products',title='Top 3 Categories',color='categories',color_discrete_sequence=colors)
                        figure.update_layout(
                            width=800,
                            height=500
                        )
                        st.plotly_chart(figure,use_container_width=True)


                    # visualize orders by categories

                    the_url = f'http://127.0.0.1:8111/eachOrder/{the_shop_id}'
                    the_response = requests.get(the_url)
                    the_order_dates = {}
                    if the_response.status_code == 200:
                        the_json_values = the_response.json()
                        if the_json_values['success'] == 'True':
                            the_data = the_json_values['data']
                            all_product_ordered = []
                            all_categories_ordered = []
                            for order in the_data:
                                # st.write(order)
                                all_categories_ordered.append(order[-1])
                                all_product_ordered.append(order[14])
                                # getting the data for only the day of the order
                                each_order_date = order[5].split(' ')[0].split('-')[2]
                                if each_order_date in the_order_dates:
                                    # if there is any order to that date alredy add one more
                                    the_order_dates[each_order_date] += 1
                                else:
                                    # else just add an order to that particular date
                                    the_order_dates[each_order_date] = 1

                            the_df_dict_data = {
                                'product_ordered':all_product_ordered,
                                'categories_ordered':all_categories_ordered
                            }

                            [the_col] = st.columns(1)

                            with the_col:
                                second_colors = ['#98FF98','#FFDAB9','#003366']
                                df_categories = pd.DataFrame(the_df_dict_data)
                                value_counts = df_categories['categories_ordered'].value_counts().head(3)
                                reseting = value_counts.reset_index()
                                reseting.columns = ['categories_ordered','Products']
                                the_figure = pl.pie(reseting,names='categories_ordered',values='Products',color='categories_ordered',title='Top 3 Categories Ordered',color_discrete_sequence=second_colors)
                                the_figure.update_layout(
                                    width=800,
                                    height=600
                                )
                                st.plotly_chart(the_figure,use_container_width=True)


                        # Visualize By Product's Price
                            the_product_prices_df = {
                                'Product_Name':all_products,
                                'Product_Price':product_prices
                            }

                            [the_kol] = st.columns(1)

                            with the_kol:
                                third_colors = ['#4682B4','#DC143C','#E6E6FA']
                                df_dict = pd.DataFrame(the_product_prices_df)
                                df_dict['Product_Price'] = df_dict['Product_Price'].astype(float)
                                grouping = df_dict.groupby('Product_Name')['Product_Price'].sum()
                                sorting = grouping.sort_values(ascending=False).head(5)
                                reseting_i = sorting.reset_index()
                                the_fig = pl.pie(reseting_i,names='Product_Name',values='Product_Price',color='Product_Name',title='Top 5 Most Expensive Products',color_discrete_sequence=third_colors)
                                the_fig.update_layout(
                                    width=800,
                                    height=500
                                )
                                st.plotly_chart(the_fig,use_container_width=True)

                            # Now I need to visualize the amount of products The Store Sells  each day
                            if the_order_dates:
                                list_for_df_dates = []
                                list_for_df_orders = []
                                for day_of_order in the_order_dates:
                                    list_for_df_dates.append(day_of_order)
                                    list_for_df_orders.append(the_order_dates[day_of_order])

                                [the_line_col] = st.columns(1)
                                with the_line_col:
                                    orders_ready_df = {
                                        'Day:':list_for_df_dates,
                                        'Number Of Orders:':list_for_df_orders
                                    }
                                    orders_data_frame = pd.DataFrame(orders_ready_df)
                                    orders_data_frame['Day:'] = orders_data_frame['Day:'].astype(float)
                                    orders_data_frame['Number Of Orders:'] = orders_data_frame['Number Of Orders:'].astype(float)
                                    the_line = pl.line(orders_data_frame,x='Day:',y='Number Of Orders:',title='Orders For This Shop For Each Day')
                                    the_line.update_traces(line=dict(color='#DC143C'))
                                    st.plotly_chart(the_line)
                            else:
                                st.write('No Orders There!')

                        else:
                            st.error('No More Data To Visualize')
                    else:
                        st.error(response.text)

                    # visualizing the data
                    # by comparing
                    # the user rating with the user's orders

                    endpoint_to_request = f'http://127.0.0.1:8111/ratingsFromStore/{the_shop_id}'
                    response_ = requests.get(endpoint_to_request)
                    if response_.status_code == 200:
                        into_json_data = response_.json()
                        if into_json_data['success'] == 'True':
                            the_ratings = into_json_data['ratings']
                            the_orders = into_json_data['orders']
                            merged_data = []

                            for i,rate in enumerate(the_ratings):
                                merged = []
                                merged.append(the_ratings[i])
                                merged.append(the_orders[i])
                                merged_data.append(merged)
                            into_df = pd.DataFrame(merged_data,columns=['Rating From User','Orders From User'])
                            figure = pl.scatter(into_df,x=into_df.columns[0],y=into_df.columns[1],title='Number Of Orders From Users Who Rated')
                            st.plotly_chart(figure)

                    # TOP 3 USERS WITH MOST ORDERS
                    the_dictionarie_with_users = {}
                    the_url_getting= f'http://127.0.0.1:8111/mostOrdersUsers/{the_shop_id}'
                    response_for_users = requests.get(the_url_getting)
                    if response_for_users.status_code == 200:
                        if response_for_users.json()['success'] == 'True':
                            into_json_users = response_for_users.json()['users']
                            for user in into_json_users:
                                if user[8] in the_dictionarie_with_users:
                                    the_dictionarie_with_users[user[8]] += 1
                                else:
                                    the_dictionarie_with_users[user[8]] = 1
                            into_items = sorted(the_dictionarie_with_users.items(),key=lambda item:item[1],reverse=True)[:3]
                            list_with_names = []
                            list_with_values = []

                            for item in into_items:
                                list_with_names.append(item[0])
                                list_with_values.append(item[1])

                            the_dict_for_df = {
                                'Username':list_with_names,
                                'Orders':list_with_values
                            }

                            into_df_ = pd.DataFrame(the_dict_for_df)
                            grouping = into_df_.groupby('Username')['Orders'].sum().reset_index()
                            sorting = grouping.sort_values(by='Orders',ascending=False)
                            fig = pl.bar(sorting,x='Username',y='Orders',title='Top 3 Users With Most Orders')
                            fig.update_traces(marker=dict(line=dict(width=0)),width=0.3)
                            st.plotly_chart(fig)

# if user is logged call the function search bar
if st.session_state['userId']:
    search_bar()

# there we have the sign up logic
if st.session_state[key_var] == 'Sign Up':
    def signUpLogic():

        [the_col] = st.columns(1)
        [log_in_column] = st.columns(1)
        with the_col:
            with st.form(key='my_form'):
                the_username = st.text_input('Enter Username')
                the_email = st.text_input('Enter Email')
                the_password = st.text_input('Enter Your Password',type='password')
                the_submit_button = st.form_submit_button('Sign Up')

            if the_submit_button:
                if the_username and the_email and the_password:
                    the_model = {
                        'username':the_username,
                        'email':the_email,
                        'password':the_password
                    }
                    the_url = 'http://127.0.0.1:8111/signUp'
                    the_request = requests.post(the_url,json=the_model)
                    if the_request.status_code == 200:
                        into_json = the_request.json()
                        if into_json['success'] == 'User Added':
                            st.session_state[key_var] = 'Log In'
                        else:
                            st.write('Failed')
                    else:
                        st.write('Error',the_request.text)

        with log_in_column:
            if st.button('Have Account?'):
                # if we have an account switch the page to the log in page
                st.session_state[key_var] = 'Log In'

    signUpLogic()


# the log in page
elif st.session_state[key_var] == 'Log In':
    # we call the function at once not both at times
    # so if it is signUp then call that function else if it is log in call another function
    def logIn():
        [the_column] = st.columns(1)
        with the_column:
            with st.form(key='second_form'):
                the_username = st.text_input('Enter Username')
                the_password = st.text_input('Enter Password',type='password')
                the_submit_1,the_submit_2,the_submit_3 = st.columns(3)
                with the_submit_2:
                    the_submit = st.form_submit_button('Log In')
            if the_submit:
                the_url = 'http://127.0.0.1:8111/logIn'
                the_data = {
                    'username':the_username,
                    'password':the_password
                }
                requesting = requests.post(the_url,json=the_data)
                if requesting.status_code == 200:
                    into_json = requesting.json()
                    if into_json['success'] == 'Logged In':
                        st.session_state['userId'] = into_json['fetched'][0]
                        # If The Log In Is Successful Then Go To The Home Page
                        st.session_state[key_var] = 'Home'
                    else:
                        st.error('Wrong Credentinals')
        [the_sign_col] = st.columns(1)
        with the_sign_col:
            if st.button('Dont Have Account?'):
                st.session_state[key_var] = 'Sign Up'
    logIn()


elif st.session_state[key_var] == 'Home':

    def home_page():
        create_shop,log_out = st.columns(2)
        dump1,look_stores,dump2 = st.columns(3)
        store_name1,store_name2 = st.columns(2)
        with create_shop:
            if st.button('Create Shop'):
                # if button is clicked change the page to
                # the Create Shop page
                st.session_state[key_var] = 'Create Shop'
                


        # take the stores of the current user
        with look_stores:
            ## here go and check if the current user has any store
            st.subheader('Your Stores')
            the_url = f'http://127.0.0.1:8111/userStore/{st.session_state['userId']}'
            response = requests.get(the_url)
            if response.status_code == 200:
                if response.json()['success'] == 'True':
                    into_json_data = response.json()['data'] # [[],[],[]] each array inside the big array represent the data for a particular store
                    for store in into_json_data:
                        [column_store] = st.columns(1)
                        with column_store:
                            if st.button(store[2],key=f'Store {store[0]}'):
                                st.session_state['storeId'] = store[0]
                                st.session_state['storeName'] = store[2]
                                st.session_state[key_var] = 'Personal Store'

                else:
                    st.error('You Dont Own Any Store')
            else:
                st.write(response.text)
            st.sidebar.text(" ")
            st.sidebar.text(" ")
            st.sidebar.text(" ")
            st.sidebar.text(" ")
            with store_name1:
                st.sidebar.text('Compare Two Stores Here:')
                the_store_name = st.sidebar.text_input('Enter First Store Name')
            with store_name2:
                the_store_name2 = st.sidebar.text_input('Enter Second Store Name')

            [the_col_button] = st.columns(1)
            with the_col_button:
                if st.sidebar.button('Compare'):
                    comparing_two_stores(the_store_name, the_store_name2)

    home_page()

# Create A New Store
elif st.session_state[key_var] == 'Create Shop':
        def create_shop():
            [the_column] = st.columns(1)
            with the_column:
                with st.form(key='my_form'):
                    the_array_with_data = None
                    get_categories = 'http://127.0.0.1:8111/getCategories'
                    response = requests.get(get_categories)
                    if response.status_code == 200:
                        into_json = response.json()
                        the_array_with_data = into_json['data']
                    else:
                        st.write('Error',response.text)
                    the_array_dropdown = [data[1] for data in the_array_with_data]
                    personal_name = st.text_input('Your Name')
                    the_store_name = st.text_input('Store Name')
                    the_select = st.selectbox('Select A Category', the_array_dropdown)
                    the_id = st.session_state['userId']
                    the_new_model = models.shopCreateModel(user_id=the_id,shop_name=the_store_name)
                    the_submit_button = st.form_submit_button('Create')
                if the_submit_button:
                    st.write('Hello')
                    responses = requests.post('http://127.0.0.1:8111/createStore',json=the_new_model.dict())
                    if responses.status_code == 200:
                        the_json = responses.json()
                        st.session_state['storeName'] = the_store_name
                        # saving to the sessions the store id
                        st.session_state['storeId'] = the_json['id']
                        st.session_state[key_var] = 'Personal Store'
                    else:
                        st.write(responses.text)

        create_shop()

# At your own store you can add products
elif st.session_state[key_var] == 'Add Products':
    def add_product():
        [the_col] = st.columns(1)
        with the_col:
            with st.form(key='my_form'):
                # first get categories to allow the user choose a category
                # which will represent the product
                get_categories = 'http://127.0.0.1:8111/getCategories'

                response = requests.get(get_categories)

                if response.status_code == 200:
                    into_json = response.json()
                    the_array_with_data = into_json['data']
                the_select_box_data = [data[1] for data in the_array_with_data]
                the_dict_values = {}
                for data in the_array_with_data:
                    the_dict_values[data[1]] = data[0]

                product_name = st.text_input('Enter Product Name')
                product_category = st.selectbox('Product Category',the_select_box_data)
                product_price = st.number_input('Product Price')

                the_submit_button = st.form_submit_button('Add Product')

            if the_submit_button:
                the_store_name = st.session_state['storeName']
                the_user_id = st.session_state['userId']
                store_data = models.shopCreateModel(user_id=the_user_id,shop_name=the_store_name)
                store_url = 'http://127.0.0.1:8111/getStore'
                response_shop = requests.post(store_url,json=store_data.dict())
                if response_shop.status_code == 200:
                    the_data = response_shop.json()['data']
                else:
                    st.write(response_shop.text)

                #### ####

                # now be ready to add the product
                the_model_data = models.addProduct(product_name=product_name,category_id=the_dict_values[product_category],product_store_id=the_data[0],product_price=product_price)
                the_url = 'http://127.0.0.1:8111/addProduct'

                response_product = requests.post(the_url,json=the_model_data.dict())

                if response_product.status_code == 200:
                    product_json = response_product.json()
                    if product_json['success'] == 'True':
                        st.session_state[key_var] = 'Home'
                else:
                    st.write(response_product.text)

    add_product()


# there you can see your personal store
elif st.session_state[key_var] == 'Personal Store':
    the_adding_part,see_products = st.columns(2)

    [see_orders] = st.columns(1)

    [see_visualized_data] = st.columns(1)

    # see orders
    with see_orders:
        if st.button('See Orders'):
            the_store_id = st.session_state['storeId']
            endpoint = f'http://127.0.0.1:8111/eachOrder/{the_store_id}'
            response = requests.get(endpoint)
            if response.status_code == 200:
                into_json_part = response.json()
                if into_json_part['success'] == 'True':
                    the_orders = into_json_part['data']
                    the_orders = the_orders[::-1]
                    for order_accepted in the_orders:
                        the_order_user = order_accepted[11]
                        the_product_ordered = order_accepted[15]
                        the_product_price = order_accepted[-3]
                        the_address_ordered = order_accepted[4]
                        the_user,the_product,the_price = st.columns(3)
                        the_null,the_address,the_null2 = st.columns(3)
                        with the_user:
                            st.text(f'The User: {the_order_user}')
                        with the_product:
                            st.text(f'The Product: {the_product_ordered}')
                        with the_price:
                            st.text(f'The Price: {the_product_price}$')

                        with the_address:
                            st.text(f'The Address: {the_address_ordered} ')
                else:
                    st.error('No Orders')
            else:
                st.error(response.text)

    # add product
    with the_adding_part:
        [the_column_button] = st.columns(1)
        with the_column_button:
            if st.button('Add Product'):
                # if button is clicked we change the page to add products page
                st.session_state[key_var] = 'Add Products'

    # see your own products
    with see_products:
        [the_column_button] = st.columns(1)
        with the_column_button:
            if st.button('See Your Products'):
                the_url = f'http://127.0.0.1:8111/seeStoreProducts/{st.session_state['storeId']}'
                response = requests.get(the_url)
                if response.status_code == 200:
                    the_json = response.json()
                    if the_json['success'] == 'True':
                        the_data = the_json['data']
                        for product in the_data:
                            st.text(f'Product Name:{product[1]} Product Price:{product[4]}$')
                            st.text(" ")
                            st.text(" ")
                            st.text(" ")
                    else:
                        st.write('No Products Added Yet')
                else:
                    st.write(response.text)


    # see data visualized for your own store
    with see_visualized_data:
        the_shop_id = st.session_state['storeId']
        if st.button('See Data Visualized'):
            visualizing_data(the_shop_id)

elif st.session_state[key_var] == 'Search Shop':
    # search a particular store after we got the id and the store name from a previous function
    if st.session_state['shopSearched']:
        # if we have found the store we are looking for
        # go on and show the products of that store
        # and all the visualization
        if st.session_state['shopName']:
            the_col1,the_col2,the_col3 = st.columns(3)
            with the_col2:
                st.text(f'Welcome To {st.session_state['shopName']}')
        the_shop_id = st.session_state['shopSearched']
        the_user_id = st.session_state['userId']
        the_data_to_sent = models.checkRelation(user_id=the_user_id,store_id=the_shop_id)
        the_url = 'http://127.0.0.1:8111/checkRelation'
        the_response = requests.post(the_url,json=the_data_to_sent.dict())

        if the_response.status_code == 200:
            the_json_format = the_response.json()
            if the_json_format['success'] == 'True':
                [the_col] = st.columns(1)
                with the_col:
                    the_slider_form = st.sidebar.slider('Rate Your Experience With This Shop',min_value=0,max_value=10)
                    if the_slider_form:
                        the_url = 'http://127.0.0.1:8111/addRating'
                        the_data_to_add = models.addRating(user_id=the_user_id,store_id=the_shop_id,rate=the_slider_form)
                        the_res = requests.post(the_url,json=the_data_to_add.dict())
                        if the_res.status_code == 200:
                            data_json = the_res.json()
                            if data_json['success'] and data_json['info']:
                                st.error('You Alredy Rated Your Experience')
                            elif data_json['success'] and not data_json['info']:
                                st.success('Store Got Your Rating!Thank You!')
                            else:
                                st.error('Something Went Wrong')

                        else:
                            st.write(the_res.text)
        visualizing_data(the_shop_id)
    else:
        st.write('Something Went Wrong')


# confirming the order adding the address
elif st.session_state[key_var] == 'Confirm Order':
    if st.session_state['shopSearched']:
        the_product_id = st.session_state['productIdOrdered']
        store_id = st.session_state['shopSearched']
        user_ordering = st.session_state['userId']
        the_total = 0

        # first make a request
        the_data_model = models.getCart(user_id=user_ordering,store_id=store_id)
        the_url = 'http://127.0.0.1:8111/getProducts'
        response = requests.post(the_url,json=the_data_model.dict())
        the_order_ids = []
        if response.status_code == 200:
            the_data = response.json()
            if the_data['success'] == 'True':
                [the_column] = st.columns(1)
                with the_column:
                    the_whole_data = the_data['data']
                    for data in the_whole_data:
                        the_order_ids.append(data[0])
                        st.text(f'Product: {data[8]}  Price: {data[-1]}$')
                        the_total += data[-1]

                    total_col1,total_col2,total_col3 = st.columns(3)
                    with total_col2:
                        st.text(f'The Total: {the_total}$')
            else:
                st.write('No Data For You')
        the_address = st.text_input('Enter Address')

        if the_address:
            if st.button('Complete Order'):
                order_confirmed = False
                updating_orders = 'http://127.0.0.1:8111/updatingOrders'
                the_model_data = models.updatingOrders(order_ids=the_order_ids,order_address=the_address)
                the_response = requests.post(updating_orders,json=the_model_data.dict())
                if the_response.status_code == 200:
                    st.write(the_response.json())
                    order_confirmed = True
                else:
                    st.error('Wrong')
                    raise ValueError('Failed')

                points = math.floor(the_total/5)
                the_data = models.updatePoints(user_id=user_ordering,store_id=store_id,points=points)
                url_to_request = 'http://127.0.0.1:8111/addingPoints'
                the_response = requests.post(url_to_request,json=the_data.dict())
                if the_response.status_code == 200:
                    st.session_state[key_var] = 'Search Shop'

        else:
            st.error('Enter The Address To Complete Order')

    else:
        st.write(st.session_state['shopSearched'])
        st.write(st.session_state['productIdOrdered'])


elif st.session_state[key_var] == 'Product For Free':
    [the_product] = st.columns(1)
    with the_product:
        the_product_name = st.session_state['Product Free']
        the_product_price = st.session_state['Product Free Price']
        the_text = f'You Won The {the_product_name} With The Price Of {the_product_price}'
        st.write(the_text)
    button_dump1,button_,button_dump2 = st.columns(3)
    with button_:
        the_address = st.text_input('Enter The Address')
        if st.button('Confirm Product'):
            st.write('You Got The Product')
            user_id = st.session_state['userId']
            store_id = st.session_state['shopSearched']
            the_data_to_sent = models.gettingPoints(user_id=user_id,store_id=store_id)
            the_url = 'http://127.0.0.1:8111/resetPoints'
            the_res = requests.post(the_url,json=the_data_to_sent.dict())
            if the_res.status_code == 200:
                if the_res.json()['success'] == 'True':
                    the_text = ''
                    st.session_state[key_var] = 'Search Shop'



# now the page for comparing two stores
elif st.session_state[key_var] == 'Comparing':

    the_store_1_id = st.session_state['firstStoreId']
    the_store_2_id = st.session_state['secondStoreId']

    store1 = st.session_state['firstStoreName']
    store2 = st.session_state['secondStoreName']
    def charts_visualized():
        [the_column] = st.columns(1)
        with the_column:
            first_store_orders = get_orders(the_store_1_id)
            second_store_orders = get_orders(the_store_2_id)

            the_dict_for_df = {
                'Store Name': [store1, store2],
                'Store Orders': [first_store_orders, second_store_orders]
            }
            comparing_df = pd.DataFrame(the_dict_for_df)
            colors = ['#001F3F', '#FFC107']
            grouping_by = comparing_df.groupby('Store Name')['Store Orders'].sum()
            sorting_values = grouping_by.sort_values(ascending=False).reset_index()
            sorting_values.columns = ['Store Name', 'Sales']
            figure = pl.pie(sorting_values, names='Store Name', color='Store Name', values='Sales', title='Most Sales',
                            color_discrete_sequence=colors)
            figure.update_layout(
                title_font=dict(size=24),
                width=700,
                height=500
            )
            st.plotly_chart(figure, use_container_width=True)
    charts_visualized()

    def scatterRating():
        the_first_average = average_rating(the_store_1_id)
        the_second_average = average_rating(the_store_2_id)

        the_dict_data = {
            'Store Name':[store1,store2],
            'Store Avg Rating':[the_first_average,the_second_average]
        }

        the_df = pd.DataFrame(the_dict_data)

        the_fig = pl.scatter(the_df,x=the_df.columns[0],y=the_df.columns[1],title='Avg Rating Per Store',size=the_df.columns[1])

        the_fig.update_layout(
            title_font = dict(size=24),
            xaxis_title='Custom X Axis Title',
            yaxis_title='Custom Y Axis Title',
            margin=dict(l=40, r=40, t=40, b=40)
        )

        the_fig.update_traces(
            marker=dict(
                opacity=0.7,  # Marker opacity
                line=dict(width=2)  # Border width
            )
        )

        st.plotly_chart(the_fig)

    scatterRating()

    def number_of_costumers():
        first_store_costumers = users_who_ordered(the_store_1_id)
        second_store_costumers = users_who_ordered(the_store_2_id)
        the_dict_df = {
            'Store Name':[store1,store2],
            'Number Of Costumers':[first_store_costumers,second_store_costumers]
        }

        into_df_pandas = pd.DataFrame(the_dict_df)
        colors = ['#FF6F61','#008080']
        grouping = into_df_pandas.groupby('Store Name')['Number Of Costumers'].sum()
        sorting = grouping.sort_values(ascending=False).reset_index()
        sorting.columns = ['Store Name','Number Of Loyal Costumers']
        the_figure = pl.pie(sorting,names='Store Name',values='Number Of Loyal Costumers',color='Store Name',title='Number Of Loyal Costumers',color_discrete_sequence=colors)
        the_figure.update_layout(
            title_font=dict(size=24),
            width=700,
            height=500
        )
        st.plotly_chart(the_figure,use_container_width=True)
        # in this function i will get first the number of loyal costumers
        # for each shop then compare those numbers using pie

    number_of_costumers()




