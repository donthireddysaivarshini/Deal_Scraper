import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(page_title="Deals Scraper", layout="wide")

# CSS styling (same as before)
st.markdown(
    """
    <style>
    .black-strip {
        background-color: #000; 
        color: #fff; 
        padding: 10px 20px; 
        display: flex; 
        align-items: center; 
        font-size: 1.2em; 
        font-weight: bold; 
        margin-bottom: 20px;
    }    
    .skyblue-header {
        background-color: skyblue;
        padding: 5px;
        border-radius: 2px;
        font-size: 20px;
        text-align: center;
        margin-bottom: 20px;
    }

    .skyblue-header h3 {
        color: black;
        font-size: 18px;
    }
  
    .products-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 15px;
        margin: 0 -10px;
    }
    
    .product-container {
        width: 250px; 
        min-height: 450px; 
        border: 1px solid #ddd; 
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
        background-color: #fff;
        padding: 10px; 
        margin: 0; 
        display: flex; 
        flex-direction: column;
        text-align: center; 
        overflow: hidden; 
    }

    .product-container img {
        max-width: 100%;
        max-height: 150px;
        object-fit: cover; 
        border-radius: 5px; 
    }
    
    .product-title-container {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        min-height: 100px; 
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .product-title {
        font-size: 0.9em; 
        font-weight: bold;
        color: #333;
        word-wrap: break-word; 
        text-align: center;
        margin: 0; 
    }
    
    .product-details {
        font-size: 0.9em;
        color: #555;
        line-height: 1.5;
        margin-top: auto;
    }
    
    .product-image-container {
        width: 100%;
        height: 140px; 
        background-color: #f0f0f0; 
        border: 1px solid #ddd;
        border-radius: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px; 
        overflow: hidden; 
    }
    
    .product-image-container img {
        max-width: 100%;
        max-height: 100%; 
        object-fit: contain;
    }
    
    /* Fix for Streamlit columns */
    [data-testid="column"] {
        align-items: flex-start;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header section
st.markdown("""
<div class="black-strip">
    <span>Deals Scraper</span>
</div>
""", unsafe_allow_html=True)
st.image("logo.png", width=220)
st.markdown(
    '<div class="skyblue-header"><h3>Choose a store or category and enter the page range </h3></div>',
    unsafe_allow_html=True,
)

# Store and category selection
stores = {
    "All Stores": "all",
    "Flipkart": "flipkart",
    "Amazon": "amazon",
    "Paytm": "paytm",
    "Foodpanda": "foodpanda",
    "Freecharge": "freecharge",
    "Paytmmall": "paytmmall"
}

categories = {
    "All Categories": "all",
    "Beauty And Personal Care": "beauty-and-personal-care",
    "Clothing Fashion & Apparels": "clothing-fashion-apparels",
    "Electronics": "electronics",
    "Grocery": "grocery",
    "Mobiles & Mobile Accessories": "mobiles-mobile-accessories",
    "Recharge": "recharge",
    "Travel Bus & Flight": "travel-bus-flight"
}

store_name = st.selectbox("Select Store", list(stores.keys()))
category_name = st.selectbox("Choose a Category", list(categories.keys()))

# Page range input
start = st.number_input('Enter start page number:', min_value=1, step=1, value=1)
end = st.number_input('Enter end page number:', min_value=start, step=1, value=start)

submit_button = st.button("Submit")

if submit_button:
    try:
        if end > 1703:
            st.error("The DealsHeaven Website has only 1703 Pages.")
        else:
            all_products = []
            empty_page_count = 0
            first_empty_page = None
            with st.spinner('Scraping deals...'):
                for current_page in range(start, end + 1):
                    # Determine which URL to use based on selections
                    if store_name == "All Stores" and category_name == "All Categories":
                        url = f"https://dealsheaven.in/?page={current_page}"
                    elif store_name == "All Stores":
                        # Only category selected
                        url = f"https://dealsheaven.in/category/{categories[category_name]}/?page={current_page}"
                    elif category_name == "All Categories":
                        # Only store selected - use store URL directly
                        url = f"https://dealsheaven.in/store/{stores[store_name]}/?page={current_page}"
                    else:
                        # Both store and category selected - use category URL and filter by store
                        url = f"https://dealsheaven.in/category/{categories[category_name]}/?page={current_page}"
                    
                    try:
                        response = requests.get(url, timeout=10)
                        if response.status_code != 200:
                            st.warning(f"Failed to retrieve page {current_page} (Status code: {response.status_code}).")
                            continue
                            
                        soup = BeautifulSoup(response.text, 'html.parser')
                        all_items = soup.find_all("div", class_="product-item-detail")
                        
                        if not all_items:
                            empty_page_count += 1
                            if first_empty_page is None:
                                first_empty_page = current_page
                            continue
                            
                        for item in all_items:
                            # For store-only case (All Categories), we don't need to check store
                            if category_name == "All Categories" and store_name != "All Stores":
                                product_store = store_name  # Assume all products are from this store
                            else:
                                # Find store logo and get store name
                                store_img = item.find("img", src=lambda x: x and "shops/" in x)
                                product_store = store_img['title'] if store_img and 'title' in store_img.attrs else "Unknown"
                            
                            # Only keep products from selected store (or all stores)
                            if store_name == "All Stores" or product_store.lower() == store_name.lower():
                                product = {
                                    'Title': item.find("h3", title=True)['title'].replace("[Apply coupon] ", "").replace('"', '') 
                                            if item.find("h3", title=True) else "N/A",
                                    'Image': item.find("img", src=True)['data-src'] 
                                            if item.find("img", src=True) and 'data-src' in item.find("img", src=True).attrs 
                                            else item.find("img", src=True)['src'] if item.find("img", src=True) else None,
                                    'Price': item.find("p", class_="price").text.strip() 
                                            if item.find("p", class_="price") else "N/A",
                                    'Discount': item.find("div", class_="discount").text.strip() 
                                              if item.find("div", class_="discount") else "N/A",
                                    'Special Price': item.find("p", class_="spacail-price").text.strip() 
                                                   if item.find("p", class_="spacail-price") else "N/A",
                                    'Link': item.find("a", href=True)['href'] if item.find("a", href=True) else "N/A"
                                }
                                all_products.append(product)
                            
                    except requests.exceptions.RequestException as e:
                        st.warning(f"Error accessing page {current_page}: {str(e)}")
                        continue
            
            # Display information about empty pages
            if empty_page_count > 0:
                if empty_page_count == (end - start + 1):
                    st.warning("No products found on any of the requested pages.")
                else:
                    if empty_page_count == 1:
                        st.warning(f"Found no products on page {first_empty_page}.")
                    else:
                        st.warning(f"Found no products on {empty_page_count} pages (starting from page {first_empty_page}).")
            
            # Display products in grid
            if not all_products:
                st.warning(f"No products found matching your criteria.")
            else:
                display_text = f"Found {len(all_products)} products"
                if store_name != "All Stores":
                    display_text += f" from {store_name}"
                if category_name != "All Categories":
                    display_text += f" in {category_name} category"
                st.success(display_text)
                
                # Display 5 products per row
                for i in range(0, len(all_products), 5):
                    cols = st.columns(5)
                    for j, col in enumerate(cols):
                        if i + j < len(all_products):
                            product = all_products[i + j]
                            col.markdown(
                                f"""
                                <div class="product-container">
                                    <div class="product-image-container">
                                        <img src="{product['Image'] or 'https://via.placeholder.com/150'}" alt="Product Image" />
                                    </div>
                                    <div>
                                        <div class="product-title-container">
                                            <div class="product-title">{product['Title']}</div>
                                        </div>
                                        <p><b>Price:</b> {product['Price']}</p>
                                        <p><b>Discount:</b> {product['Discount']}</p>
                                        <p><b>Special Price:</b> {product['Special Price']}</p>
                                        <a href="{product['Link']}" target="_blank">View Deal</a>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
