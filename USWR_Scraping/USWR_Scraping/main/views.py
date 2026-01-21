from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
def scrape(prod_id):
    
    response = requests.get(f"https://hilka.co.uk/catalogsearch/result/?q={prod_id}")
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    product_links = [a["href"] for a in links if f"-{prod_id}.html" in a["href"]]
    response = requests.get(product_links[0])
    soup2 = BeautifulSoup(response.text, "html.parser")
    specs = soup2.get_text()

    in_stock = soup2.select_one(".stock-level").get_text(strip = True).strip("Stock level:")
    specs = {}
    name = soup2.select_one(".page-title").get_text(strip=True)
    for row in soup2.select("#specificationinfo li"):
        key = row.select_one("strong").get_text(strip=True)
        val = row.get_text(strip=True).strip(key)
        specs[key] = val

    price = soup2.select_one(".price").get_text(strip=True)

    data = {"id":prod_id,"name":name,"price":price,"specs":specs}
    return data

# Create your views here.
def home(request):
    return render(request,"index.html")

def check(request):
    prod_id = request.GET.get("prod_id")
    if prod_id:
        data = scrape(prod_id=prod_id)
    return JsonResponse(data)