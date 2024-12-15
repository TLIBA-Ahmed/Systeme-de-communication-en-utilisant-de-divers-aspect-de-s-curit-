# rbac_utils.py
ROLES_PERMISSIONS = {
    "admin": ["decrypt"],  
    "user": []  
}

# Rôle de l'utilisateur actuel
current_user_role = "user"  

def has_permission(action):
    """
    Vérifie si l'utilisateur actuel a la permission d'effectuer une action donnée.
    """
    permissions = ROLES_PERMISSIONS.get(current_user_role, [])
    return action in permissions