from fastapi import FastAPI
import re
import databaz
import models
from typing import List


app = FastAPI()


@app.post('/signUp')
async def signUp(the_data:models.UserModel):
    the_username = the_data.username
    the_email = the_data.email
    the_password = the_data.password
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern,the_email) and len(the_password) >= 8:
        return {
            'success': 'Check Password Or Email'
        }
    the_new_model = models.UserModel(username=the_username, email=the_email, password=the_password)
    the_function = databaz.addUser(the_new_model)
    if the_function['success'] == 'Added':
        return {
            'success':'User Added'
        }
    else:
        return {
            'success':'Something Went Wrong'
        }

@app.post('/logIn')
async def logIn(the_data:models.LogInModel):
    the_db_function = databaz.logInFunction(the_data)
    if the_db_function['success'] == 'True':
        return {'success':'Logged In','fetched':the_db_function['fetched']}
    else:
        return {'success':'Not Logged'}

@app.post('/categories')
async def addCategories(the_categories:List[str]):
    for category in the_categories:
        the_creation = databaz.create_category(category)
        if the_creation['success'] == 'False':
            return

    return {'success':'True'}

@app.get('/getCategories')
async def selectCategories():
    the_function = databaz.selectCategories()
    if the_function:
        return {'success':'True','data':the_function}
    else:
        return {'success':'False'}

@app.post('/createStore')
async def createStore(the_store:models.shopCreateModel):
    the_creation = databaz.createStore(the_store)
    if the_creation['success'] == 'True':
        return {'success':'True','id':the_creation['id']}
    else:
        return {'success':'False'}


