# Part 1: Introduction, CV & Projects (1–20)

### 1. Tell me about yourself.
I am Md. Omar Faruk, a Python Django Backend Developer. I work with Python, Django, Django REST Framework, PostgreSQL, REST APIs, JWT authentication, and Django ORM. I enjoy building secure and efficient backend applications.

### 2. What are your technical skills?
My technical skills include Python, Django, Django REST Framework, PostgreSQL, SQL, REST APIs, JWT authentication, Git, and database management.

### 3. Why did you choose Python?
I chose Python because it has simple syntax, a large ecosystem, and powerful frameworks for web development and automation.

### 4. Why do you want to become a backend developer?
I enjoy working with business logic, databases, APIs, authentication, and server-side application architecture.

### 5. What is your main responsibility as a backend developer?
My main responsibilities include implementing business logic, designing APIs, managing databases, handling authentication, and ensuring application security and performance.

### 6. Describe your Django project.
I have worked on Django-based applications involving backend logic, database models, REST APIs, authentication, and CRUD operations.

### 7. What is a CRUD operation?
CRUD stands for Create, Read, Update, and Delete. These are the four basic operations for managing data.

### 8. What is your role in a project?
My role is to develop backend features, design database models, build REST APIs, implement authentication, and test application functionality.

### 9. What challenges have you faced in a project?
Common challenges include debugging errors, optimizing database queries, validating user input, and handling authentication securely.

### 10. How do you solve technical problems?
I reproduce the issue, inspect logs and error messages, identify the root cause, implement a solution, and test the result.

### 11. What is clean code?
Clean code is readable, maintainable, well-organized code that is easy to understand and modify.

### 12. What is debugging?
Debugging is the process of identifying, analyzing, and fixing errors in a program.

### 13. What is version control?
Version control tracks changes to source code and helps developers collaborate safely.

### 14. What is Git?
Git is a distributed version control system used to track code changes and manage development history.

### 15. What is GitHub?
GitHub is a platform for hosting Git repositories and collaborating on software projects.

### 16. What is teamwork?
Teamwork means collaborating with others, communicating clearly, sharing responsibilities, and working toward a common goal.

### 17. How do you learn new technologies?
I read official documentation, build small projects, practice coding, and apply what I learn to practical problems.

### 18. What are your strengths?
My strengths include problem-solving, willingness to learn, attention to detail, and commitment to writing maintainable code.

### 19. What is your weakness?
I sometimes spend extra time exploring different solutions, so I am improving my ability to prioritize tasks and manage time effectively.

### 20. Why should we hire you?
I have a solid foundation in Python and Django backend development, and I am eager to contribute, solve problems, and grow with the team.

# Part 2: Python Fundamentals (21–50)

### 21. What is Python?
Python is a high-level, general-purpose programming language known for its readable syntax and extensive ecosystem.

### 22. What are the main features of Python?
Python is dynamically typed, cross-platform, object-oriented, and supports multiple programming paradigms.

### 23. Is Python interpreted or compiled?
Python source code is typically compiled into bytecode and executed by the Python runtime. The exact implementation depends on the Python implementation.

### 24. What is a variable?
A variable is a name that refers to an object in Python.

### 25. What is dynamic typing?
Dynamic typing means variable names do not require explicit type declarations, and the types of objects are determined at runtime.

### 26. What are Python's built-in data types?
Common built-in types include int, float, complex, bool, str, list, tuple, range, set, frozenset, dict, and NoneType.

### 27. What is the difference between a list and a tuple?
A list is mutable, while a tuple is immutable.

### 28. What is the difference between a list and a set?
A list maintains sequence order and allows duplicates. A set stores unique elements and does not guarantee positional order.

### 29. What is a dictionary?
A dictionary stores data as key-value pairs.

### 30. What is mutability?
Mutability is the ability of an object to change after it has been created.

### 31. What are mutable objects?
Lists, dictionaries, and sets are common mutable objects.

### 32. What are immutable objects?
Integers, floats, strings, and tuples are common immutable types. A tuple may still contain references to mutable objects.

### 33. What is the difference between == and is?
The == operator compares values, while is checks object identity.

### 34. What is type casting?
Type casting converts a value from one data type to another, such as int("10").

