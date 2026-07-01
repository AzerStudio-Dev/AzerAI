"""
AzerAI - Əsas Assistant Sinifi
"""
from dotenv import load_dotenv
import asyncio
from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, FunctionToolsExecutedEvent
from livekit.plugins import (
    google,
    openai,
    silero,
    noise_cancellation,
)
from .plugins import get_all_tools, get_plugin_info, get_plugin_prompts, get_plugin_updates
from .prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from .memory import MemoryManager

load_dotenv(".env")
load_dotenv(".env.local")

class Assistant(Agent):
    def __init__(self) -> None:
        # Yaddaş menecerini başlat
        self.memory = MemoryManager()
        # Yaddaş kontekstini al və təlimatlara əlavə et
        memory_context = self.memory.get_memory_context()

        plugin_info = get_plugin_info()
        plugin_prompts = get_plugin_prompts()
        plugin_updates = get_plugin_updates()
        
        # Yeni versiya məlumatlarını təlimatlara əlavə et
        update_info = f"\n\nPlugin Yeniləmə Məlumatları:\n{plugin_updates}" if plugin_updates and "ən son versiyadadır" not in plugin_updates else ""
        
        super().__init__(instructions=plugin_info + plugin_prompts + update_info + AGENT_INSTRUCTION + memory_context)

    async def on_user_turn_completed(self, turn_ctx, new_message):
        """İstifadəçi danışığı bitirdikdə çağrılır - yaddaş konteksti əlavə et"""

        # Yaddaş kontekstini al və varsa istifadəçi mesajının başına əlavə et
        memory_context = self.memory.get_memory_context()
        if memory_context and new_message.content:
            # Məzmunu emlə et - bir string və ya listə ola bilər
            if isinstance(new_message.content, list):
                # Əgər məzmun bir listədirsə, yaddaş kontekstini ilk mətn elementinin başına əlavə et
                context_note = "\n[Əvvəlki danışıqlardan yadda saxla: Yuxarıdakı danışıq tarixinə görə cavab ver]\n"
                if new_message.content and isinstance(new_message.content[0], str):
                    new_message.content[0] = memory_context + context_note + new_message.content[0]
            elif isinstance(new_message.content, str):
                # Əgər məzmun bir stringdirsə, yaddaş kontekstini başına əlavə et
                context_note = "\n[Əvvəlki danışıqlardan yadda saxla: Yuxarıdakı danışıq tarixinə görə cavab ver]\n"
                new_message.content = memory_context + context_note + new_message.content
        
        await super().on_user_turn_completed(turn_ctx, new_message)
    
    async def store_conversation(self, user_message: str, assistant_message: str):
        """Danışıqı yaddaşda saxla"""
        
        if user_message and assistant_message:
            self.memory.add_conversation(user_message, assistant_message)

server = AgentServer()

@server.rtc_session(agent_name="") # Agent adı
async def my_agent(ctx: agents.JobContext):
    # Plugin bilgileri zaten Assistant'ta yükleniyor, tekrar çağrılmıyor
    all_tools = get_all_tools()
    # Yaddaşda saxlamaq üçün danışıq cütlüklərini izlə
    last_user_message = None

    # Asistan nümunəsi yarat
    assistant = Assistant()

    # AI modelini seç - Google və ya OpenAI
    import os
    from dotenv import load_dotenv
    load_dotenv(".env")
    load_dotenv(".env.local")
    
    # AI model seçimi - .env faylında AI_PROVIDER=google və ya AI_PROVIDER=openai
    ai_provider = os.getenv("AI_PROVIDER", "google").lower()
    
    if ai_provider == "openai":
        llm_model = openai.realtime.RealtimeModel(
            voice="marin"
        )
        print("🤖 OpenAI Realtime Model istifadə olunur...")
    else:
        # Defolt - Google
        llm_model = google.realtime.RealtimeModel(
            voice="Puck"
        )
        print("🤖 Google Realtime Model istifadə olunur...")
    
    session = AgentSession(
        vad=silero.VAD.load(),
        llm=llm_model,
        tools=all_tools,
    )

    # Tool çağırışlarını izləmək üçün sadə event handler
    @session.on("function_tools_executed")
    def on_function_tools_executed(event: FunctionToolsExecutedEvent):
        #print(f" [AZERAI] Tool çağırışları icra edildi: {len(event.function_calls)} tool")
        
        try:
            # Sadəcə tool adlarını yaz
            for i, call in enumerate(event.function_calls):
                print(f" [AzerAI] Tool: {call.name}")
                
        except Exception as e:
            print(f" [AzerAI] Event handler xətası: {e}")

    # Mesajları izləmək üçün danışıq elementlərini dinlə
    @session.on("conversation_item_added")
    def on_conversation_item(event):
        nonlocal last_user_message
        message = event.item

        # conversation_item_added həm ChatMessage, həm də AgentHandoff göndərə bilər.
        # AgentHandoff-də role/text_content olmur, ona görə əvvəlcə təhlükəsiz yoxla.
        role = getattr(message, "role", None)
        text_content = getattr(message, "text_content", None)

        # İstifadəçi mesajı olub olmadığını yoxla
        if role == "user" and text_content:
            last_user_message = text_content

        # Asistan mesajı olub olmadığını və uyğunlaşdırmaq üçün bir istifadəçi mesajı olub olmadığını yoxla
        elif role == "assistant" and text_content and last_user_message:
            # Danışıq cütünü saxla
            asyncio.create_task(assistant.store_conversation(
                last_user_message, 
                text_content
            ))
            last_user_message = None  # Saxladıqdan sonra sıfırla

    # Əvvəlcə otağa qoşuluruq
    await ctx.connect()

    await session.start(
        room=ctx.room,
        agent=assistant,
        # Otaq giriş konfiqurasiyası
        room_options=room_io.RoomOptions(
            # Video dəstəyi aktiv et
            video_input=room_io.VideoInputOptions(),
            
            # LiveKit Cloud təkmilləşdirilmiş gürültü aradan qaldırma
            # - Əgər self-hosting istifadə edirsinizsə, bu parametri buraxın
            # - Telephony proqramları üçün ən yaxşı nəticə üçün `BVCTelephony` istifadə edin
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    # Reminder plugin-ünə session referansını ver (əgər plugin mövcuddursa)
    try:
        from azerai_plugins_reminder.main import reminder_tools
        if reminder_tools is not None:
            reminder_tools.session_ref = session
            reminder_tools.loop_ref = __import__('asyncio').get_running_loop()
            print("[OK] Reminder plugin-ünə session referansı verildi")
        else:
            print("[NO] Reminder_tools None olduğu üçün session referansı verilmədi")
    except ImportError:
        pass

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
