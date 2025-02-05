from django.test import TestCase, RequestFactory
from django.template import Template, Context
from django.template.loader import get_template
from tests_utils.templates import compile_template
from stack_it.models import Page
from django.contrib.auth.models import AnonymousUser, User
from faker import Faker
from ddt import ddt, data


@ddt
class PageLinkTest(TestCase):
    value_template = Template(
        "{% load content_tags %}{% pagelink page 'value' 'key' 'Hello World!' %}")
    meta_template = Template(
        "{% load content_tags %}{% pagelink page 'meta' 'key' 'Hello World!' %}")

    @classmethod
    def setUpTestData(cls):
        fake = Faker()
        cls.lambda_user = User.objects.create_user(username=fake.name(),
                                                   email=fake.email(),
                                                   password=fake.name())

        cls.staff_user = User.objects.create_user(username=fake.name(),
                                                  email=fake.email(),
                                                  password=fake.name(),
                                                  is_staff=True)
        cls.request_factory = RequestFactory()
        cls.connected_request = cls.request_factory.get(path='/')
        cls.connected_request.user = cls.lambda_user
        cls.staff_request = cls.request_factory.get(path='/')
        cls.staff_request.user = cls.staff_user
        cls.anonymous_request = cls.request_factory.get(path='/')
        cls.anonymous_request.user = AnonymousUser()

    @data(
        ('connected_request', compile_template('HelloWorld')),
        ('staff_request', get_template('stack_it/editable.html')),
        ('anonymous_request', compile_template('HelloWorld')),
    )
    def test_basic_value_creation(self, data):
        request_string, output = data
        page = Page.objects.create(title="My Title")
        rendered = self.value_template.render(Context({
            'page': page,
            'request': getattr(self, request_string)
        }))
        self.assertEqual(page.contents.count(), 1)
        self.assertIn('key', page.values.keys(), page.metas)
        self.assertIn('key', page.values.keys(), page.metas)
        #TODO Check content

    @data(
        ('connected_request', compile_template('HelloWorld')),
        ('staff_request', get_template('stack_it/editable.html')),
        ('anonymous_request', compile_template('HelloWorld')),
    )
    def test_basic_content_type_update(self, data):
        request_string, output = data
        page = Page.objects.create(title="My Title")
        self.meta_template.render(Context({
            'page': page,
            'request': self.anonymous_request
        }))
        rendered = self.value_template.render(Context({
            'page': page,
            'request': getattr(self, request_string)
        }))
        self.assertEqual(page.contents.count(), 1)
        self.assertIn('key', page.values.keys(), page.metas)
        #TODO Check content

    @data(
        ('connected_request', compile_template('OKAY')),
        ('staff_request', get_template('stack_it/editable.html')),
        ('anonymous_request', compile_template('OKAY')),
    )
    def test_content_modification(self, data):
        request_string, output = data
        page = Page.objects.create(title="My Title")
        self.meta_template.render(Context({
            'page': page,
            'request': self.anonymous_request
        }))
        self.value_template.render(Context({
            'page': page,
            'request': getattr(self, request_string)
        }))
        page.values.get('key').value = "OKAY"
        page.values.get('key').save()
        rendered = self.value_template.render(Context({
            'page': page,
            'request': getattr(self, request_string)
        }))
        #TODO Check content