### 35. What is None in Python?
None represents the absence of a value.

### 36. What is indentation in Python?
Indentation defines code blocks and is required for statements such as functions, loops, and conditional blocks.

### 37. What is PEP 8?
PEP 8 is Python's style guide for writing readable and consistent code.

### 38. What are comments?
Comments explain code and are ignored during normal Python execution.

### 39. What is slicing?
Slicing extracts part of a sequence using syntax such as sequence[start:stop:step].

### 40. What is negative indexing?
Negative indexing accesses sequence elements from the end, such as items[-1].

### 41. What is a truthy value?
A truthy value evaluates to True in a Boolean context.

### 42. What is a falsy value?
Falsy values include False, None, numeric zero, and empty collections or strings.

### 43. What is the difference between break and continue?
break exits a loop, while continue skips the current iteration and proceeds to the next one.

### 44. What is pass?
pass is a placeholder statement that performs no operation.

### 45. What is the range() function?
range() produces an immutable sequence of integers commonly used in loops.

### 46. What is enumerate()?
enumerate() returns an iterator of index-value pairs from an iterable.

### 47. What is zip()?
zip() combines elements from multiple iterables into tuples, stopping when the shortest iterable is exhausted by default.

### 48. What is a module?
A module is a Python file containing code such as functions, classes, and variables.

### 49. What is a package?
A package organizes related Python modules under a common namespace.

### 50. What is __name__ == "__main__"?
It checks whether a Python file is being run as the main program rather than imported as a module.

# Part 3: Functions and Scope (51–75)

### 51. What is a function?
A function is a reusable block of code that performs a particular task.

### 52. What is a parameter?
A parameter is a variable defined in a function's signature.

### 53. What is an argument?
An argument is a value passed to a function when it is called.

### 54. What is the difference between return and print?
return sends a value back to the caller, while print() displays output.

### 55. What are positional arguments?
Positional arguments are matched to parameters based on their position.

### 56. What are keyword arguments?
Keyword arguments pass values by explicitly naming the parameters.

### 57. What is *args?
*args allows a function to receive additional positional arguments as a tuple.

### 58. What is **kwargs?
**kwargs allows a function to receive additional keyword arguments as a dictionary.

### 59. What is a default parameter?
A default parameter has a predefined value used when the caller omits that argument.

### 60. Why should mutable default arguments be avoided?
Mutable defaults are shared between calls. Use None and create a new mutable object inside the function when needed.

### 61. What is a lambda function?
A lambda function is a small anonymous function consisting of a single expression.

### 62. What is recursion?
Recursion occurs when a function calls itself to solve a problem.

### 63. What is a base case?
A base case is the condition that stops recursive calls.

### 64. What is variable scope?
Variable scope determines where a name can be accessed in a program.

### 65. What is a local variable?
A local variable is defined inside a function and is generally accessible within that function's scope.

### 66. What is a global variable?
A global variable is defined at module level.

### 67. What is the global keyword?
The global keyword allows a function to reassign a module-level variable.

### 68. What is the nonlocal keyword?
The nonlocal keyword allows a nested function to reassign a variable in an enclosing function scope.

### 69. What is a closure?
A closure is a function that retains access to variables from its enclosing scope.

### 70. What is a decorator?
A decorator wraps a function or class to add or modify behavior without directly changing the original implementation.

### 71. What is a higher-order function?
A higher-order function accepts functions as arguments, returns a function, or both.

### 72. What is map()?
map() applies a function to each item of an iterable and returns an iterator.

### 73. What is filter()?
filter() returns an iterator containing items that satisfy a specified condition.

### 74. What is a docstring?
A docstring is a string used to document a module, class, or function.

### 75. What is function annotation?
Function annotations provide metadata about parameters and return values; Python does not automatically enforce them.

# Part 4: Object-Oriented Programming (76–100)

### 76. What is OOP?
Object-Oriented Programming organizes software around objects that combine data and behavior.

### 77. What is a class?
A class is a blueprint for creating objects.

### 78. What is an object?
An object is an instance of a class.

### 79. What is __init__()?
__init__() initializes an object's state after it has been created.

### 80. What is self?
self refers to the current instance inside an instance method.

### 81. What are the four pillars of OOP?
The four pillars are encapsulation, inheritance, polymorphism, and abstraction.

### 82. What is encapsulation?
Encapsulation combines data and methods and helps control access to an object's internal state.

### 83. What is inheritance?
Inheritance allows a class to reuse or extend behavior from another class.

### 84. What is polymorphism?
Polymorphism allows different objects to respond to the same interface in different ways.

### 85. What is abstraction?
Abstraction exposes essential functionality while hiding implementation details.

### 86. What is method overriding?
Method overriding occurs when a subclass provides its own implementation of an inherited method.

### 87. What is method overloading?
Method overloading means using the same method name with different parameter signatures. Python does not support traditional signature-based overloading directly, but alternatives exist.

### 88. What is multiple inheritance?
Multiple inheritance allows a class to inherit from more than one parent class.

### 89. What is super()?
super() provides access to methods from a parent class according to Python's method resolution order.

### 90. What is a class variable?
A class variable is defined on a class and is shared through the class unless shadowed by an instance attribute.

### 91. What is an instance variable?
An instance variable stores data associated with a particular object.

### 92. What is a class method?
A class method receives the class as its first argument and is declared using @classmethod.

### 93. What is a static method?
A static method belongs to a class namespace but receives neither self nor cls automatically.

### 94. What is an abstract class?
An abstract class defines an interface or shared behavior that subclasses are expected to implement.

### 95. What is an interface?
An interface describes expected behavior that different implementations can provide. Python commonly uses abstract base classes and protocols for this purpose.

### 96. What is composition?
Composition builds a class by combining objects of other classes.

### 97. What is aggregation?
Aggregation is a relationship where one object references another object that can exist independently.

### 98. What is MRO?
Method Resolution Order defines the order Python follows when searching for methods in an inheritance hierarchy.

### 99. What is a magic method?
A magic method, such as __str__() or __len__(), enables an object to work with Python's built-in operations and protocols.

### 100. What is the difference between __str__() and __repr__()?
__str__() provides a user-friendly representation, while __repr__() aims to provide a useful developer-oriented representation.

# Part 5: Exceptions, Iterators and Memory (101–120)

### 101. What is an exception?
An exception is an event that interrupts normal program execution when an error or exceptional condition occurs.

### 102. What is exception handling?
Exception handling manages errors using try, except, else, and finally.

### 103. What is finally?
The finally block runs during normal completion and exception propagation, making it useful for cleanup.

### 104. What is raise?
raise explicitly raises an exception.

### 105. What is a custom exception?
A custom exception is a user-defined exception class, usually derived from Exception.

### 106. What is an iterator?
An iterator is an object that returns items one at a time using __next__() and supports the iterator protocol.

### 107. What is an iterable?
An iterable is an object that can provide an iterator, usually through iter().

### 108. What is a generator?
A generator produces values lazily, commonly using yield.

### 109. What is yield?
yield produces a value from a generator and suspends its execution until it resumes.

### 110. What is the difference between return and yield?
return ends a function call, while yield produces a value and suspends a generator's execution.

### 111. What is a generator expression?
A generator expression creates a generator using syntax similar to a comprehension, such as (x*x for x in numbers).

### 112. What is list comprehension?
List comprehension creates a list using a concise expression, such as [x*x for x in numbers].

### 113. What is shallow copy?
A shallow copy creates a new outer object but retains references to nested objects.

### 114. What is deep copy?
A deep copy recursively copies nested objects where supported, using copy.deepcopy().

### 115. What is garbage collection?
Garbage collection reclaims memory occupied by objects that are no longer needed; CPython primarily uses reference counting plus cyclic garbage collection.

### 116. What is reference counting?
Reference counting tracks how many references point to an object and can reclaim objects when the count reaches zero.

### 117. What is memory management in Python?
Python manages object memory automatically through its memory management system and garbage collection mechanisms.

### 118. What is the difference between del and None?
del removes a reference or binding, while assigning None replaces a variable's current reference with None.

### 119. What is a context manager?
A context manager manages setup and cleanup around a block of code, commonly using the with statement.

### 120. What is the with statement?
The with statement uses a context manager to ensure resources are managed appropriately, including cleanup when exceptions occur.

