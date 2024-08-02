import os
from uuid import uuid4
from flask import Blueprint, request
import requests
from cps import logger, render_template, config
from cps.usermanagement import login_required_if_no_ano
from libgen_api import LibgenSearch

download = Blueprint('download', __name__)
log = logger.create()

@download.route("/download", methods=["GET"])
@login_required_if_no_ano
def start_search():
    return render_template.render_title_template('downloader.html')

@download.route("/search_books", methods=["POST"])
# @login_required_if_no_ano
def search_libgen():
    if request.is_json:
        data = request.get_json()
        book = data.get('title')
        author = data.get('author')
        category = data.get('category')

        results, search = getBookOptions(book, author, category)
        return results
    else:
        log.error_or_exception("Request is not JSON")
        log.error_or_exception("Request Data: %s", request.data)
        log.error_or_exception("Request Headers: %s", request.headers)
        return "Error"

@download.route("/download_book", methods=["POST"])
def download_book():
    if request.is_json:
        data = request.get_json()
        print(data)
        search = LibgenSearch()
        download_links = search.resolve_download_links(data.get('book'))

        print(download_links)

        downloadURL = download_links.get('GET')
        print(downloadURL)

        with requests.get(downloadURL, stream=True) as response:
            response.raise_for_status()
            print("FIRST LAYER")

            titleHeader = response.headers.get('content-disposition')
            filename = getFileNameFromHeader(titleHeader)
            directory = config.config_calibre_download_dir

            file_path = os.path.join(directory, filename)
            print(filename)

            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                with open(file_path, 'wb') as file:
                    print("SECOND LAYER")
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                    file.flush()
                    os.fsync(file.fileno())
            except Exception as error:
                print(error)
                
        with open(f'./downloads/{filename}', 'a'):
            os.utime(f'./downloads/{filename}', None)
            print("Downloaded")

        return "Successful Download"

def getBookOptions(book, author, category):
    search = LibgenSearch(category)

    title_filters = {"Author": author}
    results = search.search_title(f"{book} {author}")

    # print(results)

    return(results, search)

def getFileNameFromHeader(header):
    if not header:
        return None
    fname = None
    if 'filename=' in header:
        fname = header.split('filename=')[-1].strip().strip('"')
        return fname
    
# def downloadBook()