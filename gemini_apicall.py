system_message = """You are a helpful assistant working on an online money transfer project in India. () You will get information from the text you have been given. From this, you will need to understand how much money the user wants to transfer and whether it is to a phone number or to a contact name. A phone number will have 10 digits and a contact name will be a name.

Return this information in JSON format 
{
        amount: money requested by user as just a number,
        recipient: phonenumber or contact name
        type: either phone, contact
}."""

import asyncio
from gemini_webapi import GeminiClient
from gemini_webapi.constants import Model

Secure_1PSID = ""
Secure_1PSIDTS = ""

async def main(text):
    client = GeminiClient(Secure_1PSID, Secure_1PSIDTS, proxy = None)
    await client.init(timeout = 30, auto_close = True, close_delay = 300, auto_refresh = True)
    
    global system_message

    prompt = system_message + text

    response1 = await client.generate_content(
        prompt,
        model = Model.G_2_0_FLASH,
    )

    return response1.text



