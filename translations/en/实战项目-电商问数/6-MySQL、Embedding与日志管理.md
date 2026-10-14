# 6 - Shopkeeper Data Q&A: MySQL, Embedding Integration, and Log Management

---

**Chapter Learning Objectives:**

- Understand the role of the `Embedding` client manager and how it connects to the subsequent vector retrieval process.
- Understand that `MySQL` plays two roles in this project: the metadata database and the data warehouse simulation database.
- Learn how the project uses unified logging configuration to support debugging, troubleshooting, and runtime observation.

**Learning Suggestions:** This chapter is a wiring diagram for three foundational capabilities: Embedding converts text into vectors, MySQL stores and queries structured data, and logging lets you know where the system is at each step. When reading the code, don't just look at the wrapper classes themselves—trace where they are initialized, how they are injected into the business layer, and whether errors can be located down to specific requests through logs.

**Corresponding code branch:** `06-mysql-embedding-log`

---

In the previous chapter, we integrated `Qdrant` and `Elasticsearch`, but there are still two key questions that remain unresolved:

1. Where do the vectors to be written into `Qdrant` actually come from?
2. How are structured data and runtime logs managed uniformly during retrieval, database building, and SQL execution?

This chapter addresses exactly these two questions.

Placing them back into the overall architecture, they can be summarized as the following chain:

```text
文本
  -> Embedding 服务
  -> 向量
  -> Qdrant 检索

结构化元数据 / 数仓数据
  -> MySQL

运行过程
  -> Loguru + request_id + contextvars
```

In other words:

- `Embedding` is responsible for "turning text into vectors"
- `MySQL` is responsible for "storing and querying structured information well"
- The logging system is responsible for "recording clearly what was done at each step"

Viewed together, these three types of capabilities are not three isolated branches; they collectively support the subsequent database building, retrieval, generation, and troubleshooting.

![How Embedding, MySQL, and logging—three foundational capabilities—support the metadata knowledge base and data query pipeline](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/6/6-0-0-1.svg)

Only when all three parts are connected will the subsequent metadata knowledge construction, hybrid recall, SQL generation and execution truly form a closed loop.

---

## 1. Embedding Client Management

### 1.1 Introduction to Embedding

`Embedding` means: **converting a sentence, a field description, or a metric name into a set of numbers that can participate in vector calculations.**

For example:

- Keywords in user questions need to be vectorized first before they can be used to retrieve similar fields and metrics from `Qdrant`
- Table descriptions, field descriptions, and metric descriptions in the metadata database also need to be vectorized first before they can be written into the vector database in advance

Therefore, this layer is not an "auxiliary feature" but a foundational capability within the entire retrieval pipeline.

In "Shopkeeper Data Q&A," we don't simply hand natural language questions to a large language model and call it done. In processes such as field recall, metric recall, and metadata knowledge construction, the system must first convert text into vectors and then pass them to `Qdrant` for similarity search. In other words, there is a very important chain here: **Text -> Embedding service -> Vector -> Qdrant retrieval**. Without this layer, the subsequent vector recall chain cannot function.

### 1.2 Introduction to TEI

This project does not choose to "load Embedding model weights directly in business code." Instead, it uses:

- **Server-side component**: `Text Embeddings Inference`, abbreviated as `TEI`
- **Embedding model**: `BAAI/bge-large-zh-v1.5`

`Text Embeddings Inference`, usually abbreviated as `TEI`. It is essentially a service framework specifically designed to deploy Embedding models and provide vector inference capabilities through HTTP interfaces.

Corresponding official documentation: https://huggingface.co/docs/text-embeddings-inference/index (English)

Within this project, it can be understood through the following chain:

```text
BAAI/bge-large-zh-v1.5
  -> TEI 服务
  -> EmbeddingClientManager
  -> 字段召回 / 指标召回 / 元知识构建
```

In other words:

- `BAAI/bge-large-zh-v1.5` is the model truly responsible for converting text into vectors
- `TEI` is responsible for running this model and exposing it as a callable service
- `EmbeddingClientManager` is responsible for integrating this service layer into the project

