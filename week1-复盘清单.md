# W1 复盘清单（10/13 – 10/19）

> **用法**：做完一条就把 `[ ]` 改成 `[x]`。
> **规矩**：每条都有「怎么算过」。**没满足「怎么算过」的，不许打勾。**
>
> 生成：2026-10-12 · 对应《执行方案_2026年10月》P1 第一周

---

## 0. 判定总览（先看这个）

| 结论 | 内容 |
|---|---|
| ⏱️ 提前完成 | W1 全部知识点（JSON / 异常 / HTTP / async / LLM）计划 10/13–10/19，实际 10/10–10/12 做完，**领先 3 天** |
| ✅ 真正做对的 | LLM 命令行问答程序（写了两遍，第二遍盲写跑通，多轮记忆生效）· JSON 专项（含 ensure_ascii 对照实验）· week1-basics 目录已提交 |
| ❌ 还没做 | Day0 硬验收 · ≥7 个小提交 · 英语线 |
| 🔴 **核心问题** | 3 个交付物是**「跑过一次，没验证过」**：Day0 / 异常处理 / 异步对比 |

> **本周唯一目标：把「跑过」变成「验证过」。**
> 不要往前赶 W2。方案第 5 节的规矩是——某周没产出就优先补，不往后赶。

---

## 1. 先确认：这三个地方不要动

- [x] **LLM 程序写两遍的方法，继续用。** `firstllm/Rewrite.py` 是关掉参考盲写的，它跑通了。这是 10/10 那次定的规矩，你是唯一真正执行的人。
- [x] **学习日志的「记认知」风格，保留。** Day2 第 1/4 条、Day3 第 1 条记的是「为什么」，不是「怎么抄」。这比操作步骤值钱。
- [x] **JSON 那一课的完成度，作为后面每一课的标准。** 主动造 `bad.json` 当测试数据、主动做 `ensure_ascii` 对照——这是「验证意识」的雏形，W1 其它三课缺的就是这个。

---

## 2. P1 · 必须补的两个洞（不补，W1 等于没学）

### [x] P1-1 · `anomaly_handling.py` 四个用例必须四种输出（10 分钟）

**问题**：四个测试用例的路径写错了，全都走了「文件不存在」分支 —— **三种异常一种都没真正触发过**。
这是最危险的一类错误：**看起来测过了，实际什么都没测到。**

**当前状态**：路径已改成 `week1-basics/JSON/...` ✅（你刚改的），但**还没验证过**，而且 `no_permission.json` 权限仍是 `644`。

**怎么做**：

```bash
cd /Users/zzzz/Desktop/Learn-journey-git
chmod 000 week1-basics/JSON/no_permission.json     # 这一步不能省，否则测不到 PermissionError
python3 week1-basics/JSON/anomaly_handling.py
chmod 644 week1-basics/JSON/no_permission.json     # 记得改回来
```

**怎么算过** —— 四行输出必须是四个样子（我已实测确认这四行是正确的期望值）：

```
{'ok': True,  'error': None,        'content': {...}}   ← JSON/season.json
{'ok': False, 'error': '文件不存在',  'content': None}
{'ok': False, 'error': 'JSON 格式错误', 'content': None}   ← JSON/bad.json
{'ok': False, 'error': '权限错误',    'content': None}   ← 靠 chmod 000 触发
```

- [x] 四行输出四个样子，且顺序对得上
- [x] 从中明白一件事：**「没报错」不等于「测到了」**
- [x] 顺带修：`anomaly_handling.py` 文件末尾缺换行（`\ No newline at end of file`）

---

### [ ] P1-2 · Day0 硬验收（本周最重要的一条）

**现状**（`/Users/zzzz/Desktop/Learn/Day0实测/Day0.py`，**还不在仓库里**）：
- 只 `print(word)`，**没有计数、没有前 10、没有 result.json**
- 成功路径**没有 return**，函数返回 `None`
- `word = []` 之后 `for word in line.split():` —— **列表被循环变量同名覆盖**（真 bug）
- 你已学会 `for line` + `for word in line.split()`（遍历粒度 ✅），但**从「单词」到「计数」那一步，和 10/10 那天一样，一步都没走**

**唯一需要新学的知识就一行，背下来**：

```python
d[key] = d.get(key, 0) + 1
```

**其余全部自己写，不许打开旧文件。**

**五天拆解**：

- [x] **10/14** 数出词频并打印（核心就是上面那一行落地）
- [x] **10/15** 加 Top10：`sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:10]`
- [x] **10/16** 写入 `result.json`，格式 `[{"word": "the", "count": 42}, ...]`，**打开文件亲眼确认格式**
- [x] **10/17** 拆成 ≥2 个函数 + `if __name__ == "__main__":`；加「sample.txt 不存在」的友好提示；把 `Day0实测/` **移进仓库**
- [x] **10/19** 🎯 **删掉整个文件，20 分钟从空白重建**

