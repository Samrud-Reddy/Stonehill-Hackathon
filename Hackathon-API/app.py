from fastapi import FastAPI, HTTPException
import functions
import functions.encryption
import functions.regex
import functions.db

app = FastAPI()

@app.post("/api/user/loginUser/")
def login(phone_number: str, upi_id: str, upi_pin: str):
    
    if functions.regex.validate_login(phone_number=phone_number,
                                      upi_id=upi_id):
        
        final_pin, salt = functions.encryption.salt_hash_pin(upi_pin=upi_pin)
        print(final_pin)
        
        functions.db.user_exists(phone_number=phone_number, upi_id=upi_id,
                                 balance=100.0, pin=final_pin, salt=salt)
        
        result = functions.encryption.create_jwt_token(phone_number=phone_number,
                                              upi_id=upi_id)
        
        raise HTTPException(status_code=404, detail=f"{result}")
        
@app.post("/api/user/transactions/makeTransaction/")
def send_money(jwt_token: str, amount: float, sender_phone_num: str = None, receiver_phone_num: str = None, 
               sender_upi: str = None, receiver_upi: str = None):
    
    if functions.encryption.validate_jwt_token(jwt_token=jwt_token):
        
        functions.db.send_money(
            amount=amount,
            sender_phone_num=sender_phone_num,
            receiver_phone_num=receiver_phone_num,
            sender_upi=sender_upi,
            receiver_upi=receiver_upi
            )

        raise HTTPException(status_code=200, detail="Transaction succesful.")
    
    else:
        
        raise HTTPException(status_code=404, detail="JWT Token Expired.")
    
@app.post("/api/user/validatePIN/")
def validate_pin(salted_pin: int):
    
    result = functions.db.pin_exists(salted_pin=salted_pin)
    if result:
        raise HTTPException(status_code=200, detail="Pin exists.")
    else:
        raise HTTPException(status_code=404, detail="Pin is not correct.")
    
@app.post("/api/user/checkBalance/")
def check_balance(phone_number: int):
    balance = functions.db.check_balance(phone_number=phone_number)
    return {"balance": f"{balance}"}