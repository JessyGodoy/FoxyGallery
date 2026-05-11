#criar as rotas do nosso site (links)
from flask import render_template, url_for, redirect
from foxygallery import app, database, bcrypt
from foxygallery.models import Usuario, Post
from flask_login import login_required, login_user, logout_user, current_user
from foxygallery.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename  #biblioteca que corrige os nomes, caso tenha caracteres especiais


#criar servidor local
@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):#verifica se a senha é a correta que o usuario escreveu
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
        
    fotos = Post.query.order_by(Post.data_criacao.desc()).limit(20).all()
    return render_template("homepage.html", form=form_login, fotos=fotos)


#metodo GET os usuario pega as informações do site, no POST ele envia informações para o site
@app.route("/criarconta", methods=["GET", "POST"]) 
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data) #criptografia da senha
        usuario = Usuario(username=form_criarconta.username.data ,email=form_criarconta.email.data, 
                          senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)#faz o login do usuario e permanece logado
        return redirect(url_for("perfil", id_usuario=usuario.id))#redireciona o usuario apos o cadastro
    fotos = Post.query.order_by(Post.data_criacao.desc()).limit(20).all()
    return render_template("criarconta.html", form=form_criarconta, fotos=fotos)


#criando caminho do perfil
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required     #atributo que só pode ser acessa quando o usuario estiver logado
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        #o usuario esta vendo o proprio perfil
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # para salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), #caminho/local original do arquivo onde o código esta escrito (routes)
                            app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # resgistrar arquivo no banco de dados
            foto = Post(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto) #add a foto
            database.session.commit() #salva modificação


        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/excluir-foto/<id_foto>")
@login_required
def excluir_foto(id_foto):

    foto = Post.query.get(id_foto)

    if foto.id_usuario == current_user.id:

        database.session.delete(foto)
        database.session.commit()

    return redirect(url_for("perfil", id_usuario=current_user.id))


@app.route("/logout")
@login_required
def logout():
    logout_user() #desloga o usuario
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Post.query.order_by(Post.data_criacao.desc()).all()[:10]
    return render_template("feed.html", fotos=fotos)