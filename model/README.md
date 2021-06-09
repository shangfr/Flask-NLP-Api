## 不同模式下对数据库的操作方法

**python: sqlite3、sqlalchemy、qlalchemy.orm**

### 1 sqlite3 模式-创建表-插入数据

#### 1.1 创建数据库(建立连接-引擎)

```
import sqlite3
conn = sqlite3.connect('nlp.db')
cur = conn.cursor()
```

#### 1.2 创建表

```
cur.execute(
    '''CREATE TABLE user_dict (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, freq INT default 10,tag TEXT)''')

```

#### 1.3 插入数据

```
cur.execute('''INSERT INTO user_dict (word, freq, tag) VALUES('云计算', 5, 'n')''')
cur.execute('''INSERT INTO user_dict (word, freq) VALUES('中国梦', 10)''')
cur.execute('''INSERT INTO user_dict (word) VALUES('新冠病毒')''')
```

#### 1.4 提交、关闭连接

```
conn.commit()
conn.close()
```

### 2 sqlalchemy 模式-创建表-插入数据

#### 2.1 sql 语句创建数据库、创建表、插入数据、提交、自动关闭连接

```
from sqlalchemy import text
engine = create_engine('sqlite:///nlp.db')

with engine.connect() as conn:
    conn.execute(
        text("CREATE TABLE user_dict (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, freq INT default 10,tag TEXT)")
    )

    conn.execute(
        text("INSERT INTO user_dict (word, freq, tag) VALUES (:word, :freq, :tag)"),
        [{"word": '云计算', "freq": 5, "tag": 'n'},
         {"word": '中国梦', "freq": 10,"tag": None},
         {"word": '新冠病毒', "freq": 10, "tag": None}]
    )

# 注：此模式下，插入数据的字段不能有缺失。

```

#### 2.2 orm 创建数据库、创建表、插入数据、提交、自动关闭连接

##### 2.2.1 创建数据库、声明 ORM 映射类的基类

```
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base


engine = create_engine('sqlite:///nlp.db', echo=True)
# 声明ORM映射类的基类
Base = declarative_base()

# 构造UserDict类
class UserDict(Base):
    __tablename__ = 'user_dict'

    id = Column(Integer, primary_key=True)
    word = Column(String(30))
    freq = Column(Integer,default=10)
    tag = Column(String)

    def __repr__(self):
        return f"UserDict(id={self.id!r}, word={self.word!r}, tag={self.tag!r})"

UserDict.__table__
#user_dict = UserDict.__table__
```

##### 2.2.2 向数据库发送 DDL、创建表

```
Base.metadata.create_all(engine)
```

##### 2.2.3 插入数据

```
# 使用Session插入数据
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
sessionobj = Session()

word01 = UserDict(word="云计算", freq=10,tag='n')
word02 = UserDict(word="中国梦")
#sessionobj.add(word01)
sessionobj.add_all([word01,word02])
sessionobj.commit()
```

### 3 通过表反射，连接各种模式下创建的数据表，使用 sqlalchemy insert 插入数据

```
# 表反射
from sqlalchemy import MetaData
metadata = MetaData()
user_dict = Table("user_dict", metadata, autoload_with=engine)

```

```
# 使用sqlalchemy insert插入数据
from sqlalchemy import insert
with engine.connect() as conn:
     result = conn.execute(
         insert(user_dict),
         [
             {"word": '云计算2', "freq": 5, "tag": 'n'},
             {"word": '中国梦2', "freq": 10,"tag": None}
         ]
     )

```
