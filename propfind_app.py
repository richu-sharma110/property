import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PropFind – Buy, Sell & Rent",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white; padding: 60px 40px; border-radius: 20px;
    text-align: center; margin-bottom: 32px;
}
.hero h1 { font-size: 2.8rem; font-weight: 700; margin: 0 0 10px; }
.hero p  { font-size: 1.15rem; opacity: 0.85; margin: 0; }

/* ── Nav Buttons (Home page) ── */
.nav-btn {
    display: block; width: 100%; padding: 22px 16px;
    border-radius: 16px; text-align: center;
    font-size: 1.1rem; font-weight: 600;
    cursor: pointer; border: none; margin-bottom: 12px;
    transition: transform .15s, box-shadow .15s;
}
.nav-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.15); }
.btn-sell { background: linear-gradient(135deg,#ff6b6b,#ee5a24); color: white; }
.btn-buy  { background: linear-gradient(135deg,#4e54c8,#8f94fb); color: white; }
.btn-rent { background: linear-gradient(135deg,#11998e,#38ef7d); color: white; }

/* ── Property Card ── */
.prop-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 16px; padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
    transition: transform .15s, box-shadow .15s;
}
.prop-card:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(0,0,0,0.12); }
.prop-price { font-size: 1.6rem; font-weight: 700; color: #1a1a2e; }
.prop-title { font-size: 1rem; font-weight: 600; margin: 4px 0; }
.prop-loc   { color: #64748b; font-size: 13px; margin-bottom: 10px; }
.prop-meta  { display: flex; gap: 14px; font-size: 13px; color: #475569; flex-wrap: wrap; }

/* ── Badge ── */
.badge {
    display: inline-block; padding: 4px 12px;
    border-radius: 20px; font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: .4px;
}
.badge-sell { background:#fee2e2; color:#991b1b; }
.badge-buy  { background:#dbeafe; color:#1e40af; }
.badge-rent { background:#dcfce7; color:#166534; }

/* ── Auth Card ── */
.auth-card {
    max-width: 440px; margin: 0 auto;
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 20px; padding: 36px 32px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}

/* ── Detail Box ── */
.detail-box {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 20px; margin-top: 8px;
}
.tag {
    display: inline-block; background: #f1f5f9; color: #475569;
    border-radius: 8px; padding: 3px 10px; font-size: 12px; margin: 2px;
}

/* ── Section Title ── */
.sec-title {
    font-size: 1.4rem; font-weight: 700; color: #1a1a2e;
    margin: 0 0 20px; padding-left: 14px;
    border-left: 4px solid #4e54c8;
}

div[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
</style>
""", unsafe_allow_html=True)


# ─── Data Files ───────────────────────────────────────────────────────────────
USERS_FILE      = "users.json"
PROPERTIES_FILE = "properties.json"

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ─── Sample Properties ────────────────────────────────────────────────────────
SAMPLE = [
    # SELL
    {
        "id":1, "listing":"Sell", "title":"2 BHK Flat",
        "type":"Flat/Apartment", "price":4500000,
        "location":"Sector 22, Chandigarh", "city":"Chandigarh",
        "bedrooms":2, "bathrooms":2, "area":950, "age":5,
        "furnishing":"Semi-Furnished", "facing":"East",
        "floor":"3rd / 8", "posted_by":"Owner",
        "contact":"9876543210",
        "description":"Well maintained flat in prime location. Vastu compliant. Near market and school.",
        "amenities":["Parking","Lift","24x7 Water","Power Backup"],
        "date":"2024-04-20"
    },
    {
        "id":2, "listing":"Sell", "title":"3 BHK Independent House",
        "type":"Independent House", "price":9800000,
        "location":"Sector 35, Chandigarh", "city":"Chandigarh",
        "bedrooms":3, "bathrooms":3, "area":1850, "age":8,
        "furnishing":"Unfurnished", "facing":"North",
        "floor":"Ground", "posted_by":"Agent",
        "contact":"9812345678",
        "description":"Spacious house with garden. Gated colony. Close to PGI hospital.",
        "amenities":["Garden","Parking","Security/CCTV","Power Backup"],
        "date":"2024-04-18"
    },
    {
        "id":3, "listing":"Sell", "title":"4 BHK Villa",
        "type":"Villa", "price":18500000,
        "location":"Sector 5, Panchkula", "city":"Panchkula",
        "bedrooms":4, "bathrooms":4, "area":3200, "age":2,
        "furnishing":"Fully Furnished", "facing":"East",
        "floor":"Ground + 1", "posted_by":"Builder",
        "contact":"9871234560",
        "description":"Luxury villa with modular kitchen, Italian tiles, home theatre. Ready to move.",
        "amenities":["Swimming Pool","Gym","Clubhouse","Parking","Garden","Security/CCTV"],
        "date":"2024-04-15"
    },
    {
        "id":4, "listing":"Sell", "title":"Plot / Land 1200 sqft",
        "type":"Plot/Land", "price":5500000,
        "location":"Sector 20, Panchkula", "city":"Panchkula",
        "bedrooms":0, "bathrooms":0, "area":1200, "age":0,
        "furnishing":"N/A", "facing":"North-East",
        "floor":"N/A", "posted_by":"Owner",
        "contact":"9870099001",
        "description":"Corner plot in residential area. HRERA approved, clear title. Wide road facing.",
        "amenities":["Corner Plot","Wide Road","Electricity Available","RERA Approved"],
        "date":"2024-04-12"
    },
    {
        "id":5, "listing":"Sell", "title":"2 BHK Flat",
        "type":"Flat/Apartment", "price":5200000,
        "location":"Phase 7, Mohali", "city":"Mohali",
        "bedrooms":2, "bathrooms":2, "area":1050, "age":3,
        "furnishing":"Semi-Furnished", "facing":"West",
        "floor":"5th / 12", "posted_by":"Owner",
        "contact":"9988001122",
        "description":"Modern flat in gated society. Metro connectivity nearby. Society has gym and park.",
        "amenities":["Gym","Parking","Lift","Children Play Area","Power Backup"],
        "date":"2024-04-10"
    },
    # BUY (these are properties people want to buy - i.e. listed as Buy Requirement)
    {
        "id":6, "listing":"Buy", "title":"Looking for 2 BHK Flat",
        "type":"Flat/Apartment", "price":5000000,
        "location":"Sector 22 or nearby, Chandigarh", "city":"Chandigarh",
        "bedrooms":2, "bathrooms":2, "area":900, "age":0,
        "furnishing":"Any", "facing":"Any",
        "floor":"Any", "posted_by":"Buyer",
        "contact":"9876500001",
        "description":"Looking for a 2BHK flat in Sector 22 or Sector 17. Budget up to 50 Lakh. Ready to move preferred.",
        "amenities":["Parking","Lift"],
        "date":"2024-04-19"
    },
    {
        "id":7, "listing":"Buy", "title":"Need 3 BHK House",
        "type":"Independent House", "price":10000000,
        "location":"Panchkula preferred", "city":"Panchkula",
        "bedrooms":3, "bathrooms":2, "area":1500, "age":0,
        "furnishing":"Any", "facing":"East preferred",
        "floor":"N/A", "posted_by":"Buyer",
        "contact":"9812300001",
        "description":"Family of 4 looking for independent house. Need parking for 2 cars. School nearby preferred.",
        "amenities":["Parking","Garden","Security/CCTV"],
        "date":"2024-04-17"
    },
    {
        "id":8, "listing":"Buy", "title":"Looking for Plot in Mohali",
        "type":"Plot/Land", "price":4000000,
        "location":"Mohali Phases", "city":"Mohali",
        "bedrooms":0, "bathrooms":0, "area":1000, "age":0,
        "furnishing":"N/A", "facing":"Any",
        "floor":"N/A", "posted_by":"Buyer",
        "contact":"9900112201",
        "description":"Looking for residential plot in Mohali Phase 3A, 5 or 7. RERA approved only. Loan required.",
        "amenities":["RERA Approved","Wide Road"],
        "date":"2024-04-14"
    },
    # RENT
    {
        "id":9, "listing":"Rent", "title":"1 BHK Flat for Rent",
        "type":"Flat/Apartment", "price":15000,
        "location":"Phase 7, Mohali", "city":"Mohali",
        "bedrooms":1, "bathrooms":1, "area":600, "age":4,
        "furnishing":"Fully Furnished", "facing":"East",
        "floor":"2nd / 6", "posted_by":"Owner",
        "contact":"9988776655",
        "description":"Fully furnished 1BHK. Ideal for working professionals. WiFi included. Metro 500m away.",
        "amenities":["Furnished","WiFi","Lift","Parking"],
        "date":"2024-04-17"
    },
    {
        "id":10, "listing":"Rent", "title":"2 BHK Flat for Rent",
        "type":"Flat/Apartment", "price":22000,
        "location":"Sector 17, Chandigarh", "city":"Chandigarh",
        "bedrooms":2, "bathrooms":2, "area":1050, "age":6,
        "furnishing":"Semi-Furnished", "facing":"North",
        "floor":"4th / 9", "posted_by":"Owner",
        "contact":"9871100220",
        "description":"Semi-furnished flat near bus stand and market. Family preferred. Peaceful locality.",
        "amenities":["Parking","Lift","24x7 Water","Power Backup"],
        "date":"2024-04-14"
    },
    {
        "id":11, "listing":"Rent", "title":"3 BHK House for Rent",
        "type":"Independent House", "price":35000,
        "location":"Sector 9, Panchkula", "city":"Panchkula",
        "bedrooms":3, "bathrooms":2, "area":1600, "age":10,
        "furnishing":"Unfurnished", "facing":"East",
        "floor":"Ground", "posted_by":"Owner",
        "contact":"9900335566",
        "description":"Spacious independent house with small garden. Car parking. Vegetarian family preferred.",
        "amenities":["Garden","Parking","Security/CCTV","Power Backup"],
        "date":"2024-04-11"
    },
    {
        "id":12, "listing":"Rent", "title":"Commercial Shop on Rent",
        "type":"Commercial", "price":28000,
        "location":"Sector 9, Chandigarh", "city":"Chandigarh",
        "bedrooms":0, "bathrooms":1, "area":350, "age":7,
        "furnishing":"Unfurnished", "facing":"North",
        "floor":"Ground", "posted_by":"Owner",
        "contact":"9876111222",
        "description":"Ground floor shop on main road. High footfall. Suitable for retail, pharmacy, clinic.",
        "amenities":["Parking","Power Backup","Wide Road"],
        "date":"2024-04-09"
    },
]


# ─── Session State Init ───────────────────────────────────────────────────────
if "logged_in"   not in st.session_state: st.session_state.logged_in   = False
if "username"    not in st.session_state: st.session_state.username    = ""
if "page"        not in st.session_state: st.session_state.page        = "home"
if "view_id"     not in st.session_state: st.session_state.view_id     = None
if "properties"  not in st.session_state:
    st.session_state.properties = load_json(PROPERTIES_FILE, SAMPLE)


def go(page):
    st.session_state.page    = page
    st.session_state.view_id = None
    st.rerun()

def fmt_price(p, listing):
    if listing == "Rent":
        return f"₹{p:,}/mo"
    if p >= 10_000_000: return f"₹{p/10_000_000:.2f} Cr"
    if p >= 100_000:    return f"₹{p/100_000:.1f} L"
    return f"₹{p:,}"

def prop_icon(t):
    return {"Flat/Apartment":"🏢","Independent House":"🏠","Villa":"🏡",
            "Plot/Land":"🌳","Commercial":"🏪"}.get(t,"🏠")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN / SIGNUP
# ═══════════════════════════════════════════════════════════════════════════════
def show_auth():
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <span style='font-size:3rem;'>🏠</span>
        <h1 style='margin:8px 0 4px; font-size:2rem; color:#1a1a2e;'>PropFind India</h1>
        <p style='color:#64748b;'>Buy, Sell & Rent Properties</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

        users = load_json(USERS_FILE, {})

        # ── Login ──────────────────────────────────────────────────────────
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username", key="li_user")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="li_pass")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔑 Login", use_container_width=True):
                if not username or not password:
                    st.error("Please fill all fields.")
                elif username not in users:
                    st.error("User not found. Please sign up first.")
                elif users[username]["password"] != hash_pw(password):
                    st.error("Wrong password. Try again.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.username  = username
                    st.session_state.page      = "home"
                    st.success(f"Welcome back, {username}! 👋")
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            st.info("💡 Demo: username = **demo** | password = **demo123**")

            # Auto-create demo user
            if "demo" not in users:
                users["demo"] = {"password": hash_pw("demo123"), "name": "Demo User",
                                  "phone": "9876543210", "joined": "2024-01-01"}
                save_json(USERS_FILE, users)

        # ── Sign Up ────────────────────────────────────────────────────────
        with tab_signup:
            st.markdown("<br>", unsafe_allow_html=True)
            new_name  = st.text_input("Full Name",  placeholder="Your full name",     key="su_name")
            new_user  = st.text_input("Username",   placeholder="Choose a username",  key="su_user")
            new_phone = st.text_input("Mobile No.", placeholder="10-digit number",    key="su_phone")
            new_pass  = st.text_input("Password",   type="password",
                                      placeholder="Min 6 characters",                  key="su_pass")
            new_pass2 = st.text_input("Confirm Password", type="password",
                                      placeholder="Re-enter password",                 key="su_pass2")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("📝 Create Account", use_container_width=True):
                if not all([new_name, new_user, new_phone, new_pass, new_pass2]):
                    st.error("Please fill all fields.")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                elif new_pass != new_pass2:
                    st.error("Passwords do not match.")
                elif len(new_phone) != 10 or not new_phone.isdigit():
                    st.error("Enter valid 10-digit mobile number.")
                elif new_user in users:
                    st.error("Username already taken. Try another.")
                else:
                    users[new_user] = {
                        "password": hash_pw(new_pass),
                        "name": new_name,
                        "phone": new_phone,
                        "joined": datetime.now().strftime("%Y-%m-%d"),
                    }
                    save_json(USERS_FILE, users)
                    st.success("✅ Account created! Please login now.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME / DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def show_home():
    props = st.session_state.properties

    # Top navbar
    n1, n2, n3 = st.columns([6, 2, 2])
    n1.markdown(f"### 🏠 PropFind &nbsp; <small style='color:#64748b;font-weight:400;'>Welcome, **{st.session_state.username}** 👋</small>", unsafe_allow_html=True)
    if n2.button("➕ Post Property", use_container_width=True):
        go("post")
    if n3.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        go("auth")

    st.markdown("---")

    # Hero
    st.markdown("""
    <div class="hero">
        <h1>🏠 Find Your Perfect Property</h1>
        <p>Chandigarh Tricity – Buy, Sell & Rent made simple</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    sell_c = len([p for p in props if p["listing"]=="Sell"])
    buy_c  = len([p for p in props if p["listing"]=="Buy"])
    rent_c = len([p for p in props if p["listing"]=="Rent"])

    s1,s2,s3,s4 = st.columns(4)
    s1.metric("🏘️ Total Listings", len(props))
    s2.metric("🏷️ For Sale",       sell_c)
    s3.metric("🛒 Buy Requests",   buy_c)
    s4.metric("🔑 For Rent",       rent_c)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3 Big Navigation Buttons
    st.markdown('<div class="sec-title">What are you looking for?</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#ff6b6b,#ee5a24);
             color:white; border-radius:20px; padding:32px 24px; text-align:center;'>
            <div style='font-size:3rem;'>🏷️</div>
            <div style='font-size:1.4rem; font-weight:700; margin:8px 0 6px;'>Sell Property</div>
            <div style='opacity:.85; font-size:.95rem;'>{sell_c} properties listed for sale</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("View Sell Listings →", key="go_sell", use_container_width=True):
            go("sell")

    with c2:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#4e54c8,#8f94fb);
             color:white; border-radius:20px; padding:32px 24px; text-align:center;'>
            <div style='font-size:3rem;'>🛒</div>
            <div style='font-size:1.4rem; font-weight:700; margin:8px 0 6px;'>Buy Property</div>
            <div style='opacity:.85; font-size:.95rem;'>{buy_c} buy requests posted</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("View Buy Requests →", key="go_buy", use_container_width=True):
            go("buy")

    with c3:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#11998e,#38ef7d);
             color:white; border-radius:20px; padding:32px 24px; text-align:center;'>
            <div style='font-size:3rem;'>🔑</div>
            <div style='font-size:1.4rem; font-weight:700; margin:8px 0 6px;'>Rent Property</div>
            <div style='opacity:.85; font-size:.95rem;'>{rent_c} properties for rent</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("View Rent Listings →", key="go_rent", use_container_width=True):
            go("rent")

    # Recent listings preview
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">🆕 Recently Added</div>', unsafe_allow_html=True)
    recent = sorted(props, key=lambda x: x["date"], reverse=True)[:4]
    cols = st.columns(2)
    for i, prop in enumerate(recent):
        with cols[i%2]:
            badge_map = {"Sell":"badge-sell","Buy":"badge-buy","Rent":"badge-rent"}
            st.markdown(f"""
            <div class="prop-card">
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
                    <span style='font-size:1.8rem;'>{prop_icon(prop['type'])}</span>
                    <span class='badge {badge_map.get(prop["listing"],"badge-sell")}'>{prop["listing"]}</span>
                </div>
                <div class='prop-price'>{fmt_price(prop['price'], prop['listing'])}</div>
                <div class='prop-title'>{prop['title']}</div>
                <div class='prop-loc'>📍 {prop['location']}</div>
                <div class='prop-meta'>
                    {f"<span>🛏 {prop['bedrooms']} Bed</span>" if prop['bedrooms'] else ""} {f"<span>🚿 {prop['bathrooms']} Bath</span>" if prop['bathrooms'] else ""} <span>📐 {prop['area']} sqft</span> <span>👤 {prop['posted_by']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# REUSABLE: Property Listing Page
# ═══════════════════════════════════════════════════════════════════════════════
def show_listing_page(listing_type):
    color_map = {
        "Sell": ("🏷️","#ee5a24","#fee2e2","#991b1b"),
        "Buy":  ("🛒","#4e54c8","#dbeafe","#1e40af"),
        "Rent": ("🔑","#11998e","#dcfce7","#166534"),
    }
    icon, accent, badge_bg, badge_fg = color_map[listing_type]

    # Back button + title
    col1, col2 = st.columns([1,5])
    if col1.button("← Back"):
        go("home")
    col2.markdown(f"## {icon} {listing_type} Properties")

    st.markdown("---")

    props = [p for p in st.session_state.properties if p["listing"] == listing_type]

    # ── Filters ──────────────────────────────────────────────────────────────
    with st.expander("🔍 Search & Filter", expanded=True):
        f1, f2, f3 = st.columns(3)
        search  = f1.text_input("", placeholder="🔍 Search location, type...", label_visibility="collapsed")
        city_f  = f2.selectbox("City", ["All Cities","Chandigarh","Mohali","Panchkula"], label_visibility="collapsed")
        type_f  = f3.selectbox("Type", ["All Types","Flat/Apartment","Independent House","Villa","Plot/Land","Commercial"], label_visibility="collapsed")

        f4, f5, f6 = st.columns(3)
        bhk_f   = f4.selectbox("Bedrooms", ["Any","1","2","3","4+"])
        fur_f   = f5.selectbox("Furnishing", ["Any","Unfurnished","Semi-Furnished","Fully Furnished","N/A"])
        sort_f  = f6.selectbox("Sort by", ["Newest First","Price: Low → High","Price: High → Low","Area: Large → Small"])

        if props:
            prices = [p["price"] for p in props]
            pr = st.slider("Budget Range (₹)", min(prices), max(prices),
                           (min(prices), max(prices)), step=50000, format="₹%d")
        else:
            pr = (0, 999999999)

    # Apply filters
    res = props.copy()
    if search:
        kw = search.lower()
        res = [p for p in res if kw in p["location"].lower() or
               kw in p["title"].lower() or kw in p["description"].lower()]
    if city_f != "All Cities":  res = [p for p in res if p["city"]       == city_f]
    if type_f != "All Types":   res = [p for p in res if p["type"]       == type_f]
    if fur_f  != "Any":         res = [p for p in res if p["furnishing"] == fur_f]
    if bhk_f  != "Any":
        res = [p for p in res if p["bedrooms"] >= 4] if bhk_f=="4+" \
              else [p for p in res if p["bedrooms"] == int(bhk_f)]
    res = [p for p in res if pr[0] <= p["price"] <= pr[1]]

    sort_key = {"Newest First":"date","Price: Low → High":"price",
                "Price: High → Low":"price","Area: Large → Small":"area"}
    sort_rev  = {"Newest First":True,"Price: Low → High":False,
                 "Price: High → Low":True,"Area: Large → Small":True}
    res.sort(key=lambda x: x[sort_key[sort_f]], reverse=sort_rev[sort_f])

    st.markdown(f"**{len(res)} listings found**")
    st.markdown("<br>", unsafe_allow_html=True)

    if not res:
        st.info("😕 No properties match your filters.")
        return

    # ── Property Cards ────────────────────────────────────────────────────────
    cols = st.columns(2)
    for i, prop in enumerate(res):
        with cols[i%2]:
            amen_tags = " ".join([f'<span class="tag">{a}</span>' for a in prop["amenities"][:4]])

            st.markdown(f"""
            <div class="prop-card">
                <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;'>
                    <span style='font-size:2.2rem;'>{prop_icon(prop['type'])}</span>
                    <span style='background:{badge_bg};color:{badge_fg};
                          padding:4px 14px;border-radius:20px;font-size:11px;font-weight:700;
                          text-transform:uppercase;letter-spacing:.4px;'>
                        For {prop['listing']}
                    </span>
                </div>
                <div class='prop-price'>{fmt_price(prop['price'], prop['listing'])}</div>
                <div class='prop-title'>{prop['title']}</div>
                <div class='prop-loc'>📍 {prop['location']}</div>
                <div class='prop-meta' style='margin:10px 0;'>
                    {f"<span>🛏 {prop['bedrooms']} Bed</span>" if prop['bedrooms'] else ""} {f"<span>🚿 {prop['bathrooms']} Bath</span>" if prop['bathrooms'] else ""} <span>📐 {prop['area']} sqft</span> <span>🏗 {prop['age']} yrs</span> <span>🪑 {prop['furnishing']}</span>
                </div>
                <div style='margin-top:6px;'>{amen_tags}</div>
                <div style='margin-top:10px;font-size:12px;color:#94a3b8;'>
                    👤 {prop['posted_by']} &nbsp;|&nbsp; 📅 {prop['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # View Details button
            btn_label = "📋 View Details" if st.session_state.view_id != prop["id"] else "✖ Close Details"
            if st.button(btn_label, key=f"vd_{prop['id']}", use_container_width=True):
                st.session_state.view_id = prop["id"] if st.session_state.view_id != prop["id"] else None
                st.rerun()

            # ── Detail Panel ──────────────────────────────────────────────
            if st.session_state.view_id == prop["id"]:
                st.markdown(f"""
                <div class="detail-box">
                    <h4 style='margin:0 0 12px;color:#1a1a2e;'>📋 Full Details</h4>
                    <table style='width:100%;font-size:14px;border-collapse:collapse;'>
                        <tr><td style='color:#64748b;padding:5px 0;width:40%;'>Property Type</td>
                            <td style='font-weight:500;'>{prop['type']}</td></tr>
                        <tr><td style='color:#64748b;padding:5px 0;'>Furnishing</td>
                            <td style='font-weight:500;'>{prop['furnishing']}</td></tr>
                        <tr><td style='color:#64748b;padding:5px 0;'>Facing</td>
                            <td style='font-weight:500;'>{prop['facing']}</td></tr>
                        <tr><td style='color:#64748b;padding:5px 0;'>Floor</td>
                            <td style='font-weight:500;'>{prop['floor']}</td></tr>
                        <tr><td style='color:#64748b;padding:5px 0;'>Age</td>
                            <td style='font-weight:500;'>{prop['age']} years</td></tr>
                        <tr><td style='color:#64748b;padding:5px 0;'>Area</td>
                            <td style='font-weight:500;'>{prop['area']} sqft</td></tr>
                        <tr><td style='color:#64748b;padding:5px 0;'>Posted By</td>
                            <td style='font-weight:500;'>{prop['posted_by']}</td></tr>
                    </table>
                    <hr style='border:none;border-top:1px solid #e2e8f0;margin:14px 0;'>
                    <p style='font-size:14px;color:#334155;margin:0 0 12px;'><b>Description:</b><br>{prop['description']}</p>
                    <p style='font-size:13px;color:#475569;margin:0 0 10px;'><b>Amenities:</b><br>
                    {''.join([f"<span class='tag'>{a}</span>" for a in prop['amenities']])}</p>
                </div>
                """, unsafe_allow_html=True)

                st.success(f"📞 Contact {prop['posted_by']}: **{prop['contact']}**")

                # EMI Calculator only for Sell
                if listing_type == "Sell":
                    st.markdown("---")
                    st.markdown("**💰 EMI Calculator**")
                    ec1, ec2, ec3 = st.columns(3)
                    down   = ec1.number_input("Down Payment (₹)", value=int(prop["price"]*0.2),
                                              step=50000, key=f"dp_{prop['id']}")
                    rate   = ec2.number_input("Interest Rate (%)", value=8.5, step=0.1,
                                              key=f"rt_{prop['id']}")
                    tenure = ec3.number_input("Tenure (Years)", 1, 30, 20,
                                              key=f"tn_{prop['id']}")
                    loan = prop["price"] - down
                    r, n = rate/(12*100), tenure*12
                    if r > 0 and loan > 0:
                        emi   = loan * r * (1+r)**n / ((1+r)**n - 1)
                        total = emi * n
                        st.success(f"📊 Monthly EMI: **₹{emi:,.0f}** &nbsp;|&nbsp; "
                                   f"Total Payable: **₹{total:,.0f}** &nbsp;|&nbsp; "
                                   f"Interest: **₹{total-loan:,.0f}**")
                st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: POST PROPERTY
# ═══════════════════════════════════════════════════════════════════════════════
def show_post():
    col1, _ = st.columns([1,5])
    if col1.button("← Back"):
        go("home")

    st.markdown("## ➕ Post a Property")
    st.markdown("Fill in the details to list your property.")
    st.markdown("---")

    with st.form("post_form", clear_on_submit=True):
        st.subheader("📋 Basic Info")
        b1, b2, b3 = st.columns(3)
        title_in   = b1.text_input("Title *", placeholder="e.g. 2 BHK Flat")
        type_in    = b2.selectbox("Property Type *",
                        ["Flat/Apartment","Independent House","Villa","Plot/Land","Commercial"])
        listing_in = b3.selectbox("Listing Type *", ["Sell","Buy","Rent"])

        st.subheader("📍 Location")
        l1, l2, l3 = st.columns(3)
        city_in     = l1.selectbox("City *", ["Chandigarh","Mohali","Panchkula"])
        sector_in   = l2.text_input("Sector / Locality *", placeholder="e.g. Sector 22")
        facing_in   = l3.selectbox("Facing", ["East","West","North","South","North-East","Any"])

        st.subheader("🏠 Property Details")
        d1, d2, d3, d4, d5 = st.columns(5)
        price_in   = d1.number_input("Price (₹) *", min_value=0, step=50000)
        area_in    = d2.number_input("Area (sqft) *", min_value=0, step=50)
        beds_in    = d3.number_input("Bedrooms", 0, 10, 2)
        baths_in   = d4.number_input("Bathrooms", 0, 10, 1)
        age_in     = d5.number_input("Age (years)", 0, 100, 0)

        e1, e2, e3 = st.columns(3)
        fur_in     = e1.selectbox("Furnishing", ["Unfurnished","Semi-Furnished","Fully Furnished","N/A"])
        floor_in   = e2.text_input("Floor", placeholder="e.g. 3rd / 8")
        posted_in  = e3.selectbox("You are *", ["Owner","Agent","Builder","Buyer"])

        desc_in    = st.text_area("Description *", height=100,
                                   placeholder="Describe the property, nearby landmarks, condition...")

        amen_options = ["Parking","Lift","24x7 Water","Power Backup","Security/CCTV",
                        "Garden","Gym","Swimming Pool","Furnished","WiFi","Modular Kitchen",
                        "Clubhouse","Children Play Area","RERA Approved","Corner Plot","Wide Road"]
        amen_in    = st.multiselect("Amenities", amen_options)

        st.subheader("📞 Contact")
        contact_in = st.text_input("Mobile Number *", placeholder="10-digit number")

        submitted = st.form_submit_button("🚀 Post Property", use_container_width=True)

        if submitted:
            errors = []
            if not title_in:    errors.append("Title")
            if not sector_in:   errors.append("Locality")
            if price_in <= 0:   errors.append("Price")
            if area_in  <= 0:   errors.append("Area")
            if not desc_in:     errors.append("Description")
            if len(str(contact_in).strip()) < 10: errors.append("Contact number")

            if errors:
                st.error(f"Please fill: {', '.join(errors)}")
            else:
                all_props = st.session_state.properties
                new_id    = max(p["id"] for p in all_props) + 1 if all_props else 1
                new_prop  = {
                    "id": new_id, "listing": listing_in, "title": title_in,
                    "type": type_in, "price": price_in,
                    "location": f"{sector_in}, {city_in}", "city": city_in,
                    "bedrooms": int(beds_in), "bathrooms": int(baths_in),
                    "area": int(area_in), "age": int(age_in),
                    "furnishing": fur_in, "facing": facing_in,
                    "floor": floor_in, "posted_by": posted_in,
                    "contact": contact_in, "description": desc_in,
                    "amenities": amen_in,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                }
                all_props.append(new_prop)
                st.session_state.properties = all_props
                save_json(PROPERTIES_FILE, all_props)
                st.success(f"✅ '{title_in}' posted successfully!")
                st.balloons()


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_auth()
else:
    p = st.session_state.page
    if   p == "home": show_home()
    elif p == "sell": show_listing_page("Sell")
    elif p == "buy":  show_listing_page("Buy")
    elif p == "rent": show_listing_page("Rent")
    elif p == "post": show_post()
    else:             show_home()
