from db import schema
from core import utils

seedData = []
seeds = [schema.user.User(username='aong',
                          password=utils.calculateHashCodeForString('1234'),
                          email='i@aong.cn',
                          active=1,
                          createtime=utils.getCurrentTime(),
                          uuid=utils.generateGUID()),
         schema.user.User(username='ruby',
                                   password=utils.calculateHashCodeForString('12345'),
                                   email='ruby@aong.cn',
                                   active=1,
                                   createtime=utils.getCurrentTime(),
                                   uuid=utils.generateGUID()),
         schema.user.User(username='userA',
                                   password=utils.calculateHashCodeForString('12345'),
                                   email='a@example.cn',
                                   active=1,
                                   createtime=utils.getCurrentTime(),
                                   uuid=utils.generateGUID()),
         schema.user.User(username='userB',
                                   password=utils.calculateHashCodeForString('12345'),
                                   email='b@example.cn',
                                   active=1,
                                   createtime=utils.getCurrentTime(),
                                   uuid=utils.generateGUID()),
         schema.manager.Manager(username='aong',
                                email='i@aong.cn',
                                password=utils.calculateHashCodeForString('1234'),
                                uuid=utils.generateGUID())
         ]

for i in seeds:
    seedData.append(i)
