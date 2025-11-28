from flask import Flask, render_template, request, session
import json
import re 

app = Flask(__name__)
app.secret_key = 'une_clé_secrète'

# Charger les données FAQ
with open("data/faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

def get_answer(user_input):
    cleaned_input = user_input.lower().strip()

    # Salutations
    if re.search(r"\b(bonjour|salut|salam|bonsoir)\b", cleaned_input):
        return "Bonjour ! Je suis OrientaBot 🤖. Comment puis-je vous aider ?"

    # Présentation
    match = re.search(r"\b(je suis|moi c'est|mon nom est)\s+([a-zA-Zéèàç]+)", cleaned_input)
    if match:
        session["user_name"] = match.group(2).capitalize()
        return f"Enchanté {session['user_name']} 😊 ! Comment puis-je vous aider ?"

    # Rappel prénom
    if "user_name" in session and re.search(r"\bmoi\b", cleaned_input):
        return f"Je me souviens de vous, {session['user_name']} ! Que puis-je faire pour vous ?"

    # Au revoir / merci
    if re.search(r"\b(merci|thanks|au revoir|bye|à bientôt)\b", cleaned_input):
        return "Avec plaisir 😊 ! N'hésitez pas à revenir si vous avez d'autres questions. Bonne journée ! 👋"

    # Recherche FAQ
    for item in faq_data:
        if any(keyword in cleaned_input for keyword in item["keywords"]):
            return item["answer"]

    return "Désolé, je n’ai pas compris votre message. Pouvez-vous reformuler ?"

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        question = request.form["question"]
        answer = get_answer(question)
        session["history"].append(("Vous", question))
        session["history"].append(("Bot", answer))
        session.modified = True

    return render_template("index.html", history=session["history"])

if __name__ == "__main__":
    app.run(debug=True)
