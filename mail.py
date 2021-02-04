#!/usr/bin/python3
import smtplib as root
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

class Reciver:
	def __init__(self, login:str, password:str, imap=None):
		self.imap = imap if imap else 'imap.{}'.format(login.split('@')[-1])
		self.connection = imaplib.IMAP4_SSL(self.imap)
		self.connection.login(login, password)

	def load(self, folder:str='inbox', enc="(RFC822)", count=1):
		result = []
		status, messages = self.connection.select("inbox")
		if status == 'OK':
			messages = int(messages[0])

			for i in range(messages, messages-count, -1):
				current_message = {'message':''}
				res, msg = self.connection.fetch(str(i), enc)
				for response in msg:
					if isinstance(response, tuple):
						msg = email.message_from_bytes(response[1])
						subject, encoding = decode_header(msg["Subject"])[0]
						
						if isinstance(subject, bytes):
							subject = subject.decode(encoding)
						current_message['subject'] = subject

						From, encoding = decode_header(msg.get("From"))[0]
						if isinstance(From, bytes):
							From = From.decode(encoding)
						current_message['from'] = From

						if msg.is_multipart():
							current_message['attach'] = []
							for part in msg.walk():
								try:
									current_message['message'] += part.get_payload(decode=True).decode()
								except:
									pass
								current_message['attach'].append([part, str(part.get("Content-Disposition"))])
						else:
							current_message['message'] = msg.get_payload(decode=True).decode()

						current_message['content_type'] = msg.get_content_type()

				result.append(current_message)

		return result

	def download_attachment(self, part, content_disposition, folder='.'):
		if "attachment" in content_disposition:
			filename = part.get_filename()
			if filename:
				filepath = os.path.join(folder, filename)
				open(filepath, "wb").write(part.get_payload(decode=True))


class EMail:
	def __init__(self, **kwargs):
		self._login      = kwargs['login']
		self._password   = kwargs['password']
		self._smtp = kwargs['smtp'] if 'smtp' in kwargs else ('smtp.'+self._login.split('@')[-1], 456)

		self._server = root.SMTP_SSL( *self._smtp )
		self._server.login( self._login, self._password )
		self.reader = Reciver(self._login, self._password)

	def mail(self, **data):
		""" Method for sending emils """
		msg = MIMEMultipart()

		msg[ 'Subject' ] = data['subject']
		msg[ 'From' ] = self._login
		msg.attach( MIMEText( data['message'], 'plain' ) )

		self._server.sendmail( self._login, data['to'], msg.as_string() )

	def image(self,**data):
		""" Method for sending images """
		with open(data['path'], 'rb') as f :
			img_data = f.read()

		msg = MIMEMultipart()

		msg[ 'Subject' ] = data['subject']
		msg[ 'From' ] = self._login

		msg.attach( MIMEText( data['message'], 'plain' ) )
		image = MIMEImage(img_data, name=os.path.basename(data['path']))
		msg.attach(image)

		self._server.sendmail( self._login, data['to'], msg.as_string() )

	def bomb(self, **data):
		""" Method for sending emils """
		msg = MIMEMultipart()

		msg[ 'Subject' ] = data['subject']
		msg[ 'From' ] = self._login
		msg.attach( MIMEText( data['message'], 'plain' ) )

		for i in range(int(data['count'])):
			self._server.sendmail( self._login, data['to'], msg.as_string() )

	def html_message(self, **data):
		html = data['html']

		msg = MIMEMultipart()

		msg[ 'Subject' ] = data['subject']
		msg[ 'From' ] = self._login
		msg.attach( MIMEText( html, 'html' ) )

		self._server.sendmail( self._login, data['to'], msg.as_string() )

	def read_file(self, path, encoding="utf-8"):
		with open(path, 'r', encoding=encoding) as f:
			return f.read()


	def stop(self):
		self._server.quit()

if __name__ == '__main__':
	mail = EMail(login='Your@mail.login', password='yourmailpassword')
	mail.mail(message="Hello", subject='Simple Html Message', to='reciver@email.addres')
	mail.stop()

