# File Names
config_db_file = 'config_db.html'
config_db_new_content = 'download_config.html'
config_db_old_content = '''
                <span class="input-group-btn">
                    <button type="button" data-toggle="modal" id="calibre_modal_download_path" data-link="config_calibre_download_dir" data-filefilter="metadata.db" data-target="#fileModal" id="library_path" class="btn btn-default"><span class="glyphicon glyphicon-folder-open"></span></button>
                </span>
            </div>'''

main_file = 'main.py'
main_category = 'main'
main_import_line = "    from .plugins.calibre_web_downloader.download import download"
main_import_current_line = "from .search import search"
main_register_line = "app.register_blueprint(download)"
main_blueprint_registration_current_line = "app.register_blueprint(search)"
