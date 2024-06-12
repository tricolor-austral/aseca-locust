import threading
import uuid

from locust import LoadTestShape, HttpUser
from locust.user import task


class Test(HttpUser):

    @task
    def getorder(self):
        self.client.get(
            "/order"
        )

    @task
    def order(self):
        unique_buyer_id = str(uuid.uuid4())

        self.client.post("/order", json={
            "buyerId": unique_buyer_id,
            "products": [
                {
                    "productIds": "mac3",
                    "qty": 1
                }
            ]
        })

    @task
    def ship(self):
        self.client.post("/cross-docking/delivered", json={
            "orderID": "1234",
            "buyerId": "1234"
        })

    @task
    def checkStock(self):
        self.client.get("/product/mac3/stock/10")

    @task
    def getProducts(self):
        self.client.get("/product")


class PeakLoadShape(LoadTestShape):

    def __init__(self):
        self.total_run_time = 60 * 3
        self.peak_users = 100
        self.ramp_up_time = 60
        self.peak_time = 60
        self.ramp_down_time = 60
        super().__init__()

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.ramp_up_time:
            user_count = int((self.peak_users / self.ramp_up_time) * run_time)
        elif run_time < self.ramp_up_time + self.peak_time:
            user_count = self.peak_users
        elif run_time < self.ramp_up_time + self.peak_time + self.ramp_down_time:
            elapsed_ramp_down_time = run_time - (self.ramp_up_time + self.peak_time)
            user_count = self.peak_users - int((self.peak_users / self.ramp_down_time) * elapsed_ramp_down_time)
        else:
            return None

        return user_count, user_count
