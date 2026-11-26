# Web FraudGuard AI
1. Instala Node.js LTS.
2. Copia `.env.example` como `.env` y conserva `VITE_API_URL=http://127.0.0.1:8000`.
3. En una terminal, desde esta carpeta: `npm install` y `npm run dev`.
4. Abre http://localhost:5173.
La API debe seguir activa desde la raíz del proyecto: `uvicorn backend.api:app --reload`.
El historial de esta primera versión es temporal y desaparece al recargar.
