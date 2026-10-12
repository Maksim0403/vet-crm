import os

from locust import HttpUser, between, task


class VetCRMUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        email = os.getenv("VETCRM_EMAIL")
        password = os.getenv("VETCRM_PASSWORD")

        if not email or not password:
            raise RuntimeError("Set VETCRM_EMAIL and VETCRM_PASSWORD before starting Locust")

        with self.client.post(
            "/auth/login",
            data={"username": email, "password": password},
            name="POST /auth/login",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                token = response.json()["access_token"]
                self.client.headers.update({"Authorization": f"Bearer {token}"})
            else:
                response.failure(f"Login failed: HTTP {response.status_code}")

    @task(5)
    def list_pets(self):
        self.client.get("/pets/", name="GET /pets/")

    @task(3)
    def list_appointments(self):
        self.client.get(
            "/clinic/appointments",
            name="GET /clinic/appointments",
        )

    @task(2)
    def user_home(self):
        self.client.get("/user/home", name="GET /user/home")

    @task(1)
    def health_check(self):
        self.client.get("/health", name="GET /health")
