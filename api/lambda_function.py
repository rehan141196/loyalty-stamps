import json
import boto3
from time import gmtime, strftime

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('StampInfo')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def lambda_handler(event, context):
    # extract data from request
    request_type = event['requestType']
    store_id = event['storeId']
    customer_id = event['customerId']

    response = {}

    # call function based on request type
    if request_type == "getStamps": 
        response = get_stamps(store_id, customer_id)
    elif request_type ==  "addStamps":
        number_of_stamps = event['numberOfStamps']
        response = add_stamps(store_id, customer_id, number_of_stamps)
    elif request_type ==   "resetStamps":
        response = reset_stamps(store_id, customer_id)
    elif request_type ==   "deleteStamps":
        number_of_stamps = event['numberOfStamps']
        response = delete_stamps(store_id, customer_id, number_of_stamps)
    elif request_type ==   "setupCustomer":
        customer_name = event['customerName']
        response = setupCustomer(store_id, customer_name)

    return response

def get_stamps(store_id, customer_id):
    """
    Gets stamp data from table for a store-customer pair

    :param store_id: The StoreId of the store
    :param customer_id: The CustomerId of the customer
    :return: TBD
    """
    return {}

def add_stamps(store_id, customer_id, number_of_stamps):
    """
    Adds stamps for a store-customer pair if the pair exists. Creates the pair if it does not exist

    :param store_id: The StoreId of the store
    :param customer_id: The CustomerId of the customer
    :param number_of_stamps: The number of stamps to add
    :return: dictionary with HTTP response
    """
    get_response = table.get_item(Key={'StoreId': store_id, 'CustomerId': customer_id})

    if 'Item' in get_response:
        current_stamps = int(get_response['Item']['Stamps'])
        update_response = table.update_item(
            Key={'StoreId': store_id, 'CustomerId': customer_id},
            UpdateExpression="set Stamps = Stamps + :val",
            ExpressionAttributeValues={':val': number_of_stamps},
            ReturnValues="UPDATED_NEW")
    else:
        put_response = table.put_item(
        Item={
            'StoreId': store_id,
            'CustomerId': customer_id,
            'Stamps': number_of_stamps
            })
    return {
    'statusCode': 200,
    'body': json.dumps('Sucessfully added ' + str(number_of_stamps) + ' stamps for StoreId: ' + store_id + ' and CustomerId: ' + customer_id)
    }

def reset_stamps(store_id, customer_id):
    """
    Resets number of stamps to 0 for a store-customer pair

    :param store_id: The StoreId of the store
    :param customer_id: The CustomerId of the customer
    :return: dictionary with HTTP response
    """
    get_response = table.get_item(Key={'StoreId': store_id, 'CustomerId': customer_id})

    if 'Item' in get_response:
        current_stamps = int(get_response['Item']['Stamps'])
        update_response = table.update_item(
            Key={'StoreId': store_id, 'CustomerId': customer_id},
            UpdateExpression="set Stamps = :val",
            ExpressionAttributeValues={':val': 0},
            ReturnValues="UPDATED_NEW")
        return {
            'statusCode': 200,
            'body': json.dumps('Sucessfully reset stamps for StoreId: ' + store_id + ' and CustomerId: ' + customer_id)
            }
    return {
    'statusCode': 200,
    'body': json.dumps('Could not find record with StoreId: ' + store_id + ' and CustomerId: ' + customer_id)
    }

def delete_stamps(store_id, customer_id, number_of_stamps):
    """
    Deletes stamps for a store-customer pair

    :param store_id: The StoreId of the store
    :param customer_id: The CustomerId of the customer
    :param number_of_stamps: The number of stamps to add
    :return: dictionary with HTTP response
    """
    get_response = table.get_item(Key={'StoreId': store_id, 'CustomerId': customer_id})

    if 'Item' in get_response:
        current_stamps = int(get_response['Item']['Stamps'])

        new_stamps = max(current_stamps - number_of_stamps, 0)

        update_response = table.update_item(
            Key={'StoreId': store_id, 'CustomerId': customer_id},
            UpdateExpression="set Stamps = :val",
            ExpressionAttributeValues={':val': new_stamps},
            ReturnValues="UPDATED_NEW")
        return {
            'statusCode': 200,
            'body': json.dumps('Sucessfully deleted ' + str(number_of_stamps) + ' stamps for StoreId: ' + store_id + ' and CustomerId: ' + customer_id + '. New number of stamps: ' + str(new_stamps))
            }
    return {
    'statusCode': 200,
    'body': json.dumps('Could not find record with StoreId: ' + store_id + ' and CustomerId: ' + customer_id)
    }

# For local testing
if __name__ == '__main__':
    event = {
        'requestType': 'addStamps',
        'storeId': '12345',
        'customerId': '54312',
        'numberOfStamps': 1
    }
    print(lambda_handler(event, None))