From an engineering perspective, `TEI` solves two practical problems here: there is no need to load model weights in business code, and the backend can obtain Embedding results simply by accessing the service via an HTTP address.

In this project, `TEI` still runs as an **independent service**. More specifically, it is not an ordinary Python class written in the backend code; rather, it is started as a container service within the project's Docker base service environment, and the backend calls it through the configured `host` and `port`.

### 1.3 Common Server-Side Component Overview

The server-side component used in this project is `Text Embeddings Inference（TEI）`. It is well suited for this tutorial because its positioning is very clear: **dedicated to Embedding model inference**.

Besides `TEI`, common server-side components on the market can be roughly divided into several categories:

- **General model serving platforms**
  For example, `Xinference`, `Ollama`, `BentoML`, `Ray Serve`
- **LLM-focused inference frameworks**
  For example, `vLLM`, `TGI`, `SGLang`, `LMDeploy`, `Triton Inference Server`
- **Cloud provider managed services**
  For example, `OpenAI Embeddings API`, `Azure OpenAI`, `阿里云百炼`, `火山方舟`, `百度千帆`, `AWS Bedrock`

If we only consider the needs of the current project, the most important judgments are:

- If you want to **deploy an Embedding service locally or self-hosted**, `TEI` is a very fitting choice
- If you want to **centrally manage multiple types of model services**, platforms like `Xinference` are more common
- If you want to **directly call cloud Embedding APIs**, you would use managed interfaces provided by various cloud vendors or model service providers

Therefore, this chapter uses `TEI` not because it is the only solution, but because it best fits the chain of "**deploying an Embedding service -> exposing an HTTP interface -> unified backend integration**" in the current project.

### 1.5 Access Methods for TEI

Official documentation: https://huggingface.co/docs/text-embeddings-inference/quick_tour (English)

There are mainly **3 ways** to access `TEI` for inference:

- **Directly call the native HTTP interface**: for example, using `curl` to directly request `/embed`
- **Use Hugging Face's Python client**: that is, the `InferenceClient` in `huggingface_hub`
- **Use the OpenAI-compatible method**: that is, treat the interface exposed by `TEI` as an OpenAI-style `/v1/embeddings` to call

However, in the current project, these native calling methods are not used directly. Instead, a solution more aligned with the entire tutorial's technology stack is chosen: using the `HuggingFaceEndpointEmbeddings` provided by LangChain.

This approach has two obvious benefits: it stays consistent with the `LangChain / LangGraph` system already learned earlier, and it provides a more unified interface for subsequent calls in the service layer and Agent nodes. In other words, the current project does not lack the ability to directly call `TEI`; rather, it deliberately chooses an integration layer that better fits the entire tutorial's technology stack.

### 1.6 Wrapping the Embedding Client

Corresponding project file path: `shopkeeper-agent/app/clients/embedding_client_manager.py`

The code is as follows:

```python
import asyncio
from typing import Optional

from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.app_config import EmbeddingConfig, app_config


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        # 客户端在模块导入阶段先不立即创建，避免启动时就发起外部依赖连接
        self.client: Optional[HuggingFaceEndpointEmbeddings] = None
        # 保存 Embedding 服务配置，供 init() 时组装服务访问地址使用
        self.config = config

    def _get_url(self):
        # 当前项目通过 host + port 访问外部已启动的 Embedding 推理服务
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        # 在应用启动阶段显式调用，完成真正的客户端初始化
        self.client = HuggingFaceEndpointEmbeddings(model=self._get_url())


# 模块级单例，供其他模块按需复用同一个客户端管理器
embedding_client_manager = EmbeddingClientManager(app_config.embedding)


if __name__ == "__main__":
    # 本地调试入口：初始化客户端后执行一次最小化向量化调用
    embedding_client_manager.init()
    client = embedding_client_manager.client

    async def test():
        # 使用示例文本验证 Embedding 服务是否可正常响应
        text = "What is deep learning?"
        query_result = await client.aembed_query(text)
        # 只打印前 3 个维度，便于快速确认返回结果结构正确
        print(query_result[:3])

    # 运行调试测试
    asyncio.run(test())
```

Execute the file for verification; it succeeds:

```bash
(shopkeeper-agent) didilili@DidililiMacBook-Pro shopkeeper-agent % python3 -m app.clients.embedding_client_manager

[-0.005919582676142454, 0.005813124123960733, 0.018300632014870644]

```

#### 1.6.1 Responsibilities of This Layer's Wrapper

Without looking at the details, this manager does only three things:

1. Saves the Embedding service configuration
2. Constructs the service URL based on `host + port`
3. Creates a globally reusable Embedding client

It does not handle: model training, model downloading, or vector post-processing. It handles only one thing: centralizing "how the project accesses the Embedding service."

#### 1.6.2 Responsibilities of config and client

```python
class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: Optional[HuggingFaceEndpointEmbeddings] = None
        self.config = config
```

There are two core attributes here:

- `self.config`: saves the configuration object, which contains `host`, `port`, and `model`
- `self.client`: saves the actually callable Embedding client instance

Like the client managers discussed earlier, initialization is not completed immediately in the constructor. Instead, the object is created first, and the client is actually generated later in `init()`.

#### 1.6.3 The Role of \_get_url() and URL Composition

```python
def _get_url(self):
    return f"http://{self.config.host}:{self.config.port}"
```

What is done here is not complicated, but it is critical: **combining `host` and `port` from the configuration file into a unified service URL**.

Extracting this into a separate method has two benefits: the service URL construction logic is maintained in only one place, and future changes will be more centralized if the deployment method changes.

In the current project, this URL typically points to the `TEI` service already started in the Docker environment.

#### 1.6.4 The Initialization Process of init()

```python
def init(self):
    self.client = HuggingFaceEndpointEmbeddings(model=self._get_url())
```

The most noteworthy point here is: what is passed to `model=` is not a model name from Hugging Face, but the **address of the locally deployed Embedding service**.

In other words, the calling method of this client can be understood as:

- It does not directly access Hugging Face over the internet
- It does not load model weights itself
- Instead, it sends requests to the locally started TEI service

This is also why this layer is more like "service integration" than "model training" or "model loading."

#### 1.6.5 Why a Separate close() Method Is Not Provided

The previously mentioned `Qdrant`, `Elasticsearch`, and `MySQL` clients often require explicit initialization and shutdown because they are closer to: long-lived connections, connection pools, and persistent database connections.

This Embedding client, however, is essentially closer to **a stateless HTTP call wrapper**. Unlike database connections, it does not need to hold connection resources for a long time, so there is no dedicated `close()` method written here. This is also why its implementation is noticeably lighter.

---

## 2. MySQL Client Management

### 2.1 Why Two Sets of MySQL

Many readers' most common confusion when first looking at the project configuration is: why are there two sets of configurations when they are both called MySQL?

The answer is simple: because they serve two different responsibilities:

| Configuration Item    | Connects To | Primary Responsibility                                               |
| --------- | ---------- | ------------------------------------------------------ |
| `db_meta` | Metadata database   | Stores table information, field information, metric information, field-metric relationships, and other metadata |
| `db_dw`   | Data warehouse simulation database | Provides the data that real business queries need to access, used to validate SQL and execute SQL   |

So the key understanding here is not "why is it so troublesome," but rather:

> **One is responsible for "what the system knows exists in the database," and the other is responsible for "what the system ultimately queries."**

This is also why the project ultimately does not create just one MySQL client, but two:

- `meta_mysql_client_manager`
- `dw_mysql_client_manager`

### 2.2 Introduction to SQLAlchemy

Official documentation: https://www.sqlalchemy.org/

Before diving into the MySQL client implementation, it will be smoother to first understand `SQLAlchemy` separately, because the MySQL integration in this project is not built on hand-written low-level connections, but on top of `SQLAlchemy`.

Grasp three key terms:

- **ORM**: a translation layer between database tables and Python classes. You operate on classes and objects in code, and the ORM translates those operations into SQL that the database can execute.
- **Engine**: the main entry point for a program to connect to the database, responsible for establishing connections with the database and maintaining a set of reusable connections.
- **Session**: A working window for a specific database operation. A round of querying, writing, and committing is usually completed through it.

