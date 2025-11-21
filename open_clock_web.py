import webbrowser
import pathlib

p = pathlib.Path(__file__).parent / 'clock_web.html'
webbrowser.open(p.as_uri())
print('Opened', p)
