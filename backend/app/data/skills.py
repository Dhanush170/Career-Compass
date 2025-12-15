ALIASES = {
    # Cloud
    "amazon web services": "aws",
    "microsoft azure": "azure",
    "google cloud": "gcp",
    "google cloud platform": "gcp",

    # JS ecosystem
    "react.js": "react",
    "nextjs": "next.js",
    "vuejs": "vue",
    "nodejs": "node.js",
    "node js": "node.js",

    # ML/NLP
    "huggingface": "hugging face",
    "ml ops": "mlops",
    "scikit learn": "scikit-learn",

    # DevOps
    "k8s": "kubernetes",
    "ci/cd": "cicd",
    "ci cd": "cicd",

    # Databases
    "postgres": "postgresql",
    "ms sql": "sql server",
    "sqlserver": "sql server",

    # Frameworks
    "springboot": "spring boot",
    "asp.net core": "asp.net",
    "aspnet": "asp.net",

    # AI/LLM
    "rag pipeline": "rag",
    "bert model": "bert",
    "gpt model": "gpt",
}
TECH_SKILLS = {
    "languages": [
        # Major languages
        "c", "c++", "c#", "java", "python", "javascript", "typescript",
        "golang", "ruby", "php", "rust", "kotlin", "scala", "swift",
        "dart", "r", "perl",

        # Scripting
        "bash", "shell", "powershell",

        # Low-level & embedded
        "assembly", "vhdl", "verilog",

        # Functional
        "haskell", "clojure", "elixir", "erlang",
    ],

    "web_frontend": [
        "html", "css", "sass", "less",
        "react", "react.js", "next.js",
        "angular", "angularjs",
        "vue", "nuxt.js",
        "svelte", "sveltekit",
        "jquery", "bootstrap", "tailwind css", "material ui"
    ],

    "web_backend": [
        "node.js", "express", "fastify",
        "django", "flask", "fastapi",
        "spring", "spring boot",
        "asp.net", "asp.net core",
        "laravel", "codeigniter",
        "ruby on rails",
        "gin", "fiber",
    ],

    "mobile": [
        "android", "android studio", "kotlin", "java",
        "ios", "swift", "swiftui",
        "react native", "flutter", "dart",
        "ionic", "cordova"
    ],

    "cloud": [
        "aws", "amazon web services",
        "azure", "microsoft azure",
        "gcp", "google cloud", "google cloud platform",
        "digitalocean", "heroku", "vercel", "netlify",
        "firebase", "supabase", "openstack"
    ],

    "cloud_services": [
        # AWS
        "ec2", "s3", "lambda", "dynamodb", "rds", "api gateway",
        "cloudwatch", "cloudformation", "sns", "sqs", "eks",

        # Azure
        "azure functions", "azure devops", "cosmos db",

        # GCP
        "compute engine", "cloud run", "cloud functions",
        "bigquery", "pubsub"
    ],

    "devops": [
        "docker", "kubernetes", "k8s",
        "jenkins", "gitlab ci", "github actions", "circleci", "azure pipelines",
        "terraform", "ansible", "chef", "puppet",
        "argo cd", "helm",
        "nginx", "apache",
        "prometheus", "grafana", "splunk", "elk stack", "kibana",
        "sonarqube"
    ],

    "databases_sql": [
        "mysql", "postgresql", "sqlite",
        "mariadb", "oracle", "sql server",
        "redshift", "snowflake", "bigquery"
    ],

    "databases_nosql": [
        "mongodb", "redis", "dynamodb",
        "cassandra", "couchdb",
        "neo4j", "elasticsearch", "influxdb"
    ],

    "big_data": [
        "hadoop", "spark", "hive", "pig", "flink",
        "kafka", "kinesis", "zookeeper"
    ],

    "data_engineering": [
        "airflow", "dbt", "kafka connect",
        "databricks", "glue", "lake formation",
        "streamlit", "tableau", "power bi"
    ],

    "ml_frameworks": [
        "tensorflow", "pytorch", "keras",
        "scikit-learn", "xgboost", "lightgbm",
        "catboost"
    ],

    "nlp_ai": [
        "hugging face", "transformers", "langchain",
        "spacy", "nltk", "gensim",
        "openai", "llama", "bert", "gpt",
        "rag", "vector search", "chromadb", "milvus", "pinecone"
    ],

    "mlops": [
        "mlflow", "weights and biases", "wandb",
        "kubeflow", "dvc",
        "sagemaker"
    ],

    "cybersecurity": [
        "wireshark", "metasploit", "nmap", "burp suite",
        "nessus", "oscp", "owasp", "kali linux",
        "penetration testing", "ethical hacking"
    ],

    "testing": [
        "jest", "mocha", "chai",
        "pytest", "unittest",
        "selenium", "cypress", "junit"
    ],

    "networking": [
        "tcp/ip", "dns", "http", "https",
        "load balancing", "reverse proxy", "cdn"
    ],

    "api_technologies": [
        "rest api", "graphql", "grpc", "soap"
    ],

    "version_control": [
        "git", "github", "gitlab", "bitbucket"
    ],

    "operating_systems": [
        "linux", "ubuntu", "centos", "windows", "macos"
    ],

    "robotics_embedded": [
        "arduino", "raspberry pi", "ros",
        "embedded systems", "iot"
    ],

    "blockchain": [
        "solidity", "ethereum", "smart contracts",
        "web3", "polygon", "metamask"
    ],

    "game_engines": [
        "unity", "unreal engine"
    ],

    "monitoring_sre": [
        "prometheus", "grafana", "new relic", "datadog"
    ],

    "messaging": [
        "kafka", "rabbitmq", "activemq", "sqs", "pubsub"
    ]
}


def build_flat_skills():
    flat = {}
    for cat, items in TECH_SKILLS.items():
        for s in items:
            flat[s] = cat
    for a, canon in ALIASES.items():
        flat[a] = flat.get(canon, "other")
    return flat

FLAT_SKILLS = build_flat_skills()