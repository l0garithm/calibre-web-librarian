import importlib
import os
from flask import Blueprint
from pathlib import Path

EXCLUDED_DIRS = {'__', 'plugin-utils'}
REQUIRED_PLUGIN_FILES = { '__init__.py', 'install.py', 'uninstall.py' }

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.app = None


    def is_valid_plugin_dir(self, item, plugin_dir):
        plugin_path = Path(plugin_dir).joinpath(item)
        print(f"Plugin Dir: {plugin_path}")
        is_valid_dir = plugin_path.is_dir() and not any(item.startswith(prefix) for prefix in EXCLUDED_DIRS)
        print(f"Directory Valid: {is_valid_dir}")
        
        if not is_valid_dir:
            return False
        
        return self.has_required_files(plugin_path)


    def has_required_files(self, plugin_path):
        required_files = set(REQUIRED_PLUGIN_FILES)
        existing_files = set(file.name for file in plugin_path.iterdir() if file.is_file())
        missing_files = required_files - existing_files
        
        if missing_files:
            print(f"Missing required files for plugin in {plugin_path}: {', '.join(missing_files)}")

        return required_files.issubset(existing_files)

    def discover_plugins(self, plugin_dir):
        for item in os.listdir(plugin_dir):
            if self.is_valid_plugin_dir(item, plugin_dir):
                try:
                    plugin = importlib.import_module(f'cps.plugins.{item}')
                    if hasattr(plugin, 'initialize_plugin'):
                        self.plugins[item] = plugin
                except ImportError as e:
                    print(f"Error loading plugin {item}: {e}")

    def initialize_plugins(self, app):
        for name, plugin in self.plugins.items():
            try:
                blueprint = plugin.initialize_plugin()
                if isinstance(blueprint, Blueprint):
                    app.register_blueprint(blueprint)
                    print(f"Initialized plugin: {name}")
                    plugin.install()
                    print(f"Installed plugin: {name}")
            except Exception as e:
                print(f"Error initializing plugin {name}: {str(e)}")
                import traceback
                traceback.print_exc()

plugin_manager = PluginManager()