If you only need to remember one sentence, it can be summarized as: `Engine` is more like the "connection infrastructure", while `Session` is more like "the working context for this database operation".

### 2.3 SQLAlchemy Quickstart Example

Official documentation: https://docs.sqlalchemy.org/en/20/orm/quickstart.html

This quickstart can help us first establish the following most basic chain of understanding:

```text
声明模型
  -> 创建 Engine
  -> 建表
  -> 创建 Session
  -> 写入对象
  -> 查询对象
```

For ease of learning, the official example uses synchronous coding and the SQLite in-memory database. Our project ultimately uses asynchronous coding and MySQL. In other words, **the scenarios differ, but the core concepts are the same**. Therefore, this section is the most suitable for helping us understand these basic concepts of `ORM / Engine / Session / 模型映射`.

First, let's look at the model declarations in the official example:

```python
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")
```

Understand what it is expressing:

- `Base`: The base class that all ORM models inherit from.
- `User`, `Address`: Classes in the program that also correspond to two tables in the database, respectively.
- `__tablename__`: Specifies which table in the database this class maps to.
- `mapped_column(...)`: Defines field types, primary keys, and other information.
- `relationship(...)`: Used to describe relationships between tables.

Next, create the `Engine`:

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)
```

It is particularly worth adding here: `Engine` is not "a particular query"; it is more like the core object of the database connection layer, which maintains the connection pool for us underneath.

After that, create tables directly from the models:

```python
Base.metadata.create_all(engine)
```

This line of code means: **automatically generate the corresponding table structures based on the previously declared models**. However, it is also worth reminding you here: in our project, we did not take this route of "letting the ORM create tables automatically". The database and table structures of the current project were already initialized during the earlier environment preparation phase, so this is more about helping you understand the boundaries of SQLAlchemy's capabilities, rather than the table creation method the project actually relies on at runtime.

Then, for writing data, use `Session` like this:

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")

    session.add_all([spongebob, sandy, patrick])
    session.commit()
```

This section mainly explains two things:

- When writing data to the database, what actually interacts with the database is the `Session`.
- The ORM style looks like operating on Python objects, but underneath, SQL is ultimately generated and sent to the database.

This also corresponds exactly to the two key actions of `add_all()` and `commit()`.

Finally, perform a simple query:

```python
from sqlalchemy import select

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print(user)
```

This code expresses:

- First construct a query statement, `stmt`.
- Then execute this statement through `Session`.
- Finally, iterate through the queried ORM objects.

Here you can also see that the official quickstart tends to demonstrate the ORM-style query approach. The ORM style here can be understood as: **instead of writing SQL strings manually, use classes, attributes, and methods in Python to express "what I want to query"**. However, when it comes to the actual current project, we do not force all queries to be written in this form. For complex SQL, especially in data warehouse query scenarios, writing raw SQL directly is often more intuitive and makes it easier to control the details.

Therefore, the value of this quickstart in the current tutorial can be summarized in one sentence: it mainly helps us first understand the basic components and usage order of SQLAlchemy, and then the project code later makes trade-offs and implementations based on the real needs of asynchronous MySQL.

### 2.4 Encapsulating the MySQL Client

Corresponding project file path: `shopkeeper-agent/app/clients/mysql_client_manager.py`

The core code of this part is the MySQL client encapsulation in the current project. The preceding `SQLAlchemy` basics, quickstart, Engine, and Session are ultimately all meant to help us understand this code.

There is also one point to add here that is easily overlooked in the course but is actually already used in the code: `asyncmy` is the MySQL asynchronous driver used in the current project. More specifically, `SQLAlchemy` is responsible for providing the database abstraction layer, while the underlying driver that actually communicates asynchronously with MySQL is `asyncmy`.

#### 2.4.1 MySQL Client Code Implementation

