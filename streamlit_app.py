import streamlit as st
from src.chatbot import get_ai_response 
import textwrap
import json


st.set_page_config(
    page_title="ShopSense AI | Smart Shopping Assistant",
    page_icon="🛍️"
)


# Load products for Smart Cart
with open("data/products.json", "r", encoding="utf-8") as file:
    products = json.load(file)


# Create a product lookup dictionary
product_lookup = {}

for product in products:
    product_lookup[product["name"]] = product



st.markdown(textwrap.dedent("""
<style>
.stApp {
    background: #FAF8F5;
    color: #30263A;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

.shopsense-brand {
    font-size: 1.25rem;
    font-weight: 800;
    color: #49314F;
    margin-bottom: 1.5rem;
    letter-spacing: -0.5px;
}

.shopsense-hero {
    background: linear-gradient(120deg, #F2E8F2, #FFF8F0);
    padding: 2.5rem;
    border-radius: 24px;
    border: 1px solid #E9DDE8;
    margin-bottom: 2rem;
}

.shopsense-eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: #805D85;
    margin-bottom: 1rem;
}

.shopsense-heading {
    font-family: Georgia, serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    line-height: 1.2;
    color: #432B50;
    margin-bottom: 1rem;
}

.shopsense-description {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #625568;
    max-width: 620px;
}

.shopsense-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 1.5rem;
}

.shopsense-tag {
    background: #FFFFFF;
    border: 1px solid #E4D7E6;
    border-radius: 30px;
    padding: 8px 14px;
    font-size: 0.85rem;
    color: #563D60;
}
</style>


<div class="shopsense-brand">🛍️ ShopSense AI</div>

<div class="shopsense-hero">
<div class="shopsense-eyebrow">YOUR PERSONAL SHOPPING COMPANION</div>
<div class="shopsense-heading">Discover products that<br>feel made for you.</div>
<div class="shopsense-description">Explore skincare and haircare essentials with intelligent, personalized recommendations. Your smarter shopping journey starts here.</div>
<div class="shopsense-tags">
<span class="shopsense-tag">✨ Skincare</span>
<span class="shopsense-tag">💇 Haircare</span>
<span class="shopsense-tag">🧴 Body Care</span>
<span class="shopsense-tag">✦ AI-Powered Discovery</span>
</div>
</div>

"""), unsafe_allow_html=True)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


# Smart Cart - initialize shopping cart
if "cart" not in st.session_state:
    st.session_state.cart = {}


# Add a product to the shopping cart

def add_to_cart(product_name):
    product = product_lookup[product_name]

    if product["availability"].lower() != "in stock":
        return False

    if product_name not in st.session_state.cart:
        st.session_state.cart[product_name] = 1
    else:
        st.session_state.cart[product_name] += 1

    return True


# Decrease product quantity
def decrease_quantity(product_name):
    if product_name in st.session_state.cart:
        st.session_state.cart[product_name] -= 1

        if st.session_state.cart[product_name] == 0:
            del st.session_state.cart[product_name]


# Find catalog products mentioned in the AI response
def find_recommended_products(response):
    recommended_products = []

    for product_name in product_lookup:
        if product_name.lower() in response.lower():
            recommended_products.append(product_name)

    return recommended_products




# Smart Cart - product selection
st.subheader("🛒 Smart Cart")

selected_product = st.selectbox(
    "Choose a product",
    list(product_lookup.keys())
)


if st.button("➕ Add to Cart"):
    if add_to_cart(selected_product):
        st.success(f"{selected_product} added to cart!")
    else:
        st.warning(f"{selected_product} is currently unavailable.")

# Display shopping cart
st.subheader("Your Shopping Cart")

if not st.session_state.cart:
    st.write("Your cart is empty.")

else:
    cart_total = 0

    
    for product_name, quantity in list(st.session_state.cart.items()):
        price = product_lookup[product_name]["price"]
        subtotal = price * quantity

        cart_total += subtotal

        
        col1, controls, col5 = st.columns([6, 1.5, 1.5])

        with col1:
            st.write(f"{product_name} × {quantity} = ₹{subtotal}")

        with controls:
            col2, col3, col4 = st.columns([1, 1, 1], gap="small")
        

            with col2:
                if st.button("➖", key=f"minus_{product_name}"):
                    decrease_quantity(product_name)
                    st.rerun()

            with col3:
                st.markdown(
                    f"<div style='text-align: center; color: #30263A; "
                    f"font-weight: 600; padding-top: 10px;'>{quantity}</div>",
                    unsafe_allow_html=True
                )

            with col4:
                if st.button("➕", key=f"plus_{product_name}"):
                    add_to_cart(product_name)
                    st.rerun()

        with col5:
            if st.button("Remove", key=f"remove_{product_name}"):
                del st.session_state.cart[product_name]
                st.rerun()


    st.write(f"**Total: ₹{cart_total}**")






if st.button("🗑️ Clear Chat"):
    st.session_state.conversation_history = []
    st.session_state.pop("selected_question", None)
    st.rerun()


for index, message in enumerate(st.session_state.conversation_history):
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            
            recommended_products = [
                product_name
                for product_name in message.get("recommended_products", [])
                if product_name in product_lookup
            ]

            if recommended_products:
                st.markdown("### 🛍️ Recommended for You")

                for product_name in recommended_products:
                    product = product_lookup[product_name]

                    st.write(f"**{product_name}**")
                    st.write(f"Price: ₹{product['price']}")
                    st.write(f"Availability: {product['availability']}")

            for product_name in recommended_products:
                is_available = (
                    product_lookup[product_name]["availability"].lower()
                    == "in stock"
                )

                if st.button(
                    f"🛒 Add {product_name} to Cart"
                    if is_available
                    else f"🚫 {product_name} — Out of Stock",
                    key=f"saved_{index}_{product_name}",
                    disabled=not is_available
                ):

                    if add_to_cart(product_name):
                        st.success(f"{product_name} added to cart!")
                    else:
                        st.warning(f"{product_name} is currently unavailable.")
                    st.rerun()

st.write("💡 Not sure what to ask? Try one of these:")

example_questions = [
    "✨ What should I use for dull skin?",
    "💧 Recommend a cleanser for oily skin",
    "💇 I have dry and frizzy hair. What should I use?",
    "🧴 Recommend body care products for dry skin",
    "💰 What products are under ₹500?",
    "🛍️ Do you have any skincare combos?"
]

for question in example_questions:
    if st.button(question):
        st.session_state.selected_question = question

user_input = st.chat_input("What are you shopping for today? 🛍️")

if "selected_question" in st.session_state:
    user_input = st.session_state.pop("selected_question")

if user_input:
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.write(user_input)
    api_history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in st.session_state.conversation_history
    ]

    response = get_ai_response(api_history)   
                                                                                                                                                                                                        

    with st.chat_message("assistant"):
        st.write(response.message)

    
        
    st.session_state.conversation_history.append({
        "role": "assistant",
        "content": response.message,
        "recommended_products": response.recommended_products     
    })

    
    st.rerun()
