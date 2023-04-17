# Protocolo criptográfico

- Instalación del dispositivo: fabricante carga en auditor:
    1. ID del dispositivo
    2. Función hash: BLAKE2b
    3. Contraseña inicial := BLAKE2B([ID del dispositivo] || [número aleatorio seleccionado por el auditor])
- Registro del auditor con Centro de Control