# Part 6: Concurrency and Advanced Python (121–140)

### 121. What is a process?
A process is an executing program with its own process-level resources and memory space.

### 122. What is a thread?
A thread is an execution path within a process that shares the process's memory.

### 123. What is multithreading?
Multithreading runs multiple threads within one process and is often useful for I/O-bound workloads.

### 124. What is multiprocessing?
Multiprocessing runs multiple processes and can provide CPU parallelism.

### 125. What is the GIL?
In standard CPython builds with the GIL enabled, only one thread at a time executes Python bytecode within a process.

### 126. What is a daemon thread?
A daemon thread does not keep the Python process alive when no non-daemon threads remain.

### 127. What is a race condition?
A race condition occurs when the result depends on the timing or order of concurrent operations.

### 128. What is a lock?
A lock coordinates access to shared resources to prevent conflicting concurrent operations.

### 129. What is deadlock?
Deadlock occurs when tasks wait indefinitely for resources held by each other.

### 130. What is asynchronous programming?
Asynchronous programming allows tasks to yield control while waiting for operations, enabling other tasks to make progress.

### 131. What is async?
async defines a coroutine function when used with def.

### 132. What is await?
await suspends a coroutine until an awaitable operation produces a result.

### 133. What is asyncio?
asyncio is Python's library for concurrent programming using async and await, especially for I/O-bound tasks.

### 134. What is a coroutine?
A coroutine is an asynchronous computation that can suspend and resume execution.

### 135. What is synchronous programming?
Synchronous programming executes operations in sequence, where each operation may block further execution until it completes.

### 136. What is the difference between concurrency and parallelism?
Concurrency manages multiple tasks in overlapping periods, while parallelism executes multiple tasks simultaneously.

### 137. What is a thread-safe operation?
A thread-safe operation behaves correctly when accessed concurrently by multiple threads.

### 138. What is a queue?
A queue is a data structure that commonly follows FIFO order.

### 139. What is a stack?
A stack is a data structure that follows LIFO order.

### 140. What is a hash function?
A hash function maps an input to a hash value used by structures such as dictionaries and sets.

# Part 7: Django Fundamentals (141–160)

### 141. What is Django?
Django is a high-level Python web framework for building secure and maintainable web applications.

### 142. What is MVT architecture?
MVT stands for Model, View, and Template. Models manage data, views handle request logic, and templates manage presentation.

### 143. What is a Django project?
A Django project contains the settings and configuration for a complete Django application.

### 144. What is a Django app?
A Django app is a modular component that implements a specific feature or group of related features.

### 145. What is settings.py?
settings.py contains project configuration such as installed apps, middleware, database settings, and security options.

### 146. What is urls.py?
urls.py defines URL patterns that route incoming requests to views.

### 147. What is a Django model?
A Django model is a Python class that defines data structure and database behavior.

### 148. What is a Django view?
A Django view processes an HTTP request and returns an HTTP response.

### 149. What is a Django template?
A Django template generates presentation output, commonly HTML, using template syntax.

### 150. What is Django middleware?
Middleware processes requests and responses globally as they pass through Django's request-response cycle.

### 151. What is Django ORM?
Django ORM provides a Python API for querying and modifying database data.

### 152. What is a migration?
A migration records schema changes and applies them to the database.

### 153. What is makemigrations?
makemigrations creates migration files based on model changes.

### 154. What is migrate?
migrate applies unapplied migrations to the database.

### 155. What is Django admin?
Django admin is a built-in interface for managing registered models and their data.

### 156. What is a QuerySet?
A QuerySet represents a collection of database queries and results; it is generally evaluated lazily.

### 157. What is lazy evaluation in Django ORM?
A QuerySet usually does not execute its database query until its results are needed.

### 158. What is a Django signal?
A signal allows a receiver to respond when a particular event occurs in Django.

### 159. What is a Django manager?
A manager provides the interface used to perform database queries for a model.

### 160. What is Django authentication?
Django authentication provides functionality for user identification, password management, and permission integration.

# Part 8: Django REST Framework (161–180)

### 161. What is DRF?
Django REST Framework is a toolkit for building REST APIs with Django.

