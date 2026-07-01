# 🚀 Astronauta: Missão Sobrevivência
Um jogo em Python com pygame, onde você controla um astronauta que precisa sobreviver aos meteoros e coletar cristais espaciais para voltar à Terra.

<img width="937" height="693" alt="image" src="https://github.com/user-attachments/assets/ce31dd1b-5290-455f-8bd9-535966540089" />
# 🎮 Como jogar
Seta Esquerda/Direita → mover o astronauta

Objetivo → alcançar 300 pontos

Ganhe pontos → sobrevivendo ao tempo e coletando cristais (+15 pontos cada)

Cuidado → se perder todas as vidas, é Game Over

<img width="938" height="700" alt="image" src="https://github.com/user-attachments/assets/45d2e960-6610-4072-b993-d0a8c2f8de68" />


# 🖼️ Recursos
Menu inicial com opções de Start Game e Exit

Sprites personalizados: astronauta, meteoro, cristal espacial

Fundos temáticos para menu, gameplay e tela final

Placar em tempo real e tela de vitória/derrota
<img width="936" height="690" alt="image" src="https://github.com/user-attachments/assets/3fdbc0a4-e8a4-4b60-9f49-d2325b144801" />

## ⚙️ Instalação
Clone este repositório:

bash
git clone https://github.com/seuusuario/dangerous-space.git
cd dangerous-space
Crie e ative um ambiente virtual:

bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Instale as dependências:

bash
pip install -r requirements.txt

## ▶️ Executando o jogo
No terminal:

bash
python main.py

## 📂 Estrutura do projeto
Código
dangerous-space/
│── code/
│   ├── Const.py
│   ├── Game.py
│   ├── Menu.py
│   └── __init__.py
│── imagens/
│   ├── player.png
│   ├── meteoro.png
│   ├── cristal.png
│   ├── fundo_menu.jpg
│   ├── fundo_jogo.jpg
│   └── fundo_fim.png
│── main.py
│── requirements.txt
│── README.md

##✨ Créditos
Desenvolvido por Ariane

Arte das imagens do jogo criadas com apoio de IA

Projeto inspirado em exercícios da disciplina de programação de jogos

