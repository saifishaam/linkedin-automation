from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

class EmailRequest(BaseModel):
    email: str
    subject: str
    message: str

class LinkedInRequest(BaseModel):
    linkedin_url: str
    message: str

@app.post("/send_email")
def send_email(request: EmailRequest):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        message = f"Subject: {request.subject}\n\n{request.message}"
        server.sendmail("your_email@gmail.com", request.email, message)
        server.quit()
        return {"status": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_linkedin_message")
def send_linkedin_message(request: LinkedInRequest):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(request.linkedin_url)
        message_box = driver.find_element(By.CSS_SELECTOR, "textarea")
        message_box.send_keys(request.message)
        send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        send_button.click()
        driver.quit()
        return {"status": "LinkedIn message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))