import asyncio
from gemini_webapi import GeminiClient
from gemini_webapi.constants import Model

# Replace "COOKIE VALUE HERE" with your actual cookie values.
# Leave Secure_1PSIDTS empty if it's not available for your account.
Secure_1PSID = "g.a000twhSwMgHGW9897YmZyt-lf2kYc_fuAz-oJJQW07JEG1q13BlrYcFK1e1rWS_pp3e9ynPGgACgYKAaQSARMSFQHGX2MiNx9HlVfXCmdXvlkSHeL-mBoVAUF8yKo7m2FhiLTSRguq8O_g02wr0076"
Secure_1PSIDTS = "sidts-CjIBEJ3XVwzCA1yWn-FAPG7WcDclS8ZsiTscgPA6rXFx5Xps6EtbSDvt1BqKQXx2U-xyQBAA"

async def main():
    # If browser-cookie3 is installed, simply use `client = GeminiClient()`
    client = GeminiClient(Secure_1PSID, Secure_1PSIDTS, proxy=None)
    await client.init(timeout=30, auto_close=False, close_delay=300, auto_refresh=True)
    
    response1 = await client.generate_content(
        "Who is shambhavi!",
        model=Model.G_2_0_FLASH,
    )
    print(f"{response1.text}")


asyncio.run(main())