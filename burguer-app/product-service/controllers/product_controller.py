from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from services.product_service import ProductService

class ProductController:
    def __init__(self):
        self.product_service = ProductService()
        # Initialize products on controller creation
        self.product_service.initialize_products()
    
    def list_products(self):
        """Lista todos os produtos disponíveis"""
        products = self.product_service.get_available_products()
        categories = self.product_service.get_categories()
        category_filter = request.args.get('category')
        
        if category_filter:
            products = self.product_service.get_products_by_category(category_filter)
        
        return render_template("product_list.html", products=products, categories=categories, selected_category=category_filter)
    
    def admin_products(self):
        """Lista todos os produtos para administração"""
        products = self.product_service.get_all_products()
        categories = self.product_service.get_categories()
        return render_template("admin_products.html", products=products, categories=categories)
    
    def create_product(self):
        """Cria um novo produto"""
        if request.method == "POST":
            data = request.form
            ingredients = [ing.strip() for ing in data["ingredients"].split(",") if ing.strip()]
            available = data.get("available") == "on"
            
            response, status = self.product_service.create_product(
                name=data["name"],
                description=data["description"],
                category=data["category"],
                price=data["price"],
                ingredients=ingredients,
                available=available
            )
            
            if status != 201:
                flash(response["error"])
                return redirect(url_for("product.create"))
            
            flash("Produto criado com sucesso!")
            return redirect(url_for("product.admin_products"))
        
        categories = self.product_service.get_categories()
        return render_template("create_product.html", categories=categories)
    
    def edit_product(self, product_id):
        """Edita um produto existente"""
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            flash("Produto não encontrado.")
            return redirect(url_for("product.admin_products"))
        
        if request.method == "POST":
            data = request.form
            ingredients = [ing.strip() for ing in data["ingredients"].split(",") if ing.strip()]
            available = data.get("available") == "on"
            
            response, status = self.product_service.update_product(
                product_id=product_id,
                name=data["name"],
                description=data["description"],
                category=data["category"],
                price=data["price"],
                ingredients=ingredients,
                available=available
            )
            
            if status == 200:
                flash("Produto atualizado com sucesso!")
            else:
                flash(response.get("error", "Erro ao atualizar produto."))
            
            return redirect(url_for("product.admin_products"))
        
        categories = self.product_service.get_categories()
        return render_template("edit_product.html", product=product, categories=categories)
    
    def delete_product(self, product_id):
        """Deleta um produto"""
        response, status = self.product_service.delete_product(product_id)
        
        if status == 200:
            flash("Produto excluído com sucesso!")
        else:
            flash(response.get("error", "Erro ao excluir produto."))
        
        return redirect(url_for("product.admin_products"))
    
    def product_details(self, product_id):
        """Mostra detalhes de um produto"""
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            flash("Produto não encontrado.")
            return redirect(url_for("product.list_products"))
        
        return render_template("product_details.html", product=product)
    
    def api_products(self):
        """API endpoint para obter produtos (para integração com outros serviços)"""
        category = request.args.get('category')
        if category:
            products = self.product_service.get_products_by_category(category)
        else:
            products = self.product_service.get_available_products()
        
        return jsonify(products)
    
    def api_categories(self):
        """API endpoint para obter categorias"""
        categories = self.product_service.get_categories()
        return jsonify(categories)

# Instância do controller para uso nas rotas
product_controller = ProductController()

# Criação do blueprint e rotas
product_bp = Blueprint("product", __name__)

@product_bp.route("/list")
def list_products():
    return product_controller.list_products()

@product_bp.route("/admin")
def admin_products():
    return product_controller.admin_products()

@product_bp.route("/create", methods=["GET", "POST"])
def create():
    return product_controller.create_product()

@product_bp.route("/edit/<product_id>", methods=["GET", "POST"])
def edit(product_id):
    return product_controller.edit_product(product_id)

@product_bp.route("/delete/<product_id>", methods=["POST"])
def delete(product_id):
    return product_controller.delete_product(product_id)

@product_bp.route("/details/<product_id>")
def details(product_id):
    return product_controller.product_details(product_id)

@product_bp.route("/api/products")
def api_products():
    return product_controller.api_products()

@product_bp.route("/api/categories")
def api_categories():
    return product_controller.api_categories()
