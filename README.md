# PicLingo 🎨🗣️

**An Aided System for Language-Disabled Children**

PicLingo is a graduation project that combines **Text-to-Image (TTI)** generation and **Speech-to-Text (STT)** technology to support language development for children with language disorders. The platform lets mentors generate meaningful images from English text prompts, and lets children practice communication skills through an interactive "Show-and-Tell" speaking game.

---

## 📖 About the Project

Children with language disorders face unique challenges in learning and effective communication. Since visual learning can account for up to 90% of how children absorb information, PicLingo was built to turn text into engaging, meaningful images — giving mentors and educators a fast, low-cost way to enrich learning content, and giving children a fun, judgment-free way to practice describing what they see.

This project was developed as a **Bachelor's degree graduation project** in Computer Science at the **College of Computer Science and Engineering, Taibah University**.

### 🎯 Objectives

- Study existing Text-to-Image generation techniques and NLP/ML approaches
- Evaluate and compare different TTI model architectures on a benchmark dataset
- Build a website that converts English text prompts into colorful, meaningful images
- Build an interactive game using speech recognition and similarity scoring
- Design a child-friendly, accessible user interface

---

## ✨ Features

- **🖼️ Text-to-Image Generation** — Mentors write a description (objects, style, and details), and PicLingo generates a matching image using a Stable Diffusion-based model.
- **🎤 Show-and-Tell Game** — Children pick an image from predefined categories, describe it out loud, and receive feedback based on how closely their spoken description matches the image caption.
- **📊 Speech-to-Text Evaluation** — Spoken descriptions are transcribed and compared to the reference caption using cosine similarity, giving children a meaningful communication score.
- **⭐ Favorites List** — Save generated images to revisit and reuse later.
- **👩‍🏫 Mentor Tools** — Manage the game's image categories and content.
- **👶 Child-Friendly UI** — Simple, colorful, and accessible interface designed with young users in mind.

---

## 🧠 Behind the Model

Several TTI architectures were experimented with and evaluated using **Inception Score (IS)**, **Fréchet Inception Distance (FID)**, and human evaluation (**Fleiss' Kappa**). The proposed model outperformed the baseline (VQGAN) with an IS of **4.28** and an FID of **1.83**, and achieved substantially higher human-rated agreement (68% vs. 17% Fleiss' Kappa) — and was selected for integration into the website.

---

## 📰 Publication

This project has been published as a peer-reviewed research paper:

> **PicLingo: A GenAI-Based System for Language-Disabled Children**
> Razan Alatawi, Shahad Alamri, Renad Almaghthawi, Shada Alofi, Ghada Alharbi, Rehab Albeladi
> *International Journal of Advanced Computer Science and Applications (IJACSA)*, 17(3), 2026
> DOI: [10.14569/IJACSA.2026.01703105](https://doi.org/10.14569/IJACSA.2026.01703105)

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Backend** | Python, Flask |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | SQLite (via Flask-SQLAlchemy) |
| **Authentication** | Flask-Login |
| **Image Generation** | Stable Diffusion (Hugging Face Inference API) |
| **Speech Recognition** | Speech-to-Text (STT) |
| **ML Development** | Google Colaboratory, PyTorch, Diffusers, NLTK, TorchMetrics |
| **UI/Design** | Figma, Webflow, Bootstrap |
| **Tools** | Visual Studio Code, GitHub, Overleaf |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A Hugging Face account and access token ([get one here](https://huggingface.co/settings/tokens))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RenadAlmaghthawi/PicLingo.git
   cd PicLingo
   ```

2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Hugging Face token**

   Create a file at `website/static/js/token.js` (this file is git-ignored and kept local for security):
   ```javascript
   const token = "your_hugging_face_token_here";
   ```

4. **Run the app**
   ```bash
   cd "piclingo-site-53449e.webflow (3)"
   python main.py
   ```

5. Open your browser at `http://127.0.0.1:5000`


## 📄 License

This project was developed for academic purposes as part of a graduation project requirement.
