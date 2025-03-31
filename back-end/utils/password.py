import bcrypt

class CryptographyUtil:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Criptografa a senha usando bcrypt.
        
        Args:
            password (str): Senha em texto plano
        
        Returns:
            str: Senha criptografada
        """
        # 📌 Gera um salt e hasheia a senha
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha em texto plano corresponde ao hash.
        
        Args:
            plain_password (str): Senha em texto plano
            hashed_password (str): Senha hashada
        
        Returns:
            bool: True se a senha está correta, False caso contrário
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )