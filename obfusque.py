import base64

# Code obfusque
obfuscated_code = """IyByYmFjX3V0aWxzLnB5ClJPTEVTX1BFUk1JU1NJT05TID0gewogICAgImFkbWluIjogWyJkZWNyeXB0Il0sICAjIFNldWxzIGxlcyBhZG1pbnMgcGV1dmVudCBkw4PCqWNyeXB0ZXIKICAgICJ1c2VyIjogW10gICMgTGVzIHV0aWxpc2F0ZXVycyBuJ29udCBwYXMgY2V0dGUgcGVybWlzc2lvbgp9CgojIFLDg8K0bGUgZGUgbCd1dGlsaXNhdGV1ciBhY3R1ZWwKY3VycmVudF91c2VyX3JvbGUgPSAiYWRtaW4iICAjIENoYW5nZXogZW4gInVzZXIiIHBvdXIgdGVzdGVyIGxlIGNhcyBzYW5zIHBlcm1pc3Npb24KCmRlZiBoYXNfcGVybWlzc2lvbihhY3Rpb24pOgogICAgIiIiCiAgICBWw4PCqXJpZmllIHNpIGwndXRpbGlzYXRldXIgYWN0dWVsIGEgbGEgcGVybWlzc2lvbiBkJ2VmZmVjdHVlciB1bmUgYWN0aW9uIGRvbm7Dg8KpZS4KICAgICIiIgogICAgcGVybWlzc2lvbnMgPSBST0xFU19QRVJNSVNTSU9OUy5nZXQoY3VycmVudF91c2VyX3JvbGUsIFtdKQogICAgcmV0dXJuIGFjdGlvbiBpbiBwZXJtaXNzaW9ucw=="""

decoded_code = base64.b64decode(obfuscated_code).decode()
with open("rbac_utils_decrypted.py", "w") as output_file:
    output_file.write(decoded_code)

print("Le fichier deobfusque a ete genere : rbac_utils_decrypted.py")
