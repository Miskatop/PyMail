# PyMail - mail client by python

## Requirements\`
```
email 4.0+
```
## Usage\`

### Send Simple Message\`
```python

mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.mail(message="Hello", subject='Simple Html Message', to='mail@to.recive')
mail.stop()

```

### Send Message Bomber (many messages) \`
```python
mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.bomb(message="Hello", subject='Simple Html Message', to='mail@to.recive', count=10) # count message recive the client
mail.stop()
```

### Send html Bomber \`
```python
mail = EMail(login='your@mail.login', password='yourmailpassword')
mail.html(html="<h1>Hello</h1>", subject='Simple Html Message', to='mail@to.recive')
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
