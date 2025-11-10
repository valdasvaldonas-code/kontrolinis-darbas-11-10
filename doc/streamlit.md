# Streamlit: Interactive Python Web Applications

Streamlit is an open-source Python library that transforms Python scripts into interactive web applications with minimal code. It provides a declarative API for creating data dashboards, machine learning tools, and internal applications without requiring frontend development expertise. The framework runs a Tornado-based backend server that communicates with a React-based frontend via WebSocket using Protocol Buffers, enabling real-time reactivity and automatic UI updates when script state changes.

Built by Snowflake Inc., Streamlit follows a unique execution model where the entire Python script reruns on user interaction, with intelligent caching mechanisms (`@st.cache_data`, `@st.cache_resource`) to optimize performance. The library supports a wide range of components including data visualization (Altair, Plotly, Matplotlib), interactive widgets (sliders, buttons, text inputs), layout containers (columns, tabs, sidebars), and database connections (SQL, Snowflake). Session state management enables stateful applications, while fragments allow partial reruns for performance optimization.

## Core APIs and Functions

### Display Text and Markdown

```python
import streamlit as st

# Display markdown with formatting
st.write("Hello, *World!* :sunglasses:")

# Multiple arguments combined
st.write("1 + 1 = ", 2)

# Display title, header, subheader
st.title("Main Application Title")
st.header("Section Header")
st.subheader("Subsection Header")

# Display code with syntax highlighting
st.code("""
def hello_world():
    print("Hello, World!")
""", language="python")

# Display LaTeX equations
st.latex(r"\sum_{i=1}^{n} x_i^2")
```

### Display DataFrames and Tables

```python
import streamlit as st
import pandas as pd
import numpy as np

# Create sample data
df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=["a", "b", "c", "d", "e"]
)

# Interactive dataframe with sorting and selection
event = st.dataframe(
    df,
    key="my_dataframe",
    on_select="rerun",
    selection_mode=["multi-row", "multi-column"],
    hide_index=False,
    width=700,
    height=400
)

# Access selected rows
if event.selection.rows:
    st.write("Selected rows:", event.selection.rows)
    selected_data = df.iloc[event.selection.rows]
    st.write(selected_data)

# Static table display
st.table(df.head())

# Display JSON data
st.json({
    "name": "John Doe",
    "age": 30,
    "skills": ["Python", "Streamlit", "Data Science"]
})
```

### Input Widgets - Text and Numbers

```python
import streamlit as st

# Text input with icon and validation
name = st.text_input(
    "Enter your name",
    value="",
    max_chars=50,
    placeholder="John Doe",
    help="Please enter your full name",
    icon="👤",
    key="name_input"
)

# Password input
password = st.text_input(
    "Password",
    type="password",
    autocomplete="current-password"
)

# Multi-line text area
description = st.text_area(
    "Description",
    value="",
    height=150,
    placeholder="Enter detailed description..."
)

# Number input with bounds
age = st.number_input(
    "Age",
    min_value=0,
    max_value=120,
    value=25,
    step=1,
    help="Enter your age in years"
)

# Slider with range
temperature = st.slider(
    "Temperature",
    min_value=-50,
    max_value=50,
    value=20,
    step=1,
    format="%d°C"
)

# Date and time inputs
from datetime import date, time

birth_date = st.date_input(
    "Date of birth",
    value=date(1990, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=date.today()
)

appointment_time = st.time_input(
    "Appointment time",
    value=time(9, 0)
)
```

### Selection Widgets

```python
import streamlit as st

# Dropdown selectbox
option = st.selectbox(
    "Choose an option",
    options=["Option 1", "Option 2", "Option 3"],
    index=0,
    help="Select one option from the dropdown"
)

# Multi-select dropdown
selected_colors = st.multiselect(
    "Choose colors",
    options=["Red", "Green", "Blue", "Yellow", "Orange"],
    default=["Red", "Blue"],
    help="You can select multiple colors"
)

# Radio buttons
radio_choice = st.radio(
    "Select mode",
    options=["Development", "Production", "Testing"],
    index=0,
    horizontal=True
)

# Checkbox
agree = st.checkbox("I agree to terms and conditions")

if agree:
    st.success("Thank you for agreeing!")

# Select slider with custom options
size = st.select_slider(
    "Size",
    options=["XS", "S", "M", "L", "XL", "XXL"],
    value="M"
)

# Pills (new segmented control)
view_mode = st.pills(
    "View mode",
    options=["Grid", "List", "Gallery"],
    default="Grid",
    selection_mode="single"
)
```

### Buttons and Interactive Elements

