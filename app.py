import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np
import csv


class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def read_credentials():
    credentials = {}
    with open("data/credentials.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            credentials[row[0]] = {"password": row[1], "email": row[2]}
    return credentials

def write_credentials(username, password, email):
    with open("data/credentials.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password, email])

def login(username, password):
    credentials = read_credentials()
    if username in credentials and credentials[username]["password"] == password:
        return True
    return False

def signup(username, password, email):
    credentials = read_credentials()
    if username not in credentials:
        write_credentials(username, password, email)
        return True
    return False

username = None

def main():
    session_state = SessionState(username=None)
    
    st.title("Welcome")
    
    lr = LinearRegression()
    


    nav = st.sidebar.radio("Navigation", ["Login", "Home", "Prediction", "Contribute"])

    if nav == "Login":
        st.subheader("Login")
        mode = st.radio("Choose Mode:", ("Login", "Signup"))

        if mode == "Login":
            st.subheader("Login")
            username_input = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if login(username_input, password):
                    session_state.username = username_input
                    st.success("Logged in successfully!")
                    # return username
                else:
                    st.error("Username or password incorrect.")
                    # username = username_input

        elif mode == "Signup":
            st.subheader("Signup")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            new_email = st.text_input("Email")

            if st.button("Signup"):
                if signup(new_username, new_password, new_email):
                    st.success("Signup successful! Please login.")
                else:
                    st.error("Username already exists.")

    elif nav == "Home":
        if session_state.username:
            st.write("Hii "+username+" , welcome to our page.")

        st.image("data/salary.png", width=500)
        data = pd.read_csv("data/Salary_Data.csv")

        if st.checkbox("Show Table"):
            st.table(data)

        graph = st.selectbox("What kind of graph?", ["Non-Interactive", "Interactive"])

        val = st.slider("Filter data using years", 0, 20)
        data = data.loc[data["YearsExperience"] >= val]

        if graph == "Non-Interactive":
            plt.figure(figsize=(10, 3))
            fig, ax = plt.subplots()
            ax.scatter(data["YearsExperience"], data["Salary"])
            plt.ylim(0)
            plt.xlabel("Years Of Experience")
            plt.ylabel("Salary")
            plt.tight_layout()
            st.pyplot(fig)

        if graph == "Interactive":
            layout = go.Layout(
                xaxis=dict(range=[0, 16]),
                yaxis=dict(range=[0, 2100000])
            )
            fig = go.Figure(data=go.Scatter(x=data["YearsExperience"], y=data["Salary"], mode="markers"), layout=layout)
            st.plotly_chart(fig)

    elif nav == "Prediction":
        data = pd.read_csv("data/Salary_Data.csv")
        x = np.array(data["YearsExperience"]).reshape(-1, 1)
        lr.fit(x, np.array(data["Salary"]))
        st.header("Let's Predict your salary")
        val = st.number_input("Enter your experience", 0.00, 20.00, step=0.25)
        val = np.array(val).reshape(1, -1)
        pred = lr.predict(val)[0]

        if st.button("Predict"):
            st.success(f"Your predicted salary is {round(pred)}")

    elif nav == "Contribute":
        data = pd.read_csv("data/Salary_Data.csv")
        st.header("Contribute to our data set")
        # Check if user is logged in
        ex = st.number_input("Enter your experience (In years)", 0.00, 20.00, step=0.50)
        sal = st.number_input("Enter your salary", 0.00, 1000000.00, step=1000.0)
        if st.button("Submit"):
            to_add = {"YearsExperience": [ex], "Salary": [sal]}
            to_add = pd.DataFrame(to_add)
            to_add.to_csv("data/Salary_Data.csv", mode='a', header=False, index=False)
            st.success("Submitted Successfully")

if __name__ == "__main__":
    main()
