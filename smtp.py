import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
def notify(pill, address): 
	fromaddr = "pharmabot4@gmail.com"
	toaddr = address
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "DISPENSE!"
 
	body = "YOUR PILL" + pill.name + "HAS BEEN DISPENSED AT" +str(pill.time[0])+ ":"+str(pill.time[1])
	msg.attach(MIMEText(body, 'plain'))
 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "pharmabot44")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)

