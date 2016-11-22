from peewee import *

# 创建数据库实例
db = SqliteDatabase('base.db')


# 建议自己的项目使用一个新的基类，Model是peewee的基类
class MyBaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def getOne(cls, *query, **kwargs):
        # 为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None


# 示范一个表
class User(MyBaseModel):
    name = CharField(unique=True)
    password = CharField()
    group = CharField(default='admin')
    value = FloatField(default=0.0)


# 建表，仅需创建一次
User.create_table()

# 新增行
User.create(name=name, password=password)

# 查询一行
user = User.getOne(User.name = 'MyGod')
print(user.password)

# 更新
user.value += 1
user.save()

# 删除
user.delete_instances()

# 查询多行
usersInGroup = User.select().where(User.group == 'admin')
usersStartsWithA = User.select().where(User.name ** 'A%')  # 不区分大小写的like查询
usersWithOrder = User.select().where(User.group == 'admin').order_by(User.name.desc())  # 按姓名倒序排序

# 统计admin用户组所有用户的value总和
total = User.select(fn.Sum(User.value).alias('totalvalue')).where(User.group == 'admin')

# 更新多个(将a打头的用户的value全部更新为1)
User.update(value=1).where(User.name ** 'A%').execute()