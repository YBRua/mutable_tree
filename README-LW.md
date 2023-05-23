# 对通用部分的修改
- 修改读取language.so路径
- visitor中generic_visit, 当node是NodeList时, 为了避免一边遍历node.children, 一边修改node.children, 增加了new_node_list来记录未修改的child和修改后的child 
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
