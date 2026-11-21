import html

import pandas as pd
import plotly.express as px
import streamlit as st

from api import (
    register_user,
    login_user,
    get_user_profile,
    get_applications,
    create_application,
    update_application,
    delete_application,
)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JobTrack",
    page_icon="💼",
    layout="wide",
)


# ============================================================
# 2. SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# 3. CUSTOM DESIGN
# ============================================================

def apply_custom_design():
    """Apply the JobTrack light-content / navy-sidebar theme."""

    st.markdown(
        """
        <style>
        
/* Text inputs */
[data-testid="stMain"] input {
    background-color: #FFFFFF !important;
    color: #172033 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

/* Text areas */
[data-testid="stMain"] textarea {
    background-color: #FFFFFF !important;
    color: #172033 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

/* Dropdowns */
[data-testid="stMain"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #172033 !important;
    border-color: #CBD5E1 !important;
}

/* Date input fields */
[data-testid="stMain"] [data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    color: #172033 !important;
}

/* Input placeholders */
[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #94A3B8 !important;
}

/* Focus effect */
[data-testid="stMain"] input:focus,
[data-testid="stMain"] textarea:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 1px #2563EB !important;
}

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 4. LOGIN AND REGISTRATION
# ============================================================

def show_authentication():
    st.title("💼 JobTrack")
    st.subheader("Your Job Search, Organized.")

    st.write(
        "Track applications, manage interviews, "
        "and organize your job search in one place."
    )

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Welcome Back")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if login_button:
            if not email.strip() or not password:
                st.error("Please enter your email and password.")
            else:
                response = login_user(email.strip(), password)

                if response is None:
                    st.error("Cannot connect to backend.")
                elif response.status_code == 200:
                    token = response.json().get("access_token")
                    profile = get_user_profile(token) if token else None

                    if profile is not None and profile.status_code == 200:
                        st.session_state.token = token
                        st.session_state.user = profile.json()
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Unable to retrieve your user profile.")
                else:
                    try:
                        message = response.json().get(
                            "detail", "Login failed."
                        )
                    except (ValueError, AttributeError):
                        message = "Login failed."
                    st.error(message)

    with register_tab:
        st.subheader("Create an Account")

        with st.form("register_form"):
            username = st.text_input("Username")
            reg_email = st.text_input("Email", key="register_email")
            reg_password = st.text_input(
                "Password",
                type="password",
                key="register_password",
            )
            register_button = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

        if register_button:
            if not username.strip() or not reg_email.strip() or not reg_password:
                st.error("Please fill in all registration fields.")
            else:
                response = register_user(
                    username.strip(),
                    reg_email.strip(),
                    reg_password,
                )

                if response is None:
                    st.error("Cannot connect to backend.")
                elif response.status_code == 201:
                    st.success(
                        "Account created successfully! Please log in."
                    )
                else:
                    try:
                        message = response.json().get(
                            "detail", "Registration failed."
                        )
                    except (ValueError, AttributeError):
                        message = "Registration failed."
                    st.error(message)


# ============================================================
# 5. FETCH APPLICATIONS
# ============================================================

def fetch_applications(token):
    with st.spinner("Loading your applications..."):
        response = get_applications(token)

    if response is None:
        st.error("Cannot connect to FastAPI backend.")
        return None

    if response.status_code == 401:
        st.warning("Your session has expired. Please log in again.")
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()
        return None

    if response.status_code != 200:
        st.error(f"Failed to load applications: {response.text}")
        return None

    try:
        return response.json()
    except ValueError:
        st.error("The backend returned an invalid response.")
        return None


# ============================================================
# 6. DASHBOARD OVERVIEW
# ============================================================

def show_overview(applications, total):
    user = st.session_state.user or {}
    username = html.escape(str(user.get("username", "User")))

    st.markdown(
        f"""
        <div style="padding: 8px 0 20px 0;">
            <h1 style="color: #172033 !important;
                       font-size: 36px;
                       margin-bottom: 8px;">
                💼 JobTrack Dashboard
            </h1>
            <p style="color: #334155 !important;
                      font-size: 19px;
                      margin-bottom: 4px;">
                Welcome, <strong>{username}</strong>!
            </p>
            <p style="color: #64748B !important;
                      font-size: 15px;
                      margin-top: 0;">
                Your job search activity at a glance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    interviews = sum(
        1
        for application in applications
        if "interview" in str(application.get("status") or "").lower()
    )

    offers = sum(
        1
        for application in applications
        if (
            "offer" in str(application.get("status") or "").lower()
            or str(application.get("status") or "").lower() == "selected"
        )
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("📄 Total Applications", total)
    col2.metric("📅 Interviews", interviews)
    col3.metric("🎉 Offers / Selected", offers)

    st.divider()

    st.markdown(
        """
        <h2 style="color: #172033 !important;">
            Recent Applications
        </h2>
        """,
        unsafe_allow_html=True,
    )

    if applications:
        df = pd.DataFrame(applications)
        preferred_columns = [
            "company",
            "job_title",
            "location",
            "status",
            "applied_date",
        ]
        available_columns = [
            column for column in preferred_columns if column in df.columns
        ]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(
            "No applications yet. Go to Applications "
            "to add your first job application."
        )


# ============================================================
# 7. ADD APPLICATION
# ============================================================

def show_add_application(token):
    st.subheader("➕ Add New Job Application")

    with st.form("add_application_form"):
        company = st.text_input("Company Name")
        job_title = st.text_input("Job Title")
        location = st.text_input("Job Location")

        status = st.selectbox(
            "Application Status",
            [
                "Applied",
                "Interview",
                "Selected",
                "Rejected",
                "Offer Received",
            ],
        )

        applied_date = st.date_input("Applied Date")
        interview_date = st.date_input("Interview Date", value=None)
        notes = st.text_area("Additional Notes")

        submit = st.form_submit_button(
            "Save Application",
            use_container_width=True,
        )

    if submit:
        if not company.strip() or not job_title.strip():
            st.error("Company name and job title are required.")
            return

        application_data = {
            "company": company.strip(),
            "job_title": job_title.strip(),
            "location": location.strip(),
            "status": status,
            "applied_date": applied_date.isoformat(),
            "interview_date": (
                interview_date.isoformat() if interview_date else None
            ),
            "notes": notes,
        }

        result = create_application(token, application_data)

        if result is None:
            st.error("Cannot connect to backend.")
        elif result.status_code == 201:
            st.success("Application added successfully!")
            st.rerun()
        else:
            st.error(f"Error: {result.text}")


# ============================================================
# 8. EDIT AND DELETE APPLICATIONS
# ============================================================

def show_manage_applications(token, applications):
    st.subheader("✏️ Manage Applications")

    if not applications:
        st.info("No applications available to manage.")
        return

    application_options = {
        (
            f"{app.get('id')} - {app.get('company', 'Unknown')} - "
            f"{app.get('job_title', 'Untitled')}"
        ): app
        for app in applications
    }

    selected_label = st.selectbox(
        "Select an application",
        list(application_options.keys()),
    )
    selected_app = application_options[selected_label]

    edit_tab, delete_tab = st.tabs(
        ["Edit Application", "Delete Application"]
    )

    with edit_tab:
        status_options = [
            "Applied",
            "Interview",
            "Selected",
            "Rejected",
            "Offer Received",
        ]

        current_status = selected_app.get("status", "Applied")
        if current_status not in status_options:
            current_status = "Applied"

        with st.form("edit_application_form"):
            edit_company = st.text_input(
                "Company",
                value=selected_app.get("company", ""),
            )
            edit_job_title = st.text_input(
                "Job Title",
                value=selected_app.get("job_title", ""),
            )
            edit_location = st.text_input(
                "Location",
                value=selected_app.get("location") or "",
            )
            edit_status = st.selectbox(
                "Status",
                status_options,
                index=status_options.index(current_status),
            )
            edit_notes = st.text_area(
                "Notes",
                value=selected_app.get("notes") or "",
            )
            update_button = st.form_submit_button(
                "Update Application",
                use_container_width=True,
            )

        if update_button:
            if not edit_company.strip() or not edit_job_title.strip():
                st.error("Company and job title are required.")
            else:
                update_data = {
                    "company": edit_company.strip(),
                    "job_title": edit_job_title.strip(),
                    "location": edit_location.strip(),
                    "status": edit_status,
                    "notes": edit_notes,
                }

                result = update_application(
                    token,
                    selected_app["id"],
                    update_data,
                )

                if result is None:
                    st.error("Cannot connect to backend.")
                elif result.status_code == 200:
                    st.success("Application updated successfully!")
                    st.rerun()
                else:
                    st.error(result.text)

    with delete_tab:
        st.warning(
            "Are you sure you want to delete "
            f"{selected_app.get('company', 'this company')} - "
            f"{selected_app.get('job_title', 'this application')}?"
        )

        if st.button("Delete Application", type="primary"):
            result = delete_application(token, selected_app["id"])

            if result is None:
                st.error("Cannot connect to backend.")
            elif result.status_code == 200:
                st.success("Application deleted successfully!")
                st.rerun()
            else:
                st.error(result.text)


# ============================================================
# 9. SEARCH AND FILTER APPLICATIONS
# ============================================================

def show_search_applications(token):
    st.subheader("🔍 Search and Filter Applications")

    col1, col2, col3 = st.columns(3)

    with col1:
        search_company = st.text_input(
            "Search Company",
            placeholder="Enter company name",
        )

    with col2:
        search_status = st.selectbox(
            "Filter by Status",
            [
                "All",
                "Applied",
                "Interview",
                "Selected",
                "Rejected",
                "Offer Received",
            ],
        )

    with col3:
        search_location = st.text_input(
            "Filter by Location",
            placeholder="Enter location",
        )

    if st.button("Apply Filters", use_container_width=True):
        filtered_response = get_applications(
            token,
            company=search_company or None,
            status=search_status,
            location=search_location or None,
        )

        if filtered_response is None:
            st.error("Cannot connect to backend.")
        elif filtered_response.status_code == 200:
            filtered_data = filtered_response.json()
            filtered_applications = filtered_data.get("applications", [])

            if filtered_applications:
                st.success(
                    f"Found {len(filtered_applications)} matching applications."
                )
                st.dataframe(
                    pd.DataFrame(filtered_applications),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No matching applications found.")
        else:
            st.error(filtered_response.text)


# ============================================================
# 10. APPLICATIONS PAGE
# ============================================================

def show_applications_page(token, applications):
    st.title("📂 Applications")
    st.caption(
        "Add, update, delete, and search your job applications."
    )

    add_tab, manage_tab, search_tab, all_tab = st.tabs(
        [
            "➕ Add Application",
            "✏️ Edit / Delete",
            "🔍 Search",
            "📋 All Applications",
        ]
    )

    with add_tab:
        show_add_application(token)

    with manage_tab:
        show_manage_applications(token, applications)

    with search_tab:
        show_search_applications(token)

    with all_tab:
        if applications:
            st.dataframe(
                pd.DataFrame(applications),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No applications found.")


# ============================================================
# 11. ANALYTICS PAGE
# ============================================================


def show_analytics(applications, total):

    st.title("📊 Job Search Analytics")
    st.caption("Understand your job search progress.")

    if not applications:
        st.info("Add job applications to see your analytics.")
        return

    df = pd.DataFrame(applications)

    col1, col2 = st.columns(2)

    # --------------------------------
    # Applications by Status
    # --------------------------------

    with col1:

        st.subheader("Applications by Status")

        if "status" in df.columns:

            status_counts = (
                df["status"]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Status")
                .reset_index(name="Count")
            )

            fig_status = px.pie(
                status_counts,
                names="Status",
                values="Count",
                hole=0.45,
                title="Status Distribution",
                template="plotly_white"
            )

            st.plotly_chart(
                fig_status,
                use_container_width=True
            )

        else:
            st.info("Status information is unavailable.")

    # --------------------------------
    # Applications by Company
    # --------------------------------

    with col2:

        st.subheader("Applications by Company")

        if "company" in df.columns:

            company_counts = (
                df["company"]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Company")
                .reset_index(name="Applications")
            )

            fig_company = px.bar(
                company_counts,
                x="Company",
                y="Applications",
                title="Company-wise Applications",
                template="plotly_white"
            )

            st.plotly_chart(
                fig_company,
                use_container_width=True
            )

        else:
            st.info("Company information is unavailable.")

    # --------------------------------
    # Application Summary
    # --------------------------------

    st.divider()
    st.subheader("Application Summary")
    st.metric("Total Applications", total)



# ============================================================
# 12. MY PROFILE PAGE
# ============================================================

def show_profile(user):
    st.title("👤 My Profile")
    st.caption("View your account information.")
    st.divider()
    st.subheader("Account Details")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Username",
            value=user.get("username", ""),
            disabled=True,
        )

    with col2:
        st.text_input(
            "Email",
            value=user.get("email", ""),
            disabled=True,
        )

    st.info("Your profile information is currently read-only.")


# ============================================================
# 13. MAIN DASHBOARD AND NAVIGATION
# ============================================================

def show_dashboard():
    apply_custom_design()

    user = st.session_state.user or {}
    token = st.session_state.token

    st.sidebar.title("💼 JobTrack")
    st.sidebar.caption("Job Application Manager")
    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Applications",
            "Analytics",
            "My Profile",
        ],
    )

    st.sidebar.divider()
    st.sidebar.write(
        f"Logged in as: **{user.get('username', 'User')}**"
    )

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()

    applications = []
    total = 0

    if page in ["Dashboard", "Applications", "Analytics"]:
        data = fetch_applications(token)

        if data is None:
            return

        applications = data.get("applications", [])
        total = data.get("total", len(applications))

    if page == "Dashboard":
        show_overview(applications, total)
    elif page == "Applications":
        show_applications_page(token, applications)
    elif page == "Analytics":
        show_analytics(applications, total)
    elif page == "My Profile":
        show_profile(user)


# ============================================================
# 14. APPLICATION ENTRY POINT
# ============================================================

if st.session_state.token is None:
    show_authentication()
else:
    try:
        show_dashboard()
    except Exception as error:
        st.error("Something went wrong while loading JobTrack.")
        st.exception(error)
