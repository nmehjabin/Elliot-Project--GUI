
import boto3
import time
from datetime import datetime, timedelta

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')

# Set table name
TABLE_NAME = 'ModelTestingUiSessionData'

def lambda_handler(event, context):
    """
    Lambda function to calculate unique session IDs from DynamoDB
    and publish the count to CloudWatch.
    """
    try:
        # Reference the DynamoDB table
        table = dynamodb.Table(TABLE_NAME)
        
        # Calculate the time range for the last 30 minutes
        now = int(time.time())
        past_30_minutes = now - (30 * 60)

        # Scan DynamoDB for items in the last 30 minutes
        response = table.scan(
            FilterExpression="timestamp >= :start_time",
            ExpressionAttributeValues={":start_time": past_30_minutes}
        )

        # Extract unique session IDs
        unique_sessions = len(set(item['session_id'] for item in response.get('Items', [])))

        # Publish the metric to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='MyApp',
            MetricData=[
                {
                    'MetricName': 'UniqueCookies',
                    'Value': unique_sessions,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )

        print(f"Metric published: {unique_sessions} unique cookies.")
        return {"statusCode": 200, "body": f"Metric published: {unique_sessions}"}

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
