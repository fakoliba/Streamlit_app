
import smtplib
import streamlit as st

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Page Configuration
#st.set_page_config(page_title="Mo's playground", layout="centered")
st.sidebar.success("Select a demo from the options above to explore and intereact with some of my work .")
# Title and Introduction Section
st.title("Mo's playground")
st.write("Welcome!")


# Summary of Experiences
#st.header("Summary of Experiences")
st.write("""
I’m Mo,  an accomplished engineering leader with deep expertise in observability, reliability engineering, and cloud technologies. Over my career, I’ve successfully led teams to design, implement, and scale resilient systems that drive performance, availability, and exceptional user experiences. At Nike, I’ve spearheaded initiatives improving platform uptime, optimizing launch processes, and fostering a culture of innovation through automation and collaboration.

With a solid foundation in DevOps, cloud infrastructure, and cutting-edge technologies like AWS, Kubernetes, and machine learning, I’m passionate about solving complex problems and mentoring teams to achieve technical excellence. Whether managing critical launches or exploring AI-driven solutions, I thrive on turning challenges into opportunities for growth and success..
""")

# Links to Online Profiles
st.header("Connect with Me")
linkedin_url = "https://www.linkedin.com/in/mohamed-c-57ba0a1b3/"
github_url = "https://github.com/fakoliba"

st.write(f"[LinkedIn Profile]({linkedin_url})")
st.write(f"[GitHub Profile]({github_url})")

# Footer or Additional Information
st.write("Feel free to explore my profiles and reach out for collaboration opportunities!")        


# Email Form
st.header("Send Me an Email")
with st.form(key='email_form'):
    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    submit_button = st.form_submit_button(label='Send Email')

    if submit_button:
        if user_name and user_email and subject and message:
            try:
                # Email configuration
                sender_email = "your_email@example.com"  # Replace with your email
                receiver_email = "your_email@example.com"  # Replace with your email
                password = "your_email_password"  # Replace with your email password

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject

                body = f"Name: {user_name}\nEmail: {user_email}\n\n{message}"
                msg.attach(MIMEText(body, 'plain'))

                # Send the email
                server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server and port
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                server.sendmail(sender_email, receiver_email, text)
                server.quit()

                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please fill out all fields.")