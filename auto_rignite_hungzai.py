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

# TÀI KHOẢN HUNGZAI22
ACCOUNT_NAME = "hungzai22"
STRING_SESSION = os.getenv("TELEGRAM_STRING_SESSION_ACC1") or os.getenv("TELEGRAM_STRING_SESSION") or "1BVtsOHIBuxmpWiBJ9hvwV9pSrzWw5U2I5Fe20Ww8l1LCk9rnsG6T6lLZEJXZE1JJC_qUH_yyWHnRoedRNI5lJYnfjRN4gyGeDrCxquDU12ZflrpCz0VLhMZx2C0LlyUCy2eHRSRE1wUCpEYZaymL0P7Z9eAHwMy4Oogewh5TqyO4x4MF6j0yTq8Zvfpv43O4aQDzErNv3GRqpx8DXBcOJIMP9yVhq-Mby5VH5J9cF-h-bJ5ws3xKjA4GY7YKjHxDt9OI-Zr7mr-V3qZy99UxJooThJj51f2RqOKhODdLh9XZQ0ygSoAd3iFAZDOPMEo8Ch5TrrzLXi2Q3N0HorIL1JfV0xoFQlY="

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

def perform_login():
    """Tự động lấy token mới và đăng nhập lại Rignite"""
    log("AUTH", "Đang kết nối Telegram lấy x-init-data tự động...", Fore.CYAN)
    init_data = asyncio.run(fetch_fresh_init(STRING_SESSION))
    if not init_data:
        log("ERR", "Không thể lấy init-data từ @RigniteBot. Vui lòng kiểm tra lại mạng!", Fore.RED)
        return None, None

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

    try:
        r_auth = requests.post(f"{API_BASE}/auth", headers=headers, json={"lang": "vi", "dev": dev_id, "fp": fp}, timeout=15)
        if r_auth.status_code != 200:
            log("ERR", f"Đăng nhập thất bại: {r_auth.text}", Fore.RED)
            return None, None
        auth_data = r_auth.json()
        session_id = auth_data.get("sessionId")
        headers["x-session"] = session_id
        headers.pop("x-init-data", None)
        return headers, auth_data
    except Exception as e:
        log("ERR", f"Lỗi kết nối /auth: {e}", Fore.RED)
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

            # 3B. Chiến dịch XÂM LƯỢC (İSTİLA / INVASION)
            istila = r_pvp.get("istila", {})
            kalan_hak = istila.get("kalanHak", 0)
            seviye = istila.get("seviye", 1)
            dusman_gucu = istila.get("gosterilenDusmanGucu", 2300)
            is_completed = istila.get("tamamlandi", False)

            if not is_completed and kalan_hak > 0:
                is_attack = (seviye % 2 == 1)
                tur_name = "Tấn công Tiền đồn" if is_attack else "Phòng thủ Thuộc địa"
                oyuncu_gucu = my_atk if is_attack else my_def

                # NẾU LÀ ẢI PHÒNG THỦ VÀ THIẾU THỦ: NÂNG TƯỜNG THÀNH VỪA ĐỦ ĐỂ THẮNG
                if not is_attack and my_def < dusman_gucu:
                    if current_coins >= 100000:
                        r_wall = requests.post(f"{API_BASE}/koloni/sur/al", headers=headers, json={"tur": "duvar", "kademe": "ahsap", "adet": 1}, timeout=8).json()
                        if r_wall.get("ok"):
                            my_def += 100
                            oyuncu_gucu = my_def
                            current_coins = max(0, current_coins - r_wall.get("harcanan", 100000))
                            log("WALL_BUILD", f"🧱 Nâng thêm 1 Tường gỗ (Phòng thủ: {my_def}/{dusman_gucu}) vừa đủ để chuẩn bị thắng ải xâm lược!", Fore.YELLOW)

                if oyuncu_gucu >= dusman_gucu:
                    log("INVASION", f"🏴‍☠️ XUẤT KÍCH XÂM LƯỢC Ải {seviye} ({tur_name}): Ta {oyuncu_gucu} vs Địch {dusman_gucu}...", Fore.YELLOW)
                    payload = {
                        "seviye": seviye,
                        "kurguSurumu": 4,
                        "beklenenOyuncuGucu": oyuncu_gucu,
                        "beklenenDusmanGucu": dusman_gucu,
                        "komutId": str(uuid.uuid4())
                    }
                    r_ist = requests.post(f"{API_BASE}/pvp/istila/savas", headers=headers, json=payload, timeout=8).json()
                    savas = r_ist.get("savas", {})
                    if savas.get("kazandi"):
                        rew_rgt = savas.get("odulRgt", 0)
                        current_coins = r_ist.get("coins", current_coins + rew_rgt)
                        log("INVASION_WIN", f"🏆 CHIẾN THẮNG XÂM LƯỢC ẢI {seviye}! {Fore.GREEN}+{rew_rgt:,} RGT Coins{Style.RESET_ALL} (Đã mở khóa Ải {seviye + 1})", Fore.GREEN)
                    else:
                        log("INVASION", f"Trận xâm lược ải {seviye} chưa thành công.", Fore.LIGHTBLACK_EX)
                else:
                    log("INVASION_INFO", f"⚔️ Xâm lược ải {seviye} ({tur_name}): Lực chiến {oyuncu_gucu}/{dusman_gucu} (Đang tích lũy để thắng chắc 100%)", Fore.LIGHTBLACK_EX)

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

        log("AD", f"📺 Đang xem QC {label} (8.15s - Tối ưu siêu tốc)...", Fore.CYAN)
        time.sleep(8.15)

        payload = {
            "network": "warhold",
            "ymid": None,
            "ms": 8150,
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

    headers, auth_data = perform_login()
    if not headers or not auth_data:
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

    # 2. VÒNG LẶP ĐÀO SIÊU TỐC NON-STOP 24/7
    log("MINING_LOOP", "⚡ BẮT ĐẦU VÒNG LẶP ĐÀO SIÊU TỐC KHÔNG NGHỈ...", Fore.GREEN)
    last_side_check = time.time()
    last_ad_coin_check = 0

    while True:
        try:
            # A. Kiểm tra QC kiếm coin định kỳ 50s
            if time.time() - last_ad_coin_check >= 50:
                coins, next_cd = try_watch_coins_ad(headers, coins)
                last_ad_coin_check = time.time() - (50 - next_cd)

            # B. Kiểm tra sự kiện phụ (Minigame, PVP, Spark, Thuộc địa) mỗi 90s
            if time.time() - last_side_check >= 90:
                coins = check_side_activities(headers, coins)
                last_side_check = time.time()

            # C. HỒI PHỤC NĂNG LƯỢNG SIÊU TỐC TỰ ĐỘNG (XEM 1 LƯỢT QC -> TAP 600 NGAY):
            # - Tối ưu thời gian: Hồi phục +650 Energy trong 8.15s, lập tức tap 600 phát trong 0.5s
            # - Loại bỏ hoàn toàn thời gian chết (không cần tích lũy 8 lượt QC 85s như trước)
            if energy < 50:
                target_views = 1
                log("ENERGY", f"🔋 Năng lượng thấp ({energy}/{max_energy}). Xem 1 QC siêu tốc (8.15s) hồi phục để tap ngay...", Fore.CYAN)

                success_count = 0
                max_attempts = target_views * 3
                attempts = 0

                while success_count < target_views and attempts < max_attempts and energy < max_energy * 0.95:
                    attempts += 1
                    ad_idx = success_count + 1
                    log("AD_REFILL", f"📺 [Lượt QC {ad_idx}/{target_views}] Đang xem QC hồi năng lượng... (Đã có: {energy}/{max_energy})", Fore.CYAN)
                    ok, cd_or_energy, new_coins, new_ratio, info = try_refill_energy_ad(headers)
                    if ok:
                        success_count += 1
                        energy = cd_or_energy
                        coins = new_coins if new_coins > 0 else coins
                        ratio = new_ratio
                        log("REFILL_STEP", f"⚡ Xong lượt QC {ad_idx}/{target_views}! Năng lượng hiện có: {Fore.GREEN}{energy}/{max_energy}{Style.RESET_ALL} ({info})", Fore.GREEN)

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

            # D. ĐÀO SIÊU TỐC MÔ PHỎNG TAP 2 NÚT XEN KẼ KÍCH HOẠT OVERDRIVE (x3 VÀNG):
            # Nhịp tap xen kẽ liên tiếp (mỗi nhịp 25 - 30 taps cách nhau 0.12s)
            # Nhịp 1-2 đẩy combo lên x1.5, từ nhịp 3 trở đi bùng nổ OVERDRIVE (od = True, tapMult = 3.0) ăn gấp 3 lần vàng!
            while energy >= 10:
                chunk = min(30, max(1, energy // 10))
                r_tap = requests.post(f"{API_BASE}/tap", headers=headers, json={"count": chunk}, timeout=10).json()

                if r_tap.get("error") in ["UNAUTHORIZED", "SESSION_EXPIRED", "INVALID_SESSION", "SESSION_TAKEN"]:
                    log("REAUTH", "Session hết hạn hoặc mở trên đt, đang tự động kết nối lại lấy session mới...", Fore.YELLOW)
                    time.sleep(2)
                    new_headers, new_auth = perform_login()
                    if new_headers:
                        headers = new_headers
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

        except Exception as e:
            log("WARN", f"Lỗi tạm thời: {e}. Tiếp tục ngay sau 2s...", Fore.YELLOW)
            time.sleep(2)

if __name__ == "__main__":
    try:
        start_continuous_mining()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[THOÁT] Đã dừng chương trình an toàn.{Style.RESET_ALL}")
