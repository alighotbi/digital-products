import random
import string

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail

# Create a Manager for the custom user, for createuser and createsuperuser
class UserManager(BaseUserManager):
    use_in_migrations = True
    

    def _generate_unique_username(self, base_username):
        """
        Generate a unique username based on the given base_username.a.
        """
        while User.objects.filter(username=base_username).exists():
            base_username += str(random.randint(10, 99))
        return base_username
    
    

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        """
        Create and return a regular user.
        """
        if not email and not phone_number:
            raise ValueError("Either email or phone number must be provided.")
        
        if not username:
            if email:
                username = email.split('@', 1)[0]
            elif phone_number:
                username = random.choice(string.ascii_lowercase) + str(phone_number)[-7:]
            username = self._generate_unique_username(username)
            

        email = self.normalize_email(email) if email else None
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        now = timezone.now()

        user = self.model(
            username=username,
            phone_number=phone_number,
            email=email,
            is_active=True,
            date_joined=now,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            raise ValueError("Password must be set for a user.")

        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields["is_staff"]:
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, phone_number, email, password, **extra_fields)
            

username_regex = RegexValidator(
    regex= r'^[a-zA-Z0-9_]+$',
    message="Username must be alphanumeric or contain underscores.")
phone_number_regex = RegexValidator(
    regex=r'^\+?[1-9]\d{1,14}$',  # E.164 format for international numbers
    message="Phone number must be in international format (e.g., +123456789)."
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=20, unique=True,
                                help_text= 'Required*, 20 max characters, letters, letter, numbers and symbols',
                                validators=[username_regex])
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField('email address', unique=True, blank=True, null=True)
    phone_number = models.BigIntegerField('mobile number', validators=[phone_number_regex], unique=True, null=True, blank=True)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='pass')
    is_active = models.BooleanField('active', default=True,
                                    help_text='pass')
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    last_seen = models.DateTimeField('last seen date', null=True)
    
    USERNAME_FIELD = 'username' # Specifies the unique field for login
    REQUIRED_FIELDS = ['email', 'phone_number']   # Fields required when creating a user via createsuperuser
    # user_device = models.ManyToManyField('Device', related_name='user_device', blank=True)
    
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        






class UserProfile(models.Model):
    """The UserProfile class is a Django model that extends the functionality of the User model
    by adding additional fields and relationships"""
    
    MALE= 1
    FEMALE = 2
    PREFER_NOT_TO_SAY = 3
    GENDER_TYPES =(
        (MALE, 'male'),
        (FEMALE, 'female'),
        (PREFER_NOT_TO_SAY, 'prefer not to say')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField('Nickname' , max_length=50, blank=True)
    avatar = models.ImageField('avatar', null=True, blank=True)
    birthdate = models.DateField('birthday', blank=True, null=True)
    gender =models.SmallIntegerField('gender', choices=GENDER_TYPES, help_text=('Optional'), blank=True)
    province = models.ForeignKey(verbose_name=('province'), to='Province', null=True, blank=True, on_delete=models.SET_NULL)
    
    """OR WE CAN USE THE DEFAULT USER MODEL AND ADD THE EMAIL AND PHONE IN THE USER PROFILE!"""
    # email = models.EmailField('email_address', blank=True)
    # phone_number = models.BigIntegerField('mobile number', validators=phone_number_regex, unique=True, null=True, blank=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'user profiles'
    
    def __str__(self) -> str:
        return self.nick_name
        
        
        

class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )
    # many users can have one device because its a manyToOne relation
    # related_name is for better readability and conflict_free.
    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField('Device UUID', null=True)
    last_login = models.DateTimeField('last login date', null=True)
    device_type = models.SmallIntegerField(choices=DEVICE_TYPE_CHOICES, default=WEB)
    device_model = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'user_devices'
        verbose_name = 'device'
        verbose_name_plural = 'devices'
        unique_together = ('user', 'device_uuid')
        

IRAN_CITIES = [
    ('tehran', 'Tehran'),
    ('mashhad', 'Mashhad'),
    ('isfahan', 'Isfahan'),
    ('shiraz', 'Shiraz'),
    ('tabriz', 'Tabriz'),
    ('karaj', 'Karaj'),
    ('qom', 'Qom'),
    ('ahvaz', 'Ahvaz'),
    ('kermanshah', 'Kermanshah'),
    ('rasht', 'Rasht'),
    ('hamedan', 'Hamedan'),
    ('ardabil', 'Ardabil'),
    ('kerman', 'Kerman'),
    ('yazd', 'Yazd'),
    ('zahedan', 'Zahedan'),
    ('urmia', 'Urmia'),
    ('arak', 'Arak'),
    ('sari', 'Sari'),
    ('bandar_abbas', 'Bandar Abbas'),
    ('bushehr', 'Bushehr'),
]



class Province(models.Model):
    name = models.CharField('city', choices=IRAN_CITIES, max_length=30, default='tehran')
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
    
    