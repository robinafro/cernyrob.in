# import http.server
# import socketserver
from captcha.image import ImageCaptcha
import random
import string
# from io import BytesIO

# PORT = 8002

def gen_captcha():
    # Generate CAPTCHA
    text = random_string()
    image = ImageCaptcha(width=280, height=90)
    data = image.generate(text)

    return data.getvalue(), text

# Function to generate a random string
def random_string(length=6):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

# class MyServer(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/captcha':
#             # Generate CAPTCHA
#             text = random_string()
#             image = ImageCaptcha(width=280, height=90)
#             data = image.generate(text)
#             # Store the solution temporarily
#             self.server.captcha_solution = text

#             # Set headers
#             self.send_response(200)
#             self.send_header('Content-type', 'image/png')
#             self.end_headers()

#             # Send image data
#             self.wfile.write(data.getvalue())

#         elif self.path == '/solution':
#             # Send the solution
#             solution = getattr(self.server, 'captcha_solution', 'Unknown')
#             self.send_response(200)
#             self.send_header('Content-type', 'text/plain')
#             self.end_headers()
#             self.wfile.write(solution.encode())

#         else:
#             # Handle other requests
#             super().do_GET()

# # Start the server
# with socketserver.TCPServer(("", PORT), MyServer) as httpd:
#     print("shit running", PORT)
#     httpd.serve_forever()

