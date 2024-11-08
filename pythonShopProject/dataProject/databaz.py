import sqlite3
import models
from datetime import datetime
import math
import random
from typing import List
def create_connection():
    the_connection = sqlite3.connect('stores.db')
    return the_connection


def tables():
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
        id integer primary key autoincrement,
        username text not null,
        email text not null,
        password text not null
    );''')

    the_connection.commit()

    the_cursor.execute('''CREATE TABLE IF NOT EXISTS Categories(
        category_table_id integer primary key autoincrement,
        category_name text not null
    )''')

    the_connection.commit()

    the_cursor.execute('''CREATE TABLE IF NOT EXISTS Store(
        id_store integer primary key autoincrement,
        user_id integer,
        store_name text not null,
        FOREIGN KEY (user_id) REFERENCES Users(id)
    );''')

    the_connection.commit()

    the_cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
        id_product integer primary key autoincrement,
        product_name text not null,
        category_id integer,
        product_store_id integer,
        product_price integer,
        
        FOREIGN KEY (product_store_id) REFERENCES Store(id_store),
        FOREIGN KEY (category_id) REFERENCES Categories(category_table_id)
    )''')

    the_connection.commit()

    the_cursor.execute('''CREATE TABLE IF NOT EXISTS Orders(
        order_id integer primary key autoincrement,
        product_id integer,
        store_id integer,
        user_ordering integer,
        
        FOREIGN KEY (product_id) REFERENCES products(id_product),
        FOREIGN KEY (store_id) REFERENCES Store(id_store),
        FOREIGN KEY (user_ordering) REFERENCES Users(id)
    
    
    )''')

    the_connection.commit()

    the_cursor.execute('''CREATE TABLE IF NOT EXISTS Cart(
        cart_id integer primary key autoincrement,
        order_id integer,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    )''')

    the_connection.commit()

    the_cursor.execute('''UPDATE ORDERS SET order_date = CURRENT_TIMESTAMP WHERE order_date IS NULL''')
    the_connection.commit()

    the_cursor.execute('''CREATE TABLE IF NOT EXISTS ratings(
        rating_id integer primary key autoincrement,
        user_rating_id integer,
        store_rated_id integer,
        FOREIGN KEY (user_rating_id) REFERENCES Users(id),
        FOREIGN KEY (store_rated_id) REFERENCES Store(id_store)
    )''')

    the_connection.commit()

    the_cursor.execute('''CREATE TABLE IF NOT EXISTS points(
        point_id integer primary key autoincrement,
        user_points_id integer,
        store_points_id integer,
        points integer,
        
        FOREIGN KEY (user_points_id) REFERENCES Users(id),
        FOREIGN KEY (store_points_id) REFERENCES Store(id_store)
    
    );''')
    the_connection.commit()

    the_connection.close()




tables()

def addUser(the_user:models.UserModel):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_cursor.execute('''INSERT INTO Users(username,email,password) VALUES (?,?,?)''',(the_user.username,the_user.email,the_user.password))
    the_connection.commit()
    the_row_count = the_cursor.rowcount
    the_connection.close()

    if the_row_count:
        return {'success':'Added'}
    else:
        return {'success':'Not Added'}



def logInFunction(the_user:models.LogInModel):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    try:
        the_cursor.execute('''SELECT * FROM Users WHERE username = :username and password = :password''',{'username':the_user.username,'password':the_user.password})
        the_connection.commit()
        the_fetched = the_cursor.fetchone()
    except Exception as e:
        return {'success':f'Failed Because Of {str(e)}'}
    finally:
        the_connection.close()

    if the_fetched:
        return {'success':'True','fetched':the_fetched}
    else:
        return {'success':'False'}


def create_category(category):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_cursor.execute('''INSERT INTO Categories (category_name) VALUES (?)''',(category,))
    the_connection.commit()
    the_row_diffrence = the_cursor.rowcount
    the_connection.close()

    if the_row_diffrence:
        return {'success':'True'}
    else:
        return {'success':'False'}

def selectCategories():
    the_conn = create_connection()
    the_cursor = the_conn.cursor()
    the_cursor.execute('''SELECT * FROM Categories''')
    the_conn.commit()
    the_fetched = the_cursor.fetchall()
    the_conn.close()
    return the_fetched

