from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
PG_NAME = env.str("PG_NAME")
PG_PASS = env.str("PG_PASS")
PG_HOST = env.str("PG_HOST")
DB_NAME = env.str("DB_NAME")

DB_URL = f"postgres://{PG_NAME}:{PG_PASS}@{PG_HOST}/{DB_NAME}"
