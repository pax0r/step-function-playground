import time
import uuid

import boto3


ACTIVITY_ARN = 'arn:aws:states:eu-central-1:436321073706:activity:HelloWorld'
WORKER_NAME = 'worker-{}'.format(uuid.uuid4())


def work_function(input_data):
    who = input_data.get('who', 'Anonymous')
    time.sleep(2)
    return f"Hello {who}!"


if __name__ == '__main__':
    print(f"Starting worker {WORKER_NAME}")
    while True:
        client = boto3.client('stepfunctions')
        response = client.get_activity_task(
            activityArn=ACTIVITY_ARN,
            workerName=WORKER_NAME,
        )
        print(f"Got activity task with data: {response}")
        result = work_function(response['input'])
        client.send_task_success(
            taskToken=response['token'],
            output=result
        )
        print("Success sent to AWS")
