from db import schema
from core.utils import *

seedData = []
testAccount = schema.user.User(username= 'aong', password= calculateHashCodeForString('1234'))
seedData.append(testAccount)