def createStore(shop:models.shopCreateModel):
    the_conn = create_connection()
    the_cursori = the_conn.cursor()
    the_cursori.execute('''INSERT INTO Store (user_id,store_name) VALUES (?,?)''',(shop.user_id,shop.shop_name))
    the_conn.commit()
    the_last_row_id = the_cursori.lastrowid
    the_count = the_cursori.rowcount
    the_conn.close()

    if the_count:
        return {'success':'True','id':the_last_row_id}
    else:
        return {'success':'False'}


def addProduct(product:models.addProduct):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()

    the_cursor.execute('''INSERT INTO products (product_name,category_id,product_store_id,product_price) VALUES (:product_name,:category_id,:product_store_id,:product_price)''',{'product_name':product.product_name,'category_id':product.category_id,'product_store_id':product.product_store_id,'product_price':product.product_price})
    the_connection.commit()
    the_row_count = the_cursor.rowcount
    the_connection.close()

    if the_row_count:
        return {'success':'True'}
    else:
        return {'success':'False'}


def getStore(store:models.shopCreateModel):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()

    the_cursor.execute('''SELECT * FROM Store WHERE user_id = :user_id and store_name = :store_name''',{'user_id':store.user_id,'store_name':store.shop_name})
    the_connection.commit()
    the_data = the_cursor.fetchone()
    the_connection.close()

    if the_data:
        return {'success':'True','data':the_data}
    else:
        return {'success':'False'}


def store(the_store:int):
    the_connection = create_connection()

    the_cursor = the_connection.cursor()

    the_cursor.execute('''SELECT * FROM Store WHERE user_id = ?''',(the_store,))
    fetched = the_cursor.fetchall()
    the_cursor.close()
    the_connection.close()

    if fetched:
        return {'success':'True','data':fetched}
    else:
        return {'success':'False'}


def seeing_products_of_store(store_id):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    try:
        the_cursor.execute('''SELECT * FROM Products INNER JOIN Store ON Products.product_store_id = Store.id_store WHERE Store.id_store = :id_store''',(store_id,))
        the_fetched = the_cursor.fetchall()
        if the_fetched:
            return {'success':'True','data':the_fetched}
        else:
            return {'success':'False'}
    except Exception as e:
        return {'success':f'Failed Because Of {str(e)}'}
    finally:
        the_cursor.close()
        the_connection.close()

# def selectProducts():
#     the_connection = create_connection()
#     the_cursor = the_connection.cursor()
#
#     the_cursor.execute('SELECT * FROM Products')
#
#     the_fetched = the_cursor.fetchall()
#
#     the_connection.close()
#
#     if the_fetched:
#         return {'success':'True','data':the_fetched}
#     else:
#         return {'success':'False'}


