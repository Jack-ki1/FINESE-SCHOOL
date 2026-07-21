"""NoSQL databases subtopics."""

SUBTOPICS = [
    dict(
        id="what-is-nosql",
        title="What Is NoSQL & Why It Exists",
        hook="NoSQL didn't replace SQL — it showed up because a handful of companies had data shapes and traffic patterns that rigid tables couldn't handle cheaply.",
        explanation=(
            "'NoSQL' is a loose umbrella term ('Not Only SQL') for databases that don't use the relational "
            "model of fixed tables, rows, and foreign keys. They emerged in the late 2000s at companies like "
            "Amazon (Dynamo) and Google (Bigtable) that needed to scale writes horizontally across hundreds of "
            "cheap servers, something relational databases of that era struggled with because JOINs and strict "
            "schemas don't shard cleanly.\n\n"
            "Instead of one model, NoSQL is really four different families solving different problems: document "
            "stores (MongoDB) for nested, evolving JSON-like records; key-value stores (Redis, DynamoDB) for "
            "ultra-fast lookups by a single key; wide-column stores (Cassandra, HBase) for massive write "
            "throughput across clusters; and graph databases (Neo4j) for data that's fundamentally about "
            "relationships, like social networks or fraud rings."
        ),
        code=dict(
            lang="text",
            label="The four NoSQL families at a glance",
            src=(
                "Document store   ->  MongoDB, Couchbase        ->  nested JSON documents, flexible schema\n"
                "Key-value store  ->  Redis, DynamoDB, Memcached ->  simple get(key) / set(key, value), extreme speed\n"
                "Wide-column      ->  Cassandra, HBase, Bigtable ->  billions of writes/sec across a cluster\n"
                "Graph            ->  Neo4j, Amazon Neptune      ->  nodes + edges, relationship-heavy queries"
            ),
        ),
        example=(
            "A product catalog where every category has wildly different attributes (a book has an ISBN and page "
            "count, a TV has a screen size and refresh rate) is painful in a rigid SQL schema but natural as a "
            "MongoDB document, where each product document just carries whatever fields it needs."
        ),
        best_practices=[
            "Pick the NoSQL family based on your access pattern first, not the hype — 'What's my most common query?' beats 'What's popular?'",
            "Design the document/key structure around how you'll read the data, not how you'd normalize it in SQL.",
            "Keep an eye on document growth — MongoDB documents have a 16MB cap, and unbounded arrays inside a document are a common scaling mistake.",
        ],
        pitfalls=[
            "Treating a document database like a relational one and still trying to JOIN across collections in application code for every request.",
            "Assuming NoSQL always means 'more scalable' — a well-indexed PostgreSQL table handles the vast majority of real workloads just fine.",
        ],
        prompts=[
            "When would I pick MongoDB over PostgreSQL for a new project?",
            "Explain eventual consistency like I'm new to distributed systems.",
            "What's the difference between a wide-column store and a document store?",
        ],
    ),
    dict(
        id="document-stores-mongodb",
        title="Document Stores: MongoDB Basics",
        hook="MongoDB stores JSON-like documents in collections instead of rows in tables — schema lives with the data, not enforced by the database.",
        explanation=(
            "A MongoDB document is a BSON (binary JSON) object with fields that can be strings, numbers, arrays, "
            "or even nested sub-documents. Documents live inside collections (the rough equivalent of a table), "
            "and unlike SQL, two documents in the same collection don't need the same fields — a `users` "
            "collection can have some documents with a `phone` field and others without it.\n\n"
            "This flexibility is powerful for evolving applications (add a new field without a migration) but "
            "shifts responsibility for consistency onto the application. CRUD in MongoDB maps to `insertOne` / "
            "`find` / `updateOne` / `deleteOne`, and queries use a JSON-like filter syntax rather than SQL's "
            "`WHERE` clause."
        ),
        code=dict(
            lang="javascript",
            label="Basic MongoDB CRUD (mongo shell / Node driver syntax)",
            src=(
                "// Insert\n"
                "db.users.insertOne({ name: \"Amara\", age: 29, tags: [\"admin\", \"beta\"] })\n\n"
                "// Find with a filter + projection\n"
                "db.users.find({ age: { $gte: 18 } }, { name: 1, _id: 0 })\n\n"
                "// Update a nested field\n"
                "db.users.updateOne(\n"
                "  { name: \"Amara\" },\n"
                "  { $set: { \"address.city\": \"Nairobi\" } }\n"
                ")\n\n"
                "// Delete\n"
                "db.users.deleteOne({ name: \"Amara\" })"
            ),
        ),
        example=(
            "A blog platform storing a post with its comments embedded as an array inside the same document reads "
            "the entire post-plus-comments in a single query with no JOIN — the trade-off is that a post with "
            "10,000 comments becomes an unwieldy single document, which is why embedding only makes sense for "
            "bounded, tightly-coupled data."
        ),
        best_practices=[
            "Embed data that's always read together and bounded in size; reference (store an ID) data that grows unbounded or is shared across documents.",
            "Create indexes on any field you filter or sort by — MongoDB will happily full-scan a collection without one.",
            "Use the aggregation pipeline (`$match`, `$group`, `$project`) for anything beyond simple filtering — it's MongoDB's answer to SQL's GROUP BY.",
        ],
        pitfalls=[
            "Embedding a comments array that grows without bound, eventually hitting MongoDB's 16MB document limit.",
            "Forgetting that MongoDB queries are case-sensitive and type-sensitive by default — `\"29\"` and `29` won't match the same filter.",
        ],
        prompts=[
            "Should I embed or reference this relationship in MongoDB?",
            "Write an aggregation pipeline that groups orders by customer and sums totals.",
            "How do compound indexes work in MongoDB?",
        ],
    ),
    dict(
        id="key-value-stores-redis",
        title="Key-Value Stores: Redis in Practice",
        hook="Redis keeps everything in memory and answers in sub-millisecond time — it's less a database and more a very fast, very simple dictionary that happens to persist to disk.",
        explanation=(
            "Redis stores data as key-value pairs where the value can be a plain string, but also a list, set, "
            "sorted set, hash, or stream — richer than a typical key-value store. Because everything lives in "
            "RAM, reads and writes are extremely fast (often under a millisecond), which is why Redis is the "
            "default choice for caching, session storage, rate limiting, and real-time leaderboards.\n\n"
            "Redis isn't meant to be your primary data store for everything — it's usually deployed alongside a "
            "relational or document database, absorbing the read traffic that would otherwise hammer the slower, "
            "disk-backed system. Persistence (RDB snapshots or an append-only file) protects against data loss on "
            "restart, but Redis trades some durability guarantees for speed."
        ),
        code=dict(
            lang="python",
            label="Caching a slow query result with Redis",
            src=(
                "import redis, json, time\n\n"
                "r = redis.Redis(host=\"localhost\", port=6379, decode_responses=True)\n\n"
                "def get_user_profile(user_id):\n"
                "    cache_key = f\"user:{user_id}\"\n"
                "    cached = r.get(cache_key)\n"
                "    if cached:\n"
                "        return json.loads(cached)\n\n"
                "    profile = expensive_db_lookup(user_id)   # e.g. a slow SQL join\n"
                "    r.setex(cache_key, 300, json.dumps(profile))  # cache for 5 minutes\n"
                "    return profile"
            ),
        ),
        example=(
            "A leaderboard for a game with millions of players uses a Redis sorted set (`ZADD`, `ZRANGE`) so "
            "'get the top 10 players' and 'get this player's rank' both resolve in O(log N) time, something a "
            "SQL `ORDER BY score DESC LIMIT 10` on a huge table struggles to do at the same latency under load."
        ),
        best_practices=[
            "Always set a TTL (`EXPIRE` / `SETEX`) on cache keys — an unbounded cache is a memory leak waiting to happen.",
            "Use Redis data structures (sorted sets, hashes) instead of storing serialized JSON blobs when you need to query part of the value.",
            "Treat Redis as disposable cache unless you've explicitly configured and tested persistence and replication for your durability needs.",
        ],
        pitfalls=[
            "Using Redis as the system of record for critical data without understanding its persistence trade-offs.",
            "Storing huge values (multi-MB blobs) in Redis — it's optimized for many small, fast operations, not bulk storage.",
        ],
        prompts=[
            "When should I use Redis versus Memcached?",
            "Explain Redis sorted sets with a leaderboard example.",
            "How does Redis handle persistence, and what can I lose on a crash?",
        ],
    ),
    dict(
        id="wide-column-cassandra",
        title="Wide-Column Stores: Cassandra Fundamentals",
        hook="Cassandra is built for one job above all else: absorb enormous, continuous write volume across many machines without a single point of failure.",
        explanation=(
            "Cassandra organizes data into tables with rows and columns, similar to SQL on the surface, but the "
            "critical design decision is the partition key — it determines which node in the cluster owns a "
            "given row. Every table is designed around its primary query pattern first, because Cassandra doesn't "
            "support ad-hoc JOINs or arbitrary WHERE clauses efficiently; you typically create a separate table "
            "per query shape, a practice called 'query-first modeling.'\n\n"
            "Writes are extremely fast because Cassandra appends to a commit log and an in-memory structure "
            "(memtable) rather than updating data in place, and it replicates data across multiple nodes with "
            "tunable consistency — you choose, per query, how many replicas must acknowledge a write or read "
            "before it's considered successful."
        ),
        code=dict(
            lang="sql",
            label="CQL — Cassandra Query Language",
            src=(
                "CREATE TABLE sensor_readings (\n"
                "  sensor_id  UUID,\n"
                "  reading_time TIMESTAMP,\n"
                "  temperature DOUBLE,\n"
                "  PRIMARY KEY (sensor_id, reading_time)\n"
                ") WITH CLUSTERING ORDER BY (reading_time DESC);\n\n"
                "-- Fast because it targets one partition (sensor_id)\n"
                "SELECT * FROM sensor_readings\n"
                "WHERE sensor_id = 123e4567-e89b-12d3-a456-426614174000\n"
                "LIMIT 10;"
            ),
        ),
        example=(
            "An IoT platform ingesting millions of sensor readings per minute uses Cassandra because writes scale "
            "linearly by adding nodes, and the query pattern ('give me the last 10 readings for this sensor') "
            "maps directly onto a well-chosen partition key — the exact workload Cassandra was designed for."
        ),
        best_practices=[
            "Model tables around your queries, not your entities — it's normal to duplicate data across several tables optimized for different reads.",
            "Choose a partition key with high cardinality to avoid 'hot partitions' where one node gets overloaded.",
            "Use a tunable consistency level (e.g. QUORUM) that matches your actual durability needs instead of defaulting to the strictest or loosest setting.",
        ],
        pitfalls=[
            "Designing Cassandra tables the way you would a normalized SQL schema, then discovering you can't query them efficiently.",
            "Picking a low-cardinality partition key (like `country`) that concentrates all writes for one value on a single node.",
        ],
        prompts=[
            "What does query-first data modeling mean in Cassandra?",
            "Explain tunable consistency (QUORUM vs ONE vs ALL) with an example.",
            "Why doesn't Cassandra support JOINs, and how do you work around that?",
        ],
    ),
    dict(
        id="graph-databases-neo4j",
        title="Graph Databases: Neo4j & Relationship-First Data",
        hook="When the interesting question is 'how are these things connected', a graph database answers it directly instead of forcing it through chains of JOINs.",
        explanation=(
            "A graph database stores data as nodes (entities) and edges (relationships), both of which can carry "
            "properties. Neo4j is the most widely used graph database, queried with Cypher, a pattern-matching "
            "language that reads almost like ASCII art: `(a)-[:FRIENDS_WITH]->(b)` describes a directed "
            "relationship between two nodes.\n\n"
            "The advantage over SQL shows up specifically on relationship-heavy, multi-hop queries — 'find friends "
            "of friends who like the same three bands' requires several self-JOINs in SQL, each one adding cost, "
            "while in a graph database traversing relationships is a constant-time pointer-following operation "
            "regardless of how large the overall dataset is."
        ),
        code=dict(
            lang="sql",
            label="Cypher — Neo4j's query language",
            src=(
                "// Create nodes and a relationship\n"
                "CREATE (a:Person {name: \"Amara\"})-[:FOLLOWS]->(b:Person {name: \"Kito\"})\n\n"
                "// Find friends-of-friends not already followed\n"
                "MATCH (me:Person {name: \"Amara\"})-[:FOLLOWS]->()-[:FOLLOWS]->(fof)\n"
                "WHERE NOT (me)-[:FOLLOWS]->(fof) AND fof <> me\n"
                "RETURN DISTINCT fof.name"
            ),
        ),
        example=(
            "A fraud detection system flags a new credit application by traversing the graph to see if the "
            "applicant's phone number, address, or device fingerprint connects to any known fraudulent account "
            "within two or three hops — a query that would require an unmanageable number of recursive SQL JOINs."
        ),
        best_practices=[
            "Model relationships as first-class, named, and directed (`:FOLLOWS`, `:PURCHASED`) — vague relationships make queries harder to write and read.",
            "Index node properties you'll search by directly (like an email or ID) so lookups don't require a full graph scan to find the starting node.",
            "Reach for a graph database specifically for traversal-heavy problems — recommendations, fraud rings, org charts — not as a general-purpose replacement for SQL.",
        ],
        pitfalls=[
            "Using a graph database for simple lookups or aggregations that a relational database handles just as well with less operational overhead.",
            "Letting traversals run unbounded (no hop limit) on a large graph, which can turn a cheap query into an extremely expensive one.",
        ],
        prompts=[
            "Write a Cypher query to find the shortest path between two people in a social graph.",
            "When does a graph database outperform SQL, concretely?",
            "How would you model a recommendation engine in Neo4j?",
        ],
    ),
    dict(
        id="cap-theorem-consistency",
        title="CAP Theorem & Consistency Models",
        hook="Every distributed database is making a trade-off you should be able to name — CAP theorem is the vocabulary for that trade-off.",
        explanation=(
            "CAP theorem states that a distributed system can only guarantee two of three properties at once "
            "during a network partition: Consistency (every read sees the latest write), Availability (every "
            "request gets a response), and Partition tolerance (the system keeps working despite network splits "
            "between nodes). Because networks do fail, partition tolerance is effectively mandatory for any "
            "distributed system, which really makes the choice a trade-off between consistency and availability "
            "when a partition happens.\n\n"
            "This is why MongoDB (configurable, but defaults toward consistency) behaves differently under a "
            "network split than Cassandra or DynamoDB (which default toward availability with 'eventual "
            "consistency' — every replica converges to the same value eventually, but a read right after a write "
            "might briefly return stale data)."
        ),
        code=dict(
            lang="text",
            label="Where common databases sit",
            src=(
                "Strong consistency, lower availability under partition:\n"
                "  -> PostgreSQL/MySQL (single primary), MongoDB (default read concern), HBase\n\n"
                "Eventual consistency, higher availability under partition:\n"
                "  -> Cassandra, DynamoDB, CouchDB, Riak\n\n"
                "Tunable (you choose per operation):\n"
                "  -> Cassandra consistency levels (ONE / QUORUM / ALL)"
            ),
        ),
        example=(
            "A shopping cart service favoring availability might let two data centers briefly disagree about "
            "cart contents during a network blip, then reconcile — annoying but recoverable. A bank ledger favors "
            "consistency because two data centers briefly disagreeing about an account balance is not acceptable "
            "at any cost."
        ),
        best_practices=[
            "Decide per feature, not per company, whether you need strong or eventual consistency — a single app can reasonably use both.",
            "Read your database's actual default consistency level; many NoSQL databases let you tune it per query, and the default isn't always what you'd assume.",
            "Design for eventual consistency explicitly (idempotent operations, conflict resolution) rather than hoping it never surfaces.",
        ],
        pitfalls=[
            "Assuming 'NoSQL' automatically means 'eventually consistent' — several NoSQL databases default to strong consistency.",
            "Building a feature that silently breaks under eventual consistency (e.g. 'like count must never decrease') without handling the edge case.",
        ],
        prompts=[
            "Explain CAP theorem using a real outage scenario.",
            "What's the difference between eventual consistency and strong consistency in practice?",
            "How does DynamoDB let me choose consistency per read?",
        ],
    ),
]