### 162. What is serialization?
Serialization converts complex objects into representations such as JSON-compatible data.

### 163. What is deserialization?
Deserialization converts incoming data into Python-native or validated data suitable for application processing.

### 164. What is a serializer?
A serializer converts data representations and validates incoming data.

### 165. What is ModelSerializer?
ModelSerializer automatically generates serializer fields and common behavior from a Django model.

### 166. What is APIView?
APIView is a DRF class-based view that provides request parsing, authentication, permissions, and HTTP method handlers.

### 167. What is GenericAPIView?
GenericAPIView extends APIView with common functionality such as queryset and serializer handling.

### 168. What is a ViewSet?
A ViewSet groups related API actions into a single class.

### 169. What is a ModelViewSet?
ModelViewSet provides common CRUD actions for a model-backed API, subject to configuration and permissions.

### 170. What is a router in DRF?
A router automatically generates URL patterns for registered ViewSets.

### 171. What is authentication in DRF?
Authentication identifies the credentials associated with a request.

### 172. What are permissions in DRF?
Permissions determine whether an authenticated or anonymous request is allowed to perform an action.

### 173. What is JWT authentication?
JWT authentication uses JSON Web Tokens as credentials for API requests.

### 174. What is pagination in DRF?
Pagination splits API results into smaller pages or chunks.

### 175. What is filtering in DRF?
Filtering restricts API results according to specified query parameters or filter rules.

### 176. What is throttling in DRF?
Throttling limits request rates according to configured policies.

### 177. What is API versioning?
API versioning allows an API to evolve while supporting clients using different versions.

### 178. What is a custom permission?
A custom permission implements application-specific access rules, often by overriding permission methods.

### 179. What is a validation error?
A validation error indicates that incoming data does not satisfy the required rules.

### 180. How do you secure a DRF API?
I use proper authentication, permissions, serializer validation, HTTPS, rate limiting where appropriate, and secure handling of secrets.

# Part 9: Database and SQL (181–190)

### 181. What is PostgreSQL?
PostgreSQL is an open-source relational database management system.

### 182. What is a primary key?
A primary key uniquely identifies a row in a table.

### 183. What is a foreign key?
A foreign key establishes a relationship between tables and helps enforce referential integrity.

### 184. What is normalization?
Normalization organizes database tables to reduce unnecessary duplication and improve data integrity.

### 185. What is an SQL JOIN?
A JOIN combines rows from related tables using a matching condition.

### 186. What is a database index?
An index improves the speed of certain queries at the cost of additional storage and write overhead.

### 187. What is a database transaction?
A transaction groups database operations into a logical unit that can be committed or rolled back.

### 188. What are ACID properties?
ACID stands for Atomicity, Consistency, Isolation, and Durability.

### 189. What is the N+1 query problem?
The N+1 query problem occurs when fetching related data causes an additional query for many individual records.

### 190. How do you optimize database performance?
I inspect query plans and logs, add appropriate indexes, reduce unnecessary queries, use select_related() and prefetch_related(), and measure performance.

# Part 10: APIs, Security, Testing and Deployment (191–200)

### 191. What is REST?
REST is an architectural style for designing networked applications around resources and a uniform interface.

### 192. What is HTTP?
HTTP is an application-layer protocol used for communication between clients and servers.

### 193. What is the difference between PUT and PATCH?
PUT generally replaces a resource, while PATCH updates selected fields.

### 194. What is HTTP status code 200?
200 OK indicates that the request succeeded.

### 195. What is HTTP status code 201?
201 Created indicates that the request successfully created a resource.

### 196. What is HTTP status code 400?
400 Bad Request indicates that the server cannot process the request because of a client-side request problem.

### 197. What is HTTP status code 401?
401 Unauthorized indicates that valid authentication credentials are missing or invalid.

### 198. What is HTTP status code 403?
403 Forbidden indicates that the server refuses to authorize the request.

### 199. What is unit testing?
Unit testing checks individual functions or components to verify that they behave as expected.

### 200. How do you deploy a Django application?
I configure environment variables, set DEBUG=False, configure allowed hosts and HTTPS, use a production-ready WSGI or ASGI server, configure the database and static files, and set up logging and monitoring.
