"""
TOOL AUTO RIGNITE MINING 24/7 - COMBO 3 TÀI KHOẢN (Acc 1, Acc 2, Acc 3)
Chạy tuần tự xoay vòng trên 1 Runner duy nhất của GitHub Actions
"""
import os, sys, time, json, random, uuid, asyncio, urllib.parse, requests
from colorama import Fore, Style, init
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import RequestWebViewRequest

init(autoreset=True)

API_ID = 39182276
API_HASH = "f02b155d895a3a3fbf8a1cbe810b5338"
API_BASE = "https://api.rignite.app"
WEBAPP_URL = "https://app.rignite.app/"

ACCOUNTS = [
    {
        "name": "Acc 1 (hungzai22)",
        "account_id": "hungzai22",
        "session": os.getenv("TELEGRAM_STRING_SESSION_ACC1") or "1BVtsOHIBuxmpWiBJ9hvwV9pSrzWw5U2I5Fe20Ww8l1LCk9rnsG6T6lLZEJXZE1JJC_qUH_yyWHnRoedRNI5lJYnfjRN4gyGeDrCxquDU12ZflrpCz0VLhMZx2C0LlyUCy2eHRSRE1wUCpEYZaymL0P7Z9eAHwMy4Oogewh5TqyO4x4MF6j0yTq8Zvfpv43O4aQDzErNv3GRqpx8DXBcOJIMP9yVhq-Mby5VH5J9cF-h-bJ5ws3xKjA4GY7YKjHxDt9OI-Zr7mr-V3qZy99UxJooThJj51f2RqOKhODdLh9XZQ0ygSoAd3iFAZDOPMEo8Ch5TrrzLXi2Q3N0HorIL1JfV0xoFQlY="
    },
    {
        "name": "Acc 2 (gaylobucu)",
        "account_id": "gaylobucu",
        "session": os.getenv("TELEGRAM_STRING_SESSION_ACC2") or "1BVtsOHIBuzoeRtBOmpNGh2sdyxpZ5e0nY4MrFe-6KKbmJPaM0YnCJiKRI0L9mEh1C5rwqLQqucj456LRF7vV1YIPjZNqL6JevLM0Ww3FTml1NoKdwsiPINfsy9MbBlBhKOvha7py44L4pK5aEXjwpjpoNj4LaSmtWaPiQPufJuTwPB86f4gYjSeXM3HtxhnFU7MtHR5vbZPBa9N2HQSlt2BMB47q00DbQVtvYA37R3R-TrtV2MtwixL9ozChADFq38NYcw4eRyRwKrkobVLccvz0_hvqgHXiQbrfcFLLRkRGwGlRCB-Ew4YhLLdnCbG1hjGEfxUrp9MRmF0JvS-u20MfAuvlcgQ="
    },
    {
        "name": "Acc 3 (phanhoang)",
        "account_id": "phanhoang",
        "session": os.getenv("TELEGRAM_STRING_SESSION_ACC3") or "1BVtsOHIBuxrTG6Dt9a8C_J7D3bm1disV_mQiY_mw7AP5Gp-cEVAlKU1cfvOJiDnU6yi7PInfBRG_wJBQ3uNc-1kOa8fM3ITgUcE7YkaCd77FoBTgIFqw6gMYeRfVJOS1U9S_botQyX5764dx94NBfHHm8HuQKejs0PrdAJQq6WUTDS3mkijWRWIvO4SwXSUrM5yNOFoGIrav8Mbuyl5ZFQaDPg_kwa11NT4kiqov8rVx0virTbGbQudyFeG80kP4zW2CxcuL6TObemIPJgR_2-jb8zVQRQMiI4oN829ZCfHU2JCQY2S2clWwI7onZV8AhYP1LoDBiu32dgQPuk4brS-r1DtkySc="
    }
]

MAX_RUNTIME_SECONDS = int(os.getenv("MAX_RUNTIME_SECONDS", "17500"))
REPO_NAME = "rignite"
WORKFLOW_NAME = "rignite_mining.yml"

def log(tag, msg, color=Fore.WHITE):
    t_str = time.strftime('%H:%M:%S')
    print(f"{Fore.LIGHTBLACK_EX}[{t_str}]{Style.RESET_ALL} {color}[{tag}]{Style.RESET_ALL} {msg}", flush=True)

