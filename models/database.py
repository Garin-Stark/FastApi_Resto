
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

# Tabel Pelanggan
users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("phone_number", String(20)),
    Column("email", String(255)),
)

# Tabel Pemesanan
bookings = Table(
    "bookings",
    meta,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("restaurant_id", Integer, ForeignKey("restaurants.id")),
    Column("booking_time", String(255)),
    Column("guest_count", Integer),
    Column("status", String(20)),
)
# Tabel untuk mencatat makanan dalam suatu pemesanan
booking_foods = Table(
    "booking_foods",
    meta,
    Column("id", Integer, primary_key=True),
    Column("booking_id", Integer, ForeignKey("bookings.id")),
    Column("food_id", Integer, ForeignKey("foods.id")),
    Column("quantity", Integer),
)
# Tabel Makanan
foods = Table(
    "foods",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("price", Integer),
    Column("description", String(255)),
    Column("restaurant_id", Integer, ForeignKey("restaurants.id")),
)

# Tabel Tiket
tickets = Table(
    "tickets",
    meta,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("purchase_date", String(255)),
    Column("validation_status", String(20)),
)

# Tabel Restoran
restaurants = Table(
    "restaurants",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("location", String(255)),
)
meta.create_all(engine)
