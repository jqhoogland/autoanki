import PyPDF2
import glob
import urllib.request
import os


def scrape_text_from_file(file_name):
    total_text = ""
    with open(file_name, "rb") as pdf_file:
        read_pdf = PyPDF2.PdfReader(pdf_file)
        for i in range(len(read_pdf.pages)):
            page = read_pdf.pages[i]
            page_content = page.extract_text()
            total_text += page_content
    return total_text


def scrape_text_from_dir(dir_name):
    total_text = ""
    for file_name in glob.glob(dir_name+"*\\.pdf"):
        total_text += scrape_text_from_file(file_name)
    return total_text


def scrape_text_from_arxiv(link: str):
    with urllib.request.urlopen(link) as web_file:
        with open('temp.pdf', 'wb') as local_file:
            local_file.write(web_file.read())

    text = scrape_text_from_file("temp.pdf")
    os.remove("temp.pdf")

    return text

