FRAUDGUARD AI - ENTREGA 1: MOTOR INTEGRADO + API WEB

Esta entrega está adaptada a los archivos Python que compartiste:
agente.py, analizador_url.py, analizador_texto.py, red_bayesiana.py,
reputacion.py y main.py.

ANTES DE COPIAR
1. Haz una copia de seguridad de tu carpeta agente_fraudes.
2. Descomprime este ZIP.
3. Copia el contenido de esta carpeta encima de tu proyecto agente_fraudes.
4. Acepta reemplazar solamente estos archivos existentes:
   agente.py, main.py, reputacion.py
   Añade los archivos nuevos: validador_url.py, reputacion_simulada.py,
   reputacion_virustotal.py, backend/ y archivos de configuración.
5. NO reemplaces analizador_url.py, analizador_texto.py, red_bayesiana.py,
   casos_prueba.py ni evaluar.py.

PASO A. Probar la consola
En terminal, dentro de agente_fraudes:
  python main.py "https://www.paypal.com/myaccount/summary" --texto "Revisa tu resumen mensual" --rep limpio
Prueba una entrada inválida:
  python main.py "javascript:alert(1)"
Debe mostrar un error de entrada y no producir un análisis.

PASO B. Instalar dependencias
  python -m venv .venv
Windows PowerShell:
  .venv\Scripts\Activate.ps1
Luego:
  pip install -r requirements.txt

PASO C. Iniciar la API
  uvicorn backend.api:app --reload
Abre:
  http://127.0.0.1:8000/docs
Prueba POST /api/analizar con:
  {"url":"https://example.com","texto":"Hola"}
La reputación estará como desconocida/no consultada hasta configurar una fuente externa.

PASO D. VirusTotal (opcional)
1. Lee y acepta la política de privacidad antes de compartir URLs con terceros.
2. Copia .env.example a .env.
3. Configura MODO_REPUTACION=virustotal y VIRUSTOTAL_API_KEY=tu_clave.
4. Instala/carga dotenv al iniciar el servidor (por ejemplo, agrega
   `from dotenv import load_dotenv; load_dotenv()` al inicio de backend/api.py).
5. En el JSON de solicitud usa autoriza_consulta_externa=true únicamente cuando
   el usuario haya aceptado compartir esa URL.
Nunca coloques la clave API en React o Expo ni la subas a GitHub.

NOTAS
- No se visita la URL analizada. Este backend solo valida y analiza texto/URL y,
  con consentimiento, hace una consulta de reputación externa.
- Si en el futuro agregas un componente que descargue o siga URLs, se necesitarán
  defensas SSRF adicionales; no debe hacerse desde esta API básica.
- BAJO no significa seguro.
- La interfaz web y móvil se crearán en la siguiente entrega usando esta API.
