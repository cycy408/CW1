# INT101 Course work1 — Python 学习小游戏合集

一个用 Python 写的多合一学习小游戏项目，包含知识问答、代码块拖拽排序、飞船 Boss 战三种玩法。UI 使用 tkinter / customtkinter 和 pygame 实现，用户数据通过 JSON 文件持久化存储。

（未来可能会加入 Unity 进行美化，还有加入计时器做排行榜的想法——如果这周末太闲的话。）

---

## 项目结构

```
CW1/
├── main.py              # 入口：登录/注册 + 游戏选择菜单
├── user_auth.py         # 用户认证封装（注册 / 登录）
├── data_manager.py      # JSON 数据读写层（用户 + 游戏进度）
├── game_class.py        # 第一部分：知识问答游戏（customtkinter）
├── drag_puzzel.py       # 第二部分：代码块拖拽排序（pygame）
├── spaceship_game.py    # 第三部分：飞船 Boss 问答战（pygame）
├── users.json           # 用户账号数据
├── progress.json        # 所有游戏进度数据
└── README.md
```

---

## 技术栈

| 组件 | 技术 |
|------|------|
| GUI 框架 | customtkinter（登录/问答），pygame（拖拽/飞船） |
| 数据持久化 | JSON 文件（全量读写） |
| 进程架构 | 拖拽和飞船游戏通过 subprocess 独立启动，问答在主进程内运行 |
| 图形 | 全部程序化绘制，无外部图片/音频资源 |

---

## 用户系统

`user_auth.py` 封装了注册和登录逻辑，底层调用 `data_manager.py` 读写 `users.json`。

- **注册**：检查用户名是否已存在，未存在则写入明文密码（字符串对比）。
- **登录**：校验用户名和密码是否匹配，失败则提示是否跳转注册。
- **异常处理**：任何校验失败都会要求重新输入。

（所以上传云端到底是咋做的？）

> `users.json` 是一个扁平的 `{用户名: 密码}` 字典。

`data_manager.py` 是项目唯一的持久化层，负责：
- `users.json` 的读写
- `progress.json` 的读写，按用户名组织各游戏的进度数据
- 文件不存在时自动初始化为空 `{}`
- `Player` 对象的序列化 / 反序列化（`to_dict()` / `from_dict()`）

---

## 进度系统

每一部分都加入了进度读取和自动保存，随时退出也不会丢进度。

`progress.json` 的数据结构：

```json
{
  "用户名": {
    "username": "string",
    "score": 0,            // 问答当前分数
    "level": 1,            // 问答当前等级
    "mastered_topics": [], // 已掌握主题列表
    "completed_levels": [],// 问答已通关等级
    "spaceship": {         // 飞船游戏进度
      "level": 1,
      "total_damage": 0,
      "completed_levels": []
    },
    "drag_puzzle": {       // 拖拽游戏进度
      "basic_syntax": 0,   // 每个模块完成数 (0-5)
      "control_structure": 0,
      ...
    }
  }
}
```

（额，挺没招的啊其实，这个创新点是何物，一直在追我。）

---

## 游戏部分

### 一、知识问答

**文件**: `game_class.py`| **UI**: customtkinter | **运行方式**: 主进程内

最初的设想。后来觉得有些单调、不符合游戏的要求，所以接着往后加了后面的内容。

**核心类设计：**

- **`Player`** — 玩家数据类，包含用户名、分数、等级、已掌握主题、已通关等级。提供 `add_score()`、`level_up()`、`complete_level()` 等方法。
- **`Level`** — 关卡配置类，自动根据等级分配难度（1-2 Easy / 3-4 Medium / 5-6 Hard），通关分为 40（满分 50）。
- **`QuestionBank`** — 静态题库类，6 个等级，每级 5 道 Python 选择题，题目随机打乱。
- **`GameUI`** — 主游戏窗口（620×540），包含关卡选择界面和答题界面。

**6 个等级主题：**

| 等级 | 主题 | 难度 |
|------|------|------|
| 1 | Variables & Data Types | Easy |
| 2 | Strings & Operations | Easy |
| 3 | Lists & Tuples | Medium |
| 4 | Conditionals & Loops | Medium |
| 5 | Functions | Hard |
| 6 | Dictionaries & File I/O | Hard |

**玩法流程：**

1. 关卡选择界面展示 6 关，每关显示主题、难度徽章（绿/黄/红），已完成的关卡标记 ✓。
2. 进入关卡后依次回答 5 道选择题，每题 10 分。
3. 提交后显示正误反馈（绿色正确 / 红色错误并展示正确答案），按钮变为 "Next Question"。
4. 5 题答完后结算：>= 40 分通关，记录进度；不通过可选择重试或返回。
5. 全部 6 关通过后显示胜利界面，列出所有已掌握主题。
6. 随时可点击 "Save & Quit" 保存退出。

具体代码编写逻辑其实很简单，主要是一些交互按键用 Claude 写了，其他部分应该都很好懂（实则不然）。

（后续如果还想继续优化，希望可以增加选择关卡功能——不过现在已经有了？可能指的是更自由地跳关。）

---

### 二、代码块拖拽排序

**文件**: `drag_puzzel.py`（约 842 行）| **UI**: pygame | **运行方式**: subprocess 独立进程，传用户名作为命令行参数

灵感来源于多邻国的拖拽答题界面。玩家需要将打乱的代码行按正确顺序拖入右侧编号槽位。

（Claude Code 大开智，增加了关卡选择和显示的页面，还是挺好看的，但是整体风格不统一，什么原因我也没想明白。）

**7 个模块 × 5 个关卡 = 35 个小关卡：**

