from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
import requests
from services.order_service import OrderService

class OrderController:
    def __init__(self):
        self.order_service = OrderService()
    
    def get_products_from_service(self):
        """Busca produtos do product-service"""
        try:
            response = requests.get("http://localhost:5003/product/api/products")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return []

    def get_categories_from_service(self):
        """Busca categorias do product-service"""
        try:
            response = requests.get("http://localhost:5003/product/api/categories")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []

    def create_order(self):
        """Página para criar um novo pedido"""
        if request.method == "POST":
            data = request.form
            user_email = data.get("user_email")
            
            # Processa os itens do pedido
            items = []
            total = 0.0
            
            # Exemplo simples - você pode expandir isso
            item_names = request.form.getlist("item_name")
            item_quantities = request.form.getlist("item_quantity")
            item_prices = request.form.getlist("item_price")
            
            for name, qty, price in zip(item_names, item_quantities, item_prices):
                if name and qty and price:
                    quantity = int(qty)
                    unit_price = float(price)
                    item_total = quantity * unit_price
                    
                    items.append({
                        "name": name,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total": item_total
                    })
                    total += item_total
            
            if not items:
                flash("Adicione pelo menos um item ao pedido", "error")
                return redirect(url_for("order.create"))
            
            response, status = self.order_service.create_order(user_email, items, total)
            
            if status == 201:
                flash("Pedido criado com sucesso!", "success")
                return redirect(url_for("order.list_orders"))
            elif status == 404:
                flash(response.get("error", "Usuário não encontrado"), "error")
                return redirect(url_for("order.create"))
            else:
                flash(response.get("error", "Erro ao criar pedido"), "error")
                return redirect(url_for("order.create"))
        
        # Get all users for reference in the form
        users = self.order_service.get_all_users()
        
        # Get products from product service
        products = self.get_products_from_service()
        categories = self.get_categories_from_service()
        
        return render_template("create_order.html", users=users, products=products, categories=categories)

    def list_all_orders(self):
        """Lista todos os pedidos"""
        orders = self.order_service.get_all_orders()
        return render_template("order_list.html", orders=orders)

    def get_order_details(self, order_id):
        """Exibe detalhes de um pedido específico"""
        order = self.order_service.get_order_by_id(order_id)
        if not order:
            flash("Pedido não encontrado", "error")
            return redirect(url_for("order.list_orders"))
        return render_template("order_details.html", order=order)

    def get_user_orders(self, user_email):
        """Lista pedidos de um usuário específico"""
        orders = self.order_service.get_orders_by_user(user_email)
        return render_template("order_list.html", orders=orders, user_email=user_email)

    def update_order_status(self, order_id):
        """Atualiza o status de um pedido"""
        if request.method == "POST":
            new_status = request.form.get("status")
            response, status = self.order_service.update_order_status(order_id, new_status)
            
            if status == 200:
                flash("Status do pedido atualizado com sucesso!", "success")
            else:
                flash(response.get("error", "Erro ao atualizar status"), "error")
        
        return redirect(url_for("order.order_details", order_id=order_id))

    def delete_order(self, order_id):
        """Deleta um pedido"""
        response, status = self.order_service.delete_order(order_id)
        
        if status == 200:
            flash("Pedido deletado com sucesso!", "success")
        else:
            flash(response.get("error", "Erro ao deletar pedido"), "error")
        
        return redirect(url_for("order.list_orders"))

# Criação do blueprint e instância do controller
order_controller = OrderController()
order_bp = Blueprint("order", __name__)

@order_bp.route("/create", methods=["GET", "POST"])
def create():
    return order_controller.create_order()

@order_bp.route("/list")
def list_orders():
    return order_controller.list_all_orders()

@order_bp.route("/details/<order_id>")
def order_details(order_id):
    return order_controller.get_order_details(order_id)

@order_bp.route("/user/<user_email>")
def user_orders(user_email):
    return order_controller.get_user_orders(user_email)

@order_bp.route("/update_status/<order_id>", methods=["POST"])
def update_status(order_id):
    return order_controller.update_order_status(order_id)

@order_bp.route("/delete/<order_id>", methods=["POST"])
def delete(order_id):
    return order_controller.delete_order(order_id)
