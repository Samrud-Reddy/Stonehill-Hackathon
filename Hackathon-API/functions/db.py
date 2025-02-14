import sqlite3
from fastapi import HTTPException

db = sqlite3.connect("fastapi_db.sqlite", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    phone TEXT UNIQUE,
    upi_id TEXT UNIQUE,
    balance REAL NOT NULL,
    upi_pin TEXT UNIQUE,
    salt text UNIQUE
)
""")

db.commit()

def get_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user) 

def user_exists(phone_number: str, upi_id: str, balance: int, pin: int, salt: str) -> bool:
    
    try:
        
        cursor.execute("INSERT INTO users (phone, upi_id, balance, upi_pin, salt) VALUES (?, ?, ?, ?, ?)", (phone_number, upi_id, balance, pin, salt))
        db.commit()
        print("user doesn't exist")
        return 
    
    except sqlite3.IntegrityError:
        print("user exists")
        return
    
def pin_exists(salted_pin : int) -> bool:
    
    cursor.execute("SELECT balance FROM users WHERE upi_pin = ?", (salted_pin,))
    data = cursor.fetchone()
    if not data:
        return False
    else:
        return True
    
def check_balance(phone_number: int) -> bool:
    
    cursor.execute("SELECT balance FROM users WHERE phone = ?", (phone_number,))
    data = cursor.fetchone()
    return data
    
def send_money(amount: float, sender_phone_num: str = None, receiver_phone_num: str = None, 
               sender_upi: str = None, receiver_upi: str = None) -> bool:
        
        if sender_phone_num:
            cursor.execute("SELECT balance FROM users WHERE phone = ?", (sender_phone_num,))
            sender_data = cursor.fetchone()
        elif sender_upi:
            cursor.execute("SELECT balance FROM users WHERE upi_id = ?", (sender_upi,))
            sender_data = cursor.fetchone()
        else:
            raise HTTPException(status_code=404, detail="Sender phone number or UPI ID required.")
    
        if receiver_phone_num:
            cursor.execute("SELECT balance FROM users WHERE phone = ?", (receiver_phone_num,))
            receiver_data = cursor.fetchone()
        elif receiver_upi:
            cursor.execute("SELECT balance FROM users WHERE upi_id = ?", (receiver_upi,))
            receiver_data = cursor.fetchone()
        else:
            raise HTTPException(status_code=404, detail="Receiver phone or UPI ID required")
    
        if not sender_data:
            raise HTTPException(status_code=404, detail="Sender info not provided.")
        if not receiver_data:
            raise HTTPException(status_code=404, detail="Receiver info not provided.")
        if sender_data[0] < amount:
            raise HTTPException(status_code=404, detail="Insufficient balance.")
    
        if sender_phone_num:
            cursor.execute("UPDATE users SET balance = balance - ? WHERE phone = ?", (amount, sender_phone_num))
        else:
            cursor.execute("UPDATE users SET balance = balance - ? WHERE upi_id = ?", (amount, sender_upi))
    
        print("updated sender balance")
        cursor.execute("SELECT balance FROM users WHERE phone = ?", (sender_phone_num,))
        
        if receiver_phone_num:
            cursor.execute("UPDATE users SET balance = balance + ? WHERE phone = ?", (amount, receiver_phone_num))
        else:
            cursor.execute("UPDATE users SET balance = balance + ? WHERE upi_id = ?", (amount, receiver_upi))
    
        print("updated reciever balance")
        cursor.execute("SELECT balance FROM users WHERE phone = ?", (receiver_phone_num,))
        
        db.commit()
        
        return