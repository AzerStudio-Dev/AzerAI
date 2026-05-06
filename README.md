# 🤖 AzerAI

**AzerAI** - Azərbaycan dilində qabaqcıl səsli AI Asistent
plugin əsaslı, çoxdilli AI asistent framework

## 🌟 Xüsusiyyətlər

- 🎤 **Səsli interfeys** - Real-time səsli danışıq
- 🇦🇿 **Azərbaycan dili** - Əsas dil Azərbaycan dilidir
- 🔌 **Plugin sistemi** - Genişlənəbilən plugin arxitekturası
- 💾 **Yaddaş** - Söhbət tarixçəsi və context
- 🎭 **Şəxsiyyət** - Dostlu və əyləncəli xarakter
- 🌍 **Çoxdilli** - 50+ dil dəstəyi
- 🚀 **Yüksək performans** - LiveKit ilə real-time əməliyyatlar

## Platform Dəstəyi

- 💻 **Windows** - Windows 10/11 dəstəklənir
- 🍎 **macOS** - macOS 10.15+ dəstəklənir  
- 🐧 **Linux** - Ubuntu, CentOS, Debian dəstəklənir
- 🐍 **Python** - Python 3.8+ tələb olunur

## 🚀 Quraşdırma

### Əsas quraşdırma
```bash
pip install AzerAI
```

### Bütün pluginlərlə birlikdə
```bash
pip install AzerAI[plugins]
```

### Əl ilə quraşdırma
```bash
git clone https://github.com/AzerStudio-Dev/AzerAI.git
cd AzerAI
pip install -e .
```

## ⚙️ Konfiqurasiya

`.env` faylı yaradın:
```env
# LiveKit Konfiqurasiyası
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=wss://your-livekit-server.com

# AI Model API Açarı Parametrləri
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key

# AI Model Seçimi (google və ya openai)
AI_PROVIDER=google
```

## 🎯 İstifadə

### Console modu
```bash
AzerAI console           # Konsol modunda işlə
```

### Digər əmrlər
```bash
AzerAI start             # Serveri başlad
```
```bash
AzerAI dev               # İnkişaf rejimi
```
```bash
AzerAI connect           # Qoşul
```
```bash
AzerAI download-files    # Faylları yüklə
```

## 🔌 Plugin Yaratmaq

Yeni plugin yaratmaq üçün ətraflı təlimata baxın:

📖 **[Plugin Yaratma və Yayımlama Təlimatı](https://github.com/AzerStudio-Dev/AzerAI/blob/main/PLUGIN_GUIDE.md)**

> **Sürətli Başlanğıc:**
> - Plugin adı `azerai-plugins-` prefiksi ilə başlamalıdır
> - Bütün funksiyalar `@function_tool()` dekoratoru ilə işarələnməlidir
> - Hər plugin `__init__.py`, `info.py`, `main.py`, `prompts.py` fayllarına malik olmalıdır
> - `ctx: RunContext` parametri hər funksiyada olmalıdır
> - Azərbaycan dilində təsvirlər istifadə edin
> - Funksiyalar `async` olmalıdır
> - Ətraflı təlimat üçün yuxarıdakı linkə klikləyin

## 🤝 İştirak

1. Fork edin
2. Feature branch yaradın (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request yaradın

## 📄 Lisenziya

Bu layihə MIT Lisenziyası ilə lisenziyalaşdırılıb - [LICENSE](https://github.com/AzerStudio-Dev/AzerAI/blob/main/LICENSE) faylına baxın.

## 🙏 Təşəkkürlər

- [Python](https://python.org/) - Proqramlaşdırma dili
- [LiveKit](https://livekit.io/) - Real-time audio/video framework
- [Google](https://ai.google.dev/) - AI modeli
- [OpenAI](https://openai.com/) - AI modeli
- Azərbaycan icması - Dəstək və tövsiyələr

## 📞 Əlaqə

- **Müəllif:** AzerStudio Dev
- **Email:** Info.AzerStudioDev@gmail.com
- **GitHub:** https://github.com/AzerStudio-Dev/AzerAI
- **PyPI:** https://pypi.org/project/AzerAI/

---

**🇦🇿 Azərbaycanın ilk tam plugin ekosistemli AI asistenti!** 🚀