```python
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.conf.app_config import DBConfig, app_config


class MySQLClientManager:
    def __init__(self, config: DBConfig):
        # Engine 是数据库连接层核心对象，底层会维护连接池
        self.engine: AsyncEngine | None = None
        # session_factory 用来按需创建新的 AsyncSession
        self.session_factory = None
        # 保存数据库配置，后面拼接连接地址要用
        self.config = config

    def _get_url(self):
        # mysql+asyncmy 表示：连接 MySQL，并使用 asyncmy 作为异步驱动
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.database}?charset=utf8mb4"

    def init(self):
        # 创建异步 Engine，相当于先把“数据库连接能力”准备好
        self.engine = create_async_engine(
            self._get_url(), pool_size=10, pool_pre_ping=True
        )
        # 基于 Engine 创建 Session 工厂，后面真正查库时再拿 session
        self.session_factory = async_sessionmaker(
            self.engine, autoflush=True, expire_on_commit=False
        )

    async def close(self):
        # 程序结束时释放连接池资源
        await self.engine.dispose()


# 一套连元数据库，一套连数仓模拟库
meta_mysql_client_manager = MySQLClientManager(app_config.db_meta)
dw_mysql_client_manager = MySQLClientManager(app_config.db_dw)

if __name__ == "__main__":
    # 这里演示的是数仓库查询，所以先初始化 dw 这一套客户端
    dw_mysql_client_manager.init()

    async def test():
        # 通过 session_factory 创建一次数据库会话
        async with dw_mysql_client_manager.session_factory() as session:
            sql = "select * from fact_order limit 10"
            # text(sql) 表示把原生 SQL 语句交给 SQLAlchemy 执行
            result = await session.execute(text(sql))

            # mappings().fetchall() 会把结果转成“按列名访问”的行对象列表
            rows = result.mappings().fetchall()

            # 下面三行只是为了帮助观察返回结果的结构
            print(type(rows))
            print(type(rows[0]))
            print(rows[0]["order_id"])

    asyncio.run(test())

```

Execute the file to verify, success:

```bash
(shopkeeper-agent) didilili@DidililiMacBook-Pro shopkeeper-agent % python3 -m app.clients.mysql_client_manager
<class 'list'>
<class 'sqlalchemy.engine.row.RowMapping'>
ORD20250101001
```

This manager mainly does four things:

1. Save database configuration
2. Create the `Engine`
3. Create the `Session` factory
4. Close the connection pool when the program exits

It follows the same idea as the `QdrantClientManager` and `ESClientManager` mentioned earlier: they all belong to the infrastructure layer of "unified initialization, unified shutdown, and unified provision of basic capabilities to the outside".

#### 2.4.2 Why Engine Is Suitable for Global Reuse

There is a very critical point here: `Engine` can be understood as a global singleton, but `Session` should not be made into a global singleton.

The reasons are as follows:

- The `Engine` maintains a database connection pool underneath.
- A connection pool should naturally be reused globally.
- If a new `Engine` is created for every request, it is equivalent to creating a new connection pool each time, which is costly and unnecessary.

The `Session` is different. `Session` is more like a session context corresponding to one database interaction. It should usually be **created per request and per usage scenario**, rather than keeping only one globally. The reasons are:

- A `Session` often binds a transaction context.
- Different requests should not share the same transaction session.
- Create a `Session` based on the `Engine` whenever database access is needed.

To put it more plainly: the `Engine` is responsible for maintaining connection capabilities over the long term, while the `Session` is responsible for one specific database operation.

#### 2.4.3 Why session_factory Is What Is Actually Exposed

This is another point that many beginners find difficult to understand immediately when reading the code for the first time. The current project does not "create a global `Session` object first and then pass it around everywhere"; instead, it does this:

```python
self.session_factory = async_sessionmaker(
    self.engine,
    autoflush=True,
    expire_on_commit=False,
    autobegin=True,
)
```

The reason is simple: the project is asynchronous in style, and Sessions will be created repeatedly in many places later. Rather than manually writing the creation logic every time, it is better to first create a unified **Session factory**. This way, whether it is for API dependency injection, metadata-building scripts, or the Agent execution pipeline, it can be used through:

```python
async with xxx_mysql_client_manager.session_factory() as session:
    ...
```

