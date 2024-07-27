from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
#from django.db.models.fields.related import ForeinKey,OneToOneField





# Create your models here.
class UserManager(BaseUserManager): #usermanager manje tu customize database banavtoys jaasa ki hyat tula swataun create karava lagtay entry fields email,username,first name and all whereas User ha django by default support karta tyat already entry fields present aastat 
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have an username")
        
        user=self.model(
            email=self.normalize_email(email),  #email id uppercase takli tar lower madhe convert karnaar
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password) #password la hash karnaar basically encode karnaar
        user.save(using=self._db)    #je settimgs madhe default database aahe toh ghenar configurations kelet tyala reference gheun save honaar data 
        return user

    def create_superuser(self,first_name,last_name,username,email,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
	    password=password,	
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user 

class User(AbstractBaseUser):   #this abstractbaseuser are used for modifying the customized models and also include the authentication which is supported by django .  
    VENDOR=1
    CUSTOMER=2

    ROLE_CHOICE=(
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer'),
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_no=models.CharField(max_length=12,blank=True,null=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    #required field
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'  #hyat kadi pan django username je aasta te bydefault username mahnun gheto pan aaplya la email paije te set kelay
    REQUIRED_FIELDS=['username','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):   #heh permission vale fakta admin ani super admin jeva active aasnar teva true aasnar baki normal user sathi false
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role    


    

class userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)  #hyat na one to one field vaparli aahe karanki one user can have only one user profile aani tyala varcha User chya table la link kelay on_delete manje profile delete jhala tar user che sagle details delete hoyayla paije,blank ani null aasach lilay kahi error nahi dila paije mahnun     
    profile_picture=models.ImageField(upload_to='users/profile_picures',blank=True,null=True)
    cover_photo=models.ImageField(upload_to='users/cover_photos',blank=True,null=True)
    address_line_1=models.CharField(max_length=100,blank=True,null=True)
    address_line_2=models.CharField(max_length=100,blank=True,null=True)
    country=models.CharField(max_length=15,blank=True,null=True)
    state=models.CharField(max_length=15,blank=True,null=True)
    city=models.CharField(max_length=15,blank=True,null=True)
    pin_code=models.CharField(max_length=6,blank=True,null=True)
    latiude=models.CharField(max_length=20,blank=True,null=True)
    longitude=models.CharField(max_length=20,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email  #heh User chya mail la call kelay

