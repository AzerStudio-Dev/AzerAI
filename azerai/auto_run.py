import asyncio
import subprocess
import sys
import time
import os
from threading import Thread
from dotenv import load_dotenv

# .env faylını yüklə
load_dotenv(".env")

# --- LIVEKIT BULUT BAĞLANTI BİLGİLERİ (.env'den al) ---
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
API_KEY = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")
DEFAULT_ROOM = os.getenv("LIVEKIT_ROOM_NAME")
if not DEFAULT_ROOM:
    DEFAULT_ROOM = "AzerAI_Home"

def run_manager_script_in_background(target_agent, target_room=None):
    """
    Göstərilən agenti göstərilən otağa qoşmaq üçün idarəetmə skriptini arxa planda işə salır.
    Otaq adı verilməzsə, .env faylındakı LIVEKIT_ROOM_NAME istifadə olunur.
    """
    if target_room is None:
        target_room = DEFAULT_ROOM

    def task():
        # Serverin tam hazır vəziyyətə gəlməsi üçün 3 saniyə təhlükəsiz gözləmə
        time.sleep(3)
        
        print(f"\n🔥 [Sistem] Server hazırdır. '{target_agent}' üçün '{target_room}' otağında idarəetmə və Dispatch skripti başladılır...\n")
        
        manager_script = f"""
import asyncio
import os
from dotenv import load_dotenv
from livekit import api
from livekit.api import (
    CreateRoomRequest, 
    CreateAgentDispatchRequest, 
    ListRoomsRequest, 
    ListParticipantsRequest,
    RoomParticipantIdentity
)

# Alt prosesdə də .env yüklə
load_dotenv(".env")

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
API_KEY = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")

TARGET_ROOM = "{target_room}"
TARGET_AGENT = "{target_agent}"

async def main():
    print("\\n🌐 LiveKit İdarəetmə API müştərisi bağlanır...")
    
    if not all([LIVEKIT_URL, API_KEY, API_SECRET]):
        print("❌ Xəta: .env faylında bağlantı məlumatları çatışmır!")
        return

    async with api.LiveKitAPI(LIVEKIT_URL, API_KEY, API_SECRET) as lkapi:
        
        # 1. ADDIM: Otaq yoxlanışı
        print(f"🔍 '{{TARGET_ROOM}}' otağının mövcudluğu yoxlanılır...")
        rooms_res = await lkapi.room.list_rooms(ListRoomsRequest(names=[TARGET_ROOM]))
        
        room_exists = len(rooms_res.rooms) > 0
        
        if room_exists:
            print(f"✨ Otaq artıq aktiv vəziyyətdədir! (SID: {{rooms_res.rooms[0].sid}})")
            
            # 2. ADDIM: İştirakçıların yoxlanılması və mövcud agentin otaqdan çıxarılması (Kick)
            print(f"👥 Otaqdakı iştirakçılar yoxlanılır...")
            try:
                p_res = await lkapi.room.list_participants(ListParticipantsRequest(room=TARGET_ROOM))
                
                for p in p_res.participants:
                    if p.name == TARGET_AGENT or p.metadata == TARGET_AGENT or TARGET_AGENT in p.identity:
                        print(f"⚠️ '{{TARGET_AGENT}}' agenti artıq otaqda mövcuddur (Identity: {{p.identity}}).")
                        print(f"💥 Təkrar giriş tələb edildiyi üçün köhnə agent sessiyası otaqdan çıxarılır (Kicked)...")
                        
                        request_data = RoomParticipantIdentity(
                            room=TARGET_ROOM,
                            identity=p.identity
                        )
                        
                        await lkapi.room.remove_participant(request_data)
                        print("✅ Köhnə agent uğurla otaqdan təmizləndi.")
                        
                        await asyncio.sleep(1.5)
                        break
                        
            except Exception as e:
                print(f"❌ İştirakçı yoxlanılarkən və ya çıxarılarkən xəta baş verdi: {{e}}")
        else:
            print(f"🏗️ '{{TARGET_ROOM}}' otağı tapılmadı, yenidən yaradılır...")
            room_request = CreateRoomRequest(
                name=TARGET_ROOM,
                empty_timeout=10 * 60, # 10 dakika (600 saniye)
                max_participants=20,
            )
            room_info = await lkapi.room.create_room(room_request)
            print(f"✅ Otaq sıfırdan uğurla yaradıldı! SID: {{room_info.sid}}")
        
        # 3. ADDIM: Agenti yenidən otağa çağır (Dispatch)
        print(f"🚀 '{{TARGET_AGENT}}' agenti '{{TARGET_ROOM}}' otağına yenidən çağırılır...")
        dispatch_request = CreateAgentDispatchRequest(
            room=TARGET_ROOM,
            agent_name=TARGET_AGENT
        )
        
        dispatch_info = await lkapi.agent_dispatch.create_dispatch(dispatch_request)
        
        print("\\n==================================================")
        print("🎯 AGENT OTAQDAN ÇIXARILDI VƏ YENİDƏN ÇAĞIRILDI!")
        print("==================================================")
        print(f"🔹 Hədəf Otaq    : {{TARGET_ROOM}}")
        print(f"🔹 Çağırılan Agent: {{TARGET_AGENT}}")
        print(f"🔹 Dispatch ID  : {{dispatch_info.id}}")
        print(f"🔹 Vəziyyət     : Köhnə sessiya sonlandırıldı, yeni agent yoldadır.")
        print("==================================================")

if __name__ == '__main__':
    asyncio.run(main())
"""
        # Skripti arxa planda izolyasiya olunmuş alt proses kimi işə salırıq
        subprocess.Popen([sys.executable, "-c", manager_script])

    # Thread olarak başlat
    manager_thread = Thread(target=task, daemon=True)
    manager_thread.start()
