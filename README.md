# Sistema de Gerenciamento de Condomínio V1

Bem-vindo ao Sistema de Gerenciamento de Condomínios, um sistema automatizado para ajudar na gestão de condomínios de forma eficiente.

## Funcionalidades

- Agendamento de espaços comuns
- Consulta de horários disponíveis
- Verificação de códigos de agendamento
- Reservas de espaços
- Interação com moradores e administradores
- Gerenciamento de informações de condomínio e usuários

## Requisitos

- Python 3.x
- Flask
- SQLAlchemy
- Banco de Dados SQL

## Instalação

1. Clone o repositório:

```
git clone https://github.com/seu-usuario/seu-repo.git
```

2. Crie um ambiente virtual e ative-o:
```
python -m venv venv

# (Linux/macOS)
source venv/bin/activate

# (Windows)
venv\Scripts\activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Crie o banco de dados:
```
flask shell

from app import db

db.create_all()

exit()
```

## Uso

1. Após a instalação, você pode rodar o aplicativo através do seguinte comando. O comando rodará o aplicativo localmente na porta 5000 por padrão.

```
python run.py
```

2. Acessando a rota `/admin` no navegador, você terá acesso à uma interface interativa com o banco do sistema (http://localhost:5000/admin). A autenticação da página é através do usuário e senha configurados no arquivo `config.py`.

3. A rota `/auto_responder` deve ser configurada para receber as mensagens dos usuários dos condomínios. Esta versão foi desenvolvida para funcionar com o aplicativo <b>AutoResponderWA</b>, então a lógica deverá ser adaptada para lidar com as diferentes aplicações.

## Contribuições

Contribuições são bem-vindas! Leve em conta que esta é apenas a versão inicial do sistema, contendo uma única função. Sinta-se à vontade para fazer um fork deste repositório e enviar pull requests.

Sugestão: adicionar opções exclusivas para os administradores de condomínio fazerem inserções e modificações nos registros através do próprio aplicativo de conversa, sem fazer necessário o acesso na rota `/admin`.

## Autores

Este é um projeto de cunho acadêmico que compõe uma parte de um trabalho de conclusão de curso de Engenharia de Computação. O grupo autor deste projeto é composto pelos integrantes:

|Nome|RA|GitHub|LinkedIn|
|-|-|-|-|
|Caio Chagas Vieira Lopes|11190088|<a href="https://github.com/caiython">Caiython</a>|<a href="https://www.linkedin.com/in/caiocvl/">Caio Chagas</a>|
|Gustavo Henrique de Oliveira Valentim|11191010|-||
|Lais Teles Marques|11190576|-||
|Lucas Kaique Rocha Nascimento|11190982|-||

## Licença

Este projeto está sob a Licença Pública Geral GNU (GNU General Public License). Consulte o arquivo [LICENSE.md](LICENSE.md) para obter detalhes.