def trigger_next_shift():
    log("HANDOVER", f"🔄 Chuẩn bị chuyển giao ca làm việc tiếp theo trên {REPO_NAME}...", Fore.CYAN)
    pat = os.getenv("GH_PAT") or ("ghp_" + "7NXx41Smy2fKlEj4X68Pnpv8i3GFo60cduvW")
    repo = os.getenv("GITHUB_REPOSITORY") or f"nthanhhung0122-max/{REPO_NAME}"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{WORKFLOW_NAME}/dispatches"
    headers = {"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github.v3+json"}
    try:
        r = requests.post(url, headers=headers, json={"ref": "main"}, timeout=15)
        if r.status_code == 204:
            log("HANDOVER", f"✅ Đã kích hoạt ca chạy tiếp theo trên {repo}!", Fore.GREEN)
            return True
    except Exception as e:
        log("HANDOVER", f"Lỗi retrigger: {e}", Fore.RED)
    return False
async def fetch_fresh_init(session_str):
    try:
        if session_str:
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
        elif os.path.exists(SESSION_FILE + ".session"):
            client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        else:
            return None

        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            return None

        bot = await client.get_input_entity("RigniteBot")
        res = await client(RequestWebViewRequest(
            peer=bot, bot=bot, platform="android", url=WEBAPP_URL
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

def perform_login(session_str, acc_name, max_retries=3):
    """Tự động lấy token mới và đăng nhập lại Rignite với cơ chế retry"""
    for attempt in range(1, max_retries + 1):
        log("AUTH", f"Đang kết nối Telegram lấy x-init-data tự động cho Acc 3 (phan hoàng) (Lần {attempt}/{max_retries})...", Fore.CYAN)
        try:
            init_data = asyncio.run(fetch_fresh_init(session_str))
            if not init_data:
                log("WARN", f"Chưa lấy được init-data từ @RigniteBot, đợi 5s thử lại...", Fore.YELLOW)
                time.sleep(5)
                continue

            dev_id, ua, fp = generate_device_info(acc_name)
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

def auto_upgrade_boosts(headers, coins, multitap_lvl, energy_limit_lvl):
    """Tự động nâng cấp MultiTap và Dung tích bình năng lượng (Energy Limit) khi đủ tiền"""
    if coins < 3000:
        return coins, multitap_lvl, energy_limit_lvl

    # 1. Nâng cấp Energy Limit nếu cấp còn thấp (< 12)
    if energy_limit_lvl < 12 and coins >= 2000:
        try:
            r = requests.post(f"{API_BASE}/boost/upgrade", headers=headers, json={"type": "energy_limit"}, timeout=8).json()
            if r.get("maxEnergy"):
                new_max = r.get("maxEnergy")
                energy_limit_lvl = r.get("energyLimitLevel", energy_limit_lvl + 1)
                coins = r.get("coins", coins)
                log("UPGRADE_LIMIT", f"🚀 NÂNG CẤP BÌNH CHỨA CẤP {energy_limit_lvl}! Dung tích: {Fore.GREEN}{new_max:,} Energy{Style.RESET_ALL} (Còn {coins:,} Coins)", Fore.GREEN)
        except Exception:
            pass

    # 2. Nâng cấp MultiTap nếu cấp còn thấp (< 12)
    if multitap_lvl < 12 and coins >= 2000:
        try:
            r = requests.post(f"{API_BASE}/boost/upgrade", headers=headers, json={"type": "multitap"}, timeout=8).json()
            if r.get("multitapLevel"):
                multitap_lvl = r.get("multitapLevel", multitap_lvl + 1)
                coins = r.get("coins", coins)
                log("UPGRADE_TAP", f"⚡ NÂNG CẤP MULTITAP CẤP {multitap_lvl}! Sát thương tap tăng vượt trội! (Còn {coins:,} Coins)", Fore.GREEN)
        except Exception:
            pass

    return coins, multitap_lvl, energy_limit_lvl

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
            log("SANTRAL", f"⚡ Thu hoạch 8 trạm điện thuộc địa: {Fore.GREEN}+{total_santral:,} Điện năng{Style.RESET_ALL}", Fore.GREEN)
    except Exception:
        pass

    # 2. Hộp quà bí mật Surprise (/surprise/open)
    try:
        r_surp = requests.post(f"{API_BASE}/surprise/open", headers=headers, json={}, timeout=8).json()
        if r_surp.get("ok"):
            s_rew = r_surp.get("reward", 0)
            current_coins = r_surp.get("coins", current_coins + s_rew)
            log("SURPRISE", f"🎁 Mở hộp quà bí mật: {Fore.GREEN}+{s_rew:,} Coins{Style.RESET_ALL} (Tổng: {current_coins:,})", Fore.GREEN)
    except Exception:
        pass

    # 3. Minigame Đập Kim Cương Săn Jackpot 10X (/minigame/finish)
    try:
        r_mg_state = requests.get(f"{API_BASE}/minigame/state", headers=headers, timeout=8).json()
        left_mg = r_mg_state.get("left", 0)
        while left_mg > 0:
            log("MINIGAME", f"💎 Tìm thấy {left_mg} lượt minigame kim cương. Bắt đầu đập...", Fore.CYAN)
            r_start = requests.post(f"{API_BASE}/minigame/start", headers=headers, json={}, timeout=8).json()
            if r_start.get("ok"):
                mg_token = r_start.get("token")
                time.sleep(3.5)
                r_fin = requests.post(f"{API_BASE}/minigame/finish", headers=headers, json={"token": mg_token, "score": "perfect"}, timeout=8).json()
                if r_fin.get("ok"):
                    mg_coins = r_fin.get("reward", 0)
                    current_coins = r_fin.get("coins", current_coins + mg_coins)
                    log("MINIGAME", f"💎 ĐẬP KIM CƯƠNG PERFECT: {Fore.GREEN}+{mg_coins:,} Coins!{Style.RESET_ALL} (Tổng: {current_coins:,})", Fore.GREEN)
                else:
                    break
            else:
                break
            left_mg -= 1
            time.sleep(1.5)
    except Exception:
        pass

    # 4. Đấu trường PVP Arena (/arena/fight)
    try:
        r_pvp_state = requests.get(f"{API_BASE}/arena/state", headers=headers, timeout=8).json()
        pvp_left = r_pvp_state.get("fightsLeft", 0)
        while pvp_left > 0:
            opponents = r_pvp_state.get("opponents", [])
            if opponents:
                opponents.sort(key=lambda x: x.get("power", 999999))
                target = opponents[0]
                t_id = target.get("id")
                t_name = target.get("name", "Opponent")
                log("PVP", f"⚔️ Đấu trường PVP ({pvp_left} lượt): Tấn công '{t_name}'...", Fore.CYAN)
                r_fight = requests.post(f"{API_BASE}/arena/fight", headers=headers, json={"opponentId": t_id}, timeout=8).json()
                if r_fight.get("won"):
                    p_win = r_fight.get("reward", 1000)
                    p_rank = r_fight.get("rankPoints", 25)
                    current_coins = r_fight.get("coins", current_coins + p_win)
                    log("PVP_WIN", f"🏆 CHIẾN THẮNG PVP: {Fore.GREEN}+{p_win:,} Coins | +{p_rank} Rank Points!{Style.RESET_ALL} (Tổng: {current_coins:,})", Fore.GREEN)
                else:
                    log("PVP_RES", f"Kết quả PVP: Thua/hòa ({r_fight})", Fore.YELLOW)
            else:
                break
            pvp_left -= 1
            time.sleep(2)
    except Exception:
        pass

    # 5. Kích hoạt Spark Boost (+15% Tốc độ đào mỏ)
    try:
        r_spark = requests.post(f"{API_BASE}/spark/trigger", headers=headers, json={}, timeout=8).json()
        if r_spark.get("ok"):
            log("SPARK", "⚡ ĐÃ BẮN TIA SPARK BOOST: +15% Tốc độ sản xuất mỏ!", Fore.MAGENTA)
    except Exception:
        pass

    # 6. Vòng quay may mắn Lucky Wheel (/wheel/spin)
    try:
        r_wh = requests.post(f"{API_BASE}/wheel/spin", headers=headers, json={}, timeout=8).json()
        if r_wh.get("ok"):
            w_rew = r_wh.get("reward", {})
            w_amt = w_rew.get("amount", 0)
            w_kind = w_rew.get("kind", "coins")
            log("WHEEL", f"🎡 QUAY VÒNG QUAY: Trúng [{w_kind}: +{w_amt:,}]!", Fore.GREEN)
    except Exception:
        pass

    # 7. Nhận điểm danh hàng ngày Streak (/daily/claim)
    try:
        r_daily = requests.post(f"{API_BASE}/daily/claim", headers=headers, json={}, timeout=8).json()
        if r_daily.get("ok"):
            d_rew = r_daily.get("reward", 0)
            current_coins = r_daily.get("coins", current_coins + d_rew)
            log("STREAK", f"📅 ĐIỂM DANH HÀNG NGÀY: {Fore.GREEN}+{d_rew:,} Coins!{Style.RESET_ALL} (Tổng: {current_coins:,})", Fore.GREEN)
    except Exception:
        pass

    return current_coins

def execute_ad_view(headers, ad_type, label):
    """Giả lập xem quảng cáo an toàn chuẩn giao thức Adexium"""
    try:
        r_bid = requests.post(f"{API_BASE}/ad/bid", headers=headers, json={"type": ad_type}, timeout=10).json()
        bid_token = r_bid.get("bidToken") or r_bid.get("token")
        if not bid_token:
            cd = r_bid.get("cooldown", 5)
            return False, cd, f"Chưa có bid token (cooldown {cd}s)"

        watch_time = 8.15
        time.sleep(watch_time)

        r_complete = requests.post(f"{API_BASE}/ad/complete", headers=headers, json={"type": ad_type, "bidToken": bid_token}, timeout=10).json()
        if r_complete.get("ok"):
            return True, r_complete, "Thành công"
        else:
            return False, 5, f"Complete thất bại: {r_complete.get('error')}"
    except Exception as e:
        return False, 5, f"Lỗi xem QC: {e}"

def try_refill_energy_ad(headers):
    ok, res, msg = execute_ad_view(headers, "energy", "Hồi năng lượng")
    if ok:
        energy = res.get("energy", 0)
        coins = res.get("coins", 0)
        ratio = res.get("adEnergyRatio", 1)
        return True, energy, coins, ratio, f"Hồi thành công -> {energy} Energy"
    else:
        cd = res if isinstance(res, (int, float)) else 5
        return False, cd, 0, 1, msg

def try_watch_coins_ad(headers, current_coins):
    ok, res, msg = execute_ad_view(headers, "coins", "Kiếm Coins")
    if ok:
        new_coins = res.get("coins", current_coins)
        diff = new_coins - current_coins
        log("AD_COIN", f"💰 Xem QC nhận: {Fore.GREEN}+{diff:,} Coins{Style.RESET_ALL} (Tổng: {new_coins:,})", Fore.GREEN)
        return new_coins, 50
    else:
        return current_coins, 20


def process_account_turn(acc):
    name = acc["name"]
    log("ACC", f"=== Lượt chơi: {name} ===", Fore.MAGENTA)
    
    now_t = time.time()
    if "headers" not in acc or (now_t - acc.get("last_login", 0)) > 2700:
        h, auth = perform_login(acc["session"], acc["account_id"], max_retries=2)
        if not h:
            log("LOGIN_FAIL", f"[{name}] Đăng nhập thất bại.", Fore.RED)
            return
        acc["headers"] = h
        u = auth.get("user", {})
        acc["coins"] = u.get("coins", 0)
        acc["energy"] = u.get("energy", 1000)
        acc["max_energy"] = u.get("maxEnergy", 1000)
        acc["multitap_lvl"] = u.get("multitapLevel", 1)
        acc["energy_limit_lvl"] = u.get("energyLimitLevel", 1)
        acc["full_energy_left"] = u.get("fullEnergyLeft", 0)
        acc["last_login"] = now_t
        log("LOGIN_OK", f"[{name}] Coins: {acc['coins']:,} | Energy: {acc['energy']}/{acc['max_energy']} | Booster: {acc['full_energy_left']}", Fore.GREEN)

    headers = acc["headers"]
    coins = acc.get("coins", 0)
    energy = acc.get("energy", 0)
    max_energy = acc.get("max_energy", 1000)
    full_energy_left = acc.get("full_energy_left", 0)

    # 2. Xả Energy (Tapping)
    while energy >= 10:
        chunk = min(30, max(1, energy // 10))
        try:
            r_tap = requests.post(f"{API_BASE}/tap", headers=headers, json={"count": chunk}, timeout=10).json()
            if r_tap.get("error") in ["UNAUTHORIZED", "SESSION_EXPIRED", "INVALID_SESSION", "SESSION_TAKEN"]:
                acc.pop("headers", None)
                break
            accepted = r_tap.get("accepted", 0)
            if accepted <= 0:
                break
            coins = r_tap.get("coins", coins)
            energy = r_tap.get("energy", 0)
            time.sleep(0.12)
        except Exception:
            break

    # 3. Kích hoạt Full Energy Booster nếu cạn năng lượng và còn lượt
    if energy < 50 and full_energy_left > 0:
        log("BOOSTER", f"[{name}] ⚡ Kích hoạt bình Full Energy miễn phí...", Fore.MAGENTA)
        try:
            r_fe = requests.post(f"{API_BASE}/boost/full-energy", headers=headers, json={}, timeout=8).json()
            if r_fe.get("energy"):
                energy = r_fe.get("energy")
                max_energy = r_fe.get("maxEnergy", max_energy)
                full_energy_left = r_fe.get("fullEnergyLeft", full_energy_left - 1)
                log("BOOSTER_OK", f"[{name}] 🔋 Đã đầy 100% ({energy}/{max_energy})! Tiếp tục tap...", Fore.GREEN)
                while energy >= 10:
                    chunk = min(30, max(1, energy // 10))
                    r_tap = requests.post(f"{API_BASE}/tap", headers=headers, json={"count": chunk}, timeout=10).json()
                    accepted = r_tap.get("accepted", 0)
                    if accepted <= 0:
                        break
                    coins = r_tap.get("coins", coins)
                    energy = r_tap.get("energy", 0)
                    time.sleep(0.12)
        except Exception:
            pass

    # 4. Tự động nâng cấp khi đủ coin
    coins, acc["multitap_lvl"], acc["energy_limit_lvl"] = auto_upgrade_boosts(headers, coins, acc.get("multitap_lvl", 1), acc.get("energy_limit_lvl", 1))

    # 5. Kiểm tra hoạt động phụ (Minigame, Spark, PVP)
    coins = check_side_activities(headers, coins)

    acc["coins"] = coins
    acc["energy"] = energy
    acc["max_energy"] = max_energy
    acc["full_energy_left"] = full_energy_left
    log("SUMMARY", f"[{name}] Hoàn thành lượt. Số dư: {coins:,} Coins | Energy: {energy}/{max_energy}", Fore.CYAN)

def main():
    print(f"{Fore.CYAN}{'='*72}", flush=True)
    print(f"{Fore.YELLOW}  TOOL AUTO RIGNITE MINING 24/7 - COMBO 3 ACC (NON-STOP)", flush=True)
    print(f"{Fore.CYAN}{'='*72}\n", flush=True)

    start_time = time.time()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        for acc in ACCOUNTS:
            process_account_turn(acc)
        return

    while True:
        try:
            if time.time() - start_time >= MAX_RUNTIME_SECONDS:
                log("SHIFT_END", "⏱️ Hoàn tất ca trực 4.8h. Bàn giao ca tiếp theo...", Fore.MAGENTA)
                trigger_next_shift()
                break

            for acc in ACCOUNTS:
                process_account_turn(acc)
                time.sleep(2)

            log("SLEEP", "⏳ Cả 3 acc đã xả năng lượng. Nghỉ 40s hồi phục trước vòng tiếp theo...", Fore.BLUE)
            time.sleep(40)

        except KeyboardInterrupt:
            log("STOP", "Dừng tool bằng tay.", Fore.YELLOW)
            break
        except Exception as e:
            log("ERR_LOOP", f"Lỗi vòng lặp: {e}", Fore.RED)
            time.sleep(10)

if __name__ == '__main__':
    main()
