# 🔌 AzerAI Plugin Yaratma və Yayımlama Təlimatı

Bu təlimatda addım-addım yeni AzerAI plugini yaratmağı, test etməyi və PyPI-ə yayımlamağı öyrənəcəksiniz.

---

## 📋 Mündəricat

1. [Plugin Strukturu](#1-plugin-strukturu)
2. [Başlamaq](#2-başlamaq)
3. [pyproject.toml Yaradılması](#3-pyprojecttoml-yaradılması)
4. [__init__.py Yaradılması](#4-__init__py-yaradılması)
5. [Plugin Kodunun Yazılması](#5-plugin-kodunun-yazılması)
6. [info.py Yaradılması](#6-infopy-yaradılması)
7. [prompts.py Yaradılması](#7-promptspy-yaradılması)
8. [README.md Yaradılması](#8-readmemd-yaradılması)
9. [LICENSE Yaradılması](#9-license-yaradılması)
10. [Test Etmək](#10-test-etmək)
11. [Yayımlamaq](#11-yayımlamaq)
12. [Lokal Quraşdırma](#12-lokal-quraşdırma)

---

## 1. Plugin Strukturu

```
azerai-plugins-my/
├── azerai_plugins_my/
│   ├── __init__.py
│   ├── info.py
│   ├── main.py
│   └── prompts.py
├── LICENSE
├── pyproject.toml
└── README.md
```

---

## 2. Başlamaq

Plugin qovluğu yaradın:

```bash
mkdir azerai-plugins-my
cd azerai-plugins-my
```

---

## 3. `pyproject.toml` Yaradılması

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "azerai-plugins-my"
version = "1.0.0"
description = "**AzerAI My Plugin** - Test Plugin"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
    "Operating System :: MacOS :: MacOS X",
]
keywords = ["azerai", "plugins", "ai", "azerbaijani", "test"]
requires-python = ">=3.8"

dependencies = [
    "livekit-agents"
]

[project.urls]
Homepage = "https://github.com/YourUsername/AzerAI-Plugins-My"
Repository = "https://github.com/YourUsername/AzerAI-Plugins-My.git"
"Bug Tracker" = "https://github.com/YourUsername/AzerAI-Plugins-My/issues"

[tool.setuptools.packages.find]
where = ["."]
include = ["azerai_plugins_my*"]

[tool.setuptools.package-data]
azerai_plugins_my = ["*.txt", "*.md"]
```

---

## 4. `__init__.py` Yaradılması

```python
"""
AzerAI My Plugin - Paketin Giriş Nöqtəsi Və Export Olunan Funksiyalar
"""
from .main import my_function

__all__ = [
    "my_function"
]
```

---

## 5. `main.py` Plugin Kodunun Yazılması

```python
"""
AzerAI My Plugin - Test Alətləri
"""
import logging
from livekit.agents import function_tool, RunContext

logger = logging.getLogger("AzerAI-Plugins-My")

@function_tool()
async def my_function(
    ctx: RunContext,
    param: str
) -> str:
    """Plugin funksiyası - parametrlə işləyir."""
    
    try:
        result = f"Plugin işlədi: {param}"
        logger.info(f"Plugin nəticə: {result}")
        return result
    except Exception as e:
        logger.error(f"Plugin xətası: {e}")
        return f"Xəta baş verdi: {str(e)}"
```

---

## 6. `info.py` Yaradılması

```python
"""
AzerAI My Plugin - Plugin Haqqında Məlumatlar Və Metadata
"""
PLUGIN_INFO = {
    "name": "azerai-plugins-my",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "**AzerAI My Plugin** - Test Plugin",
    "license": "MIT",
    "url": "https://github.com/yourusername/azerai-plugins-my",
    "pypi": "https://pypi.org/project/azerai-plugins-my"
}
```

---

## 7. `prompts.py` Yaradılması

```python
"""
AzerAI My Plugin - Test Plugin AI Təlimatları
"""
PLUGIN_PROMPT = """
My Plugin Capability:
You can use my_function to process parameters and return results.

Available functions:
- my_function(param) - Processes the given parameter

Function Details:

1. my_function()
   - Args:
     * param (str): Giriş parametri - istənilən mətn dəyəri
   - Returns: Str - Parametrlə birlikdə işlənmiş nəticə
     Məsələn: "Plugin işlədi: test_parametr"

When users need to process text or data, use this function.

Examples:
- "Test et" -> Use my_function("Test")
- "Məlumat işlə" -> Use my_function("məlumat")

Always provide responses in Azerbaijani language unless specifically asked otherwise.
"""
```

---

## 8. `README.md` Yaradılması

````markdown
# 🚀 AzerAI My Plugin

**AzerAI** - Azərbaycan dilində qabaqcıl səsli AI asistent üçün xüsusi plugin

## Xüsusiyyətlər

- ✨ **Xüsusi funksiya** - Özəl imkanlar
- 🌍 **Azərbaycan dilində** - Tam lokalizasiya dəstəyi
- 📈 **Genişlənəbilən** - Asan inteqrasiya

## Platform Dəstəyi

- 💻 **Windows** - Windows 10/11 dəstəklənir
- 🍎 **macOS** - macOS 10.15+ dəstəklənir  
- 🐧 **Linux** - Ubuntu, CentOS, Debian dəstəklənir
- 🐍 **Python** - Python 3.8+ tələb olunur

## Quraşdırma

```bash
pip install AzerAI-Plugins-My
```

## İstifadə

Plugin avtomatik olaraq AzerAI tərəfindən aşkar edilir.

### Əmrlər

- `"Test et"` - Test funksiyasını işlət
- `"Məlumat göstər"` - Məlumatları ekranda göstər

## Fayl struktur

```
azerai_plugins_my/
├── __init__.py
├── info.py
├── main.py
└── prompts.py
```

## Asılılıqlar

- `livekit-agents` - AI agent framework
- Digər asılılıqlar...

## 📄 Lisenziya

Bu layihə MIT Lisenziyası ilə lisenziyalaşdırılıb - [LICENSE](https://github.com/yourusername/AzerAI-Plugins-My/blob/main/LICENSE) faylına baxın.

## 📞 Əlaqə

- **Müəllif:** Sizin Adınız
- **Email:** email@example.com
- **GitHub:** https://github.com/username/AzerAI-Plugins-My
- **PyPI:** https://pypi.org/project/AzerAI-Plugins-My/

---

**🇦🇿 Azərbaycanın ilk tam plugin ekosistemli AI asistenti üçün plugin!** 🚀
````

---

## 9. `LICENSE` Yaradılması

```text
MIT License

Copyright (c) year fullname

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 10. Test Etmək

Yerli quraşdırma ilə test edin:

```bash
# Yerli quraşdırma
pip install -e .

# Test
python -c "from azerai_plugins_my import my_function; print(my_function('test'))"
```

---

## 11 Asılılıqları Quraşdırma

```bash
pip install --upgrade build setuptools wheel # Build etmək üçün
```
```bash
pip install --upgrade twine # PyPI-ə yükləmək üçün
```

## 12. Yayımlamaq

PyPI-ə yükləmək üçün:

```bash
# Build et
python -m build

# PyPI-ə yüklə
python -m twine upload dist/*
```

---

## 12. Lokal Quraşdırma

Əgər plugini yerli olaraq qurmaq istəyirsinizsə:

1. **Plugins qovluğu yaradın:**
```bash
mkdir plugins
cd plugins
```

2. **Plugini köçürün:**
```bash
cp -r /path/to/azerai_plugins_my .
```

3. **Yerli quraşdırma:**
```bash
cd azerai_plugins_my
pip install -e .
```

4. **AzerAI-ni yenidən başladın:**
```bash
AzerAI console
```

---

## 💡 İpucları

### Fayl Tələbləri
- ✅ `__init__.py` - Paketin giriş nöqtəsi və export olunan funksiyalar
- ✅ `info.py` - Plugin məlumatları (name, version, author, description, license, url, pypi)
- ✅ `main.py` - Plugin kodları və `@function_tool()` dekoratorlu funksiyalar
- ✅ `prompts.py` - AI təlimatları (PLUGIN_PROMPT dəyişəni)
- ✅ `LICENSE` - MIT lisenziya faylı
- ✅ `pyproject.toml` - Konfiqurasiya faylı (classifiers, keywords, dependencies)
- ✅ `README.md` - İstifadəçilər üçün ətraflı dokumentasiya

### Kod Tələbləri
- ✅ Plugin adı `azerai-plugins-` prefiksi ilə başlamalıdır
- ✅ Bütün funksiyalar `@function_tool()` dekoratoru ilə işarələnməlidir
- ✅ `info.py` faylında bütün metadatalar tam olmalıdır
- ✅ `ctx: RunContext` parametri hər funksiyada olmalıdır
- ✅ Azərbaycan dilində təsvirlər istifadə edin
- ✅ Funksiyalar `async` olmalıdır

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

**🇦🇿 Uğurlar! Azərbaycanın ilk tam plugin ekosistemli AI asistentinə töhfə verdiyiniz üçün təşəkkürlər!** 🚀
