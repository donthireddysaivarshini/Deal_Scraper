import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# Set page title and configuration
st.set_page_config(page_title="Deal Hunter - DealsHeaven", page_icon="🛍️", layout="centered")
st.title("🛍️ Deal Hunter")
st.subheader("Your Ultimate Deal Finder!")
st.write("Select your preferred store and page range to find the best deals.")

# Store selection with extended options
store_name = st.selectbox(
    "Select a Store",
    options=[
        "Amazon", "Airasia", "Aircel", "AmericanSwan", "askmebazar", "Abhibus", "AkbarTravels", "abof", "Airtel",
        "Babyoye", "Bigrock", "Burgerking", "Bigbasket", "bookmyshow", "Bluehost", "cromaretail", "Cleartrip",
        "crownit", "Cinepolis Cinema", "Clovia", "Dominos", "Ebay", "Edukart", "Expedia", "EaseMyTrip", "Flipkart",
        "Firstcry", "Fasttrack", "FashionAndYou", "Fabfurnish", "Fabindia", "Fashionara", "fernsnpetals", "Foodpanda",
        "Freecharge", "Freecultr", "Fasoos", "FitnLook", "Goibibo", "Groupon India", "Grofers", "Greendust", "GoAir",
        "Helpchat", "HomeShop18", "HealthKart", "Hostgator", "Indiatimes", "Infibeam", "ixigo", "IndiGo", "Jabong",
        "Jugnoo", "JustRechargeIt", "Koovs", "KFC", "LensKart", "LittleApp", "MakeMyTrip", "McDonalds", "Mobikwik",
        "Musafir", "Myntra", "Nearbuy", "Netmeds", "NautiNati", "Nykaa", "Others", "Oyorooms", "Ola", "Paytm",
        "PayUMoney", "Pepperfry", "Printvenue", "PayZapp", "Pizzahut", "Photuprint", "pharmeasy", "Redbus", "Rediff",
        "Rewardme", "Reliance Big TV", "Reliance trends", "Snapdeal", "ShopClues", "ShoppersStop", "Sweetsinbox",
        "Styletag", "ShopCJ", "Taxi for Sure", "Travelguru", "Trendin", "ticketnew", "TataCLiQ", "Tata Sky",
        "thyrocare", "udio", "UseMyVoucher", "Uber", "voonik", "Vistaprint", "VLCC", "VideoconD2H", "Vodafone",
        "Woo Hoo", "Woodland", "Yatra", "Yepme", "Zivame", "Zovi", "Zomato", "zoomin", "Zotezo"
    ]
)

# Start and end page inputs
start_page = st.number_input("Enter Start Page", min_value=1, step=1, format="%d")
end_page = st.number_input("Enter End Page", min_value=1, step=1, format="%d")

# Button to fetch deals
if st.button("Show Deals"):
    if end_page < start_page:
        st.error("End Page should be greater than or equal to Start Page.")
    else:
        all_deals = []

        # Loop through the selected page range
        for page in range(start_page, end_page + 1):
            url = f"https://dealsheaven.in/store/{store_name.lower()}?page={page}"
            response = requests.get(url)

            # Check if the page is accessible
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find deal cards
                deal_cards = soup.find_all('div', class_='deatls-inner')

                for deal_card in deal_cards:
                    title = deal_card.find('h3').text.strip() if deal_card.find('h3') else "No title"
                    price = deal_card.find('p', class_='price').text.strip() if deal_card.find('p', class_='price') else "No price"
                    special_price = deal_card.find('p', class_='spacail-price').text.strip() if deal_card.find('p', class_='spacail-price') else "No special price"

                    all_deals.append({
                        "Title": title,
                        "Original Price": price,
                        "Special Price": special_price
                    })
            else:
                st.warning(f"Page {page} could not be accessed. Status code: {response.status_code}")

        # Display the deals in a DataFrame with an index starting at 1
        if all_deals:
            deals_df = pd.DataFrame(all_deals)
            deals_df.index += 1  # Set index to start at 1 instead of 0
            st.write(f"Displaying deals for {store_name} from page {start_page} to {end_page}:")
            st.dataframe(deals_df)  # Display the data in table format
        else:
            st.write("No deals found for the selected store and page range.")