def getOrders(shop_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()

    try:
        the_cursor.execute('''SELECT * FROM Orders INNER JOIN Products ON Orders.product_id = Products.id_products INNER JOIN Store ON Orders.store_id = Store.id_store INNER JOIN Users ON Orders.user_ordering = Users.id WHERE Store.id_store = :id_store''',(shop_id,))
        the_fetched = the_cursor.fetchall()
        if the_fetched:
            return {'success':'True','data':the_fetched}
        else:
            return {'success':'No Data'}
    except Exception as e:
        return {'success':f'False Because Of {str(e)}'}
    finally:
        the_cursor.close()
        the_connection.close()


def all_shops(the_user_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    try:
        the_cursor.execute('''SELECT * FROM Store INNER JOIN Users ON Store.user_id = Users.id WHERE Store.user_id != ?''',(the_user_id,))
        fetched = the_cursor.fetchall()
        return {'success':'True','data':fetched}
    except Exception as e:
        return {'success':f'False Because Of {str(e)}'}
    finally:
        the_cursor.close()
        the_connection.close()


def get_shop_data(shop_data:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()

    try:
        the_cursor.execute('''
            SELECT a.*,d.*,e.* FROM Store as a
            LEFT JOIN Products AS d ON d.product_store_id = a.id_store 
            LEFT JOIN Categories AS e ON d.category_id = e.category_table_id
            WHERE a.id_store = ?''',(shop_data,))
        the_fetched_data = the_cursor.fetchall()
        if the_fetched_data:
            return {'success':'True','data':the_fetched_data}
        else:
            return {'success':'False'}
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_cursor.close()
        the_connection.close()


def handling_order(order:models.productOrder):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    try:
        the_cursor.execute('''INSERT INTO Orders (product_id,store_id,user_ordering,order_address,order_date) VALUES (:product_id,:store_id,:user_ordering,:order_address,:order_date)''',{"product_id":order.product_id,"store_id":order.store_id,"user_ordering":order.user_ordering,"order_address":order.order_address,'order_date':current_date})
        the_connection.commit()
        the_row_count = the_cursor.rowcount
        if the_row_count:
            return {'success':'True'}
        else:
            return {'success':'False'}
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_cursor.close()
        the_connection.close()


def orders(shop_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    order_state = "ACCEPTED"

    try:
        the_cursor.execute('''SELECT * FROM Orders 
        INNER JOIN Store ON Orders.store_id = Store.id_store 
        INNER JOIN Users ON Orders.user_ordering = Users.id
        INNER JOIN Products ON Orders.product_id = Products.id_product
        INNER JOIN Categories ON Products.category_id = Categories.category_table_id
        WHERE Store.id_store = ? AND Orders.order_completion = ?''',(shop_id,order_state))
        the_fetched = the_cursor.fetchall()
        if the_fetched:
            return {'success':'True','data':the_fetched}
        else:
            return {'success':'False'}
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_cursor.close()
        the_connection.close()


def add_to_cart(productToCart:models.productOrder):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_row_count = 0
    try:
        the_cursor.execute('''INSERT INTO Orders (product_id,store_id,user_ordering,order_address,order_date) VALUES (:product_id,:store_id,:user_ordering,:order_address,:order_date)''',{'product_id':productToCart.product_id,'store_id':productToCart.store_id,'user_ordering':productToCart.user_ordering,'order_address':productToCart.order_address,'order_date':productToCart.order_date})
        the_connection.commit()
        the_row_count = the_cursor.rowcount
        order_id_ = the_cursor.lastrowid
        if the_row_count:
            the_cursor.execute('''INSERT INTO Cart (order_id) VALUES (:order_id)''',(order_id_,))
            the_connection.commit()
            the_row_count = the_cursor.rowcount
    except Exception as e:
        return {'success':f'Failed Because Of {str(e)}'}
    finally:
        the_connection.close()

    if the_row_count:
        return {'success':'True'}
    else:
        return {'success':'False'}

def getting_from_cart(product_to_get:models.getCart):
    order_state = 'PENDING'
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    try:
        the_cursor.execute('''SELECT * FROM Orders INNER JOIN Products ON Orders.product_id = Products.id_product WHERE user_ordering = :user_ordering AND store_id = :store_id AND order_completion = :order_completion''',{
            'user_ordering':product_to_get.user_id,
            'store_id':product_to_get.store_id,
            'order_completion':order_state
        })
        the_fetched = the_cursor.fetchall()
        if the_fetched:
            return {'success':'True','data':the_fetched}
        else:
            return {'success':'False'}
    except Exception as e:
        return {'success':f'Failed Because Of {str(e)}'}
    finally:
        the_connection.close()

def selecting_all():
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_cursor.execute('''SELECT * FROM Orders''')
    fetched = the_cursor.fetchall()
    the_connection.close()

    if fetched:
        return {'success':'True','data':fetched}
    else:
        return {'success':'False'}

def updateOrders(the_order_ids:models.updatingOrders):
    the_alias = 'ACCEPTED'
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_order_ids_numbers = the_order_ids.order_ids
    is_count = True
    for the_id in the_order_ids_numbers:
        try:
            the_cursor.execute('''UPDATE Orders SET order_completion = :order_completion,order_address = :order_address WHERE order_id = :order_id''',{
                'order_completion':the_alias,
                'order_address':the_order_ids.order_address,
                'order_id':the_id
            })
            the_connection.commit()
            row_count = the_cursor.rowcount
            if not row_count:
                is_count = False
        except Exception as e:
            raise Exception(f'Failed Because Of {str(e)}')
    the_connection.close()
    if is_count:
        return {'success':'True'}
    else:
        return {'success':'False'}

def delete_order():
    the_alias = 'PENDING'
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_cursor.execute('''DELETE FROM ORDERS WHERE orders.order_completion = ?''',(the_alias,))
    the_connection.commit()
    the_row = the_cursor.rowcount
    the_connection.close()
    if the_row:
        return {'success':'True'}
    else:
        return {'success':'False'}


def checkRelation(the_details:models.checkRelation):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    order_complete = 'ACCEPTED'

    try:
        the_cursor.execute('''SELECT * FROM Orders WHERE store_id = :store_id AND user_ordering = :user_ordering AND order_completion = :order_completion''',{
            'store_id':the_details.store_id,
            'user_ordering':the_details.user_id,
            'order_completion':order_complete
        })
        the_fetch = the_cursor.fetchall()
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_connection.close()


    if the_fetch:
        return {'success':'True'}
    else:
        return {'success':'False'}


def checkIfUserRated(user_id:int,store_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    try:
        the_cursor.execute('''SELECT * FROM ratings WHERE user_rating_id = :user_rating_id AND store_rated_id = :store_rated_id''',{
            'user_rating_id':user_id,
            'store_rated_id':store_id
        })
        the_connection.commit()
        fetched = the_cursor.fetchone()
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)} ')

    finally:
        the_connection.close()

    if fetched:
        return {'success':'True','data':fetched}
    else:
        return {'success':'False'}

def addRating(adding_rating:models.addRating):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_checking = checkIfUserRated(adding_rating.user_id,adding_rating.store_id)
    if the_checking['success'] == 'True':
        return {'success':'True','info':'User Alredy Rated','rating':the_checking['data']}

    try:
        the_cursor.execute('''INSERT INTO ratings (user_rating_id,store_rated_id,the_rate) VALUES (:user_rating_id,:store_rating_id,:the_rate)''',{
            'user_rating_id':adding_rating.user_id,
            'store_rating_id':adding_rating.store_id,
            'the_rate':adding_rating.rate
        })
        the_connection.commit()
        the_row = the_cursor.rowcount
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_connection.close()

    if the_row:
        return {'success':'True','info':''}
    else:
        return {'success':'False'}

def get_avg(the_store_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    try:
        the_cursor.execute('''SELECT * FROM ratings WHERE store_rated_id = :store_rated_id''',(the_store_id,))
        the_connection.commit()
        the_fetched_data = the_cursor.fetchall()
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')

    finally:
        the_connection.close()

    if the_fetched_data:
        return {'success':'True','ratings':the_fetched_data}
    else:
        return {'success':'False'}


def get_current_points(user_id:int,store_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()

    try:
        the_cursor.execute('''SELECT * FROM points WHERE user_points_id = :user_points_id AND store_points_id = :store_points_id''',{
            'user_points_id':user_id,
            'store_points_id':store_id
        })
        the_connection.commit()
        fetched_data = the_cursor.fetchone()
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_connection.close()

    if fetched_data:
        return {'success':'True','data':fetched_data}
    else:
        return {'success':'False'}

def updatingPoints(updated:models.updatePoints):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    checking_points = get_current_points(updated.user_id,updated.store_id)
    the_row_count = 0
    try:
        if checking_points['success'] == 'True':
            the_updated = checking_points['data'][3] + updated.points # ikom marr old points + new points
            # update points to set the new points
            the_cursor.execute('''UPDATE points SET points = :points WHERE user_points_id =:user_points_id AND store_points_id = :store_points_id''',{
                'points':the_updated,
                'user_points_id':updated.user_id,
                'store_points_id':updated.store_id
            })
            the_connection.commit()
            the_row_count = the_cursor.rowcount
        else:
            # if the user until now had no points
            # create some points for him
            the_cursor.execute('''INSERT INTO points (user_points_id,store_points_id,points) VALUES (:user_points_id,:store_points_id,:points)''',{
                'user_points_id':updated.user_id,
                'store_points_id':updated.store_id,
                'points':updated.points
            })
            the_connection.commit()
            the_row_count = the_cursor.rowcount
    except Exception as e:
        raise Exception(f'Failed Updating Because Of {str(e)}')
    finally:
        the_connection.close()

    if the_row_count:
        return {'success':'True'}
    else:
        return {'success':'False'}

def productsLength(store_id:int):
    the_conn = create_connection()
    the_cursor = the_conn.cursor()
    try:
        the_cursor.execute('''SELECT id_product FROM Products WHERE product_store_id = :store_id''',(store_id,))
        the_conn.commit()
        the_fetched = the_cursor.fetchall()
    except Exception as e:
        raise Exception(f'Failed Because {str(e)}')
    finally:
        the_conn.close()

    if the_fetched:
        return {'success':'True','data':the_fetched}
    else:
        return {'success':'False'}
def randomProduct(store_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_length = productsLength(store_id)
    the_data = the_length['data']
    every_id = [id[0] for id in the_data]
        # mvyn mi marr te dhenat e tyre
    random_number = every_id[random.randint(0,(len(every_id) - 1))]
    try:
        the_cursor.execute('''SELECT * FROM Products WHERE id_product = :id_product AND product_store_id = :product_store_id''',{
            'id_product':random_number,
            'product_store_id':store_id
        })
        the_connection.commit()
        the_fetched_product = the_cursor.fetchone()
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_connection.close()

    if the_fetched_product:
        return {'success':'True','data':the_fetched_product,'number':random_number}
    else:
        return {'success':'False','number':random_number}

def updatePointsToZero(the_data:models.gettingPoints):
    the_connection = create_connection()
    the_cursori = the_connection.cursor()
    new_points = 0
    try:
        the_cursori.execute('''UPDATE points SET points = :points WHERE user_points_id = :user_points_id AND store_points_id = :store_points_id''',{
            'points':new_points,
            'user_points_id':the_data.user_id,
            'store_points_id':the_data.store_id
        })
        the_connection.commit()
        the_row_count = the_cursori.rowcount

    except Exception as e:
        raise Exception(str(e))

    finally:
        the_connection.close()

    if the_row_count:
        return {'success':'True'}
    else:
        return {'success':'False'}

def all_products():
    the_conn = create_connection()
    the_cursor = the_conn.cursor()
    the_cursor.execute('''Select * From Products''')
    the_fetched = the_cursor.fetchall()
    the_conn.close()
    return {'data':the_fetched}


def get_ratings_of_a_store(store_id:int):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_list_with_user_ids = []
    the_ratings_for_each_user = []
    try:
        the_cursor.execute('''SELECT * FROM ratings WHERE store_rated_id = :store_rated_id''',(store_id,))
        fetching = the_cursor.fetchall()
    except Exception as e:
        raise Exception(f'Failed Because Of {str(e)}')
    finally:
        the_connection.close()


    if fetching:
        for data in fetching:
            the_list_with_user_ids.append(data[1])
            the_ratings_for_each_user.append(data[3])

        the_order_for_user = get_orders_from_users_who_rate(store_id,the_list_with_user_ids)
        return {'success':'True','ratings':the_ratings_for_each_user,'orders':the_order_for_user}
    else:
        return {'success':'False'}


def get_orders_from_users_who_rate(store_id,users):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()
    the_list_with_orders = []
    try:
        for user in users:
            the_cursor.execute('''SELECT COUNT(order_id) FROM Orders WHERE user_ordering = :user_ordering AND store_id = :store_id''',{
                'user_ordering':user,
                'store_id':store_id
            })
            the_fetch = the_cursor.fetchone()
            if the_fetch:
                the_list_with_orders.append(the_fetch[0])
    except Exception as e:
        raise Exception(str(e))
    finally:
        the_connection.close()

    return the_list_with_orders

def get_most_loyal_costumers(store_id):
    the_connection = create_connection()
    the_cursor = the_connection.cursor()

    try:
        the_cursor.execute('''SELECT * FROM Orders INNER JOIN Users ON Orders.user_ordering = Users.id WHERE Orders.store_id = :store_id''',(store_id,))
        the_connection.commit()
        fetched_data = the_cursor.fetchall()
    except Exception as e:
        raise Exception(str(e))

    finally:
        the_connection.close()

    if fetched_data:
        return {'success':'True','users':fetched_data}
    else:
        return {'success':'False'}











