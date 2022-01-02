# PyMail - mail client written on python

## Requirements\`
```
email 4.0+
```

## Usage\`

### Send Simple Message\`
#### Attributes -> message, subject, to
```python

mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.mail(message="Hello", subject='Simple Html Message', to='mail@to.recive')
mail.stop()

```

### Send Message Bomber (many messages) \`
#### Attributes -> message*, subject*, to, count
```python
mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.bomb(message="Hello", subject='Simple Html Message', to='mail@to.recive', count=10) # count message recive the client
mail.stop()
```

### Send html Message \`
#### Attributes -> html*, subject*, to
```python
mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.html(html="<h1>Hello</h1>", subject='Simple Html Message', to='mail@to.recive')
mail.stop()
```

### Send Image Message \`
#### Attributes -> message*, subject*, to, path
```python
mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.image(path="hello.jpg", message="Hello World", subject='Simple Html Message', to='mail@to.recive')
mail.stop()
```

#### Note\` for send message from file you can use read_file method
### Example`
```python
mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.mail(message=mail.read_mail("Message.txt"), subject='Simple Html Message', to='mail@to.recive')
mail.stop()
```

## Read Mails\`

### Example num 1

```python

from mail import Reciver # only Reciver

# Load method Params`
# login => your email
# password => your password
# imap => imap server
r = Reciver("your@mail.login", 'yourmailpassword')

# Load method Params`
# folder => default "inbox" > folder from where load mails
# enc => default "(RFC822)" > encription of message ids
# count => defult 1 > messages to load
print(r.load())

```

### Example num 2

```python

from mail import Email

mail = Email("your@mail.login", 'yourmailpassword')

print(mail.reader.load())

```
### Example 3 - Download attachs
```python
from mail import Reciver

r = Reciver("mishamartun@mail.ru", 'M20042005')

for mail in r.load():
  print("="*100)
	print(mail['from'])
  print(mail['message'])
	for i in mail['attach']:
		r.download_attachment(*i)
```


## constructors

### EMail
#### Arguments -> login[str] -  password[str] - imap[tuple] - smtp[tuple] - reader[bool]

> load()
>> Arguments -> folder[str] - enc[str] - count[int]

> download_attachment()
>> Arguments -> part[obj] - content_disposition[obj] - folder[str]

### Reciver
#### Arguments -> login[str] -  password[str] - imap[tuple]

> read()
>> Arguments -> folder[str] - enc[str] - count[int]

> download()
>> Arguments -> part[obj] - content_disposition[obj] - folder[str]

> mail()
>> Arguments -> message[str], subject[str], to[str]

> image()
>> Arguments -> message[str], subject[str], to[str], path[str]

> bomb()
>> Arguments -> message[str], subject[str], to[str], count[int]

> html_message()
>> Arguments -> html[str], subject[str], to[str]

> read_file()
>> Arguments -> path[str] - encoding[str]

> stop()
>> Arguments -> [EMPTY]

