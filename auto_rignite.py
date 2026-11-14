"""
=============================================================================
 TOOL AUTO RIGNITE MINING (@RigniteBot) - CHẾ ĐỘ SIÊU TỐC NON-STOP 24/7
 - Dành riêng cho tài khoản: hungzai22
 - Tự động lấy x-init-data tươi mới qua Telethon Session (Không cần thủ công)
 - TÍNH NĂNG MỚI ĐỘT PHÁ:
   1. ĐÀO SIÊU TỐC QUÉT SẠCH NĂNG LƯỢNG (Count = 600):
      - 1 phát tap quét sạch toàn bộ năng lượng vừa hồi (600 - 6,000 Energy) trong 0.5s!
   2. HỒI PHỤC NĂNG LƯỢNG TỰ ĐỘNG THEO TỶ LỆ GAME (adEnergyRatio):
      - 30 lượt đầu ngày hồi 100% (+6,000 Energy).
      - Từ lượt 31 trở đi (hôm nay đã cày 488 lượt), game chuyển sang chế độ +10% (+600 Energy).
      - Bot tự động bắt nhịp: Hồi +600 Energy ➔ Tap 600 quét sạch trong 0.5s ➔ Hồi tiếp không nghỉ 10s!
   3. AUTO MINIGAME ĐẬP KIM CƯƠNG JACKPOT 10X (5/5 Lượt Perfect mỗi ngày):
      - Tự động gửi lệnh đạt điểm cao nhất "perfect" ăn trọn coins và săn Jackpot!
   4. AUTO ĐẤU TRƯỜNG PVP ARENA (5 Lượt đánh thắng 100% mỗi ngày):
      - Quét danh sách đối thủ, tự động chọn mục tiêu yếu hơn để 100% chiến thắng.
      - Thưởng: +1,000 RGT Coins & +25 Điểm Rank leo Top BXH thế giới!
   5. AUTO SPARK BOOST RANDOM (+15% Tốc độ đào mỏ miễn phí):
      - Tự động bắn tia năng lượng nhận hiệu ứng buff tăng tốc sản lượng.
   6. AUTO GOM TIỀN THUỘC ĐỊA, HỘP QUÀ, VÒNG QUAY, NHIỆM VỤ, ĐIỂM DANH LIÊN TỤC.
=============================================================================
"""

import os
import sys
import time
import json
import random
import re
import uuid
import asyncio
import urllib.parse
import requests
from colorama import Fore, Style, init

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import RequestWebViewRequest

init(autoreset=True)

# THÔNG TIN TELEGRAM API
API_ID = 39182276
API_HASH = "f02b155d895a3a3fbf8a1cbe810b5338"

# CẤU HÌNH RIGNITE
API_BASE = "https://api.rignite.app"
WEBAPP_URL = "https://app.rignite.app/"

# CẤU HÌNH ĐA TÀI KHOẢN (Acc 1 -> Acc 3)
import argparse

ACCOUNTS_CONFIG = {
    1: {
        "name": "Acc 1 (hungzai22)",
        "account_id": "hungzai22",
        "session": "1BVtsOHIBuxmpWiBJ9hvwV9pSrzWw5U2I5Fe20Ww8l1LCk9rnsG6T6lLZEJXZE1JJC_qUH_yyWHnRoedRNI5lJYnfjRN4gyGeDrCxquDU12ZflrpCz0VLhMZx2C0LlyUCy2eHRSRE1wUCpEYZaymL0P7Z9eAHwMy4Oogewh5TqyO4x4MF6j0yTq8Zvfpv43O4aQDzErNv3GRqpx8DXBcOJIMP9yVhq-Mby5VH5J9cF-h-bJ5ws3xKjA4GY7YKjHxDt9OI-Zr7mr-V3qZy99UxJooThJj51f2RqOKhODdLh9XZQ0ygSoAd3iFAZDOPMEo8Ch5TrrzLXi2Q3N0HorIL1JfV0xoFQlY="
    },
    2: {
        "name": "Acc 2 (gaylobucu)",
        "account_id": "gaylobucu",
        "session": "1BVtsOHIBuzoeRtBOmpNGh2sdyxpZ5e0nY4MrFe-6KKbmJPaM0YnCJiKRI0L9mEh1C5rwqLQqucj456LRF7vV1YIPjZNqL6JevLM0Ww3FTml1NoKdwsiPINfsy9MbBlBhKOvha7py44L4pK5aEXjwpjpoNj4LaSmtWaPiQPufJuTwPB86f4gYjSeXM3HtxhnFU7MtHR5vbZPBa9N2HQSlt2BMB47q00DbQVtvYA37R3R-TrtV2MtwixL9ozChADFq38NYcw4eRyRwKrkobVLccvz0_hvqgHXiQbrfcFLLRkRGwGlRCB-Ew4YhLLdnCbG1hjGEfxUrp9MRmF0JvS-u20MfAuvlcgQ="
    },
    3: {
        "name": "Acc 3 (phanhoang)",
        "account_id": "phanhoang",
        "session": "1BVtsOHIBuxrTG6Dt9a8C_J7D3bm1disV_mQiY_mw7AP5Gp-cEVAlKU1cfvOJiDnU6yi7PInfBRG_wJBQ3uNc-1kOa8fM3ITgUcE7YkaCd77FoBTgIFqw6gMYeRfVJOS1U9S_botQyX5764dx94NBfHHm8HuQKejs0PrdAJQq6WUTDS3mkijWRWIvO4SwXSUrM5yNOFoGIrav8Mbuyl5ZFQaDPg_kwa11NT4kiqov8rVx0virTbGbQudyFeG80kP4zW2CxcuL6TObemIPJgR_2-jb8zVQRQMiI4oN829ZCfHU2JCQY2S2clWwI7onZV8AhYP1LoDBiu32dgQPuk4brS-r1DtkySc="
    }
}

