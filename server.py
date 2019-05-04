import http.server
import socketserver
import termcolor
import requests
from seq import Seq

# Define the Server's port
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # Print the request line
        termcolor.cprint(self.requestline, 'green')
        try:

            if self.path == '/main_page' or self.path == '/':
                filename = open('main_page.html', 'r')
                contents = filename.read()
    # List the names of all the species available in the database.
            elif self.path.startswith('/listSpecies'):
                server = "http://rest.ensembl.org"
                ext = "/info/species?"
                r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                information = r.json()
                species = information['species']
                contents = """<!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>List of species page</title>
                                </head>
                                <body>
                                    <h1>LIST OF SPECIES</h1>
                                    <p>WELCOME TO THE LIST OF SPECIES PAGE</p>
                                    <p>If you prefer to see a limited amount of species </p>
                                    <form action="listSpecies" method="get">
                                        Number of species  <input type="text" name="limit">
                                        <br>
                                        <input type="submit" value="SEND">
                                        <br><br>
                                    </form>"""
                contents += 'Species: ''<p>'
                for i in species:
                    contents += '<p>' + i['name'] + '<p>'
                contents += """<p></p>
                                    <a href="main_page">MAIN page</a>
                                </body>
                                </html>"""
                if self.path.startswith('/listSpecies?limit='):

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
    # Return information about the karyotype of a specie: The name (usually a number) of all the chromosomes
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
                            Species  <input type="text" name="specie">
                            <br>
                            <input type="submit" value="SEND">
                            <br><br>
                            <br><br>
                        </form>
                        <p></p>
                        <a href="main_page">MAIN page</a>
                    </body>
                    </html>"""

                if self.path.startswith('/karyotype?specie='):

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
    # Return the Length of the chromosome named "chromo" of the given specie
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
                            Species  <input type="text" name="specie">
                            <br>
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
                if self.path.startswith('/chromosomeLength?specie='):
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
    # MEDIUM LEVEL
    # Return the sequence of a given human gene
            elif self.path.startswith('/geneSeq'):
                contents = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Gene sequence page</title>
                    </head>
                    <body>
                        <h1>GENE SEQUENCE</h1>
                        <p>WELCOME TO THE GENE SEQUENCE PAGE</p>
                        <form action="geneSeq" method="get">
                            Human gene  <input type="text" name="gene">
                            <br>
                            <input type="submit" value="SEND">
                            <br><br>
                            <br><br>
                        </form>
                        <p></p>
                        <a href="main_page">MAIN page</a>
                    </body>
                    </html>"""

                if self.path.startswith('/geneSeq?gene='):
                    msg_split = self.path.split('=')
                    server = "http://rest.ensembl.org"
                    ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])
                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                    info = r.json()
                    if msg_split[1] == info['display_name']:
                        identification = info['id']

                    server = "http://rest.ensembl.org"
                    ext = "/sequence/id/{}?".format(identification)
                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                    info = r.json()
                    gene_sequence = info['seq']

                    contents = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>Gene sequence page</title>
                            </head>
                            <body>
                                <h1>GENE SEQUENCE</h1>
                                <p> """
                    contents += 'The sequence of the human gene ' + msg_split[1] + ' is ' + gene_sequence
                    contents += """</p>
                                    <a href="main_page">MAIN page</a>
    
                                </body>
                                </html>
                                """
    # Return information about a human gene: start, end, Length, id and Chromosome
            elif self.path.startswith('/geneInfo'):
                contents = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Gene information page</title>
                    </head>
                    <body>
                        <h1>GENE INFO</h1>
                        <p>WELCOME TO THE GENE INFO PAGE</p>
                        <form action="geneInfo" method="get">
                            Human gene  <input type="text" name="gene">
                            <br>
                            <input type="submit" value="SEND">
                            <br><br>
                            <br><br>
                        </form>
                        <p></p>
                        <a href="main_page">MAIN page</a>
                    </body>
                    </html>"""

                if self.path.startswith('/geneInfo?gene='):

                    msg_split = self.path.split('=')
                    server = "http://rest.ensembl.org"
                    ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])
                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                    info = r.json()
                    if msg_split[1] == info['display_name']:
                        identification = info['id']

                    server = "http://rest.ensembl.org"
                    ext = "/lookup/id/{}?".format(identification)

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    infor = r.json()
                    start = infor['start']
                    end = infor['end']
                    id = infor['id']
                    chromo = infor['seq_region_name']

                    contents = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>Gene information page</title>
                            </head>
                            <body>
                                <h1>GENE INFO</h1>
                                <p> """
                    contents += 'The start of the human gene ' + msg_split[1] + ' is ' + str(start)
                    contents += '</p></p>'
                    contents += 'The end of the human gene ' + msg_split[1] + ' is ' + str(end)
                    contents += '</p></p>'
                    contents += 'The id of the human gene ' + msg_split[1] + ' is ' + str(id)
                    contents += '</p></p>'
                    contents += 'The chromosome of the human gene ' + msg_split[1] + ' is ' + str(chromo)
                    contents += """</p>
                                    <a href="main_page">MAIN page</a>
    
                                </body>
                                </html>
                                """
    # Performs some calculations on the given human gene and returns the total length and the percentage of all its bases
            elif self.path.startswith('/geneCalc'):
                contents = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Gene calculations page</title>
                    </head>
                    <body>
                        <h1>GENE CALCULATIONS</h1>
                        <p>WELCOME TO THE GENE CALCULATIONS PAGE</p>
                        <form action="geneCalc" method="get">
                            Human gene  <input type="text" name="gene">
                            <br>
                            <input type="submit" value="SEND">
                            <br><br>
                            <br><br>
                        </form>
                        <p></p>
                        <a href="main_page">MAIN page</a>
                    </body>
                    </html>"""

                if self.path.startswith('/geneCalc?gene='):

                    msg_split = self.path.split('=')
                    server = "http://rest.ensembl.org"
                    ext = "/lookup/symbol/homo_sapiens/{}?".format(msg_split[1])
                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                    info = r.json()
                    if msg_split[1] == info['display_name']:
                        identification = info['id']

                    server = "http://rest.ensembl.org"
                    ext = "/sequence/id/{}?".format(identification)
                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                    info = r.json()
                    gene_sequence = info['seq']
                    sequence = Seq(gene_sequence)
                    l1 = str(sequence.len())
                    percentage = sequence.perc_bases()
                    na = str(percentage['As'])
                    nt = str(percentage['Ts'])
                    ng = str(percentage['Gs'])
                    nc = str(percentage['Cs'])

                    contents = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>Gene information page</title>
                            </head>
                            <body>
                                <h1>GENE INFO</h1>
                                <p> """
                    contents += 'The length of the sequence of the human gene ' + msg_split[1] + ' is ' + l1
                    contents += '</p></p>'
                    contents += 'The percentage of As in the sequence of the human gene ' + msg_split[1] + ' is ' + na + '%'
                    contents += '</p></p>'
                    contents += 'The percentage of Ts in the sequence of the human gene ' + msg_split[1] + ' is ' + nt + '%'
                    contents += '</p></p>'
                    contents += 'The percentage of Gs in the sequence of the human gene ' + msg_split[1] + ' is ' + ng + '%'
                    contents += '</p></p>'
                    contents += 'The percentage of Cs in the sequence of the human gene ' + msg_split[1] + ' is ' + nc + '%'

                    contents += """</p>
                                    <a href="main_page">MAIN page</a>
    
                                </body>
                                </html>
                                """
    # Return the names of the genes located in the chromosome "chromo" from the start to end positions
            elif self.path.startswith('/geneList'):
                contents = """<!DOCTYPE html>
                           <html lang="en">
                           <head>
                               <meta charset="UTF-8">
                               <title>Gene List page</title>
                           </head>
                           <body>
                               <h1>GENE LIST</h1>
                               <p>WELCOME TO THE GENE LIST PAGE</p>
                               <form action="geneList" method="get">
                                   Human chromosome  <input type="text" name="chromo">
                                   <br>
                                   Start  <input type="text" name="start">
                                   <br>
                                   End  <input type="text" name="end">
                                   <br>
                                   <input type="submit" value="SEND">
                                   <br><br>
                                   <br><br>
                               </form>
                               <p></p>
                               <a href="main_page">MAIN page</a>
                           </body>
                           </html>"""

                if self.path.startswith('/geneList?chromo='):
                    msg_split = self.path.split('=')
                    msg_split2 = []
                    for i in msg_split:
                        msg_split2 += i.split('&')

                    server = "http://rest.ensembl.org"
                    ext = "/overlap/region/human/" + str(msg_split2[1]) + ":" + msg_split2[3] + "-" + msg_split2[5] + "?feature=gene;feature=transcript;feature=cds;feature=exon"
                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
                    inform = r.json()

                    contents = """
                                   <!DOCTYPE html>
                                   <html lang="en">
                                   <head>
                                       <meta charset="UTF-8">
                                       <title>Gene sequence page</title>
                                   </head>
                                   <body>
                                       <h1>GENE SEQUENCE</h1>
                                       <p> """
                    contents += 'The genes (ID) in the chromosome ' + msg_split2[1] + ' of the homo sapiens '
                    contents += ' between ' + msg_split2[3] + ' and ' + msg_split2[5] + ' are: '
                    for i in inform:
                        contents += '<p>' + i['id'] + '<p>'
                    contents += """</p>
                                           <a href="main_page">MAIN page</a>
    
                                       </body>
                                       </html>
                                       """
    # Error html
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
        except KeyError:
            filename = open('error.html', 'r')
            contents = filename.read()

            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:
            self.send_header("Content-Type", "text/html\r\n")

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))

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
