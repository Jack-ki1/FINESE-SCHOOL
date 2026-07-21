"""NoSQL databases subtopics — enriched schema."""

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
            "relationships, like social networks or fraud rings.\n\n"
            "Horizontal scaling — adding more machines to handle more load — is the core motivation behind "
            "most NoSQL designs, as opposed to vertical scaling (buying a bigger single machine), which "
            "relational databases historically leaned on more heavily. Horizontal scaling requires giving up "
            "some things that are easy on a single machine (like an efficient JOIN across arbitrary tables) in "
            "exchange for the ability to keep adding cheap commodity servers as load grows.\n\n"
            "None of this makes NoSQL strictly 'better' or 'more modern' than SQL — it's a different set of "
            "trade-offs, appropriate for specific access patterns and scale requirements, and a huge fraction "
            "of real-world applications are served perfectly well, indefinitely, by a well-indexed relational "
            "database and never need to reach for NoSQL at all."
        ),
        deep_dive=(
            "The distinction between SQL and NoSQL databases has blurred considerably over time: most "
            "relational databases now support native JSON columns (letting you store flexible, "
            "document-like data inside a normally structured table), and most NoSQL databases have added "
            "increasingly SQL-like query languages and even limited join support — 'NoSQL vs SQL' as a strict "
            "binary choice is less accurate today than 'which specific database's specific feature set and "
            "scaling model fits this specific workload.'\n\n"
            "Sharding (splitting a dataset across multiple machines based on some key, like customer ID) is "
            "central to how most NoSQL databases achieve horizontal scale, and the choice of shard key has "
            "enormous consequences — a poorly chosen shard key can concentrate load on one machine (a 'hot "
            "shard') while the rest sit relatively idle, effectively negating the benefit of having multiple "
            "machines at all.\n\n"
            "Multi-model databases (like PostgreSQL with its JSONB support, or databases explicitly designed "
            "to support multiple data models like ArangoDB) are an increasingly common middle ground, letting "
            "a single database serve relational, document, and sometimes graph-like access patterns without "
            "needing to run and synchronize multiple separate database systems."
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
        advanced_code=dict(
            lang="text",
            label="Why sharding makes some SQL features hard, conceptually",
            src=(
                "Single-machine relational DB:\n"
                "  All tables live together -> JOIN across any tables is cheap (same disk/memory)\n\n"
                "Sharded, horizontally-scaled DB:\n"
                "  Table A's rows split across machines 1, 2, 3 by shard key\n"
                "  Table B's rows split across machines 1, 2, 3 by a DIFFERENT shard key\n"
                "  -> JOINing A and B may require shuffling data across the network between machines\n"
                "  -> This is why many NoSQL/sharded systems limit or discourage arbitrary JOINs"
            ),
        ),
        example=(
            "A product catalog where every category has wildly different attributes (a book has an ISBN and "
            "page count, a TV has a screen size and refresh rate) is painful in a rigid SQL schema but natural "
            "as a MongoDB document, where each product document just carries whatever fields it needs."
        ),
        best_practices=[
            "Pick the NoSQL family based on your access pattern first, not the hype — 'What's my most common query?' beats 'What's popular?'",
            "Design the document/key structure around how you'll read the data, not how you'd normalize it in SQL.",
            "Keep an eye on document growth — MongoDB documents have a 16MB cap, and unbounded arrays inside a document are a common scaling mistake.",
            "Choose a shard key deliberately based on expected access patterns, since a poor choice can create a hot shard that bottlenecks the whole cluster.",
        ],
        pitfalls=[
            "Treating a document database like a relational one and still trying to JOIN across collections in application code for every request.",
            "Assuming NoSQL always means 'more scalable' — a well-indexed PostgreSQL table handles the vast majority of real workloads just fine.",
            "Choosing a shard key without considering access patterns, creating a hot shard that receives disproportionate load.",
        ],
        glossary=[
            dict(term="Horizontal scaling", definition="Handling more load by adding more machines, as opposed to vertical scaling (a bigger single machine)."),
            dict(term="Sharding", definition="Splitting a dataset across multiple machines based on a chosen key, central to how most NoSQL databases scale horizontally."),
            dict(term="Hot shard", definition="A shard receiving disproportionately high load due to a poorly chosen shard key, bottlenecking the whole cluster despite having multiple machines."),
            dict(term="Multi-model database", definition="A database supporting more than one data model (e.g. relational and document) within a single system."),
        ],
        faq=[
            dict(q="When would I pick MongoDB over PostgreSQL for a new project?", a="When your data genuinely has a flexible, evolving, nested shape that doesn't map cleanly to fixed tables (like wildly varying product attributes), and your access patterns rarely need complex joins across that data. For most standard business applications with well-defined relationships, PostgreSQL (including its JSONB support for flexible fields) remains a very strong default."),
            dict(q="Explain eventual consistency like I'm new to distributed systems.", a="It means that after a write, different replicas of the data might briefly show different (stale) values, but they're guaranteed to converge to the same value eventually, given no further writes. It trades strict, always-up-to-date consistency for higher availability and lower latency."),
            dict(q="What's the difference between a wide-column store and a document store?", a="A wide-column store (Cassandra) organizes data in tables with rows and columns optimized for very high write throughput across a cluster, designed around specific known queries. A document store (MongoDB) stores flexible, nested JSON-like documents per record, optimized for flexible schema and rich per-document structure rather than raw write throughput."),
        ],
        quiz=[
            dict(
                question="What is the primary motivation behind most NoSQL database designs?",
                options=["Making SQL syntax easier to learn", "Enabling horizontal scaling across many cheap machines", "Removing the need for indexes", "Eliminating the need for backups"],
                correct=1,
                explanation="NoSQL databases emerged largely to support horizontal scaling — handling growing load by adding more commodity machines rather than a single bigger one.",
            ),
        ],
        prompts=[
            "When would I pick MongoDB over PostgreSQL for a new project?",
            "Explain eventual consistency like I'm new to distributed systems.",
            "What's the difference between a wide-column store and a document store?",
            "How does sharding affect which queries are cheap versus expensive?",
        ],
    ),
    dict(
        id="document-stores-mongodb",
        title="Document Stores: MongoDB Basics",
        hook="MongoDB stores JSON-like documents in collections instead of rows in tables — schema lives with the data, not enforced by the database.",
        explanation=(
            "A MongoDB document is a BSON (binary JSON) object with fields that can be strings, numbers, "
            "arrays, or even nested sub-documents. Documents live inside collections (the rough equivalent of "
            "a table), and unlike SQL, two documents in the same collection don't need the same fields — a "
            "`users` collection can have some documents with a `phone` field and others without it.\n\n"
            "This flexibility is powerful for evolving applications (add a new field without a migration) but "
            "shifts responsibility for consistency onto the application. CRUD in MongoDB maps to `insertOne` / "
            "`find` / `updateOne` / `deleteOne`, and queries use a JSON-like filter syntax rather than SQL's "
            "`WHERE` clause.\n\n"
            "Schema validation, while not required by default, can still be added deliberately (`$jsonSchema` "
            "validators on a collection) for teams that want some of the safety of a fixed schema while "
            "keeping the general flexibility of the document model — a middle ground between 'anything goes' "
            "and a rigid relational schema.\n\n"
            "MongoDB's query language is expressive well beyond simple equality filters — comparison operators "
            "(`$gt`, `$lt`), logical combinators (`$and`, `$or`), array operators (`$in`, `$all`, `$elemMatch` "
            "for querying inside arrays of sub-documents), and text search are all supported directly in the "
            "filter document."
        ),
        deep_dive=(
            "Embedding versus referencing is the central data modeling decision in MongoDB, directly "
            "analogous to the normalization trade-offs in SQL but framed differently: embed data that's "
            "always read together and reasonably bounded in size (like a blog post's tags), reference "
            "(store an ID and look up separately) data that's shared across many documents or grows "
            "unbounded (like a blog post's potentially thousands of comments).\n\n"
            "Indexes work similarly in spirit to SQL — a `createIndex` on a frequently filtered or sorted "
            "field dramatically speeds up queries against it, and MongoDB supports compound indexes (on "
            "multiple fields), indexes on array fields (multikey indexes), and text indexes for basic full-"
            "text search, though it lacks some of the more sophisticated full-text capabilities of a dedicated "
            "search engine like Elasticsearch.\n\n"
            "Write concern and read concern settings let you tune MongoDB's consistency/durability trade-offs "
            "per operation — a write concern of `majority` waits for the write to be acknowledged by a "
            "majority of replica set members before considering it successful, trading some latency for "
            "stronger durability guarantees than the default, faster, less strict setting."
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
        advanced_code=dict(
            lang="javascript",
            label="Array querying and a compound index",
            src=(
                "// Find users who have BOTH \"admin\" and \"beta\" tags\n"
                "db.users.find({ tags: { $all: [\"admin\", \"beta\"] } })\n\n"
                "// Find orders with a line item over $100 in the \"electronics\" category\n"
                "db.orders.find({\n"
                "  items: { $elemMatch: { category: \"electronics\", price: { $gt: 100 } } }\n"
                "})\n\n"
                "db.orders.createIndex({ customerId: 1, orderDate: -1 })   // compound index"
            ),
        ),
        example=(
            "A blog platform storing a post with its comments embedded as an array inside the same document "
            "reads the entire post-plus-comments in a single query with no JOIN — the trade-off is that a post "
            "with 10,000 comments becomes an unwieldy single document, which is why embedding only makes sense "
            "for bounded, tightly-coupled data."
        ),
        best_practices=[
            "Embed data that's always read together and bounded in size; reference (store an ID) data that grows unbounded or is shared across documents.",
            "Create indexes on any field you filter or sort by — MongoDB will happily full-scan a collection without one.",
            "Use the aggregation pipeline (covered separately) for anything beyond simple filtering — it's MongoDB's answer to SQL's GROUP BY.",
            "Add schema validation for collections where some structural consistency matters, rather than relying purely on application-level discipline.",
        ],
        pitfalls=[
            "Embedding a comments array that grows without bound, eventually hitting MongoDB's 16MB document limit.",
            "Forgetting that MongoDB queries are case-sensitive and type-sensitive by default — `\"29\"` and `29` won't match the same filter.",
            "Skipping indexes on frequently queried fields, causing full collection scans that get slower as data grows.",
        ],
        glossary=[
            dict(term="Document", definition="A BSON (binary JSON) object representing one record in MongoDB, with fields that can vary between documents in the same collection."),
            dict(term="Collection", definition="A MongoDB grouping of documents, roughly analogous to a table in a relational database, but without an enforced fixed schema."),
            dict(term="Embedding", definition="Storing related data nested inside a parent document rather than in a separate, referenced document."),
            dict(term="Write concern", definition="A setting controlling how many replica set members must acknowledge a write before it's considered successful."),
        ],
        faq=[
            dict(q="Should I embed or reference this relationship in MongoDB?", a="Embed if the data is always read together with its parent and reasonably bounded in size (a handful to a few hundred items). Reference (store an ID, query separately) if the data is shared across multiple parent documents or could grow unbounded."),
            dict(q="Write an aggregation pipeline that groups orders by customer and sums totals.", a="See the dedicated MongoDB Aggregation Pipeline lesson for a full walkthrough — the short version uses $group with an _id of $customerId and a $sum accumulator on the total field."),
            dict(q="How do compound indexes work in MongoDB?", a="Similar to SQL: a compound index on multiple fields speeds up queries filtering on a leftmost prefix of those fields, in the order the index was created, and can also support efficient sorting on those same fields."),
        ],
        quiz=[
            dict(
                question="What's the main trade-off of embedding a large, unbounded array inside a MongoDB document?",
                options=["Nothing, embedding is always better", "It risks eventually hitting MongoDB's 16MB per-document size limit", "It makes queries faster with no downside", "MongoDB doesn't support arrays"],
                correct=1,
                explanation="Unbounded embedded arrays (like a growing comments list) can eventually push a single document past MongoDB's hard 16MB size cap, which is why unbounded, shared, or independently-growing data is usually referenced instead.",
            ),
        ],
        prompts=[
            "Should I embed or reference this relationship in MongoDB?",
            "Write an aggregation pipeline that groups orders by customer and sums totals.",
            "How do compound indexes work in MongoDB?",
            "Show me how to query for documents where an array field contains a specific value.",
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
            "restart, but Redis trades some durability guarantees for speed.\n\n"
            "Redis supports Pub/Sub messaging (publish messages to a channel, subscribe to receive them) and "
            "atomic operations on its richer data types (like `INCR` for atomic counters, or `SADD`/`SREM` for "
            "set membership), which are genuinely useful primitives for building rate limiters, real-time "
            "notification systems, and distributed locks without needing a separate messaging system for "
            "simple cases."
        ),
        deep_dive=(
            "Redis is fundamentally single-threaded for command execution (though newer versions have added "
            "some limited threading for I/O), which means individual commands are inherently atomic without "
            "needing explicit locking — but it also means one very slow command (like an unbounded `KEYS *` "
            "scan on a huge keyspace) can block every other client's requests until it completes, which is "
            "why `SCAN` (an incremental, non-blocking alternative) is preferred over `KEYS` in production.\n\n"
            "Redis Cluster distributes data across multiple Redis nodes using hash slots, giving horizontal "
            "scaling beyond a single machine's memory capacity — a meaningfully more complex setup than a "
            "single Redis instance, generally adopted only once a single node's memory or throughput genuinely "
            "becomes a bottleneck.\n\n"
            "Cache invalidation (deciding when cached data is stale and needs to be refreshed or removed) is "
            "widely considered one of the genuinely hard problems in software engineering — common strategies "
            "include TTL-based expiration (simple, but can serve stale data briefly), write-through caching "
            "(update the cache whenever the source of truth changes), and explicit invalidation on write, each "
            "with different trade-offs in complexity versus freshness guarantees."
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
        advanced_code=dict(
            lang="python",
            label="A leaderboard with sorted sets, and a simple rate limiter",
            src=(
                "# Leaderboard: sorted set keyed by score\n"
                "r.zadd(\"leaderboard\", {\"amara\": 4200, \"kito\": 3800})\n"
                "top_3 = r.zrevrange(\"leaderboard\", 0, 2, withscores=True)\n"
                "rank = r.zrevrank(\"leaderboard\", \"amara\")   # 0-indexed rank\n\n"
                "# Simple fixed-window rate limiter\n"
                "def is_allowed(user_id, limit=10, window_seconds=60):\n"
                "    key = f\"rate:{user_id}\"\n"
                "    count = r.incr(key)\n"
                "    if count == 1:\n"
                "        r.expire(key, window_seconds)\n"
                "    return count <= limit"
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
            "Use `SCAN` instead of `KEYS` in production, since `KEYS` blocks the single-threaded server until it completes on a large keyspace.",
            "Treat Redis as disposable cache unless you've explicitly configured and tested persistence and replication for your durability needs.",
        ],
        pitfalls=[
            "Using Redis as the system of record for critical data without understanding its persistence trade-offs.",
            "Running `KEYS *` (or a similarly unbounded pattern) against a large production keyspace, blocking every other client until it finishes.",
            "Storing huge values (multi-MB blobs) in Redis — it's optimized for many small, fast operations, not bulk storage.",
        ],
        glossary=[
            dict(term="TTL (Time To Live)", definition="How long a Redis key remains before automatically expiring and being removed."),
            dict(term="Sorted set", definition="A Redis data type storing unique members each associated with a numeric score, kept in sorted order — ideal for leaderboards and rankings."),
            dict(term="Cache invalidation", definition="Deciding when cached data is stale and needs to be refreshed or removed, widely regarded as a genuinely hard problem."),
        ],
        faq=[
            dict(q="When should I use Redis versus Memcached?", a="Redis supports richer data structures (lists, sets, sorted sets, hashes) and optional persistence, making it useful for more than pure caching (leaderboards, rate limiting, pub/sub). Memcached is simpler and purely an in-memory cache, which can be a reasonable, lighter-weight choice if you genuinely only need basic key-value caching."),
            dict(q="Explain Redis sorted sets with a leaderboard example.", a="A sorted set stores each member (like a player name) with an associated numeric score, automatically maintained in sorted order. ZADD adds/updates a member's score, ZREVRANGE fetches the top N by score, and ZREVRANK gets a specific member's rank — all in O(log N) time."),
            dict(q="How does Redis handle persistence, and what can I lose on a crash?", a="Redis offers RDB (periodic point-in-time snapshots) and AOF (append-only log of every write) persistence options, each with different trade-offs between performance and how much data you could lose since the last snapshot/log entry in a crash. Configured correctly, data loss can be minimized but Redis still generally trades some durability for its speed."),
        ],
        quiz=[
            dict(
                question="Why is KEYS * discouraged in production Redis?",
                options=["It's deprecated syntax", "Redis is single-threaded for commands, so a large KEYS scan blocks every other client until it finishes", "It only works on sorted sets", "It requires special permissions"],
                correct=1,
                explanation="Because Redis processes commands on a single thread, an unbounded KEYS scan over a large keyspace holds up every other client's requests until it completes — SCAN provides a non-blocking, incremental alternative.",
            ),
        ],
        prompts=[
            "When should I use Redis versus Memcached?",
            "Explain Redis sorted sets with a leaderboard example.",
            "How does Redis handle persistence, and what can I lose on a crash?",
            "Design a simple rate limiter using Redis.",
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
            "before it's considered successful.\n\n"
            "Cassandra has no single point of failure by design — every node is functionally equivalent (a "
            "peer-to-peer architecture, unlike a traditional primary/replica setup), and the cluster continues "
            "operating even if some nodes go down, as long as enough replicas remain available to satisfy the "
            "configured consistency level for a given operation."
        ),
        deep_dive=(
            "To model tables around queries, you typically start from the actual questions the application "
            "needs to answer ('get the last 10 sensor readings for a given sensor', 'get a user's recent "
            "orders') and design one table per question, often duplicating the same underlying data across "
            "multiple tables shaped for different queries — a deliberate trade-off of storage redundancy for "
            "query speed and simplicity, quite different from the normalization instincts SQL developers "
            "bring by default.\n\n"
            "Clustering columns (the columns after the partition key in the primary key definition) determine "
            "the sort order of rows *within* a partition, which is how Cassandra efficiently supports queries "
            "like 'give me the most recent readings for this sensor' — the data is already physically stored "
            "in that order on disk for each partition.\n\n"
            "Compaction is a background process that merges and reorganizes the SSTables (immutable on-disk "
            "data files) Cassandra accumulates from its append-only write pattern, reclaiming space from "
            "deleted/updated data — an operational detail that matters for capacity planning and can "
            "meaningfully affect read/write performance if not tuned appropriately for a given workload."
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
        advanced_code=dict(
            lang="sql",
            label="Query-first modeling: two tables for two different queries",
            src=(
                "-- Query 1: \"get a user's orders, most recent first\"\n"
                "CREATE TABLE orders_by_user (\n"
                "  user_id UUID,\n"
                "  order_time TIMESTAMP,\n"
                "  order_id UUID,\n"
                "  total DECIMAL,\n"
                "  PRIMARY KEY (user_id, order_time)\n"
                ") WITH CLUSTERING ORDER BY (order_time DESC);\n\n"
                "-- Query 2: \"look up one order by its ID\" -- SAME underlying data, different shape\n"
                "CREATE TABLE orders_by_id (\n"
                "  order_id UUID PRIMARY KEY,\n"
                "  user_id UUID,\n"
                "  order_time TIMESTAMP,\n"
                "  total DECIMAL\n"
                ");"
            ),
        ),
        example=(
            "An IoT platform ingesting millions of sensor readings per minute uses Cassandra because writes "
            "scale linearly by adding nodes, and the query pattern ('give me the last 10 readings for this "
            "sensor') maps directly onto a well-chosen partition key — the exact workload Cassandra was "
            "designed for."
        ),
        best_practices=[
            "Model tables around your queries, not your entities — it's normal to duplicate data across several tables optimized for different reads.",
            "Choose a partition key with high cardinality to avoid 'hot partitions' where one node gets overloaded.",
            "Use a tunable consistency level (e.g. QUORUM) that matches your actual durability needs instead of defaulting to the strictest or loosest setting.",
            "Design clustering columns to match your expected sort order needs, since data is physically stored in that order within each partition.",
        ],
        pitfalls=[
            "Designing Cassandra tables the way you would a normalized SQL schema, then discovering you can't query them efficiently.",
            "Picking a low-cardinality partition key (like `country`) that concentrates all writes for one value on a single node.",
            "Underestimating the operational overhead of tuning compaction and repair processes for a production Cassandra cluster.",
        ],
        glossary=[
            dict(term="Partition key", definition="The part of a Cassandra table's primary key that determines which node owns a given row, critical for both performance and even data distribution."),
            dict(term="Clustering column", definition="Columns after the partition key in the primary key, determining the sort order of rows within a partition."),
            dict(term="Query-first modeling", definition="Designing a table's structure around a specific known query pattern, often duplicating data across multiple tables for different queries."),
            dict(term="Tunable consistency", definition="Choosing, per operation, how many replicas must acknowledge a read or write before it's considered successful."),
        ],
        faq=[
            dict(q="What does query-first data modeling mean in Cassandra?", a="Instead of designing normalized tables around entities and joining them at query time (the SQL approach), you design a separate table for each specific query your application needs to run, often duplicating the same underlying data across multiple tables shaped for each query's access pattern."),
            dict(q="Explain tunable consistency (QUORUM vs ONE vs ALL) with an example.", a="ONE means only one replica needs to acknowledge for the operation to succeed (fastest, weakest guarantee). QUORUM means a majority of replicas must acknowledge (a common balance of speed and safety). ALL requires every replica to acknowledge (strongest guarantee, slowest, and least available if any replica is down)."),
            dict(q="Why doesn't Cassandra support JOINs, and how do you work around that?", a="JOINs across sharded, distributed data would require expensive cross-network data shuffling at query time, which conflicts with Cassandra's design goal of predictable, fast performance at massive scale. The workaround is denormalizing: storing pre-joined, query-shaped data across multiple purpose-built tables instead."),
        ],
        quiz=[
            dict(
                question="Why might a table using 'country' as its partition key perform poorly?",
                options=["Country codes aren't valid Cassandra data types", "It's a low-cardinality key that concentrates writes for popular countries onto a single node", "Cassandra doesn't support text partition keys", "It would violate ACID rules"],
                correct=1,
                explanation="A partition key with few distinct, unevenly-distributed values (like country) can create a hot partition where one node handles disproportionate load, undermining Cassandra's horizontal scaling.",
            ),
        ],
        prompts=[
            "What does query-first data modeling mean in Cassandra?",
            "Explain tunable consistency (QUORUM vs ONE vs ALL) with an example.",
            "Why doesn't Cassandra support JOINs, and how do you work around that?",
            "Design a Cassandra table for tracking a user's most recent 50 activity events.",
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
            "regardless of how large the overall dataset is.\n\n"
            "Nodes can have labels (like categories — `Person`, `Product`, `Company`) and arbitrary key-value "
            "properties, and relationships are always directed and typed (`:FOLLOWS`, `:PURCHASED`), which "
            "means a graph database query is fundamentally about describing a *pattern* to match against the "
            "graph, rather than filtering rows in a table."
        ),
        deep_dive=(
            "Index-free adjacency is the core architectural idea that makes graph traversal fast — each node "
            "directly stores pointers to its connected relationships, so following a relationship from one "
            "node to its neighbors is a direct memory/disk lookup rather than requiring an index scan the way "
            "a relational JOIN does. This is precisely why traversal performance in a graph database stays "
            "roughly constant regardless of overall graph size, while an equivalent multi-hop SQL query "
            "typically gets slower as the tables grow.\n\n"
            "Graph algorithms (shortest path, PageRank-style centrality, community detection) are natively "
            "supported by graph database platforms (often via a plugin library like Neo4j's Graph Data "
            "Science library), letting you run genuinely complex network analysis — 'who are the most "
            "influential nodes in this network' — as a built-in operation rather than something you'd have to "
            "hand-implement against a relational schema.\n\n"
            "Property graphs (Neo4j's model) are distinct from RDF triple stores (another graph database "
            "paradigm, common in semantic web / linked data contexts), which model everything as "
            "subject-predicate-object triples — both are 'graph databases' in a general sense but have "
            "meaningfully different query languages, tooling, and typical use cases."
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
        advanced_code=dict(
            lang="sql",
            label="Shortest path between two people in a social graph",
            src=(
                "MATCH path = shortestPath(\n"
                "  (a:Person {name: \"Amara\"})-[:FOLLOWS*..6]-(b:Person {name: \"Zuri\"})\n"
                ")\n"
                "RETURN path, length(path)\n\n"
                "-- *..6 limits the search to at most 6 hops, bounding an otherwise\n"
                "-- potentially expensive search on a large, densely-connected graph"
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
            "Bound multi-hop traversals with an explicit hop limit (like `*..6`) to avoid an unexpectedly expensive search on a large, densely-connected graph.",
        ],
        pitfalls=[
            "Using a graph database for simple lookups or aggregations that a relational database handles just as well with less operational overhead.",
            "Letting traversals run unbounded (no hop limit) on a large graph, which can turn a cheap query into an extremely expensive one.",
            "Confusing property graphs (Neo4j's model) with RDF triple stores, which have meaningfully different query languages and tooling.",
        ],
        glossary=[
            dict(term="Node", definition="An entity in a graph database, optionally labeled and carrying key-value properties."),
            dict(term="Relationship / edge", definition="A directed, typed connection between two nodes, which can also carry properties."),
            dict(term="Index-free adjacency", definition="A graph database's ability to follow a relationship via a direct pointer lookup rather than an index scan, keeping traversal fast regardless of overall graph size."),
            dict(term="Cypher", definition="Neo4j's pattern-matching query language, describing graph patterns to match rather than filtering table rows."),
        ],
        faq=[
            dict(q="Write a Cypher query to find the shortest path between two people in a social graph.", a="MATCH path = shortestPath((a:Person {name: 'X'})-[:FOLLOWS*..6]-(b:Person {name: 'Y'})) RETURN path — the *..6 bounds the search to at most 6 hops, which is important for performance on a large graph."),
            dict(q="When does a graph database outperform SQL, concretely?", a="Specifically on multi-hop relationship traversal queries — 'friends of friends', 'shortest connection between two entities', 'is there any path within N steps' — where SQL would require an escalating number of self-joins as the number of hops grows, while a graph database's traversal cost stays roughly constant per hop regardless of total graph size."),
            dict(q="How would you model a recommendation engine in Neo4j?", a="Model users, products, and interactions (PURCHASED, VIEWED, RATED) as nodes and relationships, then query patterns like 'products purchased by users who also purchased what I just bought' as a graph traversal — a natural fit for the relationship-first model."),
        ],
        quiz=[
            dict(
                question="What architectural feature makes graph traversal stay fast regardless of overall database size?",
                options=["Data compression", "Index-free adjacency -- direct pointers between connected nodes", "Automatic sharding", "In-memory storage only"],
                correct=1,
                explanation="Because each node directly references its relationships, following a connection is a direct lookup rather than an index scan, keeping traversal cost roughly constant per hop regardless of total graph size.",
            ),
        ],
        prompts=[
            "Write a Cypher query to find the shortest path between two people in a social graph.",
            "When does a graph database outperform SQL, concretely?",
            "How would you model a recommendation engine in Neo4j?",
            "Design a fraud-detection graph query connecting shared phone numbers or devices.",
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
            "might briefly return stale data).\n\n"
            "It's worth being precise that CAP theorem specifically describes behavior *during a network "
            "partition* — outside of a partition, a well-designed system can and generally does provide both "
            "consistency and availability simultaneously; the trade-off only forces a genuine choice when "
            "network communication between nodes actually breaks down."
        ),
        deep_dive=(
            "PACELC is a more complete refinement of CAP theorem, acknowledging that even without a partition "
            "(the 'else' in PACELC), there's still a trade-off between Latency and Consistency — a system can "
            "achieve stronger consistency by waiting for more replicas to confirm a write, at the cost of "
            "higher latency, or respond faster by not waiting, at the cost of weaker consistency guarantees. "
            "This framing is often more practically useful day-to-day than CAP alone, since partitions are "
            "relatively rare while the latency/consistency trade-off is present on essentially every write.\n\n"
            "'Eventual consistency' isn't one single guarantee — different systems provide different, more "
            "specific variants: read-your-own-writes consistency (guaranteeing you'll always see your own "
            "recent writes, even if other users might briefly see stale data), monotonic reads (guaranteeing "
            "you'll never see data go backward in time within your own session), and causal consistency "
            "(guaranteeing that causally related operations are seen in the correct order by everyone) are all "
            "meaningfully stronger, more specific guarantees than the bare minimum 'it'll converge "
            "eventually.'\n\n"
            "Conflict resolution strategies matter once you accept eventual consistency: last-write-wins "
            "(simplest, but can silently lose concurrent updates), vector clocks (tracking causality between "
            "updates to detect genuine conflicts), and CRDTs (Conflict-free Replicated Data Types, "
            "mathematically designed so concurrent updates always merge deterministically without conflicts) "
            "are all real, different approaches to the same underlying problem of reconciling divergent "
            "replicas."
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
        advanced_code=dict(
            lang="text",
            label="PACELC: the trade-off even without a partition",
            src=(
                "CAP:     if Partition -> choose Consistency OR Availability\n\n"
                "PACELC:  if Partition -> choose Consistency OR Availability (same as CAP)\n"
                "         Else (normal operation) -> choose Latency OR Consistency\n\n"
                "Example: waiting for 3 replicas to confirm a write (stronger consistency)\n"
                "         vs. confirming after 1 replica (lower latency, weaker consistency)\n"
                "         -- this trade-off exists on EVERY write, partition or not"
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
            "Consider PACELC's latency/consistency trade-off for day-to-day tuning decisions, not just CAP's partition-specific framing.",
        ],
        pitfalls=[
            "Assuming 'NoSQL' automatically means 'eventually consistent' — several NoSQL databases default to strong consistency.",
            "Building a feature that silently breaks under eventual consistency (e.g. 'like count must never decrease') without handling the edge case.",
            "Using naive last-write-wins conflict resolution for data where silently losing a concurrent update is genuinely unacceptable.",
        ],
        glossary=[
            dict(term="CAP theorem", definition="A distributed system can guarantee at most two of Consistency, Availability, and Partition tolerance simultaneously during a network partition."),
            dict(term="Eventual consistency", definition="A guarantee that replicas will converge to the same value over time, without guaranteeing every read reflects the most recent write immediately."),
            dict(term="PACELC", definition="An extension of CAP acknowledging a latency/consistency trade-off exists even outside of a network partition."),
            dict(term="CRDT (Conflict-free Replicated Data Type)", definition="A data structure mathematically designed so concurrent updates from different replicas always merge deterministically without conflicts."),
        ],
        faq=[
            dict(q="Explain CAP theorem using a real outage scenario.", a="If a network split separates a database cluster into two groups of nodes, each group has to decide: keep serving requests using potentially stale local data (favoring Availability), or refuse to serve requests until the partition heals and consistency can be guaranteed (favoring Consistency). You can't have perfectly fresh data AND guaranteed responses from both sides during the actual split."),
            dict(q="What's the difference between eventual consistency and strong consistency in practice?", a="Strong consistency guarantees every read reflects the most recent write immediately, everywhere, typically at some latency cost. Eventual consistency allows a brief window where different replicas might return different (stale) values after a write, in exchange for lower latency and higher availability."),
            dict(q="How does DynamoDB let me choose consistency per read?", a="DynamoDB offers both eventually consistent reads (default, faster, cheaper) and strongly consistent reads (opt-in per request, slightly higher latency and cost, guaranteed to reflect the most recent successful write) — letting you choose the right trade-off for each specific query rather than a single global setting."),
        ],
        quiz=[
            dict(
                question="According to CAP theorem, what must a distributed system choose between during a network partition?",
                options=["Speed and storage cost", "Consistency and Availability", "SQL and NoSQL", "Security and usability"],
                correct=1,
                explanation="Since partition tolerance is effectively mandatory for any real distributed system, CAP theorem's practical choice during an actual network partition is between Consistency and Availability.",
            ),
        ],
        prompts=[
            "Explain CAP theorem using a real outage scenario.",
            "What's the difference between eventual consistency and strong consistency in practice?",
            "How does DynamoDB let me choose consistency per read?",
            "What's the difference between CAP and PACELC, and why does it matter?",
        ],
    ),
]