# Política de seguridad

## Alcance

Esta política cubre los scripts, configuraciones, workflows y documentación mantenidos en 4-TERMX.

## Reportar una vulnerabilidad

Por favor, no publiques credenciales, tokens, claves privadas ni detalles explotables de una vulnerabilidad en un Issue público.

Utiliza la función **Private vulnerability reporting** de GitHub para este repositorio si está habilitada. Si no está disponible, contacta de forma privada al propietario del repositorio mediante los canales de GitHub antes de publicar detalles técnicos.

Incluye, cuando sea posible:

- componente o archivo afectado;
- pasos para reproducir el problema;
- impacto observado;
- versión o commit relevante;
- mitigación propuesta, si existe.

No adjuntes secretos reales ni datos personales innecesarios.

## Prácticas de seguridad del proyecto

- Los secretos y credenciales no deben versionarse.
- Los archivos locales de SSH y tokens deben permanecer fuera del repositorio.
- Revisa los cambios antes de ejecutar scripts o publicar commits.
- Los workflows deben usar permisos mínimos necesarios.
- La auditoría de paquetes informa sobre el estado; no debe eliminar dependencias automáticamente.
- Un registro histórico aporta evidencia, pero no demuestra por sí solo causalidad absoluta.

## Respuesta y divulgación

La recepción, investigación, corrección y divulgación se coordinarán de forma responsable. No se garantiza un plazo específico de respuesta. Evita divulgar públicamente detalles antes de que exista oportunidad razonable de evaluar y corregir el problema.