```python
import streamlit as st

# Primary button with callback
def on_submit():
    st.session_state.submitted = True
    st.session_state.count = st.session_state.get("count", 0) + 1

if st.button(
    "Submit",
    type="primary",
    help="Click to submit the form",
    on_click=on_submit,
    use_container_width=True
):
    st.write("Button was clicked!")

# Download button
import pandas as pd

df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
    type="primary"
)

# Link button
st.link_button(
    "Go to Documentation",
    "https://docs.streamlit.io",
    type="secondary"
)

# File uploader
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["csv", "txt", "json"],
    accept_multiple_files=False,
    help="Upload CSV, TXT, or JSON files"
)

if uploaded_file is not None:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

# Camera input
camera_photo = st.camera_input("Take a picture")

if camera_photo is not None:
    from PIL import Image
    image = Image.open(camera_photo)
    st.image(image, caption="Captured photo")
```

### Charts and Visualizations

```python
import streamlit as st
import pandas as pd
import numpy as np

# Sample data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)

# Line chart
st.line_chart(
    chart_data,
    x=None,
    y=["a", "b", "c"],
    color=["#FF0000", "#00FF00", "#0000FF"],
    width=0,
    height=400
)

# Bar chart
st.bar_chart(chart_data)

# Area chart
st.area_chart(chart_data)

# Scatter chart
scatter_data = pd.DataFrame({
    "x": np.random.randn(100),
    "y": np.random.randn(100),
    "size": np.random.randint(10, 100, 100),
    "color": np.random.choice(["red", "blue", "green"], 100)
})

st.scatter_chart(
    scatter_data,
    x="x",
    y="y",
    size="size",
    color="color"
)

# Altair chart with interactivity
import altair as alt

point_selector = alt.selection_point("point_selection")
interval_selector = alt.selection_interval("interval_selection")

chart = (
    alt.Chart(chart_data)
    .mark_circle(size=100)
    .encode(
        x="a:Q",
        y="b:Q",
        color=alt.condition(point_selector, "c:Q", alt.value("lightgray")),
        tooltip=["a", "b", "c"]
    )
    .add_params(point_selector, interval_selector)
)

event = st.altair_chart(
    chart,
    use_container_width=True,
    key="altair_chart",
    on_select="rerun"
)

if event.selection:
    st.write("Chart selection:", event.selection)

# Map visualization
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)

st.map(
    map_data,
    latitude='lat',
    longitude='lon',
    size=20,
    color="#0000FF"
)
```

### Layout and Containers

```python
import streamlit as st

# Columns layout
col1, col2, col3 = st.columns([1, 2, 1], gap="large")

with col1:
    st.header("Left")
    st.write("Content in left column")

with col2:
    st.header("Center")
    st.write("Content in center column (wider)")

with col3:
    st.header("Right")
    st.write("Content in right column")

# Tabs
tab1, tab2, tab3 = st.tabs(["Dataset", "Visualization", "Analysis"])

with tab1:
    st.write("Dataset content")

with tab2:
    st.write("Visualization content")

with tab3:
    st.write("Analysis content")

# Expandable container
with st.expander("Advanced Settings", expanded=False):
    st.slider("Temperature", 0, 100, 50)
    st.checkbox("Enable debug mode")

# Container with border and scrolling
with st.container(
    border=True,
    height=300,
    horizontal=False,
    horizontal_alignment="left"
):
    st.write("Content in container")
    for i in range(20):
        st.write(f"Line {i}")

# Sidebar
with st.sidebar:
    st.title("Sidebar")
    st.selectbox("Choose option", ["A", "B", "C"])
    st.button("Sidebar button")

# Status container with spinner
with st.status("Processing data...", expanded=True) as status:
    st.write("Loading dataset...")
    import time
    time.sleep(1)
    st.write("Analyzing data...")
    time.sleep(1)
    st.write("Generating report...")
    time.sleep(1)
    status.update(label="Complete!", state="complete", expanded=False)

# Popover
with st.popover("Click for more info"):
    st.write("This is additional information")
    st.write("Hidden until the popover is opened")
```

### Session State Management

```python
import streamlit as st

# Initialize session state
if "counter" not in st.session_state:
    st.session_state.counter = 0
    st.session_state.history = []

# Update session state
def increment():
    st.session_state.counter += 1
    st.session_state.history.append(st.session_state.counter)

def reset():
    st.session_state.counter = 0
    st.session_state.history = []

# Display current state
st.write(f"Counter: {st.session_state.counter}")
st.write(f"History: {st.session_state.history}")

# Buttons with callbacks
col1, col2 = st.columns(2)
with col1:
    st.button("Increment", on_click=increment)
with col2:
    st.button("Reset", on_click=reset)

# Widget with key automatically stores in session state
user_name = st.text_input("Name", key="user_name")
st.write(f"Session state user_name: {st.session_state.user_name}")

# Query parameters (URL state)
st.query_params["page"] = "home"
st.query_params["user"] = user_name

# Access query params
if "page" in st.query_params:
    current_page = st.query_params["page"]
    st.write(f"Current page: {current_page}")
```

