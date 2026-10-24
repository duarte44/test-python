from flask import Blueprint, request, render_template, redirect, url_for, flash
from services.user_service import UserService

class UserController:
    def __init__(self):
        self.user_service = UserService()
    
    def create(self):
        """Cria um novo usuário"""
        if request.method == "POST":
            data = request.form
            response, status = self.user_service.create_user(
                email=data["email"],
                password=data["password"],
                name=data["name"],
                address=data["address"],
                role=data.get("role", "cliente")
            )
            if status != 201:
                flash(response["error"])
                return redirect(url_for("user.create"))
            flash("Usuário criado com sucesso! Faça login para continuar.")
            # Redirect to auth-service login after successful registration
            return redirect("http://localhost:5000/auth/login")
        return render_template("create.html")
    
    def profile(self, email):
        """Exibe o perfil do usuário"""
        user = self.user_service.get_user_by_email(email)
        if not user:
            return "Usuário não encontrado", 404
        return render_template("profile.html", user=user)
    
    def edit(self, email):
        """Edita os dados do usuário"""
        user = self.user_service.get_user_by_email(email)
        if not user:
            flash("Usuário não encontrado")
            return redirect(url_for("user.create"))
        
        if request.method == "POST":
            name = request.form["name"]
            address = request.form["address"]
            response, status = self.user_service.update_user(email, name, address)
            
            if status == 200:
                flash("Perfil atualizado com sucesso.")
                return redirect(url_for("user.profile", email=email))
            else:
                flash(response.get("error", "Erro ao atualizar perfil"))
        
        return render_template("edit.html", user=user)
    
    def delete(self, email):
        """Remove um usuário"""
        response, status = self.user_service.delete_user(email)
        
        if status == 200:
            flash("Usuário excluído com sucesso.")
        else:
            flash(response.get("error", "Erro ao excluir usuário"))
        
        return redirect(url_for("user.create"))

# Criação do blueprint e instância do controller
user_controller = UserController()
user_bp = Blueprint("user", __name__)

@user_bp.route("/create", methods=["GET", "POST"])
def create():
    return user_controller.create()

@user_bp.route("/profile/<email>")
def profile(email):
    return user_controller.profile(email)

@user_bp.route("/edit/<email>", methods=["GET", "POST"])
def edit(email):
    return user_controller.edit(email)

@user_bp.route("/delete/<email>", methods=["POST"])
def delete(email):
    return user_controller.delete(email)
