from db import schema
from core import utils

seedData = []
seeds = [schema.user.User(username='aong', password=utils.calculateHashCodeForString('1234')),
         schema.manager.Manager(username='aong', email='i@aong.cn', password=utils.calculateHashCodeForString('1234'))]

for i in seeds:
    seedData.append(i)