to obtain a new asynchronous session object.

Therefore, the `session_factory` here can be viewed as: **a factory specifically used to create `AsyncSession` in batches, uniformly, and stably.**

#### 2.4.4 Configuration Explanation for pool_size, pool_pre_ping, and autoflush

This part has two levels of focus: **Engine parameters** and **Session parameters**.

First, look at the `Engine` level:

```python
self.engine = create_async_engine(
    url=self._get_url(),
    pool_size=10,
    pool_pre_ping=True,
)
```

##### 2.4.4.1 pool_size=10

Indicates how many reusable connections the connection pool maintains by default. This value is not the larger the better; it needs to be weighed against your concurrency, database capacity, and deployment environment. For the current tutorial project, we first provide a teaching-friendly default value.

##### 2.4.4.2 pool_pre_ping=True

Indicates that an availability check is performed when a connection is taken from the pool.

Why is this parameter important? Because the database server sometimes proactively disconnects connections that have been idle for a long time. If we take out a connection from the pool that "appears to still be there but is actually invalid", subsequent queries will report errors. What `pre_ping` does is to test whether the connection is still alive before actually using it.

Next, look at the `Session` level:

```python
self.session_factory = async_sessionmaker(
    self.engine,
    autoflush=True,
    expire_on_commit=False,
    autobegin=True,
)
```

##### 2.4.4.3 autoflush=True

It may be easier to understand it this way:

- `add()` does not mean immediately committing data to the database for final storage.
- Before the transaction is actually committed, many changes still remain in the current `Session`.
- The role of `flush()` is to synchronize these pending changes to the database connection layer, but the transaction has not yet been finally committed.

Therefore, the significance of `autoflush=True` is: before executing a query, the framework will automatically perform a `flush` for us, avoiding the confusion of "obviously an object was added earlier, but the subsequent query still cannot see it".

By the way, let's distinguish here:

- `flush`: Synchronize the pending changes in the current Session to the database connection layer.
- `commit`: Actually commit the transaction on the basis of `flush`.

In other words, `flush` is not equivalent to a final commit.

##### 2.4.4.4 expire_on_commit=False

If the default behavior is kept, after a transaction is committed, the object state will be marked as "expired"; when you access object attributes again later, the ORM may attempt to query the database again. In an asynchronous project, however, this kind of implicit re-query is not suitable as the default behavior, so it is explicitly set to `False` here to make usage more stable and predictable.

##### 2.4.4.5 autobegin=True

Indicates that a transaction is automatically started when needed. In this way, most business code does not need to manually write a boilerplate "begin transaction" block every time.

So when these parameters are considered together, they actually solve three types of problems:

- `pool_pre_ping=True`: Solves the problem of stale connections in the connection pool.
- `autoflush=True`: Solves the consistency experience problem of "objects were written but queries cannot see them".
- `expire_on_commit=False`: Solves the uncertainty problem of accessing object attributes in asynchronous scenarios.

### 2.5 Why Not Use ORM Query Syntax

Earlier, we compared it with the official `SQLAlchemy` quickstart and also looked at the ORM-style query approach. But when it comes to the current project, not all queries have been rewritten into ORM query expressions.

The reasons are very practical:

- For simple queries, using the ORM is certainly no problem.
- For complex queries, especially analytical queries leaning toward data warehousing, raw SQL is often more direct.
- The focus of the current project is not to "comprehensively demonstrate ORM syntax", but to "stably integrate database capabilities into the backend".

Therefore, the strategy here is actually very clear:

- Use `SQLAlchemy` for **connection management and Session management**.
- **Complex query statements** can still be written directly in raw SQL.

This is also why the test code directly uses:

```python
await session.execute(text("select * from table_info limit 10"))
```

---

## 3. Logging Management

### 3.1 Why Not Use print

Let's first emphasize a very practical issue here: if it is only for temporary local testing, `print` is certainly usable; but once you enter a formal project, it quickly becomes insufficient.

There are mainly two types of reasons:

