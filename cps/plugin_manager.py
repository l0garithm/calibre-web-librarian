import importlib
import os
from flask import Blueprint

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def discover_plugins(self, plugin_dir):
        for item in os.listdir(plugin_dir):
            if os.path.isdir(os.path.join(plugin_dir, item)) and not item.startswith('__'):
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
            except Exception as e:
                print(f"Error initializing plugin {name}: {e}")

plugin_manager = PluginManager()
