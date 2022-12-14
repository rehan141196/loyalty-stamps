from lambda_function import lambda_handler, table
from unittest.mock import patch
import json

def test_add_stamps_with_no_matching_record_in_DB():
    event = {
        'requestType': 'addStamps',
        'storeId': '12345',
        'customerId': '54312',
        'numberOfStamps': 1
    }

    expected = {
    'statusCode': 200,
    'body': json.dumps('Sucessfully added %s stamps for StoreId: %s and CustomerId: %s' % (event['numberOfStamps'], event['storeId'], event['customerId']))
    }

    expected_arguments = {
    	'StoreId': event['storeId'],
    	'CustomerId': event['customerId'],
    	'Stamps': event['numberOfStamps']
    }

    with patch.object(table, 'put_item', return_value={}) as mock_put_item, patch.object(table, 'get_item', return_value={}) as mock_get_item:
        result = lambda_handler(event, None)
        mock_put_item.assert_called_once()
        mock_put_item.assert_called_with(Item=expected_arguments)
        assert result == expected

def test_add_stamps_with_matching_record_in_DB():
    event = {
        'requestType': 'addStamps',
        'storeId': '12345',
        'customerId': '54312',
        'numberOfStamps': 1
    }

    expected = {
    'statusCode': 200,
    'body': json.dumps('Sucessfully added %s stamps for StoreId: %s and CustomerId: %s' % (event['numberOfStamps'], event['storeId'], event['customerId']))
    }

    get_item_response = {
    	'Item' : {
	    	'StoreId': event['storeId'],
	    	'CustomerId': event['customerId'],
	   		'Stamps': 1
	    }
    }

    expected_key = {
    	'StoreId': event['storeId'],
    	'CustomerId': event['customerId']
    }
    expected_update_expression = "set Stamps = Stamps + :val"
    expected_expression_attribute_values = {
    	':val': event['numberOfStamps']
    }
    expected_return_values = "UPDATED_NEW"

    with patch.object(table, 'update_item', return_value={}) as mock_update_item, patch.object(table, 'get_item', return_value=get_item_response) as mock_get_item:
        result = lambda_handler(event, None)
        mock_update_item.assert_called_once()
        mock_update_item.assert_called_with(Key=expected_key, UpdateExpression=expected_update_expression, ExpressionAttributeValues=expected_expression_attribute_values, ReturnValues=expected_return_values)
        assert result == expected

def test_reset_stamps_with_no_matching_record_in_DB():
    event = {
        'requestType': 'resetStamps',
        'storeId': '12345',
        'customerId': '54312'
    }

    expected = {
    'statusCode': 200,
    'body': json.dumps('Could not find record with StoreId: %s and CustomerId: %s' % (event['storeId'], event['customerId']))
    }

    expected_arguments = {
        'StoreId': event['storeId'],
        'CustomerId': event['customerId']
    }

    with patch.object(table, 'get_item', return_value={}) as mock_get_item:
        result = lambda_handler(event, None)
        assert result == expected

def test_reset_stamps_with_matching_record_in_DB():
    event = {
        'requestType': 'resetStamps',
        'storeId': '12345',
        'customerId': '54312'
    }

    expected = {
    'statusCode': 200,
    'body': json.dumps('Sucessfully reset stamps for StoreId: %s and CustomerId: %s' % (event['storeId'], event['customerId']))
    }

    get_item_response = {
        'Item' : {
            'StoreId': event['storeId'],
            'CustomerId': event['customerId'],
            'Stamps': 5
        }
    }

    expected_key = {
        'StoreId': event['storeId'],
        'CustomerId': event['customerId']
    }
    expected_update_expression = "set Stamps = :val"
    expected_expression_attribute_values = {
        ':val': 0
    }
    expected_return_values = "UPDATED_NEW"

    with patch.object(table, 'update_item', return_value={}) as mock_update_item, patch.object(table, 'get_item', return_value=get_item_response) as mock_get_item:
        result = lambda_handler(event, None)
        mock_update_item.assert_called_once()
        mock_update_item.assert_called_with(Key=expected_key, UpdateExpression=expected_update_expression, ExpressionAttributeValues=expected_expression_attribute_values, ReturnValues=expected_return_values)
        assert result == expected

def test_delete_stamps_with_no_matching_record_in_DB():
    event = {
        'requestType': 'deleteStamps',
        'storeId': '12345',
        'customerId': '54312',
        'numberOfStamps': 2
    }

    expected = {
    'statusCode': 200,
    'body': json.dumps('Could not find record with StoreId: %s and CustomerId: %s' % (event['storeId'], event['customerId']))
    }

    expected_arguments = {
        'StoreId': event['storeId'],
        'CustomerId': event['customerId']
    }

    with patch.object(table, 'get_item', return_value={}) as mock_get_item:
        result = lambda_handler(event, None)
        assert result == expected

def test_delete_stamps_when_record_in_DB_has_more_stamps_than_number_of_stamps_to_delete():
    event = {
        'requestType': 'deleteStamps',
        'storeId': '12345',
        'customerId': '54312',
        'numberOfStamps': 2
    }

    expected = {
    'statusCode': 200,
    'body': json.dumps('Sucessfully deleted %s stamps for StoreId: %s and CustomerId: %s. New number of stamps: 3' % (event['numberOfStamps'], event['storeId'], event['customerId']))
    }

    get_item_response = {
        'Item' : {
            'StoreId': event['storeId'],
            'CustomerId': event['customerId'],
            'Stamps': 5
        }
    }

    expected_key = {
        'StoreId': event['storeId'],
        'CustomerId': event['customerId']
    }
    expected_update_expression = "set Stamps = :val"
    expected_expression_attribute_values = {
        ':val': 3
    }
    expected_return_values = "UPDATED_NEW"

    with patch.object(table, 'update_item', return_value={}) as mock_update_item, patch.object(table, 'get_item', return_value=get_item_response) as mock_get_item:
        result = lambda_handler(event, None)
        mock_update_item.assert_called_once()
        mock_update_item.assert_called_with(Key=expected_key, UpdateExpression=expected_update_expression, ExpressionAttributeValues=expected_expression_attribute_values, ReturnValues=expected_return_values)
        assert result == expected

def test_delete_stamps_when_record_in_DB_has_less_stamps_than_number_of_stamps_to_delete():
    event = {
        'requestType': 'deleteStamps',
        'storeId': '12345',
        'customerId': '54312',
        'numberOfStamps': 7
    }

    expected = {
    'statusCode': 200,
    'body': json.dumps('Sucessfully deleted %s stamps for StoreId: %s and CustomerId: %s. New number of stamps: 0' % (event['numberOfStamps'], event['storeId'], event['customerId']))
    }

    get_item_response = {
        'Item' : {
            'StoreId': event['storeId'],
            'CustomerId': event['customerId'],
            'Stamps': 5
        }
    }

    expected_key = {
        'StoreId': event['storeId'],
        'CustomerId': event['customerId']
    }
    expected_update_expression = "set Stamps = :val"
    expected_expression_attribute_values = {
        ':val': 0
    }
    expected_return_values = "UPDATED_NEW"

    with patch.object(table, 'update_item', return_value={}) as mock_update_item, patch.object(table, 'get_item', return_value=get_item_response) as mock_get_item:
        result = lambda_handler(event, None)
        mock_update_item.assert_called_once()
        mock_update_item.assert_called_with(Key=expected_key, UpdateExpression=expected_update_expression, ExpressionAttributeValues=expected_expression_attribute_values, ReturnValues=expected_return_values)
        assert result == expected
