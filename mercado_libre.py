from playwright.sync_api import sync_playwright
import polars as pl

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)

page = browser.new_page()
query = "Sonos move 2"
url = f"https://www.mercadolibre.com.mx/\
        {query.replace(' ','-')}"
page.goto(url)

try:
    page.wait_for_selector('text="Agregar ubicación"',timeout=300)
    page.click('text="Más tarde"')
except:
    pass
page.wait_for_selector("#shipping_highlighted_fulfillment")
page.click("#shipping_highlighted_fulfillment")

page.wait_for_selector(li.ui-search-layout_item)
items = page.query_seelector_all("li.ui-search-layout_item")

products = []

for item in items:
    title  = item.query_selector('h3')
    price = item.query_selector('span.andes-money-amount.''andes-money-amount--cents-superscript')

    link = item.query_selector('a.poly-component__title')

    title_val = title.inner_text()

    price_val = price.inner_text().replace("\n","").strip()
    link_val = link.get_attribute("href")

    poducts.append((title_val, price_val, link_val))

browser.clos()
playwright.stop()

df = pl.DataFrame(products,schema=["Title","Price","link"],orient="row")
df.write_csv("consulta.csv")