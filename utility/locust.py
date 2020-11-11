""" Using Locust lib for the load & performance test """
from locust import TaskSet, task, between , HttpUser
from django.urls import reverse
from django.test import Client
import json

class UserBehavior(TaskSet):

    header = {}
    def on_start(self):
        self.login()

    def login(self):
        res = self.client.get("/accounts/login/")
        csrftoken = res.cookies["csrftoken"]
        global header
        header = {"X-CSRFToken": csrftoken}
        self.client.post("/accounts/login/",
                         json={"username": "GH", "password": "1234567a"},
                         headers=header)
    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def post_query_for_new_question(self):
        #data = {"course": "CZ3002", "title":"Do you love ASE", "content":"hell no"}
        self.client.get("/questions/new", headers=header)

    # @task(3)
    # def register(self):
    #     data = {'username':"test123", 'first_name':"Gary", 'last_name':"Shen",
    #               'email':"shenguangxu1009@gmail.com", 'password1':"CZ3002Test1", 'password2':"CZ3002Test1"}
    #     self.client.post("accounts/register",json = data, headers=header)

    @task(3)
    def logout(self):
        self.client.get("/accounts/logout", headers=header)

    @task(4)
    def view_admin(self):
        self.client.get("/admin/", headers=header)

    @task(5)
    def view_question_detail(self):
        self.client.get("/questions/how-to-write-code", headers = header)

    @task(6)
    def edit_question(self):
        self.client.get("/questions/how-to-write-code/edit", headers=header)

    @task(7)
    def post_query_for_new_reply(self):
        data = {"content":"yes of course"}
        self.client.post("/questions/how-to-write-code",json = data, headers=header)

    @task(8)
    def delete_question(self):
        self.client.get("/questions/how-to-write-code/delete", headers=header)


''' driver program '''
class User(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 15000
    host = "http://127.0.0.1:8000"
