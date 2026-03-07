class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Shivam@0837@db.ajzfmzjiicjcafqyjtqy.supabase.co:5432/postgres"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"sslmode": "require"}
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
