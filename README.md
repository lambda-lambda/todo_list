# todo_list
自制web框架实现todo list 

![img](
        https://github.com/lambda-lambda/todo_list/blob/master/todo_list.gif
      ) 
      

# 实现的主要功能

1. 用户的注册与登录
2. todo 的增删改查
3. todo 与用户关联

# 如何运行
```
bash
git clone git@github.com:yuancjun/todoist.git
cd todoist
# 出于安全目的, 使用者应该 修改 config.py 的 salt 变量
# salt 变量的目的是给用户密码加盐, 防止彩虹表的暴力破解
bash run.sh
```

# 项目架构分析
## model 数据层
1. 使用 JSON 文件存储
2. 实现 ORM 基类 Model
3. 提供 CRUD 的接口

## controller 逻辑处理层
1. 根据 HTTP 的 path 分发请求
2. request 与 response 两个模块抽象了 请求 与 响应

## view 视图层
1. static file 比如 css, js, image
2. html 比如用户的 登录 与 注册页面
3. 实现变量替换 template 功能

由于整个应用使用 AJAX 技术传递数据
所以 view 层 JS 的代码逻辑 又分为 api, view, event 三部分

1. api 层负责与 后端 api 传递数据
2. view 层负责更新页面内容
3. event 层负责绑定事件和回调

## web 安全验证
### 限制路由访问
1. login_required 只有已登录的用户可以访问
2. same_user_required 只有 todo 关联的 user 才可以访问

### cookie 安全
1. HttpOnly 避免 cookie 被窃取
2. SameSite=Strict 避免 CSRF 攻击
3. Max-Age 客户端 cookie 自动过期
