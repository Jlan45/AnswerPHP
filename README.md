# AnswerPHP
一个帮助你PHP反序列化的python工具

终于是写的差不多了，目前先来简单介绍一下项目的整体概况吧

## 食用方法

测试版本啦，没有输入的啦，直接在main.py里面放入想分析的php文件即可

### config.py

```
EVIL_FUNCTION_PHP=["system","这里写目标危险函数"]
START_METHODS_PHP=["__destruct","__wakeup","这里写整个反序列化链子触法函数"]
FUNC_TO_CALL=[[["函数调用列表"],"对应的魔术方法"]]#这个部分是给以后的代码用的，现在先不用管

```

## 数据结构

这个是解析后的class

```json
[
  {
    "name": "A",
    "methods": [
      {
        "name": "__construct",
        "modifiers": "",
        "funcs": [],
        "methods": [],
        "params": []
      },
      {
        "name": "__destruct",
        "modifiers": "",
        "funcs": [],
        "methods": [
          {
            "name": "action",
            "variable": [
              "$this",
              "target"
            ]
          }
        ],
        "params": []
      }
    ],
    "variables": [
      {
        "name": "$target",
        "modifiers": [
          "public"
        ],
        "initial": null
      }
    ],
    "calls": null,
    "evils": []
  },
  {
    "name": "B",
    "methods": [
      {
        "name": "action",
        "modifiers": "",
        "funcs": [],
        "methods": [],
        "params": []
      }
    ],
    "variables": [],
    "calls": null,
    "evils": []
  },
  {
    "name": "C",
    "methods": [
      {
        "name": "action",
        "modifiers": "",
        "funcs": [
          {
            "name": "eval",
            "params": [
              "test",
              "$this"
            ]
          }
        ],
        "methods": [],
        "params": []
      }
    ],
    "variables": [
      {
        "name": "$test",
        "modifiers": [
          "public"
        ],
        "initial": null
      }
    ],
    "calls": null,
    "evils": [
      "action"
    ]
  }
]
```

这个是chains的结构

```json
[
  [['A', '__destruct'], ['C', 'action']],
  [['类A', '方法A'], ['类B', '方法B']]
]
```

## 实现过程

1. 先解析class处理成上面的格式
2. 对于每个类都遍历获取到START_METHODS_PHP，这部分写在config中，作为反序列化初始链，每个都存入到chains属性中
3. 只要chains属性不为空就遍历，每次pop出一个链子，然后按如下方式分析
   - 首先分析这个对应的方法中是否有危险方法，有的话直接把当前的链子压入final_chains
   - 然后遍历这个方法中的所有methodcall，看能不能走到别的类的方法中去，如果可以就给链子添加新节点并压入final_chains
   - 哦对了需要先分析chains是否存在多次loop，有的话直接弹掉链子（这部分还没实现）
4. 直到chains属性为空就可以打印出来最后分析出的chains了

## 备注

目前就写了这么多，后面会一点点补充功能的，希望师傅们多提issue啊～～～

康桑阿米达～～～

