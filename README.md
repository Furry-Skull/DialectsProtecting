# DialectsProtecting 方言保护网站

## 注意事项

建议统一使用Visual Studio，因为上传的代码部分有VS的解决方案文件，打开大概会比较方便

## 文件结构

没有的文件夹可以自行创建（空文件夹似乎会被github屏蔽）

| 文件夹路径                                           | 文件类型       |
| ---------------------------------------------------- | -------------- |
| DialectsProtecting/DialectsProtecting/templates      | HTML模板文件   |
| DialectsProtecting/DialectsProtecting/static/content | css文件        |
| DialectsProtecting/DialectsProtecting/static/fonts   | 网页字体       |
| DialectsProtecting/DialectsProtecting/static/scripts | javascript文件 |

## 分工

| 事务                                       | 分工    | 使用的语言        |
| ------------------------------------------ | ------- | ----------------- |
| 前端：网页代码和css                        | SJH     | html css          |
| 前端：UI设计和交互设计（可能和python对接） | XH      | python javascript |
| 后端：数据库搭建                           | WGY     | SQL               |
| 后端：后端逻辑和各模块对接                 | ZQC WRY | python javascript |
| 资料收集                                   | LCX     | /                 |

## 需求

### 后端：数据库搭建



```python
#需要提供一个python类Database，以下为需要有的函数原型（私有函数和变量需要在函数名/变量名加__，构造函数是__init__）

class Database:
    def login(userName, password)  #返回是否登录成功true/false
    def register(userName, password)   #注册一个账号并返回是否注册成功
```
