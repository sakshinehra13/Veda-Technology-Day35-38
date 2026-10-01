from datetime import datetime
import json
import os
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Veda Technology Management System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- FILE STORAGE SETUP ---
DATA_DIR = "veda_data"
SERVICES_FILE = os.path.join(DATA_DIR, "services.json")
PROGRAMS_FILE = os.path.join(DATA_DIR, "programs.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
INQUIRIES_FILE = os.path.join(DATA_DIR, "inquiries.json")


def ensure_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_json(filepath):
    ensure_dir()
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return []


def save_json(filepath, data):
    ensure_dir()
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# Initialize Session State Data
if "services" not in st.session_state:
    st.session_state.services = load_json(SERVICES_FILE)
    if not st.session_state.services:
        st.session_state.services = [
            {
                "service_id": "S001",
                "name": "Cloud Migration Suite",
                "category": "Digital Services",
                "price": 4500.0,
                "status": "Active",
            },
            {
                "service_id": "S002",
                "name": "AI Data Pipeline",
                "category": "Technology",
                "price": 7200.0,
                "status": "Active",
            },
            {
                "service_id": "S003",
                "name": "Cybersecurity Assessment",
                "category": "Digital Services",
                "price": 3000.0,
                "status": "Active",
            },
        ]
        save_json(SERVICES_FILE, st.session_state.services)

if "programs" not in st.session_state:
    st.session_state.programs = load_json(PROGRAMS_FILE)
    if not st.session_state.programs:
        st.session_state.programs = [
            {
                "program_id": "P001",
                "title": "Full Stack Web Development",
                "prog_type": "Training",
                "duration": "12 Weeks",
                "status": "Active",
            },
            {
                "program_id": "P002",
                "title": "Python & AI Engineering Internship",
                "prog_type": "Internship",
                "duration": "6 Weeks",
                "status": "Active",
            },
        ]
        save_json(PROGRAMS_FILE, st.session_state.programs)

if "customers" not in st.session_state:
    st.session_state.customers = load_json(CUSTOMERS_FILE)
    if not st.session_state.customers:
        st.session_state.customers = [
            {
                "customer_id": "C001",
                "name": "Alice Smith",
                "email": "alice@example.com",
                "phone": "555-0192",
            },
            {
                "customer_id": "C002",
                "name": "Bob Johnson",
                "email": "bob@example.com",
                "phone": "555-0143",
            },
        ]
        save_json(CUSTOMERS_FILE, st.session_state.customers)

if "inquiries" not in st.session_state:
    st.session_state.inquiries = load_json(INQUIRIES_FILE)
    if not st.session_state.inquiries:
        st.session_state.inquiries = [
            {
                "inquiry_id": "I001",
                "customer_id": "C001",
                "subject": "Cloud Migration Inquiry",
                "message": "Looking for enterprise timeline.",
                "status": "Open",
                "date": "2026-10-01 10:00",
            },
            {
                "inquiry_id": "I002",
                "customer_id": "C002",
                "subject": "Internship Enrollment",
                "message": "Details regarding Python internship.",
                "status": "Resolved",
                "date": "2026-10-01 11:30",
            },
        ]
        save_json(INQUIRIES_FILE, st.session_state.inquiries)


def sync_save():
    save_json(SERVICES_FILE, st.session_state.services)
    save_json(PROGRAMS_FILE, st.session_state.programs)
    save_json(CUSTOMERS_FILE, st.session_state.customers)
    save_json(INQUIRIES_FILE, st.session_state.inquiries)


# --- SIDEBAR NAVIGATION ---
st.sidebar.image(
    "https://img.icons8.com/clouds/200/source-code.png", width=100
)
st.sidebar.title("Veda Technology")
st.sidebar.markdown("*Business & Service Management System*")
menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "💼 Services Management",
        "🎓 Program Management",
        "👥 Customers",
        "📩 Customer Inquiries",
        "🔍 Search & Advanced Filter",
    ],
)

