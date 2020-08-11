import csv
import config
import smtplib
from time import sleep
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Function to create template out of txt file
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():

    #Call template function
    message_template = read_template('message.txt') #MAKE SURE TO EDIT THE "message.txt" FILE FOR HOW YOU WANT THE BODY OF THE EMAIL TO LOOK

    #Start host communication
    s = smtplib.SMTP('host:port') #EDIT THIS WITH YOUR EMAIL SERVERS HOST AND PORT
    s.ehlo()
    s.starttls()
    s.login(config.MY_ADDR, config.PASSWORD) #EDIT YOUR USER AND PASSWORD IN THE CONFIG FILE

    #Read from csv file
    with open('emails.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        #Parse through csv file
        for row in csv_reader:
            msg = MIMEMultipart()
            college = row["College"]
            email = row["Email"]
            
            #Subsitute variables COLLEGE_NAME and EMAIL
            message = message_template.substitute(COLLEGE_NAME=college, EMAIL=email)

            #Compile Message
            msg['From'] = config.MY_ADDR
            msg['To'] = email
            msg['Subject'] = f"{college} Admissions and Scholarship Information" #CHANGE THIS. THIS IS THE SUBJECT HEADER.

            #Attach body from template and send email
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
            print(f"Sending Email To: {college}")
            del msg

            #Limit to keep host server from breaking while sending
            sleep(2)
        s.quit()

if __name__ == "__main__":
    main()
