from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    with sync_playwright() as p:
        page_url = 'https://www.psimonmyway.com/singapore-street-food-michelin-star/'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout= 60000)

        restaurant_data = []

        # Extract all restaurant spans
        restaurants = page.query_selector_all('h3 span[id]')
        
        for restaurant in restaurants:
            # Get restaurant name
            restaurant_name = restaurant.inner_text()
            
            # Get parent h3 element
            h3_element = restaurant.query_selector('xpath=ancestor::h3')

            # Get the next sibling p element which contains address and price
            p_element = h3_element.query_selector('xpath=following-sibling::p[1]')

            if p_element:
                # Extract address and price
                address = p_element.query_selector('a').inner_text() if p_element.query_selector('a') else 'N/A'
                
                price = page.evaluate('(element) => { let next = element.nextSibling; while (next && next.nodeType != 3) next = next.nextSibling; return next ? next.textContent : ""; }', p_element.query_selector('strong:has-text("💲")')) if p_element.query_selector('strong:has-text("💲")') else 'N/A'
                price = price.strip() if price else 'N/A'
                
                # Append to data list
                restaurant_data.append({
                    "Restaurant Name": restaurant_name,
                    "Address": address,
                    "Price": price
                })

                print(f"Restaurant Name: {restaurant_name}")
                print(f"Address: {address}")
                print(f"Price: {price}")
                print('---')

        browser.close()

        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(restaurant_data)
        df.to_csv('restaurant_data.csv', index=False)

if __name__ == "__main__":
    main()