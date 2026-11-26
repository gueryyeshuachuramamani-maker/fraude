"""60 casos de prueba (30 legítimos, 30 fraudulentos). DATOS SIMULADOS elaborados a mano:
los dominios fraudulentos son inventados; la reputación se simula (True = reportado,
False = consultado sin reportes, None = no disponible, p. ej. enlace nuevo o privado)."""
LEGITIMOS = [
 ("https://www.google.com/maps/place/La+Paz", None, False),
 ("https://wa.me/59170000000", "Hola, te dejo mi número para coordinar", False),
 ("https://www.facebook.com/groups/1234567/", "Únete al grupo de la universidad", None),
 ("https://t.me/+AbCdEfGh123", "Te invito al canal de la clase", None),
 ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Mira este video", False),
 ("https://es.wikipedia.org/wiki/Red_bayesiana", None, False),
 ("https://www.paypal.com/myaccount/summary", "Revisa tu resumen mensual", False),
 ("https://accounts.google.com/signin/v2/identifier", "Inicia sesión para ver el documento compartido", False),
 ("https://www.mercadolibre.com.bo/p/MLB12345", "Oferta de una laptop, ¿te interesa?", False),
 ("https://www.bnb.com.bo/PortalBNB/", "Horarios de atención", False),
 ("https://docs.google.com/document/d/1AbCdEf/edit?usp=sharing", "Aquí está el informe", None),
 ("https://www.instagram.com/p/Cxyz123/", "Mira mi publicación", False),
 ("https://github.com/torvalds/linux", None, False),
 ("https://zoom.us/j/123456789?pwd=abcdef", "Reunión a las 15:00", None),
 ("https://www.tigo.com.bo/promociones", "Promoción del mes", False),
 ("https://bit.ly/3xYzAbC", "Mira este artículo", None),
 ("https://www.amazon.com/dp/B08N5WRWNW?tag=abc&ref=sr_1_1&keywords=laptop&qid=1699999999&sprefix=lap%2Caps%2C150&crid=1ABCDEFGHIJKLM", "Esta laptop está en oferta", False),
 ("http://www.umss.edu.bo/", "Inscripciones abiertas", False),
 ("https://www.netflix.com/browse", "Estreno de la serie", False),
 ("https://www.microsoft.com/es-es/microsoft-365", "Licencia estudiantil", False),
 ("https://www.bancosol.com.bo/", "URGENTE: su cuenta será bloqueada, verifica tu cuenta", False),   # difícil: texto manipulador
 ("https://www.tiktok.com/@usuario/video/123", "¡Felicidades! Ganaste el sorteo del curso, mira el video", False),
 ("https://www.la-razon-de-bolivia.com.bo/sociedad/cuenta-regresiva-elecciones", "Nota del día", None),  # difícil: guiones + 'cuenta'
 ("https://login.microsoftonline.com/common/oauth2/authorize", "Inicia sesión con tu cuenta institucional", False),  # difícil: marca en dominio oficial distinto
 ("https://meet.google.com/abc-defg-hij", "Clase de IA a las 10", None),
 ("https://www.facebook.com/marketplace/item/123", "Vendo mi bicicleta", False),
 ("https://www.entel.bo/personas", None, False),
 ("https://open.spotify.com/playlist/37i9dQ", "Mi playlist", False),
 ("https://forms.gle/AbCdEf12345", "Llena la encuesta de la clase", None),
 ("https://www.viva.com.bo/", "Recarga", False),
]
FRAUDES = [
 ("http://whatsapp-premium.xyz/activar", "Activa WhatsApp Premium gratis hoy, ingresa el código de verificación", True),
 ("https://faceb00k-seguridad.top/login", "URGENTE: su cuenta será bloqueada, verifica tu cuenta", True),
 ("https://paypa1-verificacion.com/cuenta/verificar", "Pago pendiente, confirma tu cuenta ahora mismo", True),
 ("https://bit.ly/premio-tigo", "¡Felicidades! Ganaste un premio, reclámalo ahora mismo", None),
 ("http://185.23.44.12/banco/login.php", "Verifica tus datos bancarios, su cuenta será suspendida", True),
 ("https://secure.bancounion.verificar-datos.click/clave", "Ingrese su contraseña para evitar el bloqueo", None),
 ("https://t.me/+PremiosGratisBolivia", "Únete y gana dinero con ganancias rápidas garantizadas", None),   # difícil: dominio legítimo
 ("https://netflix-renovar-cuenta.shop/pago", "Su suscripción vence hoy, actualice su pago inmediatamente", True),
 ("https://amazon.verify-account.online/signin?id=88213", "Reembolso pendiente: confirme su cuenta", None),
 ("https://mercadolibre-ofertas.vip/laptop", "Ganaste un sorteo, transferencia requerida urgente", True),
 ("https://wa.me.chat-soporte.site/", "Soporte de WhatsApp: envíe el código de 6 dígitos", None),
 ("https://microsoft-support-alerta.com/virus", "Su equipo tiene virus, llame ahora mismo", True),
 ("http://tigo-promo-bolivia.icu/premio", "Felicidades ganador, reclama ahora mismo", None),
 ("https://instagram-verificado.xyz/formulario", "Obtén la insignia, verifica tu cuenta con tu contraseña", True),
 ("https://goog1e-drive-compartido.com/doc", "Documento compartido, confirma tu cuenta para abrir", None),
 ("https://bancosol-clientes.top/ingreso", "Su cuenta será bloqueada. Verifica tu identidad", True),
 ("https://www.tiktok-premios.live/", "Ganaste, sorteo especial", None),
 ("https://entel-recarga-gratis.xyz/", None, None),
 ("https://mail.google.com.verificar-sesion.top/inbox", "Alguien accedió a su cuenta, inicie sesión", None),
 ("https://bnb-seguro.com.bo.acceso-clientes.xyz/", "Su cuenta será suspendida, verifique", True),
 ("http://paypal.com-cuenta-actualizar.xyz/", "Actualice su cuenta o será bloqueada", None),
 ("https://www.facebook.com@evil-site.top/login", "Mira esta foto tuya", None),
 ("https://docs-google.com.bo-compartir.top/d/abc", "Te compartieron un archivo, ingresa tu contraseña", None),
 ("https://www.mercado-libre-bolivia.com/ofertas", "Compra segura, transfiere el depósito hoy", True),   # difícil: sin rasgos fuertes
 ("https://tinyurl.com/yz8abc", "Mira lo que dicen de ti", None),                                      # difícil: destino oculto
 ("https://cutt.ly/ganar-dinero", "Invierte hoy y obtén ganancias rápidas, transferencia inmediata", None),  # difícil
 ("https://telegram-canal-vip.xyz/join", "Únete ahora mismo, contraseña del canal 1234", True),
 ("https://wh4tsapp-web.top/qr", "Escanea para verificar tu cuenta, urgente", True),
 ("https://youtube-premio.click/video", "Ganaste, reclama tu regalo gratis, urgente", None),
 ("https://www.bancounion.com.bo.seguridad-online.icu/clave", "Confirma tu clave, su cuenta será bloqueada", True),
]
CASOS = [(u, t, r, 0) for u, t, r in LEGITIMOS] + [(u, t, r, 1) for u, t, r in FRAUDES]
