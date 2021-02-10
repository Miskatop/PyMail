#!/usr/bin/python3
import smtplib as root
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from .errors import *
import os


class Reciver:


	def __init__(self, login:str, password:str, imap=None, message_load_type=0):
		self.imap = imap if imap else ('imap.{}'.format(login.split('@')[-1]), 993)
		try:
			self.connection = imaplib.IMAP4_SSL(*self.imap)
		except Exception as e:
			raise ImapError(e)

		self.connection.login(login, password)
		self.message_load_type = message_load_type


	def load(self, folder:str='inbox', enc="(RFC822)", count=1):
		result = []
		status, messages = self.connection.select(folder)
		if status == 'OK':
			messages = int(messages[0])

			for i in range(messages, messages-count, -1):
				current_message = {'message':''}
				this_type = 0
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
									if self.message_load_type == this_type:
										current_message['message'] = part.get_payload(decode=True).decode()
									this_type+=1
								except:
									pass
								current_message['attach'].append([part, str(part.get("Content-Disposition"))])
						else:
							current_message['message'] = msg.get_payload(decode=True).decode()

						current_message['content_type'] = msg.get_content_type()

				result.append(current_message)

		return result

	def count(self, folder:str='inbox'):
		_, messages = self.connection.select(folder)
		return int(messages[0].decode('utf-8'))


	def download_attachment(self, part, content_disposition, folder='.'):
		if "attachment" in content_disposition:
			filename = part.get_filename()
			if filename:
				filepath = os.path.join(folder, filename)
				open(filepath, "wb").write(part.get_payload(decode=True))


class EMail:
	reader = None
	message_min_length = 10
	has_subject = True
	html_prop = 2


	def __init__(self, **kwargs):
		self._login      = kwargs['login']
		self._password   = kwargs['password']
		self._smtp = kwargs['smtp'] if 'smtp' in kwargs else ('smtp.'+self._login.split('@')[-1], 456)
		self._imap = kwargs['imap'] if 'imap' in kwargs else ('imap.{}'.format(login.split('@')[-1]), 993)


		try:
			self._server = root.SMTP_SSL( *self._smtp )
		except Exception as e:
			raise SmtpError(e)

		if 'reader' in kwargs and kwargs['reader']:
			try:
				self.reader = Reciver(self._login, self._password, imap=self._imap)
			except Exception as e:
				raise ImapError(e)

		self._server.login( self._login, self._password )


	def read(self, *args, **kwargs):
		if self.reader:
			return self.reader.load(*args, **kwargs)
		else:
			raise UndefinedReaderError('Reader is not Defined')


	def count(self, *args, **kwargs):
		if self.reader:
			return self.reader.count(*args, **kwargs)
		else:
			raise UndefinedReaderError('Reader is not Defined')


	def download(self, *args, **kwargs):
		if self.reader:
			return self.reader.download_attachment(*args, **kwargs)
		else:
			raise UndefinedReaderError('Reader is not Defined, Send reader=True as argument of class initializer')


	def mail(self, **data):
		""" Method for sending emils """
		msg = MIMEMultipart()
		if 'message' in data and len(data['message']) > self.message_min_length:
			message = data['message']
		else:
			raise EmptyMailError("message is empty send message as message atribute")

		if not 'subject' in data and self.has_subject:
			raise EmptySubjectError("send the subject of message by subject attribute")

		subject = data['subject'] if 'subject' in data else ""

		msg[ 'Subject' ] = subject
		msg[ 'From' ] = self._login
		msg.attach( MIMEText( message , 'plain' ) )

		return self._server.sendmail( self._login, data['to'], msg.as_string() )


	def image(self,**data):
		""" Method for sending images """

		if 'message' in data and len(data['message']) > self.message_min_length:
			message = data['message']
		else:
			raise EmptyMailError("message is empty send message as message atribute")

		if not 'subject' in data and self.has_subject:
			raise EmptySubjectError("send the subject of message by subject attribute")

		if 'path' in data:
			path = data['path']
		else:
			raise PathError("Path is not defined")

		subject = data['subject'] if 'subject' in data else ""

		try:
			with open(path, 'rb') as f :
				img_data = f.read()
		except Exception as e:
			raise e

		msg = MIMEMultipart()

		msg[ 'Subject' ] = subject
		msg[ 'From' ] = self._login

		msg.attach( MIMEText( data['message'], 'plain' ) )
		msg.attach( MIMEImage(img_data, name=os.path.basename(path)) )

		return self._server.sendmail( self._login, data['to'], msg.as_string() )


	def bomb(self, **data):
		""" Method for sending emils """
		msg = MIMEMultipart()
		ret = []

		msg[ 'Subject' ] = data['subject']
		msg[ 'From' ] = self._login
		msg.attach( MIMEText( data['message'], 'plain' ) )

		for i in range(int(data['count'])):
			res.append(self._server.sendmail( self._login, data['to'], msg.as_string() ))

		return res


	def html_message(self, **data):
		if 'html' in data and len(data['html']) > self.message_min_length*self.html_prop:
			html = data['html']
		else:
			raise EmptyMailError("html is empty send html as html atribute")

		if not 'subject' in data and self.has_subject:
			raise EmptySubjectError("send the subject of message by subject attribute")

		subject = data['subject'] if 'subject' in data else ""

		msg = MIMEMultipart()

		msg[ 'Subject' ] = data['subject']
		msg[ 'From' ] = self._login
		msg.attach( MIMEText( html, 'html' ) )

		return self._server.sendmail( self._login, data['to'], msg.as_string() )


	def read_file(self, path, encoding="utf-8"):
		with open(path, 'r', encoding=encoding) as f:
			return f.read()


	def stop(self):
		return self._server.quit()

if __name__ == '__main__':
	print('PyMail - Copyright (C) 2021 Mikhayil Martirosyan')
