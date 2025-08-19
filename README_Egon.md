# Egon

Projet en vision par ordinateur et deep learning.  
Ce dépôt contient le code, les scripts de sauvegarde et d’utilisation, ainsi que différents modèles.

⚠️ Certains fichiers lourds (>100 Mo) ne sont pas inclus dans GitHub.  
Merci de les télécharger séparément (voir ci-dessous).

---

## 📦 Installation

Cloner le repo :

```bash
git clone https://github.com/loubetcorentin/Egon.git
cd Egon
```

Créer un environnement Python (recommandé) :

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## 📂 Organisation du projet

```
Egon/
│
├── model_checkpoints/     # Checkpoints lourds (ignorés dans Git)
├── pose/                  # Modèles de pose
├── pretrained_models/     # Modèles pré-entraînés
├── backup_lastnight.py    # Script sauvegarde
├── backup_morning.py      # Script sauvegarde
├── main.py                # Script principal
├── parameters.py          # Paramètres
├── yolofunctions.py       # Fonctions YOLO
└── README.md              # Ce fichier
```

---

## 💾 Fichiers lourds

Les modèles trop volumineux (>100 Mo) doivent être téléchargés séparément.  

- [Lien fichiers lourds](https://drive.google.com/drive/folders/1JpiX4WwjbtErujevvYzJvpl9jgIjVw-L?usp=sharing)

---

## 🚀 Exemple d’utilisation

```bash
python main.py --input image.jpg --model sauvegarde/yolov4.onnx
```

---

## 🤝 Contribution

1. Fork le repo  
2. Crée une branche (`git checkout -b feature/ma-feature`)  
3. Commit (`git commit -m "Ajout ma feature"`)  
4. Push (`git push origin feature/ma-feature`)  
5. Ouvre une Pull Request  

---

## 📜 Licence

[MIT](LICENSE) – libre utilisation et modification
