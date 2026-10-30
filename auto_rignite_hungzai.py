"""
=============================================================================
 TOOL AUTO RIGNITE MINING (@RigniteBot) - DÀNH RIÊNG CHO ACC HUNGZAI22
 - Tự động lấy x-init-data qua Telethon Session (Không cần làm thủ công)
 - Tự động đăng nhập /auth và lấy Session Token
 - Tự động thu hoạch mỏ đào Offline (/shift/collect)
 - Tự động điểm danh hàng ngày (/daily/claim)
 - Tự động mở Hộp quà bất ngờ (/surprise/claim)
 - Tự động quay Vòng quay may mắn (/wheel/spin)
 - Tự động Tap khai thác coin đến cạn Energy
 - Tự động kích hoạt Boost Full-Energy miễn phí để hồi đầy bình và tap tiếp
 - Tự động kiểm tra & nhận thưởng Nhiệm vụ (/quests/claim)
 - Chạy vòng lặp 24/7 (nghỉ 30 phút giữa các chu kỳ để hồi phục Energy)
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
CYCLE_SLEEP_SECONDS = 1800  # Nghỉ 30 phút giữa các chu kỳ

# CHỈ CẤU HÌNH DUY NHẤT ACC HUNGZAI22
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

def run_rignite_cycle():
    print("\n" + "="*65)
    log("ACCOUNT", f"=== BẮT ĐẦU XỬ LÝ: {Fore.YELLOW}{ACCOUNT_NAME}{Style.RESET_ALL} ===", Fore.CYAN)
    print("="*65)

    # 1. Tự động lấy init-data mới từ bot
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

    # 3. Thu hoạch mỏ đào Offline (Shift Collect)
    try:
        r_shift = requests.post(f"{API_BASE}/shift/collect", headers=headers, json={}, timeout=10).json()
        collected = r_shift.get("collected", 0)
        if collected > 0:
            coins = r_shift.get("coins", coins + collected)
            log("SHIFT", f"Thu hoạch mỏ đào offline: {Fore.GREEN}+{collected:,} Coins{Style.RESET_ALL}! Số dư mới: {coins:,}", Fore.GREEN)
        else:
            log("SHIFT", "Chưa có coin mỏ offline tích luỹ mới.", Fore.WHITE)
    except Exception as e:
        log("ERR", f"Lỗi thu hoạch shift: {e}", Fore.RED)

    time.sleep(1)

    # 4. Điểm danh hàng ngày (Daily Streak)
    try:
        r_daily = requests.post(f"{API_BASE}/daily/claim", headers=headers, json={}, timeout=10).json()
        if r_daily.get("reward", 0) > 0:
            rew = r_daily.get("reward")
            coins = r_daily.get("coins", coins + rew)
            log("DAILY", f"Điểm danh hàng ngày: {Fore.GREEN}+{rew:,} Coins{Style.RESET_ALL} (Chuỗi {r_daily.get('streak')} ngày)", Fore.GREEN)
        else:
            log("DAILY", "Hôm nay bạn đã điểm danh rồi.", Fore.WHITE)
    except Exception:
        pass

    time.sleep(1)

    # 5. Mở Hộp quà bất ngờ (Surprise Box)
    try:
        r_sur = requests.post(f"{API_BASE}/surprise/claim", headers=headers, json={}, timeout=10).json()
        amt = r_sur.get("amount", 0)
        if amt > 0:
            coins = r_sur.get("coins", coins + amt)
            log("SURPRISE", f"Mở hộp quà bất ngờ: {Fore.GREEN}+{amt:,} {r_sur.get('kind', 'Coins')}{Style.RESET_ALL}", Fore.GREEN)
    except Exception:
        pass

    time.sleep(1)

    # 6. Quay vòng quay may mắn (Lucky Wheel)
    try:
        r_wheel = requests.post(f"{API_BASE}/wheel/spin", headers=headers, json={}, timeout=10).json()
        if r_wheel.get("ok"):
            log("WHEEL", f"Vòng quay may mắn: Trúng {Fore.GREEN}+{r_wheel.get('amount')} {r_wheel.get('kind')}{Style.RESET_ALL}", Fore.MAGENTA)
        else:
            log("WHEEL", "Đã hết lượt quay miễn phí hôm nay.", Fore.WHITE)
    except Exception:
        pass

    time.sleep(1)

    # 7. Tự động Tap khai thác đến cạn Energy + Dùng Boost Full-Energy
    refill_used = False
    log("TAP", f"Bắt đầu khai thác vàng (Năng lượng hiện có: {energy}/{max_energy})...", Fore.YELLOW)

    while True:
        if energy < 100:
            if not refill_used:
                log("REFILL", "Năng lượng sắp cạn, đang kích hoạt Boost Full-Energy miễn phí...", Fore.CYAN)
                try:
                    r_refill = requests.post(f"{API_BASE}/boost/full-energy", headers=headers, json={}, timeout=10).json()
                    energy = max_energy
                    refill_used = True
                    log("REFILL", f"Đã hồi đầy 100% Năng lượng ({max_energy})! Tiếp tục tap khai thác...", Fore.GREEN)
                    time.sleep(1)
                    continue
                except Exception:
                    log("REFILL", "Hôm nay đã dùng hết lượt Full-Energy.", Fore.YELLOW)
                    break
            else:
                log("TAP", f"Đã khai thác hết năng lượng ({energy}). Dừng tap.", Fore.WHITE)
                break

        tap_chunk = min(100, energy)
        try:
            r_tap = requests.post(f"{API_BASE}/tap", headers=headers, json={"count": tap_chunk}, timeout=10).json()
            accepted = r_tap.get("accepted", tap_chunk)
            coins = r_tap.get("coins", coins)
            energy = r_tap.get("energy", energy - accepted)
            log("TAP", f"Khai thác: +{accepted} taps | Số dư: {Fore.GREEN}{coins:,} Coins{Style.RESET_ALL} | Năng lượng còn: {energy}")
            time.sleep(random.uniform(1.0, 1.5))
        except Exception as e:
            log("ERR", f"Lỗi khi tap: {e}", Fore.RED)
            break

    # 8. Quét & Nhận thưởng các nhiệm vụ đã hoàn thành
    try:
        r_q = requests.post(f"{API_BASE}/quests", headers=headers, json={}, timeout=10).json()
        quests = r_q.get("quests", [])
        for q in quests:
            if q.get("claimable") and not q.get("claimed"):
                q_id = q.get("id")
                q_title = q.get("title")
                rew = q.get("reward", 0)
                log("QUEST", f"Đang nhận thưởng nhiệm vụ: {q_title} (+{rew:,} Coins)...", Fore.CYAN)
                r_qc = requests.post(f"{API_BASE}/quests/claim", headers=headers, json={"id": q_id}, timeout=10).json()
                coins = r_qc.get("coins", coins + rew)
                log("QUEST_OK", f"Hoàn thành: {q_title}! {Fore.GREEN}+{rew:,} Coins{Style.RESET_ALL}", Fore.GREEN)
                time.sleep(1)
    except Exception as e:
        log("ERR", f"Lỗi kiểm tra quests: {e}", Fore.RED)

    log("DONE", f"Hoàn thành chu kỳ cho {ACCOUNT_NAME}. Số dư cuối: {Fore.GREEN}{coins:,} Coins{Style.RESET_ALL}\n", Fore.CYAN)

def main():
    print(f"""
{Fore.CYAN}======================================================================
      TOOL AUTO RIGNITE MINING (@RigniteBot) - ACC HUNGZAI22
      - Tự động lấy x-init-data tươi mới 100% qua Telethon
      - Thu hoạch mỏ đào Offline (/shift/collect)
      - Điểm danh Daily Streak + Hộp quà Surprise + Vòng quay Wheel
      - Khai thác vàng Tap 100% Energy + Kích hoạt Boost Full-Energy
      - Tự động nhận thưởng tất cả Nhiệm vụ đạt mốc
      - Vòng lặp 24/7 (nghỉ {CYCLE_SLEEP_SECONDS // 60} phút giữa các chu kỳ)
======================================================================{Style.RESET_ALL}
    """)

    cycle = 0
    while True:
        cycle += 1
        print(f"\n{Fore.GREEN}>>>>>>>>>> BẮT ĐẦU CHU KỲ #{cycle} ({time.strftime('%Y-%m-%d %H:%M:%S')}) <<<<<<<<<<{Style.RESET_ALL}")
        run_rignite_cycle()

        log("SLEEP", f"Tạm nghỉ {CYCLE_SLEEP_SECONDS // 60} phút để mỏ đào tích lũy vàng & hồi năng lượng... (Bấm Ctrl+C để dừng)", Fore.YELLOW)
        try:
            time.sleep(CYCLE_SLEEP_SECONDS)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[THOÁT] Đã dừng chương trình theo yêu cầu.{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