@app.post('/addProduct')
async def addProduct(product:models.addProduct):
    the_product = databaz.addProduct(product)
    if the_product['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}


@app.post('/getStore')
async def getStore(store:models.shopCreateModel):
    the_store = databaz.getStore(store)
    if the_store['success'] == 'True':
        return {'success':'True','data':the_store['data']}
    else:
        return {'success':'False'}


@app.get('/userStore/{user_store}')
async def store_getting(user_store:int):
    the_store = databaz.store(user_store)
    if the_store is not None:
        if the_store['success'] == 'True':
            return {'success':'True','data':the_store['data']}
        else:
            return {'success':'False'}
    else:
        return {'success':'Store Returned Nothing'}

@app.get('/seeStoreProducts/{store_id}')
async def store_products(store_id:int):
    the_products = databaz.seeing_products_of_store(store_id)
    if the_products['success'] == 'True':
        return {'success':'True','data':the_products['data']}
    else:
        return {'success':'False'}

# @app.get('/seeAllProducts')
# async def seeAllProducts():
#     the_prod = databaz.selectProducts()
#     if the_prod['success'] == 'True':
#         return {'success':the_prod}
#     else:
#         return {'success':'False'}


@app.get('/ordersByStore/{store_id}')
async def getOrdersByStore(store_id:int):
    the_orders = databaz.getOrders(store_id)
    if the_orders['success'] == 'True':
        return {'success':'True','data':the_orders['data']}
    else:
        return {'success':'False'}


# maspari mvyn mu me i marr kejt shops
@app.get('/allShops/{the_user_id}')
async def getAllShops(the_user_id:int):
    all_shops = databaz.all_shops(the_user_id)
    if all_shops['success'] == 'True':
        return {'success':'True','data':all_shops['data']}
    else:
        return {'success':'False'}

@app.get('/shopData/{shop_data}')
async def getShopData(shop_data:int):
    shop_data = databaz.get_shop_data(shop_data)

    if shop_data['success'] == 'True':
        return {'success':'True','data':shop_data['data']}
    else:
        return {'success':'False'}

@app.post('/orderProduct')
async def order_product(product_ordered:models.productOrder):
    handling_order = databaz.handling_order(product_ordered)
    if handling_order['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}

@app.get('/eachOrder/{store_id}')
async def each_order(store_id:int):
    orders = databaz.orders(store_id)

    if orders['success'] == 'True':
        return {'success':'True','data':orders['data']}
    else:
        return {'success':'False'}

@app.get('/eachCategory/{store_id}')
async def each_category(store_id:int):
    category = databaz.get_categories(store_id)
    if category['success'] == 'True':
        return {'success':'True','data':category['data']}
    else:
        return {'success':'False'}


@app.post('/addToCart')
async def addingToCart(productToCart:models.productOrder):
    add_to_cart = databaz.add_to_cart(productToCart)
    if add_to_cart['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}


@app.post('/getProducts')
async def getProductsCart(productsCart:models.getCart):
    getting_from_cart = databaz.getting_from_cart(productsCart)
    if getting_from_cart['success'] == 'True':
        return {'success':'True','data':getting_from_cart['data']}
    else:
        return {'success':'False'}


@app.post('/updatingOrders')
async def updateOrders(the_order_ids:models.updatingOrders):
    the_db = databaz.updateOrders(the_order_ids)
    if the_db['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}

@app.delete('/deletingOrders')
async def deletingOrders():
    the_delete = databaz.delete_order()
    if the_delete['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}

@app.post('/checkRelation')
async def checkRelation(the_details:models.checkRelation):
    checked = databaz.checkRelation(the_details)
    if checked['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}

@app.post('/addRating')
async def addRating(the_rating:models.addRating):
    the_rating = databaz.addRating(the_rating)
    if the_rating['success'] == 'True' and the_rating['info']:
        return {'success':'True','info':the_rating['info']}
    elif the_rating['success'] == 'True':
        return {'success':'True','info':''}
    else:
        return {'success':'False'}

@app.get('/avgRating/{the_shop}')
async def get_avg_rating(the_shop:int):
    the_avg_rating = databaz.get_avg(the_shop)
    if the_avg_rating['success'] == 'True':
        the_rating = the_avg_rating['ratings']
        return {'success':'True','rating':the_rating}
    else:
        return {'success':'False'}

@app.post('/addingPoints')
async def adding_points(add_points:models.updatePoints):
    the_updated = databaz.updatingPoints(add_points)
    if the_updated['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}

@app.post('/getPoints')
async def gettingPoints(the_points:models.gettingPoints):
    get_points = databaz.get_current_points(the_points.user_id,the_points.store_id)
    if get_points['success'] == 'True':
        return {'success':'True','data':get_points['data']}
    else:
        return {'success':'False'}

@app.get('/randomProduct/{store_id}')
async def random(store_id:int):
    the_random_product = databaz.randomProduct(store_id)
    if the_random_product['success'] == 'True':
        return {'success':'True','data':the_random_product['data'],'number':the_random_product['number']}
    else:
        return {'success':'False','number':the_random_product['number']}


@app.post('/resetPoints')
async def resetPoints(reset_data:models.gettingPoints):
    the_reseting = databaz.updatePointsToZero(reset_data)
    if the_reseting['success'] == 'True':
        return {'success':'True'}
    else:
        return {'success':'False'}

@app.get('/allProducts')
async def getPr():
    the_products = databaz.all_products()
    return the_products

@app.get('/ratingsFromStore/{store_id}')
async def getRatingsFromStore(store_id:int):
    the_ratings = databaz.get_ratings_of_a_store(store_id)
    if the_ratings['success'] == 'True':
        return {'success':'True','ratings':the_ratings['ratings'],'orders':the_ratings['orders']}
    else:
        return {'success':'False'}

@app.get('/mostOrdersUsers/{store_id}')
async def user_with_most_orders(store_id:int):
    the_loyal_costumers = databaz.get_most_loyal_costumers(store_id)
    if the_loyal_costumers['success'] == 'True':
        return {'success':'True','users':the_loyal_costumers['users']}
    else:
        return {'success':'False'}








