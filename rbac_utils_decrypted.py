# rbac_utils.py
ROLES_PERMISSIONS = {
    "admin": ["decrypt", "view_history"],
    "user": ["view_history"],
    "guest": []
}

# Rôle de l'utilisateur actuel
current_user_role = "admin"  

def has_permission(action):
    permissions = ROLES_PERMISSIONS.get(current_user_role, [])
    return action in permissions