# import the necessary packages
import requests
import json


def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):


    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f}, 
                          data=payload,
                          )
        return r.content.decode()

def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):


    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
              }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                     )
    return r.content.decode()

def main():
    test_file_local = ocr_space_file(filename='data/pdfs/sample-pdf.pdf', language='eng')
    test_file_remote = ocr_space_url('file_url', language='eng') # replace value of file_url with valid url of image or pdf
    json_string_local = json.loads(test_file_local)
    extracted_text_local = json_string_local["ParsedResults"][0]["ParsedText"]
    extracted_text_local = extracted_text_local.replace(" \r\n", " ")
    json_string_remote = json.loads(test_file_remote)
    extracted_text_remote = json_string_remote["ParsedResults"][0]["ParsedText"]
    extracted_text_remote = extracted_text_remote.replace(" \r\n", " ")
    print("Local file data : " + extracted_text_local)
    print("Remote file data : " + extracted_text_remote)
   
    
if __name__ == "__main__":
    main()