### Caching for Performance

```python
import streamlit as st
import pandas as pd
import time

# Cache data loading
@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_data(filepath):
    """Cache expensive data loading operations."""
    time.sleep(2)  # Simulate slow loading
    df = pd.read_csv(filepath)
    return df

# Cache resource initialization
@st.cache_resource
def init_database_connection():
    """Cache database connections and ML models."""
    import sqlite3
    conn = sqlite3.connect("database.db", check_same_thread=False)
    return conn

# Use cached functions
# df = load_data("large_dataset.csv")  # Only runs once per hour
# conn = init_database_connection()  # Only runs once per session

# Cache with parameters
@st.cache_data
def expensive_computation(param1, param2):
    """Cache results based on input parameters."""
    result = param1 * param2 + sum(range(1000000))
    return result

result = expensive_computation(10, 20)
st.write(f"Result: {result}")

# Clear cache programmatically
if st.button("Clear cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()
```

### Forms and User Input Collection

```python
import streamlit as st

# Create a form
with st.form(key="user_form", clear_on_submit=True):
    st.write("User Registration Form")

    name = st.text_input("Full Name", key="form_name")
    email = st.text_input("Email", key="form_email")
    age = st.number_input("Age", min_value=18, max_value=100, key="form_age")

    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country", ["USA", "UK", "Canada", "Other"])
    with col2:
        interests = st.multiselect(
            "Interests",
            ["Sports", "Music", "Reading", "Travel"]
        )

    newsletter = st.checkbox("Subscribe to newsletter")

    # Form submit button (required)
    submitted = st.form_submit_button("Submit", type="primary")

    if submitted:
        if name and email:
            st.success(f"Form submitted for {name}!")
            st.write({
                "name": name,
                "email": email,
                "age": age,
                "country": country,
                "interests": interests,
                "newsletter": newsletter
            })
        else:
            st.error("Please fill in all required fields")
```

### Data Editor (Editable Tables)

```python
import streamlit as st
import pandas as pd

# Create editable dataframe
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
    "active": [True, False, True]
})

# Configure column types
edited_df = st.data_editor(
    df,
    num_rows="dynamic",  # Allow adding/deleting rows
    use_container_width=True,
    hide_index=False,
    column_config={
        "name": st.column_config.TextColumn(
            "Full Name",
            help="Employee full name",
            max_chars=50,
            required=True
        ),
        "age": st.column_config.NumberColumn(
            "Age",
            help="Employee age",
            min_value=18,
            max_value=100,
            step=1,
            format="%d years"
        ),
        "email": st.column_config.TextColumn(
            "Email Address",
            validate="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
            help="Valid email required"
        ),
        "active": st.column_config.CheckboxColumn(
            "Active",
            help="Is employee active?",
            default=False
        )
    },
    key="data_editor"
)

# Display edited data
if st.button("Show edited data"):
    st.write("Edited dataframe:")
    st.write(edited_df)
```

### Database Connections

```python
import streamlit as st

# SQL Connection
conn = st.connection("my_database", type="sql", url="sqlite:///mydb.db")

# Query data with caching
@st.cache_data(ttl=600)
def get_users(_conn):
    """Query users from database (note the underscore prefix for connection)."""
    df = _conn.query("SELECT * FROM users WHERE active = 1", ttl=600)
    return df

# Use connection
try:
    users_df = get_users(conn)
    st.dataframe(users_df)
except Exception as e:
    st.error(f"Database error: {e}")

# Execute updates
if st.button("Add sample user"):
    with conn.session as session:
        session.execute(
            "INSERT INTO users (name, email) VALUES (:name, :email)",
            {"name": "John Doe", "email": "john@example.com"}
        )
        session.commit()
    st.success("User added!")
    st.cache_data.clear()  # Clear cache to show new data

# Custom connection class
from streamlit.connections import BaseConnection

class MyCustomConnection(BaseConnection):
    def _connect(self, **kwargs):
        # Initialize your connection
        return {"api_key": kwargs.get("api_key")}

    def query(self, endpoint):
        # Implement your query logic
        return f"Data from {endpoint}"

# Use custom connection
# custom_conn = st.connection("my_api", type=MyCustomConnection, api_key="secret")
```

### Chat Interface

```python
import streamlit as st
import time

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "avatar": "👤"
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""

        # Simulate streaming response
        assistant_response = f"You said: {prompt}. Here's my response..."
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "avatar": "🤖"
    })
```

### Stream Output with Typewriter Effect

