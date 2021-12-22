import time
from locust import HttpUser, task, between
from client import ApiClient

class OpenAPIUser(HttpUser):
    wait_time = between(1, 5)

    # @task(3)
    # def infer_cls(self):
    #     self.client.get(f"/item?id={item_id}", name="/item")
    #     time.sleep(1)

    @task
    def upload_file(self):
        self.client.upload_file(codebase="classification", filename="one.e9be6cd7.jpg", new_token=True)

    def on_start(self):
        self.client = ApiClient()