from datetime import datetime

html = f"""
<!DOCTYPE html>
<html>
<body>

<h1>Radar Logística & Intralogística</h1>

<p>
Última atualização:
{datetime.now()}
</p>

<h2>TESTE OK</h2>

</body>
</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print("Teste concluído")
