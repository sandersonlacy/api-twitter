import flask
from flask import Flask, request, jsonify
from conexao_bd import *
from datetime import datetime

app = Flask(__name__)
flask.json.provider.DefaultJSONProvider.sort_keys = False

@app.route('/usuario/new/base', methods=['POST'])
def usuario_post_base():
    data = request.get_json()
    if 'username' not in data.keys() or 'senha' not in data.keys() or 'email' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"}), 400
    r = Usuario().new_user_base(data["username"], data["senha"], data["email"])
    return jsonify({'status': r})

@app.route('/usuario/new/email', methods=['PUT'])
def usuario_post_email():
    data = request.get_json()
    if 'username' not in data.keys() or 'email' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"}), 400
    r = Usuario().add_email(data["username"], data["email"])
    return jsonify({'status': r})

@app.route('/usuario/new/data', methods=['PUT'])
def usuario_post_data():
    data = request.get_json()
    if 'username' not in data.keys() or 'data_nascimento' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"}), 400
    try:
        datetime.strptime(data["data_nascimento"], r'%Y-%m-%d')
    except ValueError:
        return jsonify({"erro": "formato de data inválido"})
    ano = data["data_nascimento"][0:4]
    mes = data["data_nascimento"][5:7]
    dia = data["data_nascimento"][8:10]
    r = Usuario().add_data_nascimento(data["username"], dia, mes, ano)
    return jsonify({'status': r})

@app.route('/usuario/new/nome', methods=['PUT'])
def usuario_post_nome():
    data = request.get_json()
    if 'username' not in data.keys() or 'nome' not in data.keys() or 'sobrenome' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"}), 400
    r = Usuario().add_nome(data["username"], data["nome"], data["sobrenome"])
    return jsonify({'status': r})

@app.route('/usuario/delete', methods=['DELETE'])
def usuario_delete():
    data = request.get_json()
    if 'username' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"}), 400
    r = Usuario().delete_user(data["username"])
    return jsonify({"status": r})

@app.route('/usuario/get/<username>', methods=['GET'])
def usuario_get_tweet_pam(username):
    r = Usuario().select_user(username)
    if r == None:
        return jsonify({"erro": "username sem correspondência"})
    if type(r) == str:
        return jsonify({"erro": r})
    dados = {"username": r[0], "senha": r[1], "email": r[2], "nome": r[3],
              "sobrenome": r[4], "data_nascimento": r[5], "momento_criacao_usuario": r[6]}
    return jsonify(dados)

@app.route('/usuario/get/', methods=['GET'])
def usuario_get_tweet():
    r = Usuario().select_user()
    if r == None:
        return jsonify({"erro": "não há usuários na base de dados"})
    if type(r) == str:
        return jsonify({"erro": r})
    users = []
    for x in r:
        dados = {"username": x[0], "senha": x[1], "email": x[2], "nome": x[3],
                  "sobrenome": x[4], "data_nascimento": x[5], "momento_criacao_usuario": x[6]}
        users.append(dados)
    return jsonify({"users": users})

@app.route('/tweet/post', methods=['POST'])
def tweet_post():
    data = request.get_json()
    if 'username' not in data.keys() or 'value_conteudo' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    r = Conteudo().new_tweet(data["username"], data["value_conteudo"])
    return jsonify({"status": r})

@app.route('/tweet/get/<username>', methods=['GET'])
def tweet_get_pam(username):
    r = Conteudo().select_tweet(username)
    if r == None:
        return jsonify({"erro": "username sem correspondência"})
    if type(r) == str:
        return jsonify({"erro": r})
    tweets = []
    for x in r:
        tweet = {"id_conteudo": x[0], "username_possuidor": x[1], "value_conteudo": x[2], "tipo": x[3],
                  "n_curtidas": x[4], "n_comentarios": x[5], "n_retweets": x[6], "n_views": x[7],
                    "momento_criacao_conteudo": x[8], "id_imagem_conteudo": x[9]}
        tweets.append(tweet)
    return jsonify({"tweets": tweets})

@app.route('/tweet/get', methods=['GET'])
def tweet_get_no_pam():
    r = Conteudo().select_tweet()
    if r == None:
        return jsonify({"erro": "sem tweets na base de dados"})
    if type(r) == str:
        return jsonify({"erro": r})
    all_tweets = []
    for x in r:
        tweet = {"id_conteudo": x[0], "username_possuidor": x[1], "value_conteudo": x[2], "tipo": x[3],
                  "n_curtidas": x[4], "n_comentarios": x[5], "n_retweets": x[6], "n_views": x[7],
                    "momento_criacao_conteudo": x[8], "id_imagem_conteudo": x[9]}
        all_tweets.append(tweet)
    return jsonify({"all_tweets": all_tweets})

@app.route('/tweet/put/curtir', methods=['PUT'])
def tweet_put_curtir():
    data = request.get_json()
    if 'username_curtiu' not in data.keys() or 'id_conteudo_curtido' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    r = Conteudo().curtir(data["username_curtiu"], data["id_conteudo_curtido"])
    return jsonify({"status": r})

@app.route('/tweet/put/descurtir', methods=['PUT'])
def tweet_put_descurtir():
    data = request.get_json()
    if 'username_curtiu' not in data.keys() or 'id_conteudo_curtido' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    r = Conteudo().descurtir(data["username_curtiu"], data["id_conteudo_curtido"])
    return jsonify({"status": r})

@app.route('/conteudo/delete', methods=['DELETE'])
def tweet_delete():
    data = request.get_json()
    if 'id_conteudo' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    r = Conteudo().delete_conteudo(data["id_conteudo"])
    return jsonify({"status": r})

@app.route('/tag/post', methods=['POST'])
def tag_post():
    data = request.get_json()
    if 'tag' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    r = Tag().new_tag(data["tag"])
    return jsonify({"status": r})

@app.route('/tag/put/trending', methods=['PUT'])
def tag_put_trending():
    data = request.get_json()
    if 'tag' not in data.keys() or 'trending_tag' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    if data["trending_tag"] not in ['TRUE', 'FALSE']:
        return jsonify({"erro": "dados inválidos"})
    r = Tag().trending_tag(data["tag"], data["trending_tag"])
    return jsonify({"status": r})

@app.route('/tag/put/topico', methods=['PUT'])
def tag_put_topico():
    data = request.get_json()
    if 'tag' not in data.keys() or 'topico_tag' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    r = Tag().topico_tag(data["tag"], data["topico_tag"])
    return jsonify({"status": r})

@app.route('/tag/get', methods=['GET'])
def tag_get_no_pam():
    r = Tag().select_tag()
    if r == None:
        return jsonify({"erro": "sem tags na base de dados"})
    if type(r) == str:
        return jsonify({"erro": r})
    tags = []
    for x in r:
        tag = {"tag": x[0], "n_relacionamentos_tag": x[1],
                "n_relacionamentos_tag_temp": x[2], "trending_tag": x[3], "topico_tag": x[4]}
        tags.append(tag)
    return jsonify({"tags": tags})

@app.route('/tag/get/<tag_get>', methods=['GET'])
def tag_get_pam(tag_get):
    r = Tag().select_tag(tag_get)
    if r == None:
        return jsonify({"erro": "tag sem correspondência"})
    if type(r) == str:
        return jsonify({"erro": r})
    tag = {"tag": r[0], "n_relacionamentos_tag": r[1],
            "n_relacionamentos_tag_temp": r[2], "trending_tag": r[3], "topico_tag": r[4]}
    return jsonify(tag)

@app.route('/tag/delete', methods=['DELETE'])
def tag_delete():
    data = request.get_json()
    if 'tag' not in data.keys():
        return jsonify({"erro": "campos obrigatórios não informados"})
    r = Tag().delete_tag(data["tag"])
    return jsonify({"status": r})

if __name__ == '__main__':
    app.run(debug=True)