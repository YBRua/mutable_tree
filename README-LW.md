# 对通用部分的修改
- 修改读取language.so路径
- 修正更新node的逻辑
  - 存在的问题: visitor中generic_visit, 一边遍历node.children, 一边修改node.children, 违反了list操作原则
  - 示例: 同类变量拆分
    ```java
    // before:
    int i,j;
    int a = 10, b = 11;
    // after
    int i;
    int j;
    int a = 10, b = 11;
    ```
    children开始是2个, int i; int j; 插入后, children变成3个了, 遍历时忽略了最后一个statement

  - update更新放最后的问题是: update需要child_attr,也不太行. 
  ```Java
  // before:
  int i,j;
  int a = 10, b = 11;
  // 期望是:
  int i;
  int j;
  int a=10;
  int b=11;
  ```
   update更新放最后的问题是: update需要child_attr, a b 被拆开后, replace_child_at 仍然是从1开始插入, 结果就是把j覆盖了.
  ```java
  int i;
  int a=10;
  int b=11;
  ```
  - 最后修改为: 构造一个new_children, 直接将更新/删除/插入等操作在这里list上做. 全部做完后, 用new_children替换children

- 使用`inflection`库处理命名风格

## Variable Naming Style Transformers
- RopGen 是确认从一种风格转到另一种风格
- 而我们的方法应该不会提前假设方法中的命名风格是统一的, 我们更关注**转换**这件事
- 所以目前使用python `inflection` 库提供的api, 对**任意命名**风格的变量转换成**某一种**风格的变量

```
pip install inflection
```

- 由于一些特殊关键词的存在, inflection处理的结果可能不完美的(当然RopGen也是寄), e.g.

| Var | PascalCase | snake_case | underscore_case |
| --- | --- | --- | --- |
| iOSVersion | IOSVersion | i_os_version | _i_os_version |
| IOError | -  | io_error | _io_error |

## Split/Merge Same Type Variable
- ignore LocalVariableDeclaration in ForStatement. e.g.
```
// case1: 无法切分
for (int i=0,j=0;;){}

// case2: 不能轻易合并, 否则可能会改变变量的作用域
for (int i=0;;) {}
for (int i=0;;) {}
```

- SplitVarWithSameTypeVisitor 和 MergeVarWithSameTypeVisitor 不是严格的逆运算
  - ```
    // before
    int a, b=1, c;
    // after
    int a;
    int b=1;
    int c;
    ```
    SplitVarWithSameTypeVisitor 设计原因: 符合切分定义, 简单
  - ```
    // before
    int a;
    int b=1;
    int c;
    double d1;
    double d2 = b;
    // after
    int a, c;
    int b=1
    double d1;
    double d2 = b;
    ```
    MergeVarWithSameTypeVisitor 设计原因: 变量声明时如果初始化, 初始化的值可能来自于某行代码, 因此这种有初始化的声明不适合移动到别的位置去合并声明

## Variable definition position
- 忽略 LocalVariableDeclaration 中的 InitializingDeclarator
- 定义放到程序开头: 将 LocalVariableDeclaration 放到BlockStatement中前面
- 定义放到变量使用前: 检查 LocalVariableDeclaration 和当前 BlockStatement 中的每个 statement, 将声明放到第一次使用前

## 

