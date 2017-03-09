# @author Alexander Harris
# @version February/March 2016
# Network Programming
# Homework 6 : SMTP Client with TLS

# This script requires a Gmail account, and the account
# must be set to allow access from "less secure apps"
# This can be found in the settings for your Gmail account.
# https://www.google.com/settings/security/lesssecureapps

# These are the only modules you will need to import for
# this exercise.
from socket import *
import ssl
import base64

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = 'smtp.gmail.com'
mailServerPort = 587

# Create an ordinary TCP socket called clientSocket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establish connection with mailServer
clientSocket.connect((mailServer, mailServerPort))
print('Connecting')

# Recieve the response from the server. Print out the response
# message, and check to make sure the status code is the expected
# value of 220. If not, print out a message. The data comes in
# as bytes, so .decode() is necessary to convert it to ASCII text.
recv = clientSocket.recv(2048).decode()
print(recv)
if recv[:3] != '220':
     print('220 reply not received from server.')

# Send the initial HELO greeting. Note that strings are
# passed to the socket using the 'b' quotation format, which
# represents byte sequences. You could also use .encode(), but
# the 'b' notation is more concise.
clientSocket.send(b'HELO gmail.com\r\n')
print('Sending: HELO gmail.com')

# Recieve the response from the server. Print out the response
# message, and check to make sure the status code is the expected value of 250.
recv = clientSocket.recv(2048).decode()
print('Received message from server : ', recv)

# split the Received message by a delimiter of a space...
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 250):
    print("HELO fail, status should be 250 and is %s" % received_arr[0])

# Now we want to convert the insecure connection to a secure connection
# using "Opportunistic Transport Layer Security"
# https://en.wikipedia.org/wiki/Opportunistic_TLS
# The SMTP protocol is extended to enable Opportunistic TLS with the
# STARTTLS command. Now's where you should send that command. Also,
# a message to your own terminal telling you that it's sending.
command = 'STARTTLS\r\n'
clientSocket.send(command.encode())
print('Sending : STARTTLS')

# Recieve the response from the server. Print out the response
# message, and check to make sure the status code is the expected
# value of 220. If not, print out a message.
recv = clientSocket.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 220):
    print("STARTTLS fail, status should be 220 and is %s" % received_arr[0])

# Now it's time to wrap the socket in the SSL (secure socket layer)
# https://docs.python.org/3/library/ssl.html#socket-creation
clientSocketSSL =  ssl.wrap_socket(clientSocket)
print('SSL wrapper')

# Tell the server you want to log in
clientSocketSSL.send(b'AUTH login\r\n')
print('Sending: AUTH login')

# Recieve the response from the server. Print out the response
# message, and check to make sure the status code is the expected
# value of 334. If not, print out a message.
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 334):
    print("AUTH login fail, status should be 334 and is %s" % received_arr[0])

# Grab the user name from the terminal, so as not to
# have to hard code it into the script. Use the
# Python input() function to give a prompt. Be sure to
# encode the resulting string as bytes.
print('Enter username...')
username = input()

# Send username to the server in Base64 encoding
# https://docs.python.org/3.1/library/base64.html
clientSocketSSL.send(base64.b64encode(username.encode()))
clientSocketSSL.send(b'\r\n')
print('\nSending: Username')

# Recieve the response from the server. Print out the response
# message, and check to make sure the status code is the expected
# value of 334. If not, print out a message.
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 334):
    print("username fail, status should be 334 and is %s" % received_arr[0])

# Grab the password from the terminal and send it
# to the server in Base64 encoding.
print('Enter password...')
pw = input()
clientSocketSSL.send(base64.b64encode(pw.encode()))
clientSocketSSL.send(b'\r\n')
print('\nSending: Password')

# Recieve the response from the server. Print out the response
# message, and check to make sure the status code is the expected
# value of 235. If not, print out a message.
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 235):
    print("pw fail, status should be 235 and is %s" % received_arr[0])

# Now that we're authenticated in TLS, we need to start the
# SMTP protocol from the beginning again, with HELO.
# The rest proceeds as in the ordinary (non-secure) SMTP case.

# At each stage, be sure to print what you're doing to your
# own terminal, so you can see how your program is executing.
# Print out the response messages and confirm the expected
# status codes.

# Send HELO greeting and expect 250 status response
clientSocketSSL.send(b'HELO gmail.com\n')
print('Sending: HELO gmail.com')

# receive response
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 250):
    print("HELO fail, status should be 250 and is %s" % received_arr[0])

# Send MAIL FROM: and expect 250 status response
mail_from = b'MAIL FROM: <nakomurosantoshi@gmail.com> \r\n'
clientSocketSSL.send(mail_from)
print('Sending: MAIL FROM:')

# receive response
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 250):
    print("MAIL FROM: fail, status should be 250 and is %s" % received_arr[0])

# Send RECPT TO: and expect 250 status response
recpt_to = b'RCPT TO: <nakomurosantoshi@gmail.com> \r\n'
clientSocketSSL.send(recpt_to)
print('Sending: RCPT TO:')

# receive response
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 250):
    print("RCPT TO: fail, status should be 250 and is %s" % received_arr[0])

# Send RECPT TO: and expect 250 status response
recpt_to = b'RCPT TO: <alexanderbharris@gmail.com> \r\n'
clientSocketSSL.send(recpt_to)
print('Sending: RECPT TO:')

# receive response
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 250):
    print("RECPT TO: fail, status should be 250 and is %s" % received_arr[0])

# Send the DATA command, 354
data = b'DATA\r\n'
clientSocketSSL.send(data)
print('Sending: DATA')
recv = clientSocketSSL.recv(2048).decode()
print('Received message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 354):
    print("RECPT TO: fail, status should be 354 and is %s" % received_arr[0])

# Now we're sending the actual mail data, and things get
# a bit more complicated. Read about multipart content types here:
# https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html

# Because we want both text and an image in the mail, the mail
# needs to be multipart, and will need to make use of MIME encoding
# https://www.w3.org/Protocols/rfc1341/0_TableOfContents.html

# Send the header first. It should include the 'Subject' field
# The 'MIME-Version' field (with the value 1.0)
# and the 'Content-type' field. Read the documentation above to
# learn what value this should have for an email with text and
# an image. Also, you'll need to set the boundary string value here,
# which will be used to separate the first part of the mail (the text
# part) from the second part of the mail (the image part)
boundary = '~~~~~~~~'
builder = 'Subject: Network Programming HW-6\n' + \
            'MIME-Version: 1.0\n' + \
            'Content-type: multipart/mixed; boundary="'+boundary+'"\r\n'
clientSocketSSL.send(builder.encode())
print('Sending: Header')

# https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
# Send the first part of the email. This will start with the
# boundary string, prefixed by --. There's an extra carriage
# return/line feed after the boundary string and before the
# message content. Because this part is only text, no additional
# headers are needed.
content = '"Yet, even amidst the hatred and carnage, life is still worth living. It is possible for wonderful encounters and beautiful things to exist." — Hayao Miyazaki'
msg = '--'+boundary+'\r\n'+content
clientSocketSSL.send(msg.encode())
print('Sending: Message')

# Send the second part of the multipart mail. This is where
# the image part gets sent. Once again, you'll need the
# boundary string to distinguish the part. In this case,
# though, you'll also need some headers. Specifically, you'll
# need the 'Content-type' header and the 'Content-Transfer-Encoding' header.
# https://www.w3.org/Protocols/rfc1341/4_Content-Type.html
# https://www.w3.org/Protocols/rfc1341/5_Content-Transfer-Encoding.html

# For 'Content-type', you'll need to set the value so that the image
# is correctly interpreted as a JPEG image. This is also where you can
# set its name. Set the name to be "shark.jpg".
# for 'Content-Transfer-Encoding', you'll want to set it so that the
# image is read as Base64 encoding. Encoding the image in this way will
# ensure that it doesn't get corrupted.

# Be sure to send an extra carriage return/line feed at the end of the headers.
msg = '\r\n--'+boundary+'\r\nContent-Transfer-Encoding: base64\r\nContent-type: image/jpeg; name=shark.jpg\r\n'

clientSocketSSL.send(msg.encode())
print('Sending: Header')

# Finally time to load the image. First you've got to load it.
# The image shark.jpg should be in the same directory as this
# script. Use Python's open() function set to read in binary,
# then call .read() on the resulting object. Once you've done that
# close the file with .close().
fi = open('shark.jpg', 'br')
img = fi.read()
fi.close()

# And now send the image, encoded in Base64
clientSocketSSL.send(base64.b64encode(img))
print('Sending: Image')

# And end the message. First conclude the multipart mail
# with the boundary string prefixed with -- and suffixed with
# --. Then end the transmission with <CRLF>.<CRLF>
msg = '\r\n--'+boundary+'--'+'\r\n.\r\n'
clientSocketSSL.send(msg.encode())
print('Sending: Boundary')

# Expect 250 status response
recv = clientSocketSSL.recv(2048).decode()
print('\nReceived message from server : ', recv)
received_arr = recv.split(" ")
# next, cast the 0th index of the Received message to an int, and compare it to 250
if (int(received_arr[0]) != 250):
    print("body fail, status should be 250 and is %s" % received_arr[0])
else : print('Message Successfully Sent')
# Send the QUIT command, and expect 250 status response
quit = 'QUIT\r\n'
