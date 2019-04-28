import http.server
import socketserver
import termcolor
import requests

# Define the Server's port
PORT = 8000


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        if self.path.startswith('/main') or self.path == '/':
            filename = open('main_page.html', 'r')
            contents = filename.read()
        elif self.path.startswith('/listSpecies'):
            contents = """<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>List of species page</title>
                            </head>
                            <body>
                                <h1>LIST OF SPECIES</h1>
                                <p>WELCOME TO THE LIST OF SPECIES PAGE</p>
                                <p>If you prefer to see the whole list of species just click the send button</p>
                                <form action="listSpecies" method="get">
                                    Number of species  <input type="text" name="limit">
                                    <br>
                                    <input type="submit" value="SEND">
                                    <br><br>
                                </form>
                                <p></p>
                                <a href="main_page">MAIN page</a>
                            </body>
                            </html>"""
            if self.path.startswith('/listSpecies?limit='):

                server = "http://rest.ensembl.org"
                ext = "/info/species?"
                r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                information = r.json()
                species = information['species']
                msg_split = self.path.split('=')

                contents = """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>listSpecies</title>
                        </head>
                        <body>
                            <h1>LIST OF SPECIES</h1>
                            <p> """
                contents += 'Species: ''<p>'
                counter = 0
                for i in species:
                    contents += '<p>' + i['name'] + '<p>'
                    counter += 1
                    if str(counter) == msg_split[1]:
                        break

                contents += '<p>' + '\n' + '<p>'

                contents += """</p>
                                <a href="main_page">MAIN page</a>
    
                            </body>
                            </html>
                            """
        elif self.path.startswith('/karyotype'):
            contents = """<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Karyotype page</title>
                </head>
                <body>
                    <h1>KARYOTYPE</h1>
                    <p>WELCOME TO THE KARYOTYPE PAGE</p>
                    <form action="karyotype" method="get">
                        Species  <input type="text" name="species">
                        <br>
                        <input type="submit" value="SEND">
                        <br><br>
                        <br><br>
                    </form>
                    <p></p>
                    <a href="main_page">MAIN page</a>
                </body>
                </html>"""

            if self.path.startswith('/karyotype?species='):

                msg_split = self.path.split('=')
                server = "http://rest.ensembl.org"
                ext = "/info/assembly/{}?".format(msg_split[1])
                r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                information = r.json()
                karyotype = information['karyotype']
                contents = """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>karyotype</title>
                        </head>
                        <body>
                            <h1>KARYOTYPE</h1>
                            <p> """
                contents += 'The karyotype of ' + msg_split[1] + ' is: '
                for i in karyotype:
                    contents += i + ' '

                contents += """</p>
                                <a href="main_page">MAIN page</a>
    
                            </body>
                            </html>
                            """
        elif self.path.startswith('/chromosomeLength'):
            contents = """<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Chromosome length page</title>
                </head>
                <body>
                    <h1>CHROMOSOME LENGTH</h1>
                    <p>WELCOME TO THE CHROMOSOME LENGTH PAGE</p>
                    <form action="chromosomeLength" method="get">
                        Species  <input type="text" name="species">
                        <br>
                        <input type="submit" value="SEND">
                        <br><br>
                        Chromosome  <input type="text" name="chromo">
                        <br>
                        <input type="submit" value="SEND">
                        <br><br>
                        <br><br>
                    </form>
                    <p></p>
                    <a href="main_page">MAIN page</a>
                </body>
                </html>"""
            if self.path.startswith('/chromosomeLength?species='):
                msg_split = self.path.split('=')
                msg_split2 = []
                for i in msg_split:
                    msg_split2 += i.split('&')
                server = "http://rest.ensembl.org"
                ext = "/info/assembly/{}?".format(msg_split2[1])
                r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                information = r.json()
                chromo = msg_split2[3]
                for i in information['top_level_region']:
                    if chromo == i['name']:
                        length = i['length']
                contents = """
                                        <!DOCTYPE html>
                                        <html lang="en">
                                        <head>
                                            <meta charset="UTF-8">
                                            <title>Chromosome length page</title>
                                        </head>
                                        <body>
                                            <h1>CHROMOSOME LENGTH PAGE</h1>
                                            <p> """
                contents += 'The length of the chromosome ' + chromo
                contents += ' from the species ' + msg_split2[1] + ' is ' + str(length)

                contents += """</p>
                                                <a href="main_page">MAIN page</a>

                                            </body>
                                            </html>
                                            """

        else:
            filename = open('error.html', 'r')
            contents = filename.read()

        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header("Content-Type", "text/html\r\n")

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")