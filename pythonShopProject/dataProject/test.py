# first_list = [1,2,3,4,5,6,7,8,9]
# second_list = [1,2,3,4,5,6,7,8,9]
#
# the_merged_list = []
#
# for i,data in enumerate(first_list):
#     new_list = []
#     new_list.append(first_list[i])
#     new_list.append(second_list[i])
#     the_merged_list.append(new_list)
#
# print(the_merged_list)
import requests

def get_orders(the_store_id):
    the_url = f'http://127.0.0.1:8111/eachOrder/{the_store_id}'
    the_response = requests.get(the_url)
    into_json = the_response.json()['data']
    the_number_of_orders = len(into_json)
    return the_number_of_orders

print(get_orders(4))

import streamlit as st
def looking_for_store(store_inside):
    if store_inside:
        the_array_with_stores = []
        the_data = None
        the_url_request = f'http://127.0.0.1:8111/allShops/{2}'
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

print(looking_for_store('Beauty Center'))