- **Output information is not standardized enough**: If you only use `print`, you usually still have to stitch together information such as time, module name, function name, line number, and log level yourself.
- **Output destination is not flexible enough**: After a project goes live, logs often need to be output not only to the console but also written to log files for troubleshooting and archiving.

Therefore, the key point here is not that "`print` cannot be used at all", but rather: **the project needs a more stable and configurable logging solution**.

### 3.2 Introduction to loguru

Official documentation: https://loguru.readthedocs.io/en/stable/#readme

The current project chooses `loguru` for log management. Looking at its minimal example first will make it easier to understand why it was chosen here:

For example:

```python
from loguru import logger

logger.info("starting")
logger.warning("warning")
logger.error("error")
```

After running it directly, you can see log output with time, level, location, and color.

However, there is another key point here: **working out of the box does not mean the project can directly copy the default configuration**. Real projects usually also have these requirements:

- Should it output to the console?
- Should it write to a log file?
- Where should the log file be written?
- At what size should a new file be created
- How long to retain
- Whether the log format should include additional fields

Therefore, the current project did not stop at "directly using `import logger` and then printing"; instead, it went one step further: **making logging a configurable foundational capability**.

### 3.3 Logging Description in the Configuration File

Corresponding project file path: `shopkeeper-agent/conf/app_config.yaml`

The corresponding configuration is as follows:

```yaml
logging:
  file:
    enable: true
    level: INFO
    path: logs
    rotation: "10 MB"
    retention: "7 days"
  console:
    enable: true
    level: INFO
```

The design idea here is very worth understanding clearly first: logs can ultimately have two "output destinations": `console`: output to the console; `file`: output to a log file.

And the role of `enable` is to determine whether this output channel is enabled.

If broken down further, these fields can be understood as follows:

- `level`: Sets the minimum log level for this output channel
- `path`: Specifies the log file directory
- `rotation`: Specifies at what size a new file should be created
- `retention`: Specifies how long logs are retained

The two parameters that are most likely to be unfamiliar at first are `rotation` and `retention`.

- `rotation: "10 MB"`: Indicates that when the log file reaches approximately 10MB, it should automatically split into a new file
- `retention: "7 days"`: Indicates that only logs from the most recent 7 days are retained

Why are these two parameters needed? Because if you keep writing to the same file, the log file will grow larger and larger, making it inconvenient to inspect; if logs are never cleaned up, disk space will eventually be slowly consumed. Therefore, these two parameters actually address the **maintainability issues of log files during long-term operation**.

### 3.4 Encapsulating Logging Configuration

Corresponding project file path: `shopkeeper-agent/app/core/log.py`

The code is as follows:

```python
import sys
from pathlib import Path

from loguru import logger

from app.conf.app_config import app_config
from app.core.context import request_id_ctx_var

# 统一日志展示格式，包含时间、级别、请求 ID 和调用位置等关键信息
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<magenta>request_id - {extra[request_id]}</magenta> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


# 通过 Loguru patch 钩子，把上下文中的 request_id 写入每条日志的 extra 字段
def inject_request_id(record):
    request_id = request_id_ctx_var.get()
    record["extra"]["request_id"] = request_id


# 移除 Loguru 默认的输出目标，避免和项目自定义配置重复打印
logger.remove()

# 生成带 request_id 注入能力的 logger，后续业务代码统一使用这个实例
logger = logger.patch(inject_request_id)

# 根据配置决定是否输出控制台日志，适合本地开发和容器标准输出采集
if app_config.logging.console.enable:
    logger.add(
        sink=sys.stdout,
        level=app_config.logging.console.level,
        format=log_format,
    )

# 根据配置决定是否写入文件日志，并在启动时确保日志目录存在
if app_config.logging.file.enable:
    path = Path(app_config.logging.file.path)
    path.mkdir(parents=True, exist_ok=True)
    logger.add(
        sink=path / "app.log",
        level=app_config.logging.file.level,
        format=log_format,
        rotation=app_config.logging.file.rotation,
        retention=app_config.logging.file.retention,
        encoding="utf-8",
    )

```

#### 3.4.1 What This Layer of Encapsulation Does

Without looking at the details first, this logging encapsulation code mainly unifies four types of capabilities:

