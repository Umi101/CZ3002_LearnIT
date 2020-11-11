from django.urls import reverse, resolve
from django.test import TestCase, Client
from django.contrib.auth import get_user_model,authenticate
from datetime import date
from apps.questions.models import Course, Question, Reply, ReportedQuestion, ReportedReply
from apps.accounts.models import Profile
import json

# Create your tests here.
class ModelTests(TestCase):
    def setUp(self):
        """ create student accounts """
        self.student1 = get_user_model().objects.create_user(
            username = "studenttest1",
            email = "studenttest1@e.ntu.edu.sg",
            password = "123456"
        )

        self.student2 = get_user_model().objects.create_user(
            username = "studenttest2",
            email = "studenttest2@e.ntu.edu.sg",
            password = "123456"
        )

        """ create a instructor account """
        self.instructor = get_user_model().objects.create_superuser(
            username = "instructortest",
            email = "instructortest@ntu.edu.sg",
            password = "123456"
        )
        """ Create a course """
        self.course1 = Course.objects.create(
            title = "CZ3006",
            description = "Computer Networks"
        )

        """ Create a question """
        self.question1 = Question.objects.create(
            course = self.course1,
            owner = self.student1,
            title = "How to config IP",
            content = "config IP using DHCP"
        )

        """ Create a reply """
        self.reply1 = Reply.objects.create(
            creator = self.student2,
            question = self.question1,
            content = "just read through lecture notes" 
        )

        """ Create a profile """
        self.profile1 = Profile.objects.get(user=self.student1)
        self.profile1.bio = "An NTU student"
        self.profile1.city = "Singapore"
        self.profile1.state = "Singapore"
        self.profile1.birthday = date(1997,10,1)
        self.profile1.save()

        """ Store a reported question """
        self.reportedquestion1 = ReportedQuestion.objects.create(
            question = self.question1
        )

        """ Store a reported reply """
        self.reportedreply = ReportedReply.objects.create(
            reply = self.reply1 
        )


    """ test cases start """
    def test_create_student(self):
        """ test the student is created """
        student = get_user_model().objects.get(email="studenttest1@e.ntu.edu.sg")
        """ check all attributes of students are correct """
        self.assertEqual(student.username, "studenttest1")
        self.assertTrue(student.check_password("123456"))

    def test_create_instructor(self):
        """ test the instructor is created """
        instructor = get_user_model().objects.get(email="instructortest@ntu.edu.sg")
        """ check all attributes of instructor are correct """
        self.assertEqual(instructor.username, "instructortest")
        self.assertTrue(instructor.check_password("123456"))

    def test_create_question(self):
        """ test a question is created """
        question = Question.objects.get(course=self.course1, owner=self.student1)
        """ check all attributes of question are correct """
        self.assertEqual(question.title, "How to config IP")
        self.assertEqual(question.content, "config IP using DHCP")

    def test_create_reply(self):
        """ test a reply is created """
        reply = Reply.objects.get(question=self.question1, creator=self.student2)
        """ test all attributes of reply are correct """
        self.assertEqual(reply.content, "just read through lecture notes")

    def test_create_profile(self):
        """test a profile is created """
        profile = Profile.objects.get(user=self.student1)
        """ check all attributes of profile are correct """
        self.assertEqual(profile.bio, "An NTU student")
        self.assertEqual(profile.city, "Singapore")
        self.assertEqual(profile.state, "Singapore")
        self.assertEqual(profile.birthday, date(1997,10,1))

    def test_store_reportedquestion(self):
        """ test a reportedquestion is stored """
        reportedquestion = ReportedQuestion.objects.get(question=self.question1)
        """ test all attributes of reportedquestion are correct """
        self.assertEqual(reportedquestion.question.title, "How to config IP")
        self.assertEqual(reportedquestion.question.content, "config IP using DHCP")

    def test_store_reportedreply(self):
        """ test a reportedreply is stored """
        reportedreply = ReportedReply.objects.get(reply=self.reply1)
        """ test all attributes of reportedreply are correct """
        self.assertEqual(reportedreply.reply.content, "just read through lecture notes")

    """ test cases end """

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        """ create a student account """
        self.credentials1 = {
            "username" : "studenttest1",
            "email" : "studenttest1@e.ntu.edu.sg",
            "password" : "123456",
        }
        self.student1 = get_user_model().objects.create_user(**self.credentials1)

        self.credentials2 = {
            "username" : "studenttest2",
            "email" : "studenttest2@e.ntu.edu.sg",
            "password" : "123456",
        }

        self.student2 = get_user_model().objects.create_user(**self.credentials2)

        """ Create a course """
        self.course1 = Course.objects.create(
            title = "CZ3006",
            description = "Computer Networks"
        )

        """ Create a question """
        self.question1 = Question.objects.create(
            course = self.course1,
            owner = self.student1,
            title = "How to config IP",
            content = "config IP using DHCP"
        )

        """ Create a reply """
        self.reply1 = Reply.objects.create(
            creator = self.student2,
            question = self.question1,
            content = "just read through lecture notes" 
        )

        """Define url"""
        self.login_url = reverse("login")
        self.register_url = reverse("register")
        self.course_url = reverse("course", args={"slug": self.course1.slug})
        self.question_url = reverse("question", args={"slug": self.question1.slug})
        self.new_question_url = reverse("new_question")


    def test_user_login_with_no_data(self):
        """test user login with no input is not successful"""
        res = self.client.login(username="", password="")
        self.assertEqual(res, False)


    def test_user_login_with_correct_data(self):
        """test user login with correct username/passoword is successful"""
        res=self.client.login(username="studenttest1", password="123456")
        self.assertEqual(res, True)

    def test_user_login_with_wrong_data(self):
        """ test user login with incorect username/password is not successful"""
        res = self.client.login(username= "testuser@mail.com", password= "wrong-password")
        self.assertEqual(res, False)

    def test_get_student_withQuery(self):
        """ test get student data with id is successful"""
        res = self.client.get(self.register_url, email= self.student1.email)
        self.assertEqual(res.status_code, 200)


    def test_post_question(self):
        """ Create a question """

        user = authenticate(**self.credentials1)
        data = {"course": self.course1, "owner": self.student1, "title": "What is life?", "content": "I like chicken."}

        res = self.client.post(self.new_question_url , data = data , format = 'json',follow=True)
        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        self.delete_url = reverse("delete_question",args={"slug":self.question1.slug})
        res = self.client.get(self.delete_url,follow=True)
        self.assertEqual(res.status_code, 200)
    
    def test_post_question_null_data(self):
        """ Create a question """

        user = authenticate(**self.credentials1)

        res = self.client.post(self.new_question_url)
        self.assertEqual(res.status_code, 302)