# --- 1. DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("🚀 Veda Technology Control Center")
    st.markdown(
        "Welcome back! Here is a live overview of your organization's performance metrics."
    )

    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Services", value=len(st.session_state.services)
        )
    with col2:
        st.metric(
            label="Active Programs", value=len(st.session_state.programs)
        )
    with col3:
        st.metric(
            label="Registered Clients", value=len(st.session_state.customers)
        )
    with col4:
        open_inq = len(
            [i for i in st.session_state.inquiries if i["status"] == "Open"]
        )
        st.metric(label="Open Inquiries", value=open_inq)

    st.markdown("---")

    # Visual Analytics Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Services Price Distribution")
        if st.session_state.services:
            df_serv = pd.DataFrame(st.session_state.services)
            st.bar_chart(df_serv, x="name", y="price")
        else:
            st.info("No services available.")

    with c2:
        st.subheader("Inquiry Status Breakdown")
        if st.session_state.inquiries:
            df_inq = pd.DataFrame(st.session_state.inquiries)
            status_counts = df_inq["status"].value_counts()
            st.bar_chart(status_counts)
        else:
            st.info("No inquiries available.")

# --- 2. SERVICES MANAGEMENT ---
elif menu == "💼 Services Management":
    st.title("💼 Service Management Module")

    tab1, tab2 = st.tabs(["📋 View Services", "➕ Add New Service"])

    with tab1:
        if st.session_state.services:
            df = pd.DataFrame(st.session_state.services)
            st.dataframe(df, use_container_width=True)

            # Export Button
            st.download_button(
                "📥 Download Services as CSV",
                df.to_csv(index=False),
                "services.csv",
                "text/csv",
            )
        else:
            st.info("No services recorded yet.")

    with tab2:
        with st.form("service_form"):
            st.subheader("Register a New Digital/Tech Service")
            s_id = st.text_input("Service ID (e.g., S004)")
            s_name = st.text_input("Service Name")
            s_cat = st.selectbox(
                "Category", ["Digital Services", "Technology", "Consulting"]
            )
            s_price = st.number_input("Price ($)", min_value=0.0, step=100.0)
            s_status = st.selectbox("Status", ["Active", "Inactive"])

            submitted = st.form_submit_button("Save Service")
            if submitted:
                if s_id and s_name:
                    st.session_state.services.append({
                        "service_id": s_id,
                        "name": s_name,
                        "category": s_cat,
                        "price": s_price,
                        "status": s_status,
                    })
                    sync_save()
                    st.success(f"Service '{s_name}' added successfully!")
                else:
                    st.error("Please fill in all mandatory fields.")

