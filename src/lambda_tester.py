"""
Local tester class to test lambda function.
"""
from src import lambda_function


EVENT = {
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}


class TestLambdaContext():
    """
    Dummy lambda context class for local testing.
    """
    function_name = 'lambda-structured-logging'
    function_version = 'LATEST'
    invoked_function_arn = 'arn:aws:lambda:us-east-1:1234567890:lambda-structured-logging'
    aws_request_id = '022660DA-7F3E-4559-A551-B5E96A6D5E93'
    log_group_name = '/aws/lambda/lambda-structured-logging'
    log_stream_name = '2020/01/20/[$LATEST]/A551B5E96A6D5E93'


if __name__ == '__main__':
    lambda_function.lambda_handler(EVENT, TestLambdaContext)
