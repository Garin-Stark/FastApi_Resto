from sqlalchemy import create_engine, MetaData

# Konfigurasi database
DB_NAME = "fastapi"
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "3306"  # Port default untuk MySQL

# Membuat URL koneksi
# Format: mysql+pymysql://username:password@host:port/nama_database
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Membuat engine
engine = create_engine(DATABASE_URL)

# Membuat objek MetaData
meta = MetaData()

# Membuat koneksi
conn = engine.connect()

# Sekarang Anda memiliki koneksi yang siap digunakan
# Lakukan operasi database sesuai kebutuhan