# --- 3. PROGRAM MANAGEMENT ---
elif menu == "🎓 Program Management":
    st.title("🎓 Program & Training Management")

    tab1, tab2 = st.tabs(["📋 View Programs", "➕ Add New Program"])

    with tab1:
        if st.session_state.programs:
            df = pd.DataFrame(st.session_state.programs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No programs recorded yet.")

    with tab2:
        with st.form("program_form"):
            st.subheader("Add Training or Internship Program")
            p_id = st.text_input("Program ID (e.g., P004)")
            p_title = st.text_input("Program Title")
            p_type = st.selectbox(
                "Program Type", ["Training", "Internship", "Technology"]
            )
            p_dur = st.text_input("Duration (e.g., 8 Weeks)")
            p_status = st.selectbox("Status", ["Active", "Upcoming"])

            submitted = st.form_submit_button("Create Program")
            if submitted:
                if p_id and p_title:
                    st.session_state.programs.append({
                        "program_id": p_id,
                        "title": p_title,
                        "prog_type": p_type,
                        "duration": p_dur,
                        "status": p_status,
                    })
                    sync_save()
                    st.success(f"Program '{p_title}' added successfully!")
                else:
                    st.error("Please provide valid inputs.")

# --- 4. CUSTOMERS ---
elif menu == "👥 Customers":
    st.title("👥 Customer Relationship Management")

    tab1, tab2 = st.tabs(["📋 Client Directory", "➕ Register Customer"])

    with tab1:
        if st.session_state.customers:
            st.dataframe(
                pd.DataFrame(st.session_state.customers),
                use_container_width=True,
            )
        else:
            st.info("No customers registered.")

    with tab2:
        with st.form("customer_form"):
            st.subheader("New Client Registration")
            c_id = st.text_input("Customer ID (e.g., C003)")
            c_name = st.text_input("Full Name")
            c_email = st.text_input("Email Address")
            c_phone = st.text_input("Phone Number")

            submitted = st.form_submit_button("Register Customer")
            if submitted:
                if c_id and c_name:
                    st.session_state.customers.append({
                        "customer_id": c_id,
                        "name": c_name,
                        "email": c_email,
                        "phone": c_phone,
                    })
                    sync_save()
                    st.success(f"Customer {c_name} registered successfully!")
                else:
                    st.error("Please fill out required fields.")

# --- 5. CUSTOMER INQUIRIES ---
elif menu == "📩 Customer Inquiries":
    st.title("📩 Service Requests & Inquiries")

    tab1, tab2 = st.tabs(["📋 View Inquiries", "➕ Log New Inquiry"])

    with tab1:
        if st.session_state.inquiries:
            st.dataframe(
                pd.DataFrame(st.session_state.inquiries),
                use_container_width=True,
            )
        else:
            st.info("No inquiries found.")

    with tab2:
        with st.form("inquiry_form"):
            st.subheader("Log Client Inquiry")
            i_id = st.text_input("Inquiry ID (e.g., I003)")
            cust_ids = [c["customer_id"] for c in st.session_state.customers]
            i_cust = st.selectbox(
                "Select Customer ID",
                cust_ids if cust_ids else ["No Customers Available"],
            )
            i_subj = st.text_input("Subject")
            i_msg = st.text_area("Message / Details")
            i_status = st.selectbox("Status", ["Open", "Resolved"])

            submitted = st.form_submit_button("Submit Inquiry")
            if submitted:
                if i_id and i_subj:
                    st.session_state.inquiries.append({
                        "inquiry_id": i_id,
                        "customer_id": i_cust,
                        "subject": i_subj,
                        "message": i_msg,
                        "status": i_status,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    })
                    sync_save()
                    st.success("Inquiry logged successfully!")
                else:
                    st.error("Please complete the form.")

# --- 6. SEARCH & ADVANCED FILTER ---
elif menu == "🔍 Search & Advanced Filter":
    st.title("🔍 Search & Filter Portal")
    st.markdown("Search dynamically across Veda Technology data catalogs.")

    search_category = st.selectbox(
        "Select Entity to Filter",
        ["Services", "Programs", "Customers", "Inquiries"],
    )
    keyword = st.text_input("Enter search keyword").lower()

    if search_category == "Services":
        results = [
            s
            for s in st.session_state.services
            if keyword in s["name"].lower()
            or keyword in s["category"].lower()
        ]
        st.write(f"Found {len(results)} matching service(s):")
        if results:
            st.dataframe(pd.DataFrame(results))

    elif search_category == "Programs":
        results = [
            p
            for p in st.session_state.programs
            if keyword in p["title"].lower()
            or keyword in p["prog_type"].lower()
        ]
        st.write(f"Found {len(results)} matching program(s):")
        if results:
            st.dataframe(pd.DataFrame(results))

    elif search_category == "Customers":
        results = [
            c
            for c in st.session_state.customers
            if keyword in c["name"].lower() or keyword in c["email"].lower()
        ]
        st.write(f"Found {len(results)} matching customer(s):")
        if results:
            st.dataframe(pd.DataFrame(results))

    elif search_category == "Inquiries":
        results = [
            i
            for i in st.session_state.inquiries
            if keyword in i["subject"].lower() or keyword in i["status"].lower()
        ]
        st.write(f"Found {len(results)} matching inquiry/inquiries:")
        if results:
            st.dataframe(pd.DataFrame(results))