**怎么算过**：10/19 那次重建，**不看任何旧文件**，20 分钟内跑出正确的 `result.json`。
重建不出来 = W1 没过，重来一周，不许往后走。

---

## 3. P2 · 方法层面（会影响后面 23 周）

### [ ] P2-1 · 异步这一课要重做（现在得出的是反的结论）

**问题**：`async.py` 是 **1 个同步请求 vs 1 个异步请求**。N=1 时异步**不会更快**（有事件循环开销）。

我实测过你的代码：

```
你的现在：同步 1 次 1.27s 成功 / 异步 1 次 10.30s 超时
正确实验：sync x5 = 6.39s / 6.91s     async x5 (gather) = 1.31s / 1.06s   ← 5 倍
```

你 Day3 第 1 条笔记写的是「异步的价值在于并发」，**但你写的代码没有并发**。

- [x] 把 `count_time_async` 改成一口气 `asyncio.gather` 发 **5 个**请求
- [x] 同步侧也循环 **5 次**，两边打印各自总耗时
- [x] 把两组真实数字记进 `Study log.md`
- [x] 写上这句认知：**N=1 时异步不会更快；异步省的时间全部来自「同时等 5 个」**
- [x] 备注：偶发的 `ConnectTimeout`（SSL 握手超时）是网络环境问题，不是代码 bug，重跑即可

###  [ ]P2-2 · 把 `Request/Rewrite.py` 写完并跑通

盲写是对的，**但这一遍没写完也没跑**。现状：

- 没有 `if __name__ == "__main__":` → **运行它什么都不发生**（我验证过，exit=0 无输出）
- `PARAMS = {}` 是空的
- `fix_data()` 返回空字典（没实现）
- `main()` 里光秃秃一个 `except:`，成功和失败**都 return `{}`**，调用者分不清

- [ ] 补空 `PARAMS`、实现 `fix_data()`
- [ ] 加 `if __name__ == "__main__":`
- [ ] 把 `except:` 换成具体异常（照 `HTTP-requests.py` 那张清单）
- [ ] 成功和失败返回**能区分开**（例如 `{"ok": True/False, ...}`）
- [ ] 运行它，确认真的写出了文件
- [ ] 顺带：`HTTP-requests.py` 里原始模板的 docstring 和 `# TODO` 注释还在 → 说明那是「别人给的骨架」。**这一课过没过的判据是：能不能不看它，把 fetch / parse / save + main 写出来**

### [ ] P2-3 · 笔记 → 代码的落地检查（本周最该修的元问题）

你在 Day2 第 11 条自己写了：**「函数返回信息的格式最好统一化，便于维护。」**
然后：

- `async.py`：同步返回 `"sync_content"`、异步返回 `"async_content"` —— 同一设计的两个版本用了两套键名
- `Request/Rewrite.py`：成功和失败返回值完全一样

> **笔记是对的，但没落到代码里。「知道」和「做到」之间这段距离，就是 W1 到 W2 要跨的。**

- [ ] 统一 `async.py` 的返回键名（建议就叫 `content` / `time` / `ok` / `error`）
- [ ] 立一条新规矩：**每写完一个文件，回头翻一遍自己的日志，检查有没有哪条规则被自己违反了**
- [ ] 从本周起，每次自检都执行这一条

---

## 4. P3 · 工程习惯（现在改成本最低）

| 打勾 | 项 | 现状 / 怎么做 | 怎么算过 |
|---|---|---|---|
| [ ] | **绝对路径** | 6 处硬编码 `/Users/zzzz/Desktop/Learn-journey-git/...`（`HTTP-requests.py` 1 处、`Request/Rewrite.py` 1 处、`llm.py` 2 处、`firstllm/Rewrite.py` 2 处） | 全换成 `Path(__file__).parent`；`grep -rn "/Users/" --include=*.py week1-basics/` **无输出** |
| [ ] | **`.DS_Store` 被提交了** | `git rm --cached .DS_Store` + 加进 `.gitignore` | `git ls-files \| grep DS_Store` **无输出** |
| [ ] | **`no_permission.json`** | 0 字节空文件被提交 | 要么给它加内容，要么不提交 |
| [ ] | **提交信息** | 全是 `Day0`/`Day1`/`Day2`/`Day3`；`Day0` 还是**空提交**（0 行改动） | 改成 `feat: JSON 读写与 ensure_ascii 对照实验` 这种 |
| [ ] | **提交数量** | 现在 4 个，计划要求 ≥7 个 | `git log --oneline \| wc -l` **≥ 7** |
| [ ] | **README.md** | 没有 | 写「这仓库是什么 / 目录结构 / 怎么跑」 |
| [ ] | **requirements.txt** | 没有 → **换台电脑就跑不起来** | 写出依赖清单，`pip install -r requirements.txt` 能装 |
| [ ] | **输出路径不一致** | `HTTP-requests.py` 写死存到 `week1-basics/weather_beijing.json`，但文件实际在 `Request/` 下（我验证过那个路径**没有**文件，重跑会生成到别处） | 路径和实际文件位置一致 |
| [ ] | **缩进混用** | `llm.py:34`、`firstllm/Rewrite.py:30` 是 5 空格，其余 4 空格 | 全文统一 4 空格 |
| [ ] | **死代码** | `async.py` 的 `URL=""` 从未使用、`OPEN_API` 命名误导 | ✅ 你已改（`OPEN_URL`、删掉 `URL=""`），**待验证** |
| [ ] | **双 dotenv** | `dotenv 0.9.9` 和 `python-dotenv 1.2.4` 同时装着（生效的是 1.2.4，另一个是空壳残留） | `pip uninstall dotenv` |

**两条已经做对的，确认一下就好**：

- [x] `.env` 已正确 gitignore
- [x] **扫过所有被提交的文件，没有密钥泄露**；Python 3.12 + 各库版本干净

**一个可以想的点（不急）**：`llm.py` 和 `firstllm/Rewrite.py` 都强制 `response_format={"type":"json_object"}`，但方案要的是「命令行问答程序」。**问自己一句：这里为什么要是 JSON？** 只是聊天 → 该去掉；结构化抽取 → 现在是对的。分辨清楚这两者，是 W2 拆 `llm_client.py` 时要回答的问题。
另外提醒一个隐蔽行为：加载逻辑是「首条不是 system 就插入」，所以**你以后改了 `system_prompt` 会不生效**（历史里那条旧 system 还在用）。

---

## 5. P4 · 计划里被跳过的线

- [x] **英语线**（每天 30 分钟，读 `httpx` 官方文档 QuickStart，约 2 页）：**零痕迹**。这是方案里唯一的「硬性执行」项，也是你自述最弱的一环。
  - 方法：先自己读一遍 → 划出不认识的词 → 用 AI 逐段解释 → **把这段英文的技术含义用中文写下来**
  - 目标不是背单词，是练「从英文文档里提取技术信息」
- [ ] **数据结构线**（W2 起，每天 30 分钟）：列表、哈希表(dict)、集合、栈、队列 + 时间复杂度。**不刷 LeetCode**
- [ ] **学习日志格式**：计划要的是「今天做了什么 / 卡在哪里 / 明天做什么」三行。你写的是知识点日志 —— **内容更有价值，保留它**，但在每条前面加那三行。因为**你现在的日志里看不到「卡在哪里」，而卡点才是复盘时最该看的**

---

## 6. 这 7 天怎么用（可直接照着做）

| 日期 | 做什么 | 对应条目 |
|---|---|---|
| **10/13** | 修 `anomaly_handling.py` + `chmod 000`，**四个输出四个样**才算过 | P1-1 |
| **10/14** | Day0：数出词频并打印（核心 `d.get(k,0)+1`） | P1-2 |
| **10/15** | Day0：加 Top10 | P1-2 |
| **10/16** | Day0：写 `result.json` + 拆函数 + 加文件不存在的提示 + **移进仓库** | P1-2 |
| **10/17** | 异步重做：N=5 `asyncio.gather` vs 同步循环 5 次，记两组数字 | P2-1 |
| **10/18** | 写完并跑通 `Request/Rewrite.py`；开始 P3 工程习惯 + README/requirements | P2-2 / P3 |
| **10/19** | 🎯 **硬验收**：删掉 Day0 文件，20 分钟从空白重建。重建不出来就再来一周 | P1-2 |

> 每天一个提交，信息写清楚 → 7 天正好把提交数补到 7 个以上。

---

## 7. 周末回填：W1 完成度自评

| 项目 | 10/12 状态 | 10/19 状态 |
|---|---|---|
| JSON 读写 | ✅ 超计划完成 | |
| 异常处理（3 种） | ⚠️ 代码对，未验证 | |
| HTTP + requests | ⚠️ 模板版可跑，盲写版未完成 | |
| httpx + async | ⚠️ 结构对，结论反了 | |
| LLM 命令行问答 | ✅✅ 已完成 | |
| **Day0 硬验收** | ❌ 未做 | |
| 提交数 ≥7 | ❌ 4 个 | |
| 英语线 | ❌ 零痕迹 | |
| 工程习惯（P3） | ⚠️ 部分已改 | |

**一句话**：这周补的不是知识，是**验证的习惯** —— 它比 W1 任何一行代码都更值钱。

---

### 附：快速自查命令

```bash
cd /Users/zzzz/Desktop/Learn-journey-git

git log --oneline | wc -l                       # 提交数，目标 ≥7
git status --short                              # 有没有忘了提交的
git ls-files | grep DS_Store                    # 应为空
grep -rn "/Users/" --include=*.py week1-basics/ # 应为空
python3 -c "import ast,sys; [ast.parse(open(f,encoding='utf-8').read()) for f in sys.argv[1:]]" $(git ls-files '*.py')   # 全部语法检查
```
