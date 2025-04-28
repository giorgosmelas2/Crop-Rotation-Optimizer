# Optimal Crop Rotation Using Artificial Life Techniques

This project was developed as part of a diploma thesis and focuses on simulating and optimizing crop rotation strategies using **Artificial Life** and **Computational Intelligence** techniques.

## 🎯 Goals
- Predict which crops can thrive in a given field based on climate and soil conditions.
- Assist farmers in designing better crop rotation schedules to:
  - Maximize yield
  - Improve soil fertility
  - Reduce pest and disease pressure
- Develop a computational model based on:
  - Evolutionary algorithms
  - Agent-based modeling
  - Cellular automata

---

## 🛠️ Technologies Used
- **Python 3.11** (backend logic)
- **FastAPI** (RESTful API)
- **Supabase** (PostgreSQL database)
- **React + TypeScript** (frontend UI)
- **NASA POWER API** (climate data source)
- **Pandas** (data processing)

---

## 🔥 Workflow
1. The farmer inputs the field's coordinates (latitude, longitude).
2. The system retrieves **monthly climate data** (temperature, rainfall).
3. It compares the data against crop-specific requirements.
4. It filters and suggests crops suitable for the local conditions.
5. The farmer selects preferred crops.
6. The model calculates the **optimal crop rotation strategy**, considering:
   - Ecological factors
   - Economic sustainability
   - Pest dynamics