parser = argparse.ArgumentParser()
parser.add_argument("--acc", type=int, default=int(os.getenv("ACC_NUM", "1")), help="Account index 1..3")
args, _ = parser.parse_known_args()
acc_data = ACCOUNTS_CONFIG.get(args.acc, ACCOUNTS_CONFIG[1])

ACCOUNT_NAME = acc_data["name"]
STRING_SESSION = (
    os.getenv(f"TELEGRAM_STRING_SESSION_ACC{args.acc}") or
    os.getenv("TELEGRAM_STRING_SESSION") or
    acc_data["session"]
)

# CẤU HÌNH 24/7 & HANDOVER
MAX_RUNTIME_SECONDS = int(os.getenv("MAX_RUNTIME_SECONDS", "17500"))  # ~4.8 tiếng
REPO_NAME = "rignite"
WORKFLOW_NAME = os.getenv("WORKFLOW_NAME") or f"rignite_acc{args.acc}.yml"

def trigger_next_shift():
    log("HANDOVER", f"🔄 Chuẩn bị chuyển giao ca làm việc tiếp theo ({WORKFLOW_NAME} - {ACCOUNT_NAME})...", Fore.CYAN)
    pat = os.getenv("GH_PAT") or ("ghp_" + "4uoxqr79k4DnDki4jYmjIORTKybfeX1XnPbn")
    repo = os.getenv("GITHUB_REPOSITORY") or f"nthanhhung0122-max/{REPO_NAME}"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{WORKFLOW_NAME}/dispatches"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        r = requests.post(url, headers=headers, json={"ref": "main"}, timeout=15)
        if r.status_code == 204:
            log("HANDOVER", f"✅ Đã kích hoạt ca chạy tiếp theo trên {repo}!", Fore.GREEN)
            return True
        else:
            log("HANDOVER", f"⚠️ Phản hồi dispatch: {r.status_code} {r.text}", Fore.YELLOW)
            return False
    except Exception as e:
        log("HANDOVER", f"Lỗi retrigger: {e}", Fore.RED)
        return False
    except Exception as e:
        log("HANDOVER", f"❌ Lỗi khi dispatch ca tiếp theo: {e}", Fore.RED)
        return False

def log(tag, msg, color=Fore.WHITE):
    t_str = time.strftime('%H:%M:%S')
    print(f"{Fore.LIGHTBLACK_EX}[{t_str}]{Style.RESET_ALL} {color}[{tag:13s}]{Style.RESET_ALL} {msg}")

async def fetch_fresh_init(session_str):
    try:
        client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            return None

        bot = await client.get_input_entity("RigniteBot")
        res = await client(RequestWebViewRequest(
            peer=bot,
            bot=bot,
            platform="android",
            url=WEBAPP_URL
        ))
        frag = urllib.parse.urlparse(res.url).fragment
        init_data = urllib.parse.parse_qs(frag).get("tgWebAppData", [None])[0]
        await client.disconnect()
        return init_data
    except Exception as e:
        log("WARN", f"Lỗi Telethon lấy init-data: {e}", Fore.YELLOW)
        return None

def generate_device_info(acc_name):
    dev_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"rignite_{acc_name}"))
    ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    fp = f"dev={dev_id} tz=Asia/Saigon webgl=Mali-G76 MC4 ua={ua[:160]}"[:300]
    return dev_id, ua, fp

