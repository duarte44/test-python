from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from models.user_model import UserModel

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        self.user_model = UserModel()
    
    def login_page(self):
        """Exibe a página de login"""
        return render_template("login.html")
    
    def login(self):
        """Processa o login do usuário"""
        data = request.form
        user = self.auth_service.login_user(data["email"], data["password"])
        if not user:
            flash("Credenciais inválidas")
            return redirect(url_for("auth.login_page"))
        
        session["user"] = self.user_model.serialize(user)
        return redirect(url_for("auth.dashboard"))
    
    def register_page(self):
        """Redireciona para o serviço de usuário para criação de conta"""
        return redirect("http://localhost:5001/user/create")
    
    def dashboard(self):
        """Exibe o dashboard do usuário"""
        user = session.get("user")
        if not user:
            return redirect(url_for("auth.login_page"))
        return render_template("dashboard.html", user=user)
    
    def logout(self):
        """Realiza logout do usuário"""
        session.pop("user", None)
        return redirect(url_for("auth.login_page"))

# Criação do blueprint e instância do controller
auth_controller = AuthController()
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return auth_controller.login_page()

@auth_bp.route("/login", methods=["POST"])
def login():
    return auth_controller.login()

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return auth_controller.register_page()

@auth_bp.route("/dashboard")
def dashboard():
    return auth_controller.dashboard()

@auth_bp.route("/logout")
def logout():
    return auth_controller.logout()
