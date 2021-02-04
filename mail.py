#!/usr/bin/python3
import smtplib as root
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import os

class EMail:
	def __init__(self, **kwargs):
		self._login      = kwargs['login']
		self._password   = kwargs['password']
		self._smtp = kwargs['smtp'] if 'smtp' in kwargs else ('smtp.'+self._login.split('@')[-1], 456)

		self._server = root.SMTP_SSL( *self._smtp )
		self._server.login( self._login, self._password )

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