| 模块 | 主题 | 颜色 |
|------|------|------|
| 1 | Basic Syntax（变量赋值、字符串拼接、类型转换等） | 蓝 |
| 2 | Control Structures（if/else、for/while 循环等） | 紫 |
| 3 | Data Structures（列表、字典、元组、集合、列表推导式）| 青 |
| 4 | Functions（def、return、默认参数、lambda 等） | 橙 |
| 5 | OOP（class、__init__、继承、计数器类等） | 黄 |
| 6 | File I/O（读写文件、with 语句、追加模式等） | 绿 |
| 7 | Exception Handling（try/except、finally、raise、自定义异常） | 红 |

**UI 配置：**

- 窗口 820×600，60 FPS
- 17 色扁平化调色板（PALETTE 字典）
- 左侧 "DRAG FROM HERE" 区域排列打乱的代码块
- 右侧 "DROP IN ORDER" 区域排列编号槽位
- 每个模块有进度条（0/5 → 5/5）和完成星标

**玩法流程：**

1. 模块选择界面展示 7 个模块，每行含颜色条、名称、进度条、完成标记。
2. 进入关卡后，将下方代码块拖入右侧正确的顺序槽位。
3. 点击 Check：逐一比对，正确位置变绿，错误变红。
4. 答对后自动保存进度，1.2 秒后自动加载下一关。
5. 模块 5 关全部完成后弹出 "Module Complete!" 提示。

**交互设计：**

- 鼠标悬停高亮、拖拽吸附、松手回弹
- 顶部功能栏：Back / Reset / Check / Next
- 已锁定答案的方块不可再拖动

---

### 三、飞船 Boss 问答战

**文件**: `spaceship_game.py`（约 933 行）| **UI**: pygame | **运行方式**: subprocess 独立进程

俯视角太空射击 + Python 知识问答。答对题目向 Boss 发射能量弹造成伤害，答错 Boss 回血。

（原计划是让它变得更趣味，但是作者太傻了，没有游戏策划的天赋，想半天没弄懂通关逻辑，所以做了一坨大的，但是基本动画还是做了一点。主要为了用上课讲的 pygame——绝对不是其他的我不会。）

**核心类设计：**

- **`PlayerShip`**（pygame Sprite）— 60×56 像素，多边形+椭圆程序化绘制，箭头键移动（8px/s），引擎火焰随机抖动动画。
- **`BossShip`**（pygame Sprite）— 190×130 像素，复杂的暗红色外星飞船，程序化多边形绘制。横向弹跳移动，受击白色闪烁效果。
- **`Projectile`**（pygame Sprite）— 8×24 蓝色能量弹，带发光效果。命中后触发粒子爆发。
- **`Particle`** — 粒子系统，用于打击火花、引擎尾焰、胜利烟花。
- **`Game`**（约 600 行）— 主游戏类，状态机管理。

**7 个关卡（与拖拽游戏模块主题对应）：**

| 关 | 主题 | Boss HP |
|----|------|---------|
| 1 | Basic Syntax | 50 |
| 2 | Control Structures | 50 |
| 3 | Data Structures | 50 |
| 4 | Functions | 50 |
| 5 | OOP | 50 |
| 6 | File I/O | 50 |
| 7 | Exception Handling | 50 |

**状态机流转：**

```
level_select → intro → playing → level_complete → level_select
                                  → victory（全部通关）
```

**动态计分 / 连击系统：**

- 答对：伤害 = 10 + (连击数 - 1) × 2。连击 1 = 10，连击 2 = 12，连击 3 = 14，以此类推。发射弹丸 + 粒子爆发。
- 答错：连击归零，Boss 回血 5 点（不超过上限）。显示正确答案反馈。
- 答对后 90 帧冷却，期间不能出下一题。
- Boss 血量降至 0 即通关，保存进度。

（这个动态计分逻辑比较容易让人红温。其实想加"打不中就不得分"的机制——就是必须让弹丸飞到 Boss 身上才算分——但是我测试玩红温了，通不了关，遂放弃。）

**视觉效果：**

- 3 层视差星空背景（115 颗星，不同速度/亮度）
- 6 个彩色星云缓慢漂移
- Boss 受击白光闪烁（8 帧）
- 答对：绿色浮动反馈文字 + 金色粒子
- 答错：红色浮动反馈文字
- 通关：烟花粒子效果
- 胜利：金色光芒 + 脉冲提示

**控制方式：**

- ↑↓←→ 移动飞船
- Space 弹出题目
- ↑↓ 选择答案，Space 确认
- 关卡选择界面：↑↓ 导航，Space/Enter 确认，鼠标点击支持
- 胜利界面：R 重置所有进度，L 返回选关，ESC 退出

---

## 进程架构

`main.py` 作为启动器，登录后进入游戏选择界面（customtkinter，520×560）：

- **问答游戏** → 在主进程内直接实例化 `GameUI` 运行
- **代码拖拽** → `subprocess.Popen(["python", "drag_puzzel.py", username])` 独立启动，等待子进程结束后重新显示选择界面
- **飞船游戏** → 同上 subprocess 方式

（tkinter 做的 UI 交互页面，到底什么时候能好好改这坨。包括后面所有的交互都是 tkinter 做的。）

---

## 已知问题 / 可改进项

- 密码明文存储，无哈希保护
- JSON 文件全量读写，数据量大时性能下降
- 三款游戏的 UI 风格不一致（customtkinter vs pygame，配色方案不同）
- 无 `requirements.txt`，依赖需手动安装（`customtkinter`、`pygame`）
- 飞船游戏中弹丸飞行速度为纯视觉效果，不影响得分判定

（这个小糊项目的逻辑基本就是这样。）
