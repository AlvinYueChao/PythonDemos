import time
from locust import HttpUser, task, between, User
from loguru import logger

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(1)

    def on_start(self):
        self.client.post("/login", json={"username": "foo", "password": "bar"})


class CustomUser(User):
    wait_time = between(1, 5)

    def __init__(self, environment):
        super().__init__(environment)
        self.init_var = None

    @task
    def task1(self):
        logger.info("=== invoke task1, value of init_var: {} ===", self.init_var)

    @task
    def task2(self):
        logger.info("=== invoke task2, value of init_var: {} ===", self.init_var)

    def on_start(self):
        logger.info("=== on start... ===")
        self.init_var = "initialized value"

    def on_stop(self):
        logger.info("=== on stop... ===")