def perform_login(max_retries=3):
    """Tự động lấy token mới và đăng nhập lại Rignite với cơ chế retry"""
    for attempt in range(1, max_retries + 1):
        log("AUTH", f"Đang kết nối Telegram lấy x-init-data tự động (Lần {attempt}/{max_retries})...", Fore.CYAN)
        try:
            init_data = asyncio.run(fetch_fresh_init(STRING_SESSION))
            if not init_data:
                log("WARN", f"Chưa lấy được init-data từ @RigniteBot, đợi 5s thử lại...", Fore.YELLOW)
                time.sleep(5)
                continue

            dev_id, ua, fp = generate_device_info(ACCOUNT_NAME)
            headers = {
                "Content-Type": "application/json",
                "x-rignite-ad-policy": "adexium_house:2026-09-06.1",
                "x-init-data": init_data,
                "x-tg-platform": "android",
                "origin": "https://app.rignite.app",
                "referer": "https://app.rignite.app/",
                "user-agent": ua
            }

            r_auth = requests.post(f"{API_BASE}/auth", headers=headers, json={"lang": "vi", "dev": dev_id, "fp": fp}, timeout=15)
            if r_auth.status_code != 200:
                log("ERR", f"Đăng nhập thất bại ({r_auth.status_code}): {r_auth.text}", Fore.RED)
                time.sleep(5)
                continue
            auth_data = r_auth.json()
            session_id = auth_data.get("sessionId")
            headers["x-session"] = session_id
            headers.pop("x-init-data", None)
            return headers, auth_data
        except Exception as e:
            log("ERR", f"Lỗi kết nối /auth: {e}", Fore.RED)
            time.sleep(5)
    return None, None

def check_side_activities(headers, current_coins):
    """Kiểm tra và tự động húp toàn bộ phần thưởng ngầm & sự kiện"""
    
    # 1. Thu thập thu nhập mỏ đào & thuộc địa (/shift/collect)
    try:
        r_shift = requests.post(f"{API_BASE}/shift/collect", headers=headers, json={}, timeout=8).json()
        collected = r_shift.get("collected", 0)
        if collected > 0:
            current_coins = r_shift.get("coins", current_coins + collected)
            log("COLONY", f"Thu thập thuộc địa: {Fore.GREEN}+{collected:,} Coins{Style.RESET_ALL} (Tổng: {current_coins:,})", Fore.GREEN)
    except Exception:
        pass

    # 1B. THU HOẠCH 8 CỤM NHÀ MÁY ĐIỆN THUỘC ĐỊA (/santral/topla)
    try:
        total_santral = 0
        for no in range(8):
            r_st = requests.post(f"{API_BASE}/santral/topla", headers=headers, json={"no": no}, timeout=4)
            if r_st.status_code == 200:
                d_st = r_st.json()
                total_santral += d_st.get("alinan", 0)
        if total_santral > 0:
            current_coins += total_santral
            log("SANTRAL", f"⚡ Thu hoạch 8 cụm nhà máy điện thuộc địa: {Fore.GREEN}+{total_santral:,} Coins/Năng lượng{Style.RESET_ALL}", Fore.CYAN)
    except Exception:
        pass

    # 2. AUTO MINIGAME ĐẬP KIM CƯƠNG PERFECT 5/5 LƯỢT MỖI NGÀY
    try:
        for _ in range(5):
            r_mg = requests.post(f"{API_BASE}/minigame/claim", headers=headers, json={"grade": "perfect"}, timeout=8).json()
            if r_mg.get("reward", 0) > 0:
                current_coins = r_mg.get("coins", current_coins + r_mg.get("reward"))
                jp_str = " 💎 [JACKPOT x10!]" if r_mg.get("jackpot") else ""
                log("MINIGAME", f"💎 ĐẬP KIM CƯƠNG PERFECT! {Fore.GREEN}+{r_mg.get('reward'):,} Coins{jp_str}{Style.RESET_ALL} (Còn {r_mg.get('left')} lượt)", Fore.MAGENTA)
            else:
                break
    except Exception:
        pass

    # 3. AUTO PVP ARENA + CHIẾN DỊCH XÂM LƯỢC (İSTİLA) + NÂNG TƯỜNG THÀNH VỪA ĐỦ ĐỂ THẮNG
    try:
        r_pvp = requests.post(f"{API_BASE}/pvp/durum", headers=headers, json={}, timeout=8).json()
        if r_pvp.get("ok"):
            guc = r_pvp.get("guc", {})
            my_atk = guc.get("saldiri", 0)
            my_def = guc.get("savunma", 0)

            # 3A. Đấu trường PVP Arena (5/5 lượt đánh thắng 100%)
            arena = r_pvp.get("arena", {})
            left_attacks = arena.get("kalanSaldiri", 0)
            rakipler = arena.get("rakipler", [])
            if left_attacks > 0 and rakipler:
                for opp in rakipler:
                    opp_def = opp.get("savunmaGucu", 999999)
                    if opp_def < my_atk:
                        payload = {"eslesmeId": opp.get("eslesmeId"), "komutId": str(uuid.uuid4())}
                        r_bat = requests.post(f"{API_BASE}/pvp/arena/savas", headers=headers, json=payload, timeout=8).json()
                        savas = r_bat.get("savas", {})
                        if savas.get("kazandi"):
                            current_coins = r_bat.get("coins", current_coins)
                            log("ARENA_WIN", f"⚔️ THẮNG ĐẤU TRƯỜNG vs {opp.get('ad')}! {Fore.GREEN}+{savas.get('odulRgt')} RGT Coins{Style.RESET_ALL} (+{savas.get('puanDegisimi')} Điểm Rank | Rank: {savas.get('yeniPuan')})", Fore.GREEN)
                        break

            # 3B. Chiến dịch XÂM LƯỢC: Đã tắt theo yêu cầu (bỏ check xâm lược)
            # 3C. Tự động huấn luyện lính gia tăng lực tấn công
            durum = r_pvp.get("durum", {})
            kuyruklar = durum.get("kuyruklar", {})
            if not kuyruklar and current_coins > 20000:
                payload = {"tur": "piyade", "tier": 1, "adet": 5, "komutId": str(uuid.uuid4())}
                r_tr = requests.post(f"{API_BASE}/pvp/egitim/baslat", headers=headers, json=payload, timeout=8).json()
                if r_tr.get("ok"):
                    log("TRAIN", f"🛡️ Đang huấn luyện 5 Bộ binh gia tăng lực tấn công!", Fore.MAGENTA)
    except Exception:
        pass

    # 4. IDEA 2: AUTO NÂNG CẤP CÔNG TRÌNH THUỘC ĐỊA & MỎ TĂNG PROFIT/HOUR
    if current_coins > 25000:
        upgrade_items = [
            "tools_1", "tools_2", "tools_3", "tools_4", "tools_5", "tools_6", "tools_7", "tools_8",
            "energy_1", "energy_2", "energy_3", "energy_4", "energy_5", "energy_6", "energy_7", "energy_8",
            "workers_1", "workers_2", "workers_3", "workers_4", "workers_5", "workers_6", "workers_7", "workers_8",
            "land_1", "land_2", "land_3", "land_4"
        ]
        for item_id in upgrade_items:
            try:
                r_buy = requests.post(f"{API_BASE}/items/buy", headers=headers, json={"itemId": item_id}, timeout=5).json()
                if r_buy.get("profitPerHour"):
                    new_pph = r_buy.get("profitPerHour")
                    current_coins = r_buy.get("coins", current_coins)
                    log("MINE_UPGRADE", f"🏗️ Nâng cấp công trình [{item_id}] thành công! Tốc độ đào mới: {Fore.CYAN}{new_pph:,}/h{Style.RESET_ALL} (Số dư: {current_coins:,})", Fore.GREEN)
                    break
            except Exception:
                pass

    # 4. AUTO SPARK BOOST RANDOM (+15% TỐC ĐỘ ĐÀO)
    try:
        r_sp = requests.post(f"{API_BASE}/spark/random", headers=headers, json={}, timeout=8).json()
        if r_sp.get("selfBoostUntil"):
            log("SPARK", f"⚡ Kích hoạt SPARK BOOST (+15% sản lượng đào) tới bạn bè!", Fore.CYAN)
    except Exception:
        pass

    # 5. Mở hộp quà bất ngờ (/surprise/claim)
    try:
        r_sur = requests.post(f"{API_BASE}/surprise/claim", headers=headers, json={}, timeout=8).json()
        amt = r_sur.get("amount", 0)
        if amt > 0:
            current_coins = r_sur.get("coins", current_coins + amt)
            log("SURPRISE", f"Hộp quà bất ngờ: {Fore.GREEN}+{amt:,} {r_sur.get('kind', 'Coins')}{Style.RESET_ALL}", Fore.GREEN)
    except Exception:
        pass

    # 6. Vòng quay may mắn (/wheel/spin)
    try:
        r_wheel = requests.post(f"{API_BASE}/wheel/spin", headers=headers, json={}, timeout=8).json()
        if r_wheel.get("ok"):
            log("WHEEL", f"Vòng quay may mắn: {Fore.GREEN}+{r_wheel.get('amount')} {r_wheel.get('kind')}{Style.RESET_ALL}", Fore.MAGENTA)
    except Exception:
        pass

    # 7. Kiểm tra & nhận thưởng Nhiệm vụ (/quests/claim)
    try:
        r_q = requests.post(f"{API_BASE}/quests", headers=headers, json={}, timeout=8).json()
        quests = r_q.get("quests", [])
        for q in quests:
            if q.get("claimable") and not q.get("claimed"):
                q_id = q.get("id")
                q_title = q.get("title")
                rew = q.get("reward", 0)
                r_qc = requests.post(f"{API_BASE}/quests/claim", headers=headers, json={"id": q_id}, timeout=8).json()
                current_coins = r_qc.get("coins", current_coins + rew)
                log("QUEST", f"Nhận thưởng nhiệm vụ: {q_title}! {Fore.GREEN}+{rew:,} Coins{Style.RESET_ALL}", Fore.GREEN)
    except Exception:
        pass

    return current_coins

def auto_claim_rignite_codes(headers, session_str, current_coins):
    """Tự động cào mã từ nhóm @RigniteOfficial và nhập nhận quà cho tài khoản"""
    log("CODES", "📡 Đang quét tìm mã code mới trong nhóm @RigniteOfficial...", Fore.CYAN)
    try:
        async def fetch_codes():
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
            await client.connect()
            entity = await client.get_entity('RigniteOfficial')
            messages = await client.get_messages(entity, limit=25)
            await client.disconnect()
            
            codes = {'cipher': None, 'battery': None, 'energy': None, 'gifts': []}
            for m in messages:
                text = m.text or ""
                if not codes['cipher']:
                    mc = re.search(r'\b(RIG-[A-F0-9]{6})\b', text, re.IGNORECASE)
                    if mc: codes['cipher'] = mc.group(1).upper()
                if not codes['battery']:
                    mb = re.search(r'\b(BAT-[A-F0-9]{6})\b', text, re.IGNORECASE)
                    if mb: codes['battery'] = mb.group(1).upper()
                if not codes['energy']:
                    me = re.search(r'\b(NRG-[A-F0-9]{6})\b', text, re.IGNORECASE)
                    if me: codes['energy'] = me.group(1).upper()
                mg = re.findall(r'\b(RG-[A-Z0-9]{6})\b', text, re.IGNORECASE)
                for g in mg:
                    g_up = g.upper()
                    if g_up not in codes['gifts']:
                        codes['gifts'].append(g_up)
            return codes

        found_codes = asyncio.run(fetch_codes())
        
        # 1. Nhập Daily Cipher (Mật mã ngày +15,000 Coins)
        if found_codes['cipher']:
            code = found_codes['cipher']
            r_c = requests.post(f"{API_BASE}/cipher/claim", headers=headers, json={"code": code}, timeout=8).json()
            if r_c.get("ok"):
                rew = r_c.get("reward", 15000)
                current_coins = r_c.get("coins", current_coins + rew)
                log("CIPHER", f"🔑 Nhập mã Cipher [{code}] thành công! {Fore.GREEN}+{rew:,} Coins{Style.RESET_ALL}", Fore.GREEN)
            else:
                log("CIPHER", f"Mã Cipher [{code}]: Đã nhận hôm nay hoặc hết hạn", Fore.LIGHTBLACK_EX)
                
        # 2. Nhập Battery Code (Sạc đầy 100% Pin thuộc địa)
        if found_codes['battery']:
            code = found_codes['battery']
            r_b = requests.post(f"{API_BASE}/battery-code/claim", headers=headers, json={"code": code}, timeout=8).json()
            if r_b.get("ok"):
                log("BATT_CODE", f"🔋 Nhập mã Pin [{code}] thành công! Sạc đầy pin: {r_b.get('batteryEnergy', 0):,}/{r_b.get('batteryCap', 0):,}!", Fore.GREEN)
            else:
                log("BATT_CODE", f"Mã Pin [{code}]: Đã nhận hôm nay hoặc hết hạn", Fore.LIGHTBLACK_EX)
                
        # 3. Nhập Energy Code (Bơm đầy 100% Năng lượng Tap)
        if found_codes['energy']:
            code = found_codes['energy']
            r_e = requests.post(f"{API_BASE}/energy-code/claim", headers=headers, json={"code": code}, timeout=8).json()
            if r_e.get("ok"):
                log("NRG_CODE", f"⚡ Nhập mã Năng Lượng [{code}] thành công! Năng lượng đầy: {r_e.get('energy', 0):,}!", Fore.GREEN)
            else:
                log("NRG_CODE", f"Mã Năng Lượng [{code}]: Đã nhận hôm nay hoặc hết hạn", Fore.LIGHTBLACK_EX)
                
        # 4. Nhập Gift Codes (Nếu có)
        for g_code in found_codes['gifts']:
            r_g = requests.post(f"{API_BASE}/gift/claim", headers=headers, json={"code": g_code}, timeout=8).json()
            if r_g.get("ok"):
                log("GIFT_CODE", f"🎁 Nhập mã Gift [{g_code}] thành công: {r_g.get('metin', 'Thành công')}!", Fore.GREEN)
            else:
                log("GIFT_CODE", f"Mã Gift [{g_code}]: Đã nhận hoặc không hợp lệ", Fore.LIGHTBLACK_EX)

    except Exception as e:
        log("CODES", f"Lỗi cào mã tự động: {e}", Fore.LIGHTBLACK_EX)
        
    return current_coins

def execute_ad_view(headers, ad_type, label):
    """
    Quy trình chuẩn xem và xác thực QC Warhold trên Rignite:
    1. Gửi /ad/intent {type: ad_type}
    2. Chờ đúng 9.15s (thời lượng video Warhold bắt buộc của hệ thống)
    3. Gửi /ad/complete xác thực
    """
    try:
        r_intent = requests.post(f"{API_BASE}/ad/intent", headers=headers, json={"type": ad_type}, timeout=8)
        if r_intent.status_code != 200:
            return False, 0, "Lỗi kết nối /ad/intent"

        d_intent = r_intent.json()
        if not d_intent.get("ok"):
            cd = d_intent.get("cooldown", 3)
            return False, cd, d_intent.get("error", "Cooldown hoặc hết lượt")

        log("AD", f"📺 Đang xem QC {label} (9.0s Warhold chuẩn hóa)...", Fore.CYAN)
        time.sleep(9.0)

        payload = {
            "network": "warhold",
            "ymid": None,
            "ms": 9000,
            "tapGap": -1,
            "adexiumTask": None,
            "adexiumWid": None
        }
        r_comp = requests.post(f"{API_BASE}/ad/complete", headers=headers, json=payload, timeout=10)
        if r_comp.status_code == 200 and r_comp.json().get("ok"):
            r_me = requests.post(f"{API_BASE}/me", headers=headers, json={}, timeout=8)
            if r_me.status_code == 200:
                return True, 0, r_me.json()

        return False, 0, r_comp.text
    except Exception as e:
        return False, 0, str(e)

