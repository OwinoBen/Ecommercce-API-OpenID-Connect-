import random
import string
import base64
import hashlib

code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code.encode('utf-8'))

code_c = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_c).decode('utf-8').replace('=', '')

