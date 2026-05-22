"""
AzerAI Plugin System - Plugin Yükləyici Və İdarəetmə Sistemi
"""
import importlib
import os
import logging
import subprocess
import requests
import sys
from typing import List, Any, Dict

logger = logging.getLogger("AzerAI-Plugins")

class PluginManager:
    def __init__(self):
        self.loaded_plugins = {}
        self.plugin_tools = {}
        self.discover_plugins()
        self.check_for_updates()

    def check_for_updates(self):
        """PyPI-də yeni versiyaları yoxla"""

        try:
            for plugin_name in self.loaded_plugins.keys():
                if plugin_name.startswith('azerai-plugins-') or plugin_name.startswith('azerai_plugins_') or plugin_name.startswith('AzerAI-Plugins-') or plugin_name.startswith('AzerAI_Plugins_') or plugin_name == 'AzerAI' or 'azerai' in plugin_name:
                    # Pip-in qlobal versiyasını yoxla
                    current_version = self._get_installed_version(plugin_name)
                    latest_version = self._get_latest_version(plugin_name)
                    
                    if latest_version and current_version and latest_version != current_version:
                        print(f"🔄 Yeni versiya mövcuddur: {plugin_name} {current_version} → {latest_version}")
                        print(f"   Yeniləmək üçün: pip install --upgrade {plugin_name}")
        except Exception as e:
            logger.debug(f"Versiya yoxlaması xətası: {e}")

    def _get_installed_version(self, package_name: str) -> str:
        """Qurulmuş paket versiyasını pip show ilə al"""

        try:
            result = subprocess.run(['pip', 'show', package_name], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        return line.split(':')[1].strip()
        except Exception:
            pass
        return ""

    def _get_latest_version(self, package_name: str) -> str:
        """PyPI-dən ən son versiyanı al"""

        try:
            response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=3)
            if response.status_code == 200:
                data = response.json()
                return data.get('info', {}).get('version', '')
        except Exception:
            pass
        return ""

    def discover_plugins(self):
        """Hem lokal hem de pip ile yüklənmiş pluginləri aşkar et"""

        # Pip ile yüklənmiş pluginləri yüklə
        self._load_pip_plugins()
        
        # Lokal pluginləri yüklə
        self._load_local_plugins()

    def _load_pip_plugins(self):
        """Pip ile yüklənmiş pluginləri avtomatik aşkar et"""

        # Pip list ilə avtomatik kəşf
        try:
            result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('azerai-plugins-') or line.startswith('azerai_plugins_') or line.startswith('AzerAI-Plugins-') or line.startswith('AzerAI_Plugins_') or line.startswith('azerai') or line.startswith('AzerAI'):
                        plugin_name = line.split()[0]
                        # AzerAI əsas sistemdir, plugin deyil - plugin siyahısından çıxar
                        if plugin_name == 'azerai':
                            continue
                        # Modul adını kiçik hərflərə çevir
                        module_name = plugin_name.replace('-', '_').lower()
                        try:
                            module = importlib.import_module(module_name)
                            
                            # Info faylından detallı məlumatları yoxla
                            plugin_info = self._get_plugin_info(module, plugin_name)
                            
                            self.loaded_plugins[plugin_name] = plugin_info
                            print(f"[OK] {plugin_name}")
                        except ImportError as e:
                            print(f"[ERR] {module_name}: {e}")
                            logger.warning(f"Plugin yüklənə bilmədi {module_name}: {e}")
                        except Exception as e:
                            print(f"[ERR] {module_name}: {e}")
                            logger.error(f"Plugin yükləmə xətası {module_name}: {e}")
        except Exception as e:
            logger.error(f"pip list xətası: {e}")
            print(f"[ERR] pip list: {e}")

    def _load_local_plugins(self):
        """Lokal pluginləri yüklə"""

        # Çoxlu yerlərdə plugin qovluğu axtar - daha çevik yanaşma
        possible_paths = [
            # 1. AzerAI qovluğunun yanında
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'plugins'),
            # 2. Current working directory-də
            os.path.join(os.getcwd(), 'plugins'),
            # 3. Bir level yuxarı
            os.path.join(os.path.dirname(os.getcwd()), 'plugins'),
            # 4. Home directory-də
            os.path.join(os.path.expanduser('~'), 'azerai_plugins'),
        ]
        
        for local_plugins_dir in possible_paths:
            if not os.path.exists(local_plugins_dir):
                logger.debug(f"Lokal plugin qovluğu tapılmadı: {local_plugins_dir}")
                continue
                
            logger.debug(f"Lokal plugin qovluğu tapıldı: {local_plugins_dir}")
            
            for plugin_name in os.listdir(local_plugins_dir):
                plugin_path = os.path.join(local_plugins_dir, plugin_name)
                
                if os.path.isdir(plugin_path) and not plugin_name.startswith('.'):
                    # main.py faylını yoxla
                    main_file = os.path.join(plugin_path, '__init__.py')
                    if os.path.exists(main_file):
                        try:
                            # Plugin qovluğunu Python path-ə əlavə et
                            if local_plugins_dir not in sys.path:
                                sys.path.insert(0, local_plugins_dir)
                            
                            # Plugin modulunu yüklə
                            module = importlib.import_module(plugin_name)
                            
                            # Info faylından detallı məlumatları yoxla
                            plugin_info = self._get_plugin_info(module, plugin_name)
                            
                            self.loaded_plugins[plugin_name] = plugin_info
                            print(f"[OK] {plugin_name} (lokal) -> {local_plugins_dir}")
                            
                        except ImportError as e:
                            logger.error(f"Lokal plugin yüklənə bilmədi {plugin_name}: {e}")
                            print(f"[ERR] {plugin_name}: {e}")
                        except Exception as e:
                            logger.error(f"Lokal plugin xətası {plugin_name}: {e}")
                            print(f"[ERR] {plugin_name}: {e}")
            
            # Əgər pluginlər tapsaq, axtarışı dayandır
            if os.path.exists(local_plugins_dir):
                break

    def _get_plugin_info(self, module, plugin_name: str) -> Dict[str, Any]:
        """Plugin məlumatlarını yalnız info.py faylından alır"""

        base_info = {
            'name': plugin_name,
            'module': module,
            'tools': self._extract_tools(module),
        }
        
        # Yalnız info.py faylından məlumat al - avtomatik path tapma
        # Əsas info.py path-lərini yoxla
        info_paths = [
            f"{module.__name__}.info"
        ]
        
        for info_path in info_paths:
            try:
                info_module = importlib.import_module(info_path)
                if hasattr(info_module, 'PLUGIN_INFO'):
                    plugin_info = info_module.PLUGIN_INFO.copy()
                    plugin_info.update(base_info)
                    return plugin_info
            except ImportError:
                continue
        
        # Əgər info.py faylı yoxdursa, minimal məlumatlarla qaytar
        base_info.update({
            'version': 'Bilinməyən',
            'author': 'Bilinməyən',
            'description': 'info.py faylı tapılmadı',
            'license': 'Bilinməyən',
            'url': 'Bilinməyən',
            'pypi': 'Bilinməyən'
        })
        
        return base_info

    def _extract_tools(self, module) -> List[Any]:
        """Moduldan @function_tool ilə işarələnmiş funksiyaları çıxar"""

        tools = []
        
        try:
            # Moduldaki bütün atributları yoxla
            for attr_name in dir(module):
                if attr_name.startswith('_'):
                    continue
                    
                attr = getattr(module, attr_name)
                
                # Funksi olduğunu yoxla
                if callable(attr):
                    # @function_tool dekoratorunu yoxla
                    if hasattr(attr, '_livekit_function_tool'):
                        tools.append(attr)
                    # alternativ atributları yoxla
                    elif hasattr(attr, '__wrapped__') and hasattr(attr.__wrapped__, '_livekit_function_tool'):
                        tools.append(attr)
                    # LiveKit tool patternini yoxla
                    elif hasattr(attr, '__annotations__') and attr.__annotations__:
                        # ctx parametrini yoxla
                        if 'ctx' in str(attr.__annotations__) or 'RunContext' in str(attr.__annotations__):
                            tools.append(attr)
                    # function_tool importunu yoxla
                    elif 'function_tool' in str(attr) or 'livekit' in str(attr):
                        tools.append(attr)
        except Exception as e:
            logger.error(f"Tool çıxarış xətası: {e}")
        
        return tools

    def get_all_tools(self) -> List[Any]:
        """Bütün yüklənmiş pluginlərdən tool-ları qaytarır"""

        all_tools = []
        for plugin_name, plugin_data in self.loaded_plugins.items():
            if 'tools' in plugin_data:
                all_tools.extend(plugin_data['tools'])
        return all_tools

    def get_plugin_info(self) -> str:
        """Plugin məlumatlarını qaytarır"""
        if not self.loaded_plugins:
            return "Heç bir plugin yüklənməyib."
        
        info_parts = ["Yüklənmiş Pluginlər:"]
        
        for plugin_name, plugin_data in self.loaded_plugins.items():
            info_parts.append(f"\n📦 {plugin_data.get('name', plugin_name)}")
            info_parts.append(f"   Versiya: {plugin_data.get('version', 'Bilinməyən')}")
            info_parts.append(f"   Müəllif: {plugin_data.get('author', 'Bilinməyən')}")
            info_parts.append(f"   Təsvir: {plugin_data.get('description', 'Bilinməyən')}")
            info_parts.append(f"   Lisenziya: {plugin_data.get('license', 'Bilinməyən')}")
            info_parts.append(f"   GitHub: {plugin_data.get('url', 'Bilinməyən')}")
            info_parts.append(f"   PyPI: {plugin_data.get('pypi', 'Bilinməyən')}")
            info_parts.append(f"   Tool sayı: {len(plugin_data['tools'])}")
        
        return "\n".join(info_parts)

    def get_plugin_updates(self) -> str:
        """Yeni versiya məlumatlarını qaytarır"""

        updates = []
        
        for plugin_name in self.loaded_plugins.keys():
            if plugin_name.startswith('azerai-plugins-') or plugin_name.startswith('azerai_plugins_') or plugin_name.startswith('AzerAI-Plugins-') or plugin_name.startswith('AzerAI_Plugins_') or plugin_name == 'AzerAI' or 'azerai' in plugin_name:
                current_version = self._get_installed_version(plugin_name)
                latest_version = self._get_latest_version(plugin_name)
                
                if latest_version and current_version and latest_version != current_version:
                    updates.append(f"🔄 {plugin_name}: {current_version} → {latest_version}")
                    updates.append(f"   Yeniləmək üçün: pip install --upgrade {plugin_name}")
        
        if updates:
            return "\n".join(["Yeni versiyalar mövcuddur:"] + updates)
        else:
            return "Bütün pluginlər ən son versiyadadır."

    def get_plugin_prompts(self) -> str:
        """Plugin promptlarını qaytarır"""

        prompt_parts = ["AzerAI Sistem və Plugin xüsusiyyətləri:"]
        
        # AzerAI öz məlumatlarını əlavə et
        try:
            import azerai.info as azerai_info
            if hasattr(azerai_info, 'AZERAI_INFO'):
                azerai_data = azerai_info.AZERAI_INFO
                prompt_parts.append(f"\nAd: {azerai_data['name']}")
                prompt_parts.append(f"Versiya: {azerai_data['version']}")
                prompt_parts.append(f"Müəllif: {azerai_data['author']}")
                prompt_parts.append(f"Təsvir: {azerai_data['description']}")
                prompt_parts.append(f"Lisenziya: {azerai_data.get('license', 'Bilinməyən')}")
                prompt_parts.append(f"GitHub: {azerai_data.get('url', 'Bilinməyən')}")
                prompt_parts.append(f"PyPI: {azerai_data.get('pypi', 'Bilinməyən')}")
        except ImportError:
            prompt_parts.append("\nazerai: AzerAI - Azərbaycan dilində qabaqcıl səsli AI asistent")
        
        if not self.loaded_plugins:
            return "\n".join(prompt_parts)
        
        prompt_parts.append("\n--- Pluginlər ---")
        
        for plugin_name, plugin_data in self.loaded_plugins.items():
            if plugin_data['tools']:
                prompt_parts.append(f"\n{plugin_name}: {plugin_data['description']}")
                
                # Plugin prompts faylını yoxla - avtomatik path tapma
                try:
                    module = plugin_data.get('module')
                    if module:
                        # Əsas prompts.py path-lərini yoxla
                        prompts_paths = [
                            f"{module.__name__}.prompts"
                        ]
                        
                        for prompts_path in prompts_paths:
                            try:
                                prompts_module = importlib.import_module(prompts_path)
                                if hasattr(prompts_module, 'PLUGIN_PROMPT'):
                                    prompt_parts.append(prompts_module.PLUGIN_PROMPT)
                                    break
                            except ImportError:
                                continue
                except Exception as e:
                    logger.debug(f"Plugin prompt yüklənə bilmədi {plugin_name}: {e}")
        
        return "\n".join(prompt_parts)

# Qlobal plugin manager nümunəsi
plugin_manager = PluginManager()

# Geri qaytarılma uyğunluğu üçün ixrac funksiyaları
def get_all_tools() -> List[Any]:
        """Bütün yüklənmiş pluginlərdən tool-ları qaytarır"""

        return plugin_manager.get_all_tools()

def get_plugin_info() -> str:
    """Plugin məlumatlarını qaytarır"""

    return plugin_manager.get_plugin_info()

def get_plugin_prompts() -> str:
    """Plugin promptlarını qaytarır"""

    return plugin_manager.get_plugin_prompts()

def get_plugin_updates() -> str:
    """Yeni versiya məlumatlarını qaytarır"""
    
    return plugin_manager.get_plugin_updates()
