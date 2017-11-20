# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dictWebServer import app
app.run(debug=True)