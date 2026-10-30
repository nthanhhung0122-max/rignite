"""
=============================================================================
 TOOL AUTO RIGNITE MINING (@RigniteBot) - CHẾ ĐỘ ĐÀO LIÊN TỤC 24/7 KHÔNG NGHỈ
 - Dành riêng cho tài khoản: hungzai22
 - Tự động lấy x-init-data tươi mới qua Telethon Session (Không cần lấy thủ công)
 - Tự động Tap đào liên tục 24/7
 - Tự động xem QC hồi đầy năng lượng (Nút 📺 dưới thanh Energy)
 - Khi hết lượt QC trong ngày: Nghỉ 10s tự hồi là đào tiếp ngay
 - Tự động thu hoạch mỏ đào Offline (/shift/collect) định kỳ 90s
 - Tự động mở Hộp quà bất ngờ (/surprise/claim) + Quay vòng quay (/wheel/spin)
 - Tự động điểm danh hàng ngày (/daily/claim) + Nhận thưởng Quests
=============================================================================
"""

import os
import sys
import time
import json
import random
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

# CẤU HÌNH DUY NHẤT ACC HUNGZAI22
ACCOUNT_NAME = "hungzai22"
STRING_SESSION = os.getenv("TELEGRAM_STRING_SESSION_ACC1") or "1BVtsOHIBuxmpWiBJ9hvwV9pSrzWw5U2I5Fe20Ww8l1LCk9rnsG6T6lLZEJXZE1JJC_qUH_yyWHnRoedRNI5lJYnfjRN4gyGeDrCxquDU12ZflrpCz0VLhMZx2C0LlyUCy2eHRSRE1wUCpEYZaymL0P7Z9eAHwMy4Oogewh5TqyO4x4MF6j0yTq8Zvfpv43O4aQDzErNv3GRqpx8DXBcOJIMP9yVhq-Mby5VH5J9cF-h-bJ5ws3xKjA4GY7YKjHxDt9OI-Zr7mr-V3qZy99UxJooThJj51f2RqOKhODdLh9XZQ0ygSoAd3iFAZDOPMEo8Ch5TrrzLXi2Q3N0HorIL1JfV0xoFQlY="

def log(tag, msg, color=Fore.WHITE):
    t_str = time.strftime('%H:%M:%S')
    print(f"{Fore.LIGHTBLACK_EX}[{t_str}]{Style.RESET_ALL} {color}[{tag}]{Style.RESET_ALL} {msg}")

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

def check_side_activities(headers, current_coins):
    # 1. Thu hoạch mỏ đào offline
    try:
        r_shift = requests.post(f"{API_BASE}/shift/collect", headers=headers, json={}, timeout=8).json()
        collected = r_shift.get("collected", 0)
        if collected > 0:
            current_coins = r_shift.get("coins", current_coins + collected)
            log("SHIFT", f"Thu hoạch mỏ offline: {Fore.GREEN}+{collected:,} Coins{Style.RESET_ALL} (Tổng: {current_coins:,})", Fore.GREEN)
    except Exception:
        pass

    # 2. Mở hộp quà bất ngờ
    try:
        r_sur = requests.post(f"{API_BASE}/surprise/claim", headers=headers, json={}, timeout=8).json()
        amt = r_sur.get("amount", 0)
        if amt > 0:
            current_coins = r_sur.get("coins", current_coins + amt)
            log("SURPRISE", f"Hộp quà bất ngờ: {Fore.GREEN}+{amt:,} {r_sur.get('kind', 'Coins')}{Style.RESET_ALL}", Fore.GREEN)
    except Exception:
        pass

    # 3. Vòng quay may mắn
    try:
        r_wheel = requests.post(f"{API_BASE}/wheel/spin", headers=headers, json={}, timeout=8).json()
        if r_wheel.get("ok"):
            log("WHEEL", f"Vòng quay may mắn: {Fore.GREEN}+{r_wheel.get('amount')} {r_wheel.get('kind')}{Style.RESET_ALL}", Fore.MAGENTA)
    except Exception:
        pass

    # 4. Kiểm tra & nhận thưởng Quests
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

def try_refill_energy_ad(headers):
    """
    Giả lập bấm nút Xem QC hồi đầy năng lượng ở dưới thanh Energy:
    1. Gửi /ad/intent {"type": "full_energy"}
    2. Gửi /boost/full-energy
    """
    try:
        requests.post(f"{API_BASE}/ad/intent", headers=headers, json={"type": "full_energy"}, timeout=8)
        time.sleep(1)
        r_refill = requests.post(f"{API_BASE}/boost/full-energy", headers=headers, json={}, timeout=10)
        if r_refill.status_code == 200:
            d = r_refill.json()
            return True, d.get("energy", 6000), d.get("coins", 0), d.get("fullEnergyLeft", 0)
        else:
            err = r_refill.json().get("error", "")
            return False, 0, 0, err
    except Exception as e:
        return False, 0, 0, str(e)

def start_continuous_mining():
    print(f"""
{Fore.CYAN}======================================================================
     TOOL AUTO RIGNITE MINING - CHẾ ĐỘ ĐÀO LIÊN TỤC 24/7 KHÔNG NGHỈ
     - Tài khoản: {Fore.YELLOW}{ACCOUNT_NAME}{Style.RESET_ALL}
     - Tự động lấy x-init-data tươi mới qua Telethon
     - Đào liên tục không nghỉ (Không ngủ 30 phút)
     - Xem QC hồi năng lượng (Nút 📺 dưới thanh Energy)
     - Khi hết lượt QC trong ngày: Chờ 10s tự hồi là đào tiếp ngay
     - Tự động thu hoạch mỏ Offline + Điểm danh + Hộp quà + Vòng quay + Quests
======================================================================{Style.RESET_ALL}
    """)

    # 1. Lấy init-data tự động qua Telethon
    log("AUTH", "Đang kết nối Telegram lấy x-init-data tự động...", Fore.CYAN)
    init_data = asyncio.run(fetch_fresh_init(STRING_SESSION))
    if not init_data:
        log("ERR", "Không thể lấy init-data từ @RigniteBot. Vui lòng kiểm tra lại mạng!", Fore.RED)
        return

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

    # 2. Đăng nhập /auth
    try:
        r_auth = requests.post(f"{API_BASE}/auth", headers=headers, json={"lang": "vi", "dev": dev_id, "fp": fp}, timeout=15)
        if r_auth.status_code != 200:
            log("ERR", f"Đăng nhập thất bại: {r_auth.text}", Fore.RED)
            return
        auth_data = r_auth.json()
        session_id = auth_data.get("sessionId")
        u = auth_data.get("user", {})
        coins = u.get("coins", 0)
        energy = u.get("energy", 0)
        max_energy = u.get("maxEnergy", 6000)
        profit_per_hr = u.get("profitPerHour", 0)

        log("PROFILE", f"Đăng nhập thành công: {Fore.YELLOW}{u.get('username') or u.get('telegramId')}{Style.RESET_ALL} (Level {u.get('level')})", Fore.GREEN)
        log("WALLET", f"Số dư: {Fore.GREEN}{coins:,} Coins{Style.RESET_ALL} | Tốc độ đào: {Fore.CYAN}{profit_per_hr:,}/h{Style.RESET_ALL} | Năng lượng: {energy}/{max_energy}")
    except Exception as e:
        log("ERR", f"Lỗi kết nối /auth: {e}", Fore.RED)
        return

    # Chuyển headers sang session token
    headers["x-session"] = session_id
    headers.pop("x-init-data", None)
    time.sleep(1)

    # 3. Điểm danh hàng ngày
    try:
        r_daily = requests.post(f"{API_BASE}/daily/claim", headers=headers, json={}, timeout=8).json()
        if r_daily.get("reward", 0) > 0:
            rew = r_daily.get("reward")
            coins = r_daily.get("coins", coins + rew)
            log("DAILY", f"Điểm danh hàng ngày: {Fore.GREEN}+{rew:,} Coins{Style.RESET_ALL} (Chuỗi {r_daily.get('streak')} ngày)", Fore.GREEN)
    except Exception:
        pass

    coins = check_side_activities(headers, coins)

    # 4. VÒNG LẶP ĐÀO LIÊN TỤC 24/7 KHÔNG NGHỈ
    log("MINING_LOOP", "⚡ BẮT ĐẦU VÒNG LẶP ĐÀO LIÊN TỤC 24/7 KHÔNG NGHỈ...", Fore.GREEN)
    last_side_check = time.time()

    while True:
        try:
            # Định kỳ 90s kiểm tra mỏ offline, hộp quà, quests 1 lần
            if time.time() - last_side_check >= 90:
                coins = check_side_activities(headers, coins)
                last_side_check = time.time()

            # Nếu Energy >= 50 thì tap đào coin
            if energy >= 50:
                tap_chunk = min(100, energy)
                r_tap = requests.post(f"{API_BASE}/tap", headers=headers, json={"count": tap_chunk}, timeout=10).json()
                accepted = r_tap.get("accepted", tap_chunk)
                coins = r_tap.get("coins", coins)
                energy = r_tap.get("energy", energy - accepted)
                log("TAP", f"Đào +{accepted} taps | Số dư: {Fore.GREEN}{coins:,} Coins{Style.RESET_ALL} | Năng lượng: {energy}/{max_energy}")
                time.sleep(random.uniform(0.9, 1.3))

            else:
                # Khi Energy < 50: Kích hoạt Xem QC hồi đầy Energy (nút 📺 dưới thanh năng lượng)
                log("ENERGY", f"Năng lượng còn {energy}. Đang xem QC hồi đầy Energy (nút 📺 dưới thanh năng lượng)...", Fore.CYAN)
                ok, new_energy, new_coins, info = try_refill_energy_ad(headers)
                
                if ok:
                    energy = new_energy
                    coins = new_coins if new_coins > 0 else coins
                    log("REFILL_OK", f"⚡ XEM QC THÀNH CÔNG! Đầy {energy}/{max_energy} Energy (Còn {info} lượt QC hôm nay). Đào tiếp ngay!", Fore.GREEN)
                    time.sleep(1)
                    continue
                else:
                    # Khi đã xem hết số lượt QC trong ngày: Chỉ nghỉ 10s cho năng lượng tự hồi rồi đào tiếp
                    log("WAIT", f"Đã hết lượt xem QC hôm nay ({info}). Chờ 10s năng lượng tự hồi phục rồi đào tiếp...", Fore.YELLOW)
                    time.sleep(10)
                    
                    # Lấy lại thông tin Energy từ server
                    r_me = requests.post(f"{API_BASE}/me", headers=headers, json={}, timeout=10)
                    if r_me.status_code == 200:
                        d_me = r_me.json()
                        energy = d_me.get("energy", energy)
                        coins = d_me.get("coins", coins)

        except Exception as e:
            log("WARN", f"Lỗi tạm thời: {e}. Thử lại sau 5s...", Fore.YELLOW)
            time.sleep(5)

if __name__ == "__main__":
    try:
        start_continuous_mining()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[THOÁT] Đã dừng chương trình theo yêu cầu.{Style.RESET_ALL}")
