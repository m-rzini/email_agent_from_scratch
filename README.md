# Projet d'agent e-mail from scratch

Ce projet est un **guide pratique** pour apprendre à construire des agents from scratch, en partant des bases jusqu’à un agent complet et déployable.
Au fil des étapes, vous développerez un agent capable de gérer vos e-mails en se connectant à l’API Gmail.

Le parcours est structuré en quatre sections progressives, chacune illustrée par un notebook et du code source dans src/email_assistant/ :

1. Bases des agents – découvrir les fondations de la création d’un agent.

2. Évaluation – apprendre à tester et mesurer l’efficacité d’un agent.

3. Human-in-the-loop – intégrer l’intervention humaine dans le processus décisionnel.

4. Mémoire – ajouter une mémoire pour donner du contexte et de la continuité à l’agent.

Ces éléments s’assemblent pour former un agent Gmail complet, mais les principes explorés sont génériques : ils peuvent être appliqués à la conception d’autres agents, dans une grande variété de tâches et de contextes.

## Configuration de l’environnement

### Version de Python
* Assurez-vous d’utiliser Python 3.11 ou une version ultérieure.
* Cette version est requise pour une compatibilité optimale avec LangGraph.

```shell
python3 --version
```

### Clés API

* Si vous n’avez pas de clé API OpenAI, vous pouvez vous inscrire [ici](https://openai.com/index/openai-api/).
* Inscrivez-vous à LangSmith [ici](https://smith.langchain.com/).
* Générez une clé API LangSmith.

### Définir les variables d’environnement

* Créez un fichier .env à la racine du projet :

```shell
#Copier le fichier .env.example vers .env
cp .env.example .env
```

Modifiez le fichier .env avec le contenu suivant :

```shell
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT="email-agent"
OPENAI_API_KEY=your_openai_api_key
```

Vous pouvez également définir les variables d’environnement directement dans votre terminal :

```shell
export LANGSMITH_API_KEY=your_langsmith_api_key
export LANGSMITH_TRACING=true
export OPENAI_API_KEY=your_openai_api_key
```

### Installation du package
**Recommandé : avec uv (plus rapide et plus fiable)**

```shell
# Installer uv si ce n’est pas déjà fait
pip install uv

# Installer le package avec les dépendances de développement
uv sync --extra dev

# Activer l’environnement virtuel généré par uv
source .venv/bin/activate   # (Linux/Mac)
# ou
.venv\Scripts\activate      # (Windows PowerShell)
```

**Alternative : avec pip classique**

```shell
# Créer un environnement virtuel
python3 -m venv .venv

# Activer l’environnement
source .venv/bin/activate   # (Linux/Mac)
# ou
.venv\Scripts\activate      # (Windows PowerShell)

# Mettre pip à jour
python -m pip install --upgrade pip

# Installer le package en mode éditable (avec extras dev)
pip install -e ".[dev]"
```

**⚠️ IMPORTANT :**
Ne saute surtout pas l’étape d’installation du package !
L’installation en mode éditable est indispensable pour que les notebooks fonctionnent correctement.
Ton package est installé sous le nom `email_assistant`, ce qui te permet d’écrire : `from email_assistant import email_assistant_test_import`

## Structure

Le dépôt est organisé en **4 sections**, chacune avec un notebook et du code associé dans le dossier `src/email_assistant.`

### Préface : LangGraph 101

Pour une introduction rapide à LangGraph et aux concepts utilisés dans ce projet, consultez le [notebook LangGraph 101](notebooks/langgraph_101.ipynb)
.
Ce notebook présente les bases des modèles de chat, l’appel d’outils, la différence entre agents et workflows, les nœuds / arêtes / mémoire de LangGraph, ainsi que LangGraph Studio.

### Construire un agent

Notebook : [notebooks/agent.ipynb](/notebooks/agent.ipynb)

Code : [src/email_assistant/email_assistant.py](/src/email_assistant/email_assistant.py)