# 🚀 SocialFeed - Agregador de Mídias Sociais

Uma aplicação web moderna para agregar e exibir feeds de mídias sociais em websites, similar ao Tagembed.

![SocialFeed](https://img.shields.io/badge/SocialFeed-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Flask](https://img.shields.io/badge/Flask-3.0+-red)
![React](https://img.shields.io/badge/React-18+-blue)

## ✨ Funcionalidades

- 📱 **Agregação Multi-Plataforma**: Suporte para Instagram, Twitter, Facebook
- 🎨 **Interface Moderna**: Design responsivo e intuitivo
- ⚙️ **Moderação de Conteúdo**: Sistema completo de aprovação/rejeição
- 🔧 **Personalização**: Layouts e temas customizáveis
- 📊 **Código de Incorporação**: Geração automática de widgets
- 🔄 **Atualização Automática**: Feeds sempre atualizados
- 🌐 **API RESTful**: Integração fácil com outros sistemas

## 🛠️ Tecnologias

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados (Neon.com)
- **Flask-CORS** - Suporte a CORS

### Frontend
- **React** - Biblioteca JavaScript
- **Tailwind CSS** - Framework CSS
- **shadcn/ui** - Componentes UI
- **Lucide Icons** - Ícones modernos

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/socialfeed.git
cd socialfeed
```

### 2. Configure o ambiente Python
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 4. Execute a aplicação
```bash
python run_server.py
```

A aplicação estará disponível em `http://localhost:5001`

## 🌐 Deploy

### Banco de Dados (Neon.com)
1. Crie uma conta no [Neon.com](https://neon.com)
2. Crie um novo projeto PostgreSQL
3. Copie a string de conexão
4. Configure a variável `DATABASE_URL` no seu ambiente

### Hospedagem
A aplicação pode ser implantada em:
- **Heroku**
- **Railway**
- **Render**
- **DigitalOcean App Platform**
- **AWS/GCP/Azure**

## 📁 Estrutura do Projeto

```
socialfeed/
├── src/
│   ├── models/          # Modelos do banco de dados
│   ├── routes/          # Rotas da API
│   ├── static/          # Frontend construído
│   └── database/        # Configurações do banco
├── frontend/            # Código fonte React
├── requirements.txt     # Dependências Python
├── run_server.py       # Script principal
└── README.md           # Este arquivo
```

## 🔧 API Endpoints

### Feeds
- `GET /api/feeds` - Listar feeds
- `POST /api/feeds` - Criar feed
- `GET /api/feeds/{id}` - Obter feed específico
- `PUT /api/feeds/{id}` - Atualizar feed
- `DELETE /api/feeds/{id}` - Deletar feed

### Posts
- `GET /api/feeds/{id}/posts` - Listar posts do feed
- `POST /api/feeds/{id}/posts` - Adicionar post
- `PUT /api/feeds/{id}/posts/{post_id}/moderate` - Moderar post

### Incorporação
- `GET /api/feeds/{id}/embed` - Obter código de incorporação

## 🎯 Exemplo de Uso

### 1. Criar um Feed
```javascript
const response = await fetch('/api/feeds', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Meu Feed',
    description: 'Feed das redes sociais da empresa',
    sources: ['instagram', 'twitter'],
    user_id: 1
  })
});
```

### 2. Incorporar no Website
```html
<div id="social-feed-1"></div>
<script src="https://seu-dominio.com/api/feeds/1/embed"></script>
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- 📧 Email: suporte@socialfeed.com
- 💬 Discord: [SocialFeed Community](https://discord.gg/socialfeed)
- 📖 Documentação: [docs.socialfeed.com](https://docs.socialfeed.com)

## 🎉 Agradecimentos

- Inspirado no [Tagembed](https://tagembed.com)
- Comunidade Flask e React
- Todos os contribuidores

---

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐

