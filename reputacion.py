"""Fachada de reputación. Conserva consultar(caso_rep) para compatibilidad."""
def consultar(caso_rep):
    # True=reportado, False=consultado sin reportes, None=no disponible.
    return caso_rep


def crear_proveedor(modo="simulada", api_key=None):
    """Crea un proveedor intercambiable. La consulta externa requiere consentimiento."""
    if modo == "simulada":
        from reputacion_simulada import ReputacionSimulada
        return ReputacionSimulada()
    if modo == "virustotal":
        from reputacion_virustotal import ReputacionVirusTotal
        return ReputacionVirusTotal(api_key=api_key)
    raise ValueError("Modo de reputación no reconocido.")
