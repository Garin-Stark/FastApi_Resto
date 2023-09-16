import datetime
import hashlib
from fastapi import APIRouter,Path
from config.db import conn
from models.database import *
from models.utilities import *
from schemas.controller import *
from sqlalchemy import select,func,join
import uuid

user = APIRouter()

# Endpoint untuk membuat pengguna baru (pelanggan)
@user.post("/api/users", tags=["users"])
async def create_user(user_input: UserInput):
    try:
        name = user_input.name
        email = user_input.email
        phone_number = user_input.phone_number

        # Generate unique ID for the new user
        user_id = str(uuid.uuid4())


        values = {
            "id": user_id,
            "name": name,
            "email": email,
            "phone_number": phone_number,
        }

        result = conn.execute(users.insert().values(values))
        return success(message="Proses Berhasil")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint untuk mendapatkan daftar pengguna (pelanggan)
@user.get("/api/users", tags=["users"])
async def get_users():
    try:
        query = users.select()
        result = conn.execute(query)
        users_list = [dict(row) for row in result]
        return success_data(message="Proses Berhasil", data=users_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint untuk mendapatkan pengguna (pelanggan) berdasarkan ID
@user.get("/api/users/{user_id}", tags=["users"])
async def get_user(user_id: str):
    try:
        query = users.select().where(users.c.id == user_id)
        result = conn.execute(query)
        user = result.fetchone()

        if user:
            return {"message": "Berhasil mengambil data pengguna", "data": dict(user)}
        else:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint untuk menambahkan restoran baru
@user.post("/api/restaurants", tags=["restaurants"])
async def create_restaurant(restaurant_input: RestaurantInput):
    try:
        name = restaurant_input.name
        location = restaurant_input.location

        values = {
            "name": name,
            "location": location,
        }
        result = conn.execute(restaurants.insert().values(values))
        return success(message="Proses Berhasil")
    except Exception as e:
        return bad_request(str(e))
    
# Endpoint untuk mendapatkan daftar restoran
@user.get("/api/restaurants", tags=["restaurants"])
async def get_restaurants():
    try:
        query = restaurants.select()
        result = conn.execute(query)
        restaurants_list = [dict(row) for row in result]
        return success_data(message="Proses Berhasil", data=restaurants_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Endpoint untuk menambahkan makanan ke dalam suatu restoran
@user.post("/api/foods", tags=["foods"])
async def create_food(food_input: FoodInput):
    try:
        name = food_input.name
        price = food_input.price
        description = food_input.description
        restaurant_id = food_input.restaurant_id

        values = {
            "name": name,
            "price": price,
            "description": description,
            "restaurant_id": restaurant_id,
        }
        result = conn.execute(foods.insert().values(values))
        return success(message="Proses Berhasil")
    except Exception as e:
        return bad_request(str(e))
    
# Endpoint untuk mendapatkan daftar makanan dari suatu restoran berdasarkan ID restoran
@user.get("/api/foods/{restaurant_id}", tags=["foods"])
async def get_foods_by_restaurant(restaurant_id: int = Path(..., title="ID Restoran")):
    try:
        query = foods.select().where(foods.c.restaurant_id == restaurant_id)
        result = conn.execute(query)
        foods_list = [dict(row) for row in result]
        return success_data(message="Proses Berhasil", data=foods_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint untuk membuat pemesanan 
@user.post("/api/bookings", tags=["bookings"])
async def create_booking(booking_input: BookingCreateInput):
    try:
        customer_id = booking_input.customer_id
        restaurant_id = booking_input.restaurant_id
        
        # Mendapatkan waktu saat ini sebagai booking time
        booking_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Mendapatkan nomor antrian
        # Contoh: Mengambil jumlah pemesanan untuk restoran ini
        count_query = select([func.count()]).where(bookings.c.restaurant_id == restaurant_id)
        count_result = conn.execute(count_query)
        guest_count = count_result.scalar() + 1  # Nomor antrian
        # Memeriksa apakah makanan yang dimasukkan tersedia di restoran
        for food_order in booking_input.foods:
            food_id = food_order.food_id
            food_query = select([foods]).where(foods.c.id == food_id, foods.c.restaurant_id == restaurant_id)
            food_result = conn.execute(food_query)
            food = food_result.fetchone()
            if not food:
                raise HTTPException(status_code=400, detail=f"Food with ID {food_id} is not available in the restaurant.")
        # Menyiapkan data untuk pemesanan
        booking_values = {
            "user_id": customer_id,
            "restaurant_id": restaurant_id,
            "booking_time": booking_time,
            "guest_count": guest_count,
        }
        
        # Memasukkan pemesanan ke dalam database
        result = conn.execute(bookings.insert().values(booking_values))
        
        # Mendapatkan ID pemesanan yang baru saja dibuat
        booking_id = result.lastrowid
        
        # Menyimpan makanan yang dipesan
        for food_item in booking_input.foods:
            food_values = {
                "booking_id": booking_id,
                "food_id": food_item.food_id,
                "quantity": food_item.quantity,
            }
            conn.execute(booking_foods.insert().values(food_values))
        
        return success(message="Proses Berhasil")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint untuk mendapatkan daftar pemesanan untuk pelanggan tertentu
@user.get("/api/bookings/{customer_id}", tags=["bookings"])
async def get_customer_bookings(customer_id: int):
    try:
        # Ambil daftar pemesanan untuk pelanggan tertentu
        query = select([bookings]).where(bookings.c.user_id == customer_id)
        result = conn.execute(query)
        bookings_list = [dict(row) for row in result]

        # Dapatkan makanan yang dipesan untuk setiap pemesanan
        for booking in bookings_list:
            booking_id = booking['id']
            food_query = select([foods.c.name, booking_foods.c.quantity]).\
                        select_from(join(booking_foods, foods, booking_foods.c.food_id == foods.c.id)).\
                        where(booking_foods.c.booking_id == booking_id)
            food_result = conn.execute(food_query)
            food_list = [{"food_name": row[0], "quantity": row[1]} for row in food_result]
            booking['foods'] = food_list
        return success_data(message="Proses Berhasil", data=bookings_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.post("/api/tickets", tags=["tickets"])
async def purchase_ticket(ticket_input: TicketPurchaseInput):
    try:
        # Mendapatkan waktu saat ini sebagai tanggal pembelian tiket
        purchase_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Simpan data tiket ke dalam database
        ticket_values = {
            "user_id": ticket_input.customer_id,
            "purchase_date": purchase_time,
            "validation_status": ticket_input.validation_status,
        }
        conn.execute(tickets.insert().values(ticket_values))
        
        return success(message="Proses Berhasil")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint untuk mendapatkan daftar tiket
@user.get("/api/tickets", tags=["tickets"])
async def get_tickets():
    try:
        # Ambil daftar tiket dari database
        query = select([tickets])
        result = conn.execute(query)
        tickets_list = [dict(row) for row in result]
        return success_data(message="Berhasil mengambil data ticket", data=tickets_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@user.get("/api/tickets/{customer_id}", tags=["tickets"])
async def get_tickets_by_customer(customer_id: int):
    try:
        # Ambil daftar tiket berdasarkan ID pelanggan
        query = select([tickets]).where(tickets.c.user_id == customer_id)
        result = conn.execute(query)
        tickets_list = [dict(row) for row in result]
        return success_data(message="Berhasil mengambil data ticket", data=tickets_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@user.put("/api/validate_ticket/{ticket_id}", tags=["tickets"])
async def validate_ticket(ticket_id: int):
    try:
        # Lakukan validasi tiket berdasarkan ID tiket
        # Misalnya, Anda dapat memeriksa apakah tiket tersebut ada dalam database
        # dan apakah masih valid berdasarkan tanggal pembelian dan status validasi

        # Di sini, kita akan anggap tiket valid jika ada dalam database dan statusnya "Menunggu Validasi"
        ticket_query = select([tickets]).where(tickets.c.id == ticket_id)
        ticket_result = conn.execute(ticket_query)
        ticket = ticket_result.fetchone()

        if ticket and ticket["validation_status"] == "Menunggu Validasi":
            # Tiket validasi berhasil, ubah status menjadi "Valid"
            conn.execute(tickets.update().where(tickets.c.id == ticket_id).values(validation_status="Valid"))
            return {"message": "Tiket berhasil divalidasi."}
        elif ticket and ticket["validation_status"] == "Valid":
            # Tiket sudah valid, tidak perlu divalidasi lagi
            return {"message": "Tiket sudah valid."}
        else:
            # Tiket tidak ditemukan atau status bukan "Menunggu Validasi"
            return {"message": "Tiket tidak valid untuk divalidasi."}, 400  # HTTP status code 400 for bad request
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))