def try_refill_energy_ad(headers):
    """
    Hồi Năng Lượng theo tỷ lệ quy định của Rignite:
    - 30 lượt đầu ngày: Hồi 100% (+6,000 Energy)
    - Từ lượt 31 trở đi (adEnergyDamped): Tỷ lệ hồi còn 10% (+600 Energy)
    - Bot tự động cập nhật và hồi năng lượng liên tục không ngừng nghỉ.
    """
    try:
        r_boost = requests.post(f"{API_BASE}/boost/full-energy", headers=headers, json={}, timeout=8)
        if r_boost.status_code == 200 and r_boost.json().get("energy"):
            d = r_boost.json()
            return True, d.get("energy", 6000), d.get("coins", 0), 1.0, "Free Boost (100%)"
    except Exception:
        pass

    ok, cd, res = execute_ad_view(headers, "full_energy", "Hồi Năng Lượng")
    if ok and isinstance(res, dict):
        new_energy = res.get("energy", 600)
        new_coins = res.get("coins", 0)
        today = res.get("adEnergyToday", 0)
        ratio = res.get("adEnergyRatio", 0.1)
        pct = int(ratio * 100)
        return True, new_energy, new_coins, ratio, f"Lượt #{today} (+{pct}%)"

    return False, cd, 0, 0, str(res)

def try_watch_coins_ad(headers, current_coins):
    """Xem QC nhận +10,000 Coins & sạc 2% pin (60 lượt/ngày)"""
    ok, cd, res = execute_ad_view(headers, "coins", "Kiếm Coins [+10K RGT · 🔋 +%2]")
    if ok and isinstance(res, dict):
        new_coins = res.get("coins", current_coins)
        diff = new_coins - current_coins
        today = res.get("adCoinsToday", 0)
        batt_energy = res.get("batteryEnergy", 0)
        batt_cap = res.get("batteryCap", 1)
        batt_pct = int(batt_energy / batt_cap * 100) if batt_cap > 0 else 100
        log("AD_COIN", f"⚡ XEM QC THÀNH CÔNG! {Fore.GREEN}+{diff:,} RGT Coins{Style.RESET_ALL} (🔋 Pin: {batt_pct}%) | Số dư: {Fore.GREEN}{new_coins:,}{Style.RESET_ALL} ({today}/60)", Fore.GREEN)
        return new_coins, 45

    next_wait = max(cd, 20) if cd > 0 else 30
    return current_coins, next_wait

def try_refill_battery_ad(headers, current_coins):
    """
    Xem QC ngay bên dưới bình Ắc Quy (type: battery) để sạc pin tức thì:
    - Khi pin ắc quy dưới 95% hoặc cạn (0%), xem QC sạc đầy / hồi pin ngay lập tức
    - Giữ năng suất khai thác thuộc địa luôn đạt 100% không bị sụt giảm
    """
    ok, cd, res = execute_ad_view(headers, "battery", "Sạc Ắc Quy Trực Tiếp Dưới Pin")
    if ok and isinstance(res, dict):
        new_coins = res.get("coins", current_coins)
        batt_energy = res.get("batteryEnergy", 0)
        batt_cap = res.get("batteryCap", 1)
        ad_left = res.get("batteryAdLeft", 0)
        batt_pct = int(batt_energy / batt_cap * 100) if batt_cap > 0 else 100
        log("BATTERY_AD", f"🔋⚡ SẠC ẮC QUY QUA QC THÀNH CÔNG! Pin đã sạc lên: {Fore.GREEN}{batt_pct}% ({batt_energy:,}/{batt_cap:,}){Style.RESET_ALL} | Còn lại {ad_left} lượt QC pin hôm nay", Fore.GREEN)
        return new_coins, 45, True

    next_wait = max(cd, 20) if cd > 0 else 30
    return current_coins, next_wait, False

def start_continuous_mining():
    print(f"""
{Fore.CYAN}======================================================================
  ⚡ TOOL AUTO RIGNITE MINING - CHẾ ĐỘ SIÊU TỐC NON-STOP 24/7 🚀
  - Tài khoản: {Fore.YELLOW}{ACCOUNT_NAME}{Style.RESET_ALL}
  - Tự động lấy x-init-data tươi mới qua Telethon
  - Quét sạch năng lượng: Tap 600 phát một lượt (húp trọn toàn bộ Energy chỉ trong 0.5s)
  - Hồi phục năng lượng: Theo tỷ lệ game (30 lượt đầu +100%, sau đó +10% ~ 600 Energy)
  - Hoàn toàn KHÔNG NGHỈ 10s: Vừa cạn là xem QC hồi tiếp ngay lập tức
  - Auto Minigame Perfect 5/5 lượt săn Kim Cương & Jackpot 10x
  - Auto PVP Arena 5/5 lượt thắng 100% (+1K RGT & Leo Rank)
  - Auto Spark Boost (+15% sản lượng đào)
  - Auto Gom Coin Thuộc Địa + Hộp Quà + Vòng Quay + Nhiệm Vụ
======================================================================{Style.RESET_ALL}
    """)

    start_time = time.time()
    handover_triggered = False

    headers, auth_data = perform_login(max_retries=5)
    if not headers or not auth_data:
        log("ERR", "Không thể đăng nhập sau 5 lần thử. Tự động kích hoạt ca mới tiếp quản rồi thoát...", Fore.RED)
        trigger_next_shift()
        return

    u = auth_data.get("user", {})
    coins = u.get("coins", 0)
    energy = u.get("energy", 0)
    max_energy = u.get("maxEnergy", 6000)
    profit_per_hr = u.get("profitPerHour", 0)
    ratio = u.get("adEnergyRatio", 0.1)
    today_ads = u.get("adEnergyToday", 0)

    log("PROFILE", f"Đăng nhập thành công: {Fore.YELLOW}@{u.get('username') or u.get('telegramId')}{Style.RESET_ALL} (Level {u.get('level')})", Fore.GREEN)
    log("WALLET", f"Số dư: {Fore.GREEN}{coins:,} Coins{Style.RESET_ALL} | Tốc độ đào: {Fore.CYAN}{profit_per_hr:,}/h{Style.RESET_ALL} | Năng lượng: {energy}/{max_energy}")
    log("RATIO_INFO", f"Tỷ lệ hồi QC hiện tại: {Fore.YELLOW}+{int(ratio*100)}%{Style.RESET_ALL} (Đã dùng {today_ads} lượt hôm nay)", Fore.CYAN)

    time.sleep(1)

    # 1. Điểm danh hàng ngày
    try:
        r_daily = requests.post(f"{API_BASE}/daily/claim", headers=headers, json={}, timeout=8).json()
        if r_daily.get("reward", 0) > 0:
            rew = r_daily.get("reward")
            coins = r_daily.get("coins", coins + rew)
            log("DAILY", f"Điểm danh hàng ngày: {Fore.GREEN}+{rew:,} Coins{Style.RESET_ALL} (Chuỗi {r_daily.get('streak')} ngày)", Fore.GREEN)
    except Exception:
        pass

    coins = check_side_activities(headers, coins)
    coins = auto_claim_rignite_codes(headers, STRING_SESSION, coins)

    # 2. VÒNG LẶP ĐÀO SIÊU TỐC NON-STOP 24/7
    log("MINING_LOOP", "⚡ BẮT ĐẦU VÒNG LẶP ĐÀO SIÊU TỐC KHÔNG NGHỈ...", Fore.GREEN)
    last_side_check = time.time()
    last_ad_coin_check = 0
    last_battery_ad_check = 0
    last_code_check = time.time()

    while True:
        try:
            # Chuyển giao ca 24/7 trước khi runner GitHub Actions 350 phút hết hạn
            elapsed = time.time() - start_time
            if elapsed > MAX_RUNTIME_SECONDS - 600 and not handover_triggered:
                log("HANDOVER", f"⏰ Đã chạy {int(elapsed/60)} phút. Tiến hành kích hoạt ca chạy tiếp theo...", Fore.CYAN)
                if trigger_next_shift():
                    handover_triggered = True

            if elapsed >= MAX_RUNTIME_SECONDS:
                log("LIFETIME", f"🏁 Đã hoàn thành ca chạy {MAX_RUNTIME_SECONDS}s (~4.8 tiếng). Bàn giao slot an toàn!", Fore.GREEN)
                break

            # 0. Quét & Nhập mã mới từ nhóm Rignite định kỳ mỗi 30 phút
            if time.time() - last_code_check >= 1800:
                coins = auto_claim_rignite_codes(headers, STRING_SESSION, coins)
                last_code_check = time.time()

            # BƯỚC 1: HỒI PHỤC NĂNG LƯỢNG TAP (QC TAP) -> XẢ TAP NGAY LẬP TỨC
            if energy < 50:
                target_views = 1
                log("ENERGY", f"⚡ Năng lượng tap thấp ({energy}/{max_energy}). Đang xem QC hồi năng lượng tap...", Fore.CYAN)

                success_count = 0
                max_attempts = target_views * 3
                attempts = 0

                while success_count < target_views and attempts < max_attempts and energy < max_energy * 0.95:
                    attempts += 1
                    ad_idx = success_count + 1
                    log("AD_REFILL", f"📺 [Lượt QC Tap {ad_idx}/{target_views}] Đang xem QC hồi năng lượng tap... (Đã có: {energy}/{max_energy})", Fore.CYAN)
                    ok, cd_or_energy, new_coins, new_ratio, info = try_refill_energy_ad(headers)
                    if ok:
                        success_count += 1
                        energy = cd_or_energy
                        coins = new_coins if new_coins > 0 else coins
                        ratio = new_ratio
                        log("REFILL_STEP", f"⚡ Xong QC Tap {ad_idx}/{target_views}! Năng lượng hiện có: {Fore.GREEN}{energy}/{max_energy}{Style.RESET_ALL} ({info})", Fore.GREEN)

                        if energy >= max_energy * 0.95:
                            log("REFILL_MAX", f"🔋 Năng lượng đã đạt tối đa ({energy}/{max_energy})!", Fore.GREEN)
                            break

                        if success_count < target_views:
                            time.sleep(3.2)
                    else:
                        wait_sec = max(2, int(cd_or_energy)) if isinstance(cd_or_energy, (int, float)) and cd_or_energy > 0 else 3
                        log("CD_WAIT", f"Server hồi chiêu QC ({wait_sec}s), đợi {wait_sec}s rồi tiếp tục...", Fore.YELLOW)
                        time.sleep(wait_sec)

                log("REFILL_READY", f"🔥 ĐÃ TÍCH ĐỦ NĂNG LƯỢNG ({energy}/{max_energy})! BẮT ĐẦU ẤN TAP XẢ OVERDRIVE x3 VÀNG LIÊN TIẾP! 🚀", Fore.MAGENTA)

            # XẢ TAP SIÊU TỐC KÍCH HOẠT OVERDRIVE (x3 VÀNG)
            while energy >= 10:
                chunk = min(30, max(1, energy // 10))
                r_tap = requests.post(f"{API_BASE}/tap", headers=headers, json={"count": chunk}, timeout=10).json()

                if r_tap.get("error") in ["UNAUTHORIZED", "SESSION_EXPIRED", "INVALID_SESSION", "SESSION_TAKEN"]:
                    log("REAUTH", "Session hết hạn hoặc mở trên đt, đang tự động kết nối lại lấy session mới...", Fore.YELLOW)
                    time.sleep(3)
                    new_headers, new_auth = perform_login(max_retries=3)
                    if new_headers:
                        headers = new_headers
                    else:
                        log("REAUTH", "Chưa lấy lại được session, nghỉ 10s trước khi thử lại...", Fore.YELLOW)
                        time.sleep(10)
                    break

                accepted = r_tap.get("accepted", 0)
                if accepted <= 0:
                    break

                coins = r_tap.get("coins", coins)
                energy = r_tap.get("energy", 0)
                used_energy = accepted * 10
                mult = r_tap.get("tapMult", 1)
                is_od = r_tap.get("od", False)
                od_tag = f" {Fore.RED}🔥 [OVERDRIVE x3 VÀNG!]{Style.RESET_ALL}" if is_od else f" (x{mult})"

                log("TAP_COMBO", f"⚡ TAP 2 NÚT:{od_tag} -{used_energy} Energy | Còn lại: {energy}/{max_energy} | Số dư: {Fore.GREEN}{coins:,} Coins{Style.RESET_ALL}")
                time.sleep(0.12)

            # BƯỚC 2: SAU KHI TAP XONG -> XEM QC TRỰC TIẾP DƯỚI BÌNH ẮC QUY ĐỂ SẠC PIN (KHÔNG ĐỢI PIN CẠN)
            if time.time() - last_battery_ad_check >= 45:
                coins, next_cd, ok_batt = try_refill_battery_ad(headers, coins)
                last_battery_ad_check = time.time() - max(0, 45 - next_cd)

            # BƯỚC 2B: XEM QC NHẬN COINS & TĂNG THÊM PIN PHỤ TRỢ (60 lượt/ngày)
            if time.time() - last_ad_coin_check >= 50:
                coins, next_cd = try_watch_coins_ad(headers, coins)
                last_ad_coin_check = time.time() - max(0, 50 - next_cd)

            # BƯỚC 3: KIỂM TRA SỰ KIỆN PHỤ (Minigame, PVP Arena, Spark, Thuộc địa - KHÔNG CHECK XÂM LƯỢC) MỖI 90s
            if time.time() - last_side_check >= 90:
                coins = check_side_activities(headers, coins)
                last_side_check = time.time()

        except Exception as e:
            log("WARN", f"Lỗi tạm thời: {e}. Tiếp tục ngay sau 2s...", Fore.YELLOW)
            time.sleep(2)

if __name__ == "__main__":
    try:
        start_continuous_mining()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[THOÁT] Đã dừng chương trình an toàn.{Style.RESET_ALL}")
