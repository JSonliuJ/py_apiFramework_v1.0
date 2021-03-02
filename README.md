python 20201205

## 框架
### 1. common 业务逻辑层

#### 1.1 `excel`

#### 1.2` myslq`

#### 1.3 `log`

#### 1.4` email`

#### 1.5` base_api`

#### 1.6` config`

- py文件：灵活，只有Python代码能用
- ini文件：读取比较复杂，以前用得比较多，有很多历史遗留项目主要使用这种方式
- yaml文件：通用，读取简洁智能

#### 1.7 `Regex`

1. `+`  一次或多次(>=1)
2. `?` 0次或1次(0,1)

3. `*` 0次或多次 (>=0)
4. `\d` 任意数字
5. `\w` 数字、字母、下划线
6. `{m}` 匹配m次
7. `{m,} `匹配>=m次
8. `{m,n}` 匹配m到n次

9. `[]` 匹配一组字符中任意一个
10. `^`用于匹配字符串的开始，即行首。
11. `$`用于匹配字符串的末尾

### 2. conf配置数据层

**`项目地址、数据库连接参数、logger级别`**

#### 2.1 `.yaml`

#### 2.2 `.ini`

#### 2.3 `.conf`

### 3. testdata数据管理层

**`excel数据，列表保存`**

  - case.xlsx

动态数据：注册功能中手机号不能提前知道，需要通过程序去动态生成，然后在数据库当中核对



### 4. testcase 测试逻辑层

**`各个模块的测试用例方法，便于管理`**

#### 4.1` 注册`

1. 手机号码已存在
   - 不能手工写在excel
   - 从数据库中找出一条
   - 替换excel中的exist_phone字段
2. 注册成功
   - 不能手写在excel
   - 动态生成
   - 

#### 4.2`登录`

#### 4.3 `充值`

![1607268152565](C:\Users\liujie666\AppData\Roaming\Typora\typora-user-images\1607268152565.png)

 一、前置条件登录的实现方式：

1. setUp ，self.req.visit() 访问登录接口，res得到token
2. 第一条用例放已经注册可以登录成功的手机号用户，然后获取token值

二、 登录，得到充值需要的的token和member_id

#### 4.4` 提现`

#### 4.5 `添加项目`

#### 4.6 `审核项目`

#### 4.7`投资`

![1607786417264](C:\Users\liujie666\AppData\Roaming\Typora\typora-user-images\1607786417264.png)

1. 前置条件：
   - 登录
   - 标审核已通过
   - 标的状态为竞标中，要从数据库当中查找出一个
   - `select * from load where status=2;`
2. 验证
   - 接口返回数据是否正确
   - 余额是否正确
3. 业务流程
   - `可以投资自己发布的项目`
   - 当前项目必须是`竞标中状态`
   - 投资金额必须是`能被100整除的正整数`，
   - 投资金额必须`小于项目的剩余可投金额`，否则投资不成功。
   - 投资成功后，将生成一条投资记录保存到`invest表`
   - 投资用户`可用余额减少`，并新增一条流水记录保存到`financeLog` 表。
   - 当然可投金额为0时，会自动为该项目的所有的投资记录生成对应的回款计划列表。

#### 4.8 `获取项目`

### 5. result输出层

4.1 log输出

4.2 html_report 输出

### 6. run.py

**`代码入口，收集测试用例，生成测试报告`**

### 7. middleware中间件层

#### 7.1 `路径 file_path`

#### 7.2 `yaml_data `

#### 7.3` helper`

#### 7.4 `login、token、`

### 8. 总结

8.1 接口参数更多：`测试用例设计更多`

8.2 动态参数更多：`#xxx#` 更多----通过正则表达式一次替换

```
def replace_label(target):
    re_pattern = re.compile(r'#(\.*?)#')
    while re.findall(re_pattern,target):
        key = re.search(re_pattern,target).group(1)
        new_str = re.sub(re_pattern,str(getattr(Context,key)),target,1)
    return new_str
​```
```

8.3 接口依赖更多

- 把依赖接口写到excel
- 写到setUp里
- Context里设置property属性

8.4 动态参数什么时候使用？

- 先用静态数据，静态数据解决不了，或者扩展性不强

8.5 如何确定测试用例的预期结果

- 接口文档
- 开发确认