```python
import streamlit as st
import time

def generate_response():
    """Generator function for streaming output."""
    words = "This is a streaming response that appears word by word like a typewriter".split()
    for word in words:
        yield word + " "
        time.sleep(0.1)

# Stream text with cursor
if st.button("Generate response"):
    st.write_stream(generate_response(), cursor="▌")

# Stream mixed content (text and dataframes)
def generate_mixed_content():
    """Stream both text and other objects."""
    yield "Here is some text... "
    time.sleep(0.5)

    import pandas as pd
    import numpy as np
    yield pd.DataFrame(np.random.randn(5, 3), columns=["A", "B", "C"])

    yield "And more text after the dataframe!"

if st.button("Generate mixed content"):
    response = st.write_stream(generate_mixed_content())
    st.write("Full response:", response)
```

### Page Configuration and Navigation

```python
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="My App",
    page_icon="🚀",
    layout="wide",  # "centered" or "wide"
    initial_sidebar_state="expanded",  # "auto", "expanded", "collapsed"
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues',
        'About': 'My amazing Streamlit app v1.0'
    }
)

# Multi-page app navigation
from streamlit import Page

pages = [
    Page("home.py", title="Home", icon="🏠"),
    Page("data.py", title="Data Analysis", icon="📊"),
    Page("settings.py", title="Settings", icon="⚙️")
]

pg = st.navigation(pages)
pg.run()

# Programmatic page switching
if st.button("Go to Data page"):
    st.switch_page("pages/data.py")

# Page links
st.page_link("home.py", label="Home", icon="🏠")
st.page_link("pages/data.py", label="Data", icon="📊")
st.page_link("https://docs.streamlit.io", label="Documentation", icon="📚")
```

### Fragments (Partial Reruns)

```python
import streamlit as st
import time

# Regular widget - causes full rerun
full_rerun_button = st.button("Full Rerun")

st.write(f"Page loaded at: {time.time()}")

# Fragment - only reruns this section
@st.fragment
def expensive_operation():
    """This fragment reruns independently."""
    st.write("Fragment section")

    fragment_button = st.button("Fragment Rerun")
    if fragment_button:
        st.write("Only fragment reran!")

    # Expensive computation only runs when fragment reruns
    time.sleep(1)
    st.write(f"Fragment updated at: {time.time()}")

expensive_operation()

# Fragment with custom rerun interval
@st.fragment(run_every=5)  # Auto-rerun every 5 seconds
def live_data():
    """Auto-updating fragment."""
    st.write(f"Live data: {time.time()}")

live_data()
```

### Dialogs (Modal Windows)

```python
import streamlit as st

@st.dialog("Settings Dialog")
def show_settings_dialog():
    """Modal dialog for settings."""
    st.write("Configure your settings")

    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    language = st.selectbox("Language", ["English", "Spanish", "French"])

    if st.button("Save"):
        st.session_state.theme = theme
        st.session_state.language = language
        st.rerun()

# Trigger dialog
if st.button("Open Settings"):
    show_settings_dialog()

# Confirmation dialog
@st.dialog("Confirm Deletion")
def confirm_delete(item_name):
    st.write(f"Are you sure you want to delete {item_name}?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, delete", type="primary", use_container_width=True):
            st.session_state.deleted = True
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

if st.button("Delete Item"):
    confirm_delete("important_file.txt")
```

### Progress Indicators and Status

```python
import streamlit as st
import time

# Progress bar
progress_bar = st.progress(0, text="Processing...")

for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1, text=f"Processing... {i+1}%")

progress_bar.empty()

# Spinner
with st.spinner("Loading..."):
    time.sleep(2)
st.success("Done!")

# Status messages
st.info("This is an informational message")
st.success("Operation completed successfully!")
st.warning("This is a warning message")
st.error("An error occurred!")

# Toast notifications
if st.button("Show toast"):
    st.toast("Operation successful!", icon="✅")

# Balloons and snow animations
if st.button("Celebrate!"):
    st.balloons()

if st.button("Let it snow!"):
    st.snow()
```

## Integration Patterns and Use Cases

Streamlit excels in rapid prototyping of data applications, machine learning model deployment, and creating internal dashboards. Common use cases include building chatbots with LLM integration using `st.chat_message` and `st.chat_input`, creating data exploration tools with interactive filters and visualizations, deploying ML models with real-time inference through widget callbacks, and constructing admin panels with `st.data_editor` for CRUD operations. The framework's stateless execution model, where scripts rerun on interaction, is complemented by session state for maintaining user context across reruns.

For production deployments, Streamlit apps can be hosted on Streamlit Community Cloud, containerized with Docker, or deployed to cloud platforms (AWS, GCP, Azure) using standard Python application servers. Best practices include using `@st.cache_data` for expensive computations and data loading, `@st.cache_resource` for database connections and ML models, fragments (`@st.fragment`) for optimizing specific UI sections, and query parameters for shareable application states. Security considerations include validating user inputs, using environment variables for secrets (`st.secrets`), implementing authentication with `st.login`/`st.logout`, and setting appropriate CORS policies for production deployments.
