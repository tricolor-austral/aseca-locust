import uuid

from locust import HttpUser, task


class Test(HttpUser):

    @task
    def getorder(self):
        self.client.get(
            "/order"
        )

    @task
    def orderAndShip(self):
        unique_buyer_id = str(uuid.uuid4())

        order = self.client.post("/order", json={
            "buyerId": unique_buyer_id,
            "products": [
                {
                    "productIds": "2c374532-0308-40a6-b477-ea31f39a6bd1",
                    "qty": 1
                }
            ]
        })

        if order.status_code == 201:
            self.client.post("/cross-docking/delivered", json={
                "orderID": order.json().get("id"),
                "buyerId": "1234"
            })

    @task
    def checkStock(self):
        self.client.get("/product/2c374532-0308-40a6-b477-ea31f39a6bd1/stock/10")

    @task
    def getProducts(self):
        self.client.get("/product")
