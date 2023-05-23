# Framework Twisted
# ==========================================================

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
import sqlite3

# Conectare la baza de date
# conn = sqlite3.connect('reteleProiect.db')
# c = conn.cursor()

class HomePage(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader(b"content-type", b"text/plain")
        return b"Hello, World!"


class StudentiPage(resource.Resource):
    def render_GET(self, request):
        conn = sqlite3.connect('reteleProiect.db')
        c = conn.cursor()
        c.execute("SELECT * FROM STUDENTI")
        rows = c.fetchall()
        c.close()
        conn.close()
        html = b"<html><body>"
        html += b"<h1>Lista de studenti</h1>"
        html += b"<ul>"
        for row in rows:
            html += "<li>{} - {}</li>".format(row[0], row[1]).encode()
        html += b"</ul>"
        # html += b"<h2>Stergere student</h2>"
        # html += b'<form method="POST">'
        # html += b'ID student:<br>'
        # html += b'<input type="text" name="id"><br><br>'
        # html += b'<input type="submit" value="Sterge">'
        # html += b'</form>'
        html += b'<br><a href="/addStudent"><button>Adaugare student</button></a></br>'
        html += b'<br><a href="/deleteStudent"><button>Sterge student</button></a>'
        html += b"</body></html>"
        return html

    def render_POST(self, request):
        conn = sqlite3.connect('reteleProiect.db')
        c = conn.cursor()
        student_id = request.args[b"id"][0].decode("utf-8")
        c.execute("DELETE FROM STUDENTI WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        return self.render_GET(request)

class AddStudentPage(resource.Resource):
    def render_GET(self, request):
        html = b"<html><body>"
        html += b"<h1>Adaugare student</h1>"
        html += b'<form method="POST">'
        html += b'ID student:<br>'
        html += b'<input type="text" name="id"><br><br>'
        html += b'NUME student:<br>'
        html += b'<input type="text" name="name"><br><br>'
        html += b'<input type="submit" value="Adauga">'
        html += b'</form>'
        html += b"</body></html>"
        return html

    def render_POST(self, request):
        student_id = request.args[b"id"][0].decode("utf-8")
        student_name = request.args[b"name"][0].decode("utf-8")
        conn = sqlite3.connect("reteleProiect.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO STUDENTI (id, nume) VALUES (?, ?)", (student_id, student_name))
        conn.commit()
        conn.close()
        html = b"<html><body>"
        html += b"<h1>Student adaugat</h1>"
        html += b"</body></html>"
        return html

class DeleteStudentPage(resource.Resource):
    def render_GET(self, request):
        html = b"<html><body>"
        html += b"<h1>Stergere student</h1>"
        html += b'<form method="POST">'
        html += b'ID student:<br>'
        html += b'<input type="text" name="id"><br><br>'
        html += b'<input type="submit" value="Sterge">'
        html += b'</form>'
        html += b"</body></html>"
        return html

    def render_POST(self, request):
        student_id = request.args[b"id"][0].decode("utf-8")
        conn = sqlite3.connect("reteleProiect.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM STUDENTI WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        html = b"<html><body>"
        html += b"<h1>Student sters</h1>"
        html += b"</body></html>"
        return html


root = resource.Resource()
root.putChild(b"", HomePage())
root.putChild(b"studenti", StudentiPage())
root.putChild(b"deleteStudent", DeleteStudentPage())
root.putChild(b"addStudent", AddStudentPage())

endpoints.serverFromString(reactor, "tcp:8888").listen(server.Site(root))
print("Serverul ruleaza...")
reactor.run()