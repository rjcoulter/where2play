from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from .views import convertTime
from .views import HomePageView
from .views import add_unique_ids_field
from .models import Facility
from .models import Court
from .models import Our_User
from .models import Time_Slot
from .models import User
from home.sql import execute_sql
from home.sql import execute_sql_return
from .forms import SignUpForm


class ConvertTimeTests(TestCase):

    def test_convert_time_three_digits(self):
        time = '400'
        new_time = convertTime(time)
        self.assertEquals(str(new_time), '(4, 0)')

    def test_convert_time_four_digits(self):
        time = '1200'
        new_time = convertTime(time)
        self.assertEquals(str(new_time), '(12, 0)')

    def test_convert_time_invalid_input(self):
        input = 'django'
        with self.assertRaises(ValueError):
            convertTime(input)


class SignInTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'user',
            'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_signin_active(self):
        # send login data
        response = self.client.post('/signin/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)


class LogOutTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'user',
            'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_logout_user(self):
        response = self.client.post('/logout/', self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


class HomePageViewTest(TestCase):

    def test_homepage_access(self):
        c = Client()
        response = c.get('/')
        self.assertEquals(response.status_code, 200)

    def test_homepage_function_access(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')
        response = HomePageView(request)
        self.assertEquals(200, response.status_code)
 
    # Nathan Park 1
    def test_do_not_include_ampsand(self):
        class Gym:
            def __init__(self, F_Name):
                self.F_Name = F_Name
                self.name_no_space = ""
        example_gym = [Gym("Get & Rid & of & Ampersands &")]
        example_gym_2 = [Gym("& & hello & & world")]
        example_gym_3 = [Gym("No & Ampersands")]
        unique_id = "GetRidofAmpersands"
        unique_id_2 = "helloworld"
        unique_id_3 = "NoAmpersands"
        gym, gym2, gym3 = add_unique_ids_field(
            example_gym, example_gym_2, example_gym_3)
        self.assertEquals(gym[0].name_no_space, unique_id)
        self.assertEquals(gym2[0].name_no_space, unique_id_2)
        self.assertEquals(gym3[0].name_no_space, unique_id_3)

    # Nathan Park 2
    def test_remove_word_with_comma(self):
        class Gym:
            def __init__(self, F_Name):
                self.F_Name = F_Name
                self.name_no_space = ""
        example_gym = [Gym("Get Rid of Last Wor'd")]
        example_gym_2 = [Gym("h'e'l'l'o world")]
        example_gym_3 = [Gym("No ' Commas")]
        unique_id = "GetRidofLast"
        unique_id_2 = "world"
        unique_id_3 = "NoCommas"
        gym, gym2, gym3 = add_unique_ids_field(
            example_gym, example_gym_2, example_gym_3)
        self.assertEquals(gym[0].name_no_space, unique_id)
        self.assertEquals(gym2[0].name_no_space, unique_id_2)
        self.assertEquals(gym3[0].name_no_space, unique_id_3)
        
    def test_remove_ampersand_for_mixed_types(self):
        class Field:
            def __init__(self, F_Name):
                self.F_Name=F_Name
                self.F_type='Field'
                self.name_no_space = ""
        class Gym:
            def __init__(self, F_Name):
                self.F_Name=F_Name
                self.F_type='Gym'
                self.name_no_space = ""
        class Other:
            def __init__(self, F_Name):
                self.F_Name=F_Name
                self.F_type='Other Facility'
                self.name_no_space = ""
        f=[Field("& Field & 1"), Field("& & & Field 2")]
        g=[Gym("& some gym")]
        o=[Other("Other & Facility 1"), Other("Other & Facility 2")]
        field, gym, other=add_unique_ids_field(f, g, o)
        self.assertEquals(field[1].name_no_space, "Field2")
        self.assertEquals(gym[0].name_no_space, "somegym")
        self.assertEquals(other[1].name_no_space, "OtherFacility2")
    
    def test_remove_apostrophe_for_mixed_types(self):
        class Field:
            def __init__(self, F_Name):
                self.F_Name=F_Name
                self.F_type='Field'
                self.name_no_space = ""
        class Gym:
            def __init__(self, F_Name):
                self.F_Name=F_Name
                self.F_type='Gym'
                self.name_no_space = ""
        class Other:
            def __init__(self, F_Name):
                self.F_Name=F_Name
                self.F_type='Other Facility'
                self.name_no_space = ""
        f=[Field("Field 1 don't"), Field("ok' Field 2")]
        g=[Gym("it's some gym")]
        o=[Other("Other 's Facility 1"), Other("Other Facility 2 'k")]
        field, gym, other=add_unique_ids_field(f, g, o)
        self.assertEquals(field[1].name_no_space, "Field2")
        self.assertEquals(gym[0].name_no_space, "somegym")
        self.assertEquals(other[1].name_no_space, "OtherFacility2")


class AboutPageViewTest(TestCase):

    def test_aboutpage_access(self):
        c = Client()
        response = c.get('/about/')
        self.assertEquals(response.status_code, 200)


class ContactPageViewTests(TestCase):

    def test_contactpage_access(self):
        c = Client()
        response = c.get('/contact/')
        self.assertEquals(response.status_code, 200)


class LoginViewTests(TestCase):

    def test_signin_access(self):
        c = Client()
        response = c.get('/signin/')
        self.assertEquals(response.status_code, 200)


class SignUpViewTests(TestCase):

    def test_signup_access(self):
        c = Client()
        response = c.get('/signup/')
        self.assertEquals(response.status_code, 200)


class SchedulerViewTests(TestCase):

    def test_scheduler_access(self):
        c = Client()
        response = c.get('/scheduler/')
        self.assertEquals(response.status_code, 200)


class LogOutViewTests(TestCase):

    def test_logout_access(self):
        c = Client()
        response = c.get('/logout/')
        self.assertEquals(response.status_code, 302)


class FacilityTests(TestCase):

    def test_string_representation(self):
        facility = Facility(F_Name='AFC')
        self.assertEquals(str(facility), facility.F_Name)


class CourtTests(TestCase):

    def test_court_creation(self):
        court = Court()
        self.assertEquals(court.current_count, 0)

    def test_string_representation(self):
        court = Court(C_Name='court')
        self.assertEquals(str(court), court.C_Name)


class OurUserTests(TestCase):

    def test_user_creation(self):
        user = Our_User()
        self.assertEquals(user.user_type, 0)


class TimeSlotTests(TestCase):

    def test_time_slot_creation(self):
        time_slot = Time_Slot()
        self.assertEquals(time_slot.available, True)
        self.assertEquals(time_slot.signup_count, 0)

    def check_empty_when_reserved(self):
        slots = execute_sql_return(
            'SELECT * FROM home.home_time_slot WHERE available=false')
        for slot in slots:
            if slot[2] != 0:
                self.assertTrue(False)
        self.assertTrue(True)

    def check_available_when_counted(self):
        slots = execute_sql_return(
            'SELECT * FROM home.home_time_slot WHERE signup_count>0')
        for slot in slots:
            if slot[1] == False:
                self.assertTrue(False)
        self.assertTrue(True)
        
class User_Form_Tests(TestCase):

    def test_user_form_success(self):
        form=SignUpForm({'email': "jh7zr@virginia.edu"})
        if form['email']=="jh7zr@virginia.edu":
            self.assertTrue(True)
      
    def test_user_form_error(self):
        form=SignUpForm({'emai':'a@b.com'})
        if form['email']=="jh7zr@virginia.edu":
            self.assertFalse(True)
        else:
            self.assertFalse(False)
        self.assertFalse(form.is_valid())

    def test_user_form_username_success(self):
        form=SignUpForm({'username': "as3cp"})
        if form['username']=="as3cp":
            self.assertTrue(True)   

    def test_user_form_username_error(self):
        form=SignUpForm({'username':'as3cp'})
        if form['username']=="aladin":
            self.assertFalse(True)
        else:
            self.assertFalse(False)
        self.assertFalse(form.is_valid()) 
