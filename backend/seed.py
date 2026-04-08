import asyncio
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGO_DB_CONNECTION_URL")
DB_NAME = os.getenv("DB_NAME")

flashcards = [
    # ─── EASY (34 cards) ─────────────────────────────────────
    {
        "question": "What is horizontal scaling?",
        "answer": "Adding more machines to handle increased load (scaling out). Opposite of vertical scaling which upgrades existing hardware.",
        "category": "Scalability",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is vertical scaling?",
        "answer": "Upgrading the existing machine with more CPU, RAM, or storage (scaling up). Simpler but has a physical limit.",
        "category": "Scalability",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a CDN?",
        "answer": "A Content Delivery Network is a distributed network of servers that delivers content to users from the nearest location, reducing latency.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is latency?",
        "answer": "The time it takes for a request to travel from the client to the server and back. Measured in milliseconds.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is throughput?",
        "answer": "The number of requests a system can handle per unit of time. Often measured in requests per second (RPS).",
        "category": "Scalability",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a load balancer?",
        "answer": "A server that distributes incoming network traffic across multiple backend servers to ensure no single server is overwhelmed.",
        "category": "Scalability",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is caching?",
        "answer": "Storing copies of frequently accessed data in fast storage (like RAM) to reduce database load and improve response times.",
        "category": "Performance",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between SQL and NoSQL?",
        "answer": "SQL uses structured tables with fixed schemas and supports joins. NoSQL uses flexible document, key-value, or graph models — better for unstructured or rapidly changing data.",
        "category": "Databases",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is an API?",
        "answer": "An Application Programming Interface defines how software components communicate. REST and GraphQL are common API styles for web services.",
        "category": "Fundamentals",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a microservice?",
        "answer": "An architectural style where an application is built as small, independently deployable services that each handle a specific business function.",
        "category": "Architecture",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is DNS?",
        "answer": "Domain Name System translates human-readable domain names (google.com) into IP addresses that computers use to communicate.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a reverse proxy?",
        "answer": "A server that sits in front of backend servers, forwarding client requests to them. Used for load balancing, SSL termination, and caching.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is availability in system design?",
        "answer": "The percentage of time a system is operational. Often expressed as '9s' — 99.9% means ~8.7 hours downtime per year.",
        "category": "Fundamentals",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a monolithic architecture?",
        "answer": "An application where all components (UI, business logic, data layer) are tightly coupled and deployed as a single unit.",
        "category": "Architecture",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is TCP vs UDP?",
        "answer": "TCP is connection-oriented, guarantees delivery and order — used for web, email. UDP is connectionless, faster but no delivery guarantee — used for video streaming, gaming.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is HTTP vs HTTPS?",
        "answer": "HTTP is plain-text communication. HTTPS encrypts data using TLS/SSL, preventing eavesdropping and man-in-the-middle attacks. Always use HTTPS in production.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is bandwidth?",
        "answer": "The maximum amount of data that can be transmitted over a network connection per unit of time. Measured in Mbps or Gbps. Different from latency.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is ACID in databases?",
        "answer": "Atomicity (all or nothing), Consistency (data stays valid), Isolation (transactions don't interfere), Durability (committed data persists). Properties of reliable database transactions.",
        "category": "Databases",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a primary key?",
        "answer": "A unique identifier for each record in a database table. Cannot be null. Ensures each row can be uniquely identified and referenced.",
        "category": "Databases",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a foreign key?",
        "answer": "A field in one table that references the primary key of another table, establishing a relationship between the two tables.",
        "category": "Databases",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is authentication vs authorization?",
        "answer": "Authentication verifies who you are (login). Authorization determines what you're allowed to do (permissions). AuthN comes before AuthZ.",
        "category": "Security",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a container?",
        "answer": "A lightweight, isolated package that includes an app and all its dependencies. Docker is the most popular container platform. Ensures consistent environments across dev and prod.",
        "category": "Infrastructure",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is serverless architecture?",
        "answer": "A model where developers write functions and a cloud provider (AWS Lambda, GCP Cloud Functions) handles server management, scaling, and billing per invocation.",
        "category": "Architecture",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is polling?",
        "answer": "A technique where a client repeatedly requests data from a server at regular intervals to check for updates. Simple but inefficient — WebSockets or long polling are better alternatives.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a thread pool?",
        "answer": "A collection of pre-created threads ready to execute tasks. Avoids the overhead of creating/destroying threads per request. Used in web servers to handle concurrent requests.",
        "category": "Performance",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a VPN?",
        "answer": "A Virtual Private Network creates an encrypted tunnel between a client and server, masking the user's IP and securing traffic over public networks.",
        "category": "Security",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a session in web applications?",
        "answer": "A server-side mechanism to persist user state across multiple requests. A session ID is stored in a cookie on the client and maps to data stored on the server.",
        "category": "Security",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a cookie?",
        "answer": "A small piece of data stored in the browser by a website. Used to persist state (e.g., login sessions, preferences) across HTTP requests which are stateless by default.",
        "category": "Networking",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is idempotency?",
        "answer": "An operation is idempotent if calling it multiple times produces the same result as calling it once. GET and DELETE are idempotent. POST is not. Critical for safe retries.",
        "category": "Fundamentals",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a firewall?",
        "answer": "A security system that monitors and controls incoming/outgoing network traffic based on predefined rules. Can be hardware or software-based.",
        "category": "Security",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is an ORM?",
        "answer": "Object-Relational Mapping is a technique that lets you query and manipulate a database using an object-oriented language instead of raw SQL. Examples: SQLAlchemy, Hibernate, Prisma.",
        "category": "Databases",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is fault tolerance?",
        "answer": "A system's ability to continue operating correctly even when some components fail. Achieved through redundancy, replication, and failover mechanisms.",
        "category": "Fundamentals",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a queue data structure used for in system design?",
        "answer": "Queues decouple producers and consumers, buffer bursts of traffic, and enable async processing. A checkout system, for example, queues orders so the payment service isn't overwhelmed.",
        "category": "Architecture",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between concurrency and parallelism?",
        "answer": "Concurrency is dealing with multiple tasks at once (interleaving). Parallelism is executing multiple tasks simultaneously on multiple cores. Concurrency is about structure, parallelism is about execution.",
        "category": "Performance",
        "difficulty": "Easy",
        "flipped": False,
        "favourite": False
    },

    # ─── MEDIUM (33 cards) ───────────────────────────────────
    {
        "question": "What is the CAP Theorem?",
        "answer": "A distributed system can only guarantee 2 of 3: Consistency (all nodes see same data), Availability (system always responds), Partition Tolerance (works despite network failures).",
        "category": "Fundamentals",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is consistent hashing?",
        "answer": "A technique to distribute data across nodes so that when a node is added or removed, only a minimal number of keys need to be remapped. Used in distributed caches and databases.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is database sharding?",
        "answer": "Partitioning a database into smaller pieces (shards) spread across multiple servers. Each shard holds a subset of the data, enabling horizontal scaling.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is database replication?",
        "answer": "Copying data from one database server (primary) to one or more others (replicas) for redundancy, fault tolerance, and read scaling.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a message queue?",
        "answer": "A system that enables async communication between services by storing messages until the consumer is ready. Examples: RabbitMQ, AWS SQS, Kafka.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between a message queue and a pub/sub system?",
        "answer": "A queue delivers each message to one consumer. Pub/sub broadcasts each message to all subscribers. Kafka supports both patterns.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is eventual consistency?",
        "answer": "A consistency model where updates propagate to all nodes over time. The system becomes consistent eventually, but reads may temporarily return stale data.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is an LRU cache?",
        "answer": "Least Recently Used cache evicts the item that hasn't been accessed for the longest time when full. Common in Redis and in-memory caches.",
        "category": "Performance",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is rate limiting?",
        "answer": "Controlling how many requests a client can make in a given time window to prevent abuse. Common algorithms: token bucket, leaky bucket, sliding window.",
        "category": "Fundamentals",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between REST and GraphQL?",
        "answer": "REST uses fixed endpoints per resource. GraphQL uses a single endpoint where clients specify exactly what data they need, avoiding over-fetching and under-fetching.",
        "category": "Fundamentals",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a circuit breaker pattern?",
        "answer": "A design pattern that stops making requests to a failing service after a threshold is hit, allowing it time to recover. Prevents cascading failures in microservices.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is database indexing?",
        "answer": "A data structure (usually B-tree) that speeds up read queries at the cost of slower writes and extra storage. Without an index, queries require a full table scan.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is WebSocket and when do you use it?",
        "answer": "A protocol providing full-duplex communication over a single TCP connection. Used for real-time features like chat, live notifications, and collaborative editing.",
        "category": "Networking",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between process and thread?",
        "answer": "A process is an independent program with its own memory space. A thread is a unit of execution within a process, sharing memory with other threads.",
        "category": "Fundamentals",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a distributed lock?",
        "answer": "A mechanism ensuring only one node in a distributed system can access a shared resource at a time. Often implemented with Redis (SETNX) or ZooKeeper.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a Bloom filter?",
        "answer": "A probabilistic data structure that tests whether an element is in a set. Can return false positives but never false negatives. Space-efficient — used in caches and databases to avoid unnecessary lookups.",
        "category": "Performance",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is long polling?",
        "answer": "A technique where the client sends a request and the server holds it open until new data is available. More efficient than regular polling. Superseded by WebSockets for real-time apps.",
        "category": "Networking",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is OAuth?",
        "answer": "An open standard for access delegation. Allows users to grant third-party applications limited access to their resources without sharing passwords. Used in 'Login with Google/GitHub'.",
        "category": "Security",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a deadlock?",
        "answer": "A situation where two or more processes are waiting for each other to release resources, causing all to be stuck indefinitely. Prevented by lock ordering or timeouts.",
        "category": "Fundamentals",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is connection pooling?",
        "answer": "Reusing a pool of existing database connections rather than creating a new one per request. Reduces overhead and improves performance under high load.",
        "category": "Performance",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a hot spot in databases?",
        "answer": "When a disproportionate amount of traffic hits a single node or partition. Common in sharded databases when a shard key is poorly chosen (e.g., all writes go to the latest time-based shard).",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between synchronous and asynchronous communication?",
        "answer": "Synchronous: caller waits for a response before proceeding (HTTP). Asynchronous: caller sends a message and continues without waiting (message queues, events). Async improves resilience and scalability.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a service mesh?",
        "answer": "An infrastructure layer for managing service-to-service communication in microservices. Handles load balancing, service discovery, observability, and security. Examples: Istio, Linkerd.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a B-tree?",
        "answer": "A self-balancing tree data structure that maintains sorted data for O(log n) reads, inserts, and deletes. The primary data structure behind most database indexes.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is data partitioning?",
        "answer": "Dividing a database into parts to improve manageability and performance. Horizontal partitioning (sharding) splits rows; vertical partitioning splits columns into separate tables.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a fanout in system design?",
        "answer": "The process of pushing data to multiple destinations at once. In social media, fanout-on-write pre-computes timelines for all followers when a post is created.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a JWT?",
        "answer": "JSON Web Token is a compact, self-contained token for transmitting claims between parties. Contains header, payload, and signature. Used for stateless authentication in APIs.",
        "category": "Security",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between a cache hit and a cache miss?",
        "answer": "A cache hit occurs when requested data is found in cache (fast). A cache miss occurs when it's not found, requiring a slower database fetch. Hit rate is a key performance metric.",
        "category": "Performance",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a write-through vs write-behind cache?",
        "answer": "Write-through writes to cache and DB synchronously — consistent but slower. Write-behind writes to cache first, DB asynchronously — faster but risks data loss on crash.",
        "category": "Performance",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is service discovery?",
        "answer": "The mechanism by which microservices find each other's network locations. Can be client-side (client queries a registry) or server-side (load balancer queries registry). Tools: Consul, Eureka.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between strong and eventual consistency?",
        "answer": "Strong consistency guarantees all reads return the latest write — higher latency. Eventual consistency allows stale reads temporarily but offers better availability and performance.",
        "category": "Databases",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is an API gateway?",
        "answer": "A single entry point for all clients to a microservices backend. Handles routing, authentication, rate limiting, logging, and SSL termination. Examples: AWS API Gateway, Kong, Nginx.",
        "category": "Architecture",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a checksum?",
        "answer": "A value computed from data to detect errors or tampering. Sender computes and sends checksum with data; receiver recomputes and compares. Used in file transfers and data integrity checks.",
        "category": "Fundamentals",
        "difficulty": "Medium",
        "flipped": False,
        "favourite": False
    },

    # ─── HARD (34 cards) ─────────────────────────────────────
    {
        "question": "How would you design a URL shortener like bit.ly?",
        "answer": "Use Base62 encoding of an auto-incremented ID to generate short codes. Store mappings in a database with the short code as the key. Cache hot URLs in Redis. Use a load balancer for scale. Handle custom aliases separately.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a rate limiter?",
        "answer": "Use the token bucket algorithm stored in Redis. Each user key holds token count and last refill time. On each request, check and decrement tokens atomically using Lua scripts. Set TTL on keys to auto-expire idle users.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the two-phase commit protocol?",
        "answer": "A distributed transaction protocol: prepare phase (coordinator asks all nodes to confirm readiness) then commit phase (all nodes commit). Ensures atomicity but introduces latency and coordinator single point of failure.",
        "category": "Databases",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a notification system?",
        "answer": "Use Kafka to decouple producers and consumers. Separate consumers for push (FCM/APNs), email (SendGrid), SMS (Twilio). Store notification history in a database. Use a fanout service for group/broadcast notifications.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the SAGA pattern?",
        "answer": "A pattern for distributed transactions across microservices without 2PC. Each service performs a local transaction and publishes an event. On failure, compensating transactions undo previous steps. Two styles: choreography and orchestration.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a distributed cache?",
        "answer": "Use consistent hashing to distribute keys across nodes. Implement replication for fault tolerance. Handle cache invalidation with TTL and event-driven updates. Choose write-through or write-behind based on consistency needs.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between optimistic and pessimistic locking?",
        "answer": "Pessimistic locking acquires a lock before reading, blocking others. Optimistic locking reads without a lock but checks a version number before writing — retries if version changed. Optimistic is better for low-contention scenarios.",
        "category": "Databases",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a type-ahead search feature?",
        "answer": "Use a trie for prefix matching. Cache top-K results per prefix in Redis with a sorted set. Build an inverted index for full-text search. Use async indexing so writes don't block reads. Add ranking by popularity/recency.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is leader election in distributed systems?",
        "answer": "A process where nodes agree on a single coordinator. Algorithms: Bully (highest ID wins), Raft consensus. Tools like ZooKeeper and etcd provide battle-tested leader election. The leader handles writes; followers replicate.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a ride-sharing app like Uber?",
        "answer": "Use geospatial indexing (QuadTree or Google S2) for driver locations. WebSockets for real-time updates. A matching service pairs drivers and riders by proximity and ETA. Kafka handles trip events. Separate services for pricing, payments, and notifications.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is write-ahead logging (WAL)?",
        "answer": "Changes are written to a log before being applied to the database. Ensures durability and crash recovery — on restart, uncommitted transactions are rolled back. Used by PostgreSQL and most ACID-compliant databases.",
        "category": "Databases",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a distributed ID generator?",
        "answer": "Use Twitter's Snowflake approach: 64-bit ID composed of timestamp (41 bits) + datacenter ID (5 bits) + machine ID (5 bits) + sequence number (12 bits). Guarantees uniqueness and rough time-ordering without coordination.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design Twitter's news feed?",
        "answer": "Fanout-on-write for users with few followers: push tweets to all follower timelines in Redis on post. Fanout-on-read for celebrities: merge celebrity tweets at read time. Hybrid approach balances write amplification vs read latency.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a key-value store like Redis?",
        "answer": "Use a hash table for O(1) reads/writes. Support TTL with a min-heap for expiration. Persist with AOF (append-only file) or RDB snapshots. Use consistent hashing for distribution. Replicate asynchronously for read scaling.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the Raft consensus algorithm?",
        "answer": "A consensus algorithm where a leader is elected to manage log replication. Followers replicate the leader's log. On leader failure, an election is held. A candidate wins if it gets majority votes. Used in etcd and CockroachDB.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a video streaming service like YouTube?",
        "answer": "Store raw video in object storage (S3). Transcode to multiple resolutions using a worker queue. Serve via CDN for low latency. Use adaptive bitrate streaming (HLS/DASH). Separate metadata DB from video storage. Track views asynchronously.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a web crawler?",
        "answer": "Use a URL frontier (queue) seeded with initial URLs. Workers fetch pages, extract links, and add new URLs to the frontier. Deduplicate with a Bloom filter. Store crawled pages in object storage. Respect robots.txt and rate limits per domain.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a vector clock in distributed systems?",
        "answer": "A data structure tracking causality between events across nodes. Each node maintains a counter per node. Used to detect concurrent updates and resolve conflicts without a global clock. Used in Amazon Dynamo.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a chat application like WhatsApp?",
        "answer": "Use WebSockets for persistent connections. A message router directs messages to the right server. Store messages in Cassandra for scalability. Use a presence service to track online status. Implement end-to-end encryption with the Signal protocol.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a Merkle tree?",
        "answer": "A binary tree where each leaf is a hash of data and each parent is a hash of its children. Used in blockchains and distributed systems to efficiently verify data integrity and detect inconsistencies between replicas.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a payment system?",
        "answer": "Use idempotency keys to prevent duplicate charges. Implement SAGA pattern for distributed transactions (debit + credit). Store transactions in an append-only ledger. Use a queue for async processing. Partner with payment gateways (Stripe, Braintree). Comply with PCI-DSS.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design Google Maps?",
        "answer": "Use graph algorithms (Dijkstra/A*) on road network data. Tile-based map rendering served via CDN. Real-time traffic via aggregated GPS data from users. Geospatial indexing for search. Separate routing, rendering, and search into independent services.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is a time-series database?",
        "answer": "A database optimized for storing and querying data indexed by time. Supports efficient range queries, downsampling, and aggregations. Used for metrics, monitoring, and IoT. Examples: InfluxDB, TimescaleDB, Prometheus.",
        "category": "Databases",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you handle database schema migrations in a live system?",
        "answer": "Use expand-contract pattern: add new column (expand), backfill data, update app to use new column, then remove old column (contract). Never drop columns in the same deploy that stops using them. Use migration tools like Flyway or Alembic.",
        "category": "Databases",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a recommendation system?",
        "answer": "Use collaborative filtering (users with similar behavior) or content-based filtering (item attributes). Pre-compute recommendations offline using Spark/batch jobs. Store in a fast key-value store for low-latency reads. Update incrementally with streaming data.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between push and pull architecture?",
        "answer": "Push: server proactively sends data to clients (e.g. WebSockets, SSE). Pull: client requests data from server (e.g. REST polling). Push reduces latency but is harder to scale. Pull is simpler but less real-time.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a distributed file system like HDFS?",
        "answer": "Use a NameNode to store metadata (file→block mappings) and DataNodes to store actual blocks. Replicate each block 3x across different racks. Clients read block locations from NameNode then read directly from DataNodes.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the thundering herd problem?",
        "answer": "When a cache expires, many requests simultaneously hit the database causing a traffic spike. Solutions: mutex/lock on cache miss (only one request rebuilds), probabilistic early expiration, or background refresh before expiry.",
        "category": "Performance",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a monitoring and alerting system?",
        "answer": "Collect metrics via agents (Prometheus). Store in a time-series DB. Visualize with Grafana. Define alert rules with thresholds. Route alerts via PagerDuty/Slack. Use distributed tracing (Jaeger) for root cause analysis.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is backpressure in distributed systems?",
        "answer": "A mechanism where a downstream service signals to upstream producers to slow down when overwhelmed. Prevents cascading failures from overload. Implemented via queue size limits, rejection responses, or consumer-controlled pull.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design a search engine like Google?",
        "answer": "Web crawlers collect pages. An indexer builds an inverted index (word → list of documents). PageRank scores pages by inbound links. At query time, retrieve candidate docs from inverted index, rank by relevance + PageRank, return top results.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is quorum in distributed systems?",
        "answer": "The minimum number of nodes that must agree for an operation to succeed. In a 5-node cluster with quorum of 3: reads and writes need 3 confirmations. Ensures consistency even if some nodes fail. W + R > N guarantees overlap.",
        "category": "Architecture",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "How would you design an e-commerce flash sale system?",
        "answer": "Pre-load inventory count in Redis. Use atomic DECR to prevent overselling. Queue orders via Kafka for async processing. Use a waiting room (virtual queue) to control traffic spikes. Separate inventory service from order service.",
        "category": "System Design",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
    {
        "question": "What is the difference between structured, semi-structured, and unstructured data?",
        "answer": "Structured: fixed schema, stored in relational DBs (SQL tables). Semi-structured: flexible schema with tags/keys (JSON, XML, MongoDB). Unstructured: no predefined schema (images, videos, PDFs). Each requires different storage and querying strategies.",
        "category": "Databases",
        "difficulty": "Hard",
        "flipped": False,
        "favourite": False
    },
]

async def seed():
    client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())
    db = client[DB_NAME]

    await db.flashcards.delete_many({})
    print("Cleared all  existing flashcards")

    result = await db.flashcards.insert_many(flashcards)
    print(f" Inserted {len(result.inserted_ids)} flashcards")

    for level in ["Easy", "Medium", "Hard"]:
        count = sum(1 for c in flashcards if c["difficulty"] == level)
        print(f"   {level}: {count} cards")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed())