import json
import time
import uuid

import boto3


ACTIVITY_ARN = "arn:aws:states:eu-central-1:436321073706:activity:HelloWorld"
WORKER_NAME = "worker-{}".format(uuid.uuid4())


def work_function(input_data):
    who = input_data.get("who", "Anonymous")
    time.sleep(2)
    return {"result": f"Hello {who}!"}


def main():
    print(f"Starting worker {WORKER_NAME}")
    client = boto3.client("stepfunctions")
    while True:
        response = client.get_activity_task(
            activityArn=ACTIVITY_ARN, workerName=WORKER_NAME,
        )
        token = response.get("taskToken")
        if token:
            print(f"Got activity task with data: {response}")
            try:
                input_data = json.loads(response["input"])
                result = work_function(input_data)
                client.send_task_success(taskToken=token, output=json.dumps(result))
                print("Success sent to AWS")
            except Exception as exc:
                print("Error on processing task: ", exc)
                client.send_task_failure(
                    taskToken=token, error=str(exc), cause=repr(exc),
                )
        else:
            print("No task, wait a little bit before next fetch")
            time.sleep(1)


if __name__ == "__main__":
    main()