1. Define a unified log format
2. Decide whether logs output to the console or to a file
3. Enable or disable different output channels based on the configuration file
4. Automatically add `request_id` to each log entry

Therefore, the focus here is not "how to print a log entry", but: **how to make the logging capability a reusable piece of infrastructure for the entire backend project**.

#### 3.4.2 The Role of logger.remove() and logger.add(...)

The reason `loguru` is "ready to use out of the box" is that it comes with a set of default configurations. Therefore, if a project wants to use its own log format and output strategy, the first step usually involves doing:

```python
logger.remove()
```

Its role is: **first remove the default logging configuration**.

Then, through:

```python
logger.add(...)
```

Add our own output channels back. In other words, the overall logic here is:

```text
移除默认配置
  -> 判断是否启用 console
  -> 判断是否启用 file
  -> 分别添加自己的日志输出规则
```

The core goal of this logging capability is "configurability". It is not hardcoded to "always print to the console", nor is it hardcoded to "always output to a file"; instead, it lets users determine through the configuration file which output channels to enable.

#### 3.4.3 Log Format Design

In this section, the most worthwhile part to examine carefully is actually `log_format`.

```python
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<magenta>request_id - {extra[request_id]}</magenta> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
```

This is not just arbitrarily concatenating a string; it is defining: **what each log entry should ultimately look like**.

Several of these fields are the most important:

- `{time:YYYY-MM-DD HH:mm:ss.SSS}`: Time
- `{level: <8}`: Log level, aligned to a fixed width
- `{name}`: Module name
- `{function}`: Function name
- `{line}`: Line number
- `{message}`: Specific log content
- `{extra[request_id]}`: Additionally injected request identifier

What this addresses is a very practical problem: without a unified format, logs are only "readable"; but with these fields, logs become "useful for troubleshooting".

#### 3.4.4 request_id Injection Mechanism

Corresponding project file path: `shopkeeper-agent/app/core/context.py`

```python
from contextvars import ContextVar

request_id_ctx_var = ContextVar("request_id", default="1")
```

In the logging module, it is written into the log's `extra` field through the following logic:

```python
def inject_request_id(record):
    request_id = request_id_ctx_var.get()
    record["extra"]["request_id"] = request_id
```

This layer is very important. In concurrent scenarios, if multiple requests are running at the same time, logs will be interleaved. Without a unified identifier, it is very difficult to string together all logs belonging to "the same request".

Therefore, the role of `request_id` can be summarized in one sentence: **used to link all logs related to the same request into a single chain.**

This is also why the current project's log format specifically added:

```python
<magenta>request_id - {extra[request_id]}</magenta>
```

#### 3.4.5 File Log Output Strategy

```python
path = Path(app_config.logging.file.path)
path.mkdir(parents=True, exist_ok=True)
logger.add(
    sink=path / "app.log",
    level=app_config.logging.file.level,
    format=log_format,
    rotation=app_config.logging.file.rotation,
    retention=app_config.logging.file.retention,
    encoding="utf-8",
)
```

What it expresses is:

- First read the log directory from the configuration file
- If the directory does not exist, create it automatically
- Then write logs to `app.log` in this directory
- At the same time, apply the previously configured level, format, splitting strategy, and retention strategy

The design intention here is actually very clear: **not just to make the logging system work, but to make it work stably over the long term.**

---

**Chapter Summary:**

- For the **Embedding** part, the core is to connect the four layers of **models, inference services, client encapsulation, and business calls**.
- For the **MySQL** part, the core is to clarify the division of labor among **SQLAlchemy, Engine, Session, and the Session factory**.
- For the **logging** part, the core is to understand **why formal projects need unified logging configuration, and why `request_id` is important**.
- Up to this point, the foundational services of `Qdrant / Elasticsearch / Embedding / MySQL / 日志` have basically been connected, and we can now continue into the construction chain of the metadata knowledge base.

The next article will formally enter the **metadata knowledge base** section, starting with the overall goals, script entry points, configuration structure, and code layering, to first establish the main thread of "how metadata is organized, how it is built, and why it is designed this way".
