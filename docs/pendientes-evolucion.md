# 📌 Pendientes de evolución — 4-TERMX

Este documento concentra mejoras futuras identificadas durante la evolución de **4-TERMX**.

Los pendientes no representan necesariamente defectos del estado actual. Son oportunidades de evolución que deben evaluarse, diseñarse, implementarse y validarse de forma trazable.

---

## 1. Metodología de gestión del ciclo de vida del desarrollo

**Prioridad:** Alta  
**Estado:** Pendiente de diseño

### Objetivo

Diseñar e incorporar una metodología documentada para gestionar la evolución de 4-TERMX desde la identificación de una necesidad hasta su implementación, validación, deployment y posterior evolución.

La intención no es imponer Scrum de forma estricta. Se busca definir un procedimiento ligero, reproducible y trazable, adaptado a un proyecto técnico personal, pero suficientemente estructurado para que una persona o una IA pueda comprender el contexto de una evolución sin depender exclusivamente del conocimiento del autor.

### Problema que resuelve

A medida que un sistema evoluciona aparecen:

- objetivos iniciales;
- problemas e issues durante el desarrollo;
- decisiones técnicas;
- cambios derivados de otros cambios;
- ramas de desarrollo;
- pruebas;
- evidencias;
- deployments;
- versiones;
- correcciones posteriores;
- nuevas líneas de evolución.

Sin un procedimiento común, estos elementos pueden quedar distribuidos entre commits, archivos, issues, ramas y memoria personal, dificultando reconstruir posteriormente **por qué el sistema llegó a su estado actual**.

### Alcance esperado

La metodología debería permitir relacionar, como mínimo:

`objetivo → necesidad → issue → decisión → rama → implementación → prueba → evidencia → deployment → versión → evolución`

Un elemento puede originar otros elementos y una solución puede generar nuevas líneas de trabajo.

### Ciclo propuesto

1. **Identificación de la necesidad**
   - Qué se quiere mejorar o resolver.
   - Contexto que origina la necesidad.

2. **Definición del objetivo**
   - Resultado esperado.
   - Alcance.
   - Criterios de aceptación.

3. **Planificación**
   - Descomposición en tareas o issues.
   - Dependencias.
   - Rama o línea de desarrollo correspondiente.

4. **Desarrollo**
   - Implementación del cambio.
   - Registro de decisiones relevantes.
   - Relación con commits y archivos afectados.

5. **Pruebas y validación**
   - Pruebas ejecutadas.
   - Resultado.
   - Evidencias disponibles.
   - Criterios de aceptación cumplidos o pendientes.

6. **Deployment**
   - Qué se desplegó.
   - Cuándo.
   - Versión o commit asociado.
   - Resultado del deployment.

7. **Registro histórico**
   - Consolidación de la información necesaria para reconstruir la evolución.
   - Relación entre objetivo, issues, commits, pruebas y deployment.

8. **Cierre o continuación**
   - Objetivo completado.
   - Objetivo parcialmente completado.
   - Nuevos issues derivados.
   - Próxima evolución.

### Trazabilidad

La metodología debería permitir responder preguntas como:

- ¿Por qué existe este componente?
- ¿Qué necesidad originó este cambio?
- ¿Qué issue dio origen a esta implementación?
- ¿Qué decisión técnica se tomó y por qué?
- ¿Qué rama contiene el desarrollo?
- ¿Qué commit implementó la solución?
- ¿Qué pruebas demostraron su funcionamiento?
- ¿Qué evidencia existe?
- ¿Cuándo fue desplegado?
- ¿Qué cambios posteriores derivaron de esta solución?
- ¿Cuál es el estado actual y cuál es su contexto histórico?

### Contexto para IA

Uno de los objetivos principales es que la documentación pueda funcionar como **memoria técnica consultable del proyecto**.

Una IA que no conozca previamente 4-TERMX debería poder consultar la documentación y reconstruir el contexto suficiente para responder preguntas sobre:

- arquitectura;
- componentes;
- decisiones;
- evolución;
- issues;
- cambios;
- pruebas;
- deployments;
- estado actual;
- relación entre cambios históricos.

La documentación no debe depender únicamente del README. Debe existir una estructura de información que permita navegar desde un elemento técnico hacia su origen, implementación, evidencia y evolución posterior.

### Principio de diseño

La metodología debe favorecer:

- **Trazabilidad sobre memoria personal.**
- **Evidencia sobre inferencia.**
- **Contexto histórico sobre simples mensajes de commit.**
- **Relaciones explícitas entre artefactos.**
- **Documentación utilizable tanto por personas como por IA.**
- **Evolución controlada sin introducir burocracia innecesaria.**

### Resultado esperado

El resultado final debería ser un procedimiento documentado y, cuando corresponda, una estructura de archivos o metadatos que permita representar el ciclo de vida de las evoluciones del proyecto.

La implementación definitiva queda pendiente de diseño. Este documento registra **qué problema se quiere resolver y qué capacidades debe proporcionar**, sin anticipar todavía una implementación concreta.

---

## 2. Mejoras de documentación y mantenibilidad

### 2.1 Badge de estado de GitHub Actions
- [x] Añadir badge de estado del workflow principal al README.

### 2.2 Quick Start
- [x] Incorporar una sección de inicio rápido en el README.
- [ ] Documentar los pasos mínimos para comprender y utilizar el entorno.

### 2.3 Arquitectura explícita
- [x] Incorporar una explicación formal de la arquitectura en `docs/architecture.md`.
- [ ] Relacionar componentes, flujos de datos y mecanismos de reconciliación.

### 2.4 Modelo de evidencia
- [ ] Documentar las fuentes de evidencia utilizadas por el sistema.
- [ ] Definir niveles o criterios de confianza cuando corresponda.
- [ ] Diferenciar claramente observación, inferencia e historial.

### 2.5 Design Principles
- [x] Crear `docs/design-principles.md` y documentar los principios de diseño del sistema, incluyendo:
  - Evidence over inference.
  - Observed state ≠ desired state.
  - Unmanaged ≠ removable.
  - El historial constituye evidencia, no necesariamente causalidad absoluta.
  - Los secretos no pertenecen al repositorio.
  - Las acciones destructivas requieren intención explícita.

### 2.6 SECURITY.md
- [x] Añadir `SECURITY.md` con pautas para reportar vulnerabilidades de forma responsable.

### 2.7 CONTRIBUTING.md
- [x] Añadir `CONTRIBUTING.md` con un flujo de cambios y criterios de validación.

---

## 3. Criterio para cerrar un pendiente

Un pendiente no debería considerarse terminado únicamente porque exista un commit.

Cuando corresponda, su cierre debería incluir:

- objetivo definido;
- implementación realizada;
- pruebas ejecutadas;
- evidencia disponible;
- documentación actualizada;
- commit o versión identificable;
- estado final registrado.

La metodología del punto 1 deberá definir posteriormente el procedimiento formal para este ciclo.

---

## 4. Relación con la arquitectura actual

Estos pendientes deben evolucionar de forma compatible con los mecanismos que ya existen en 4-TERMX, especialmente:

- estado observado;
- estado deseado;
- historial de infraestructura;
- auditoría y reconciliación;
- evidencia de operaciones;
- documentación generada automáticamente;
- mapas estructurales y arquitectónicos.

La futura metodología de ciclo de vida deberá complementar estos mecanismos, no sustituirlos.

---

**Estado del documento:** Registro de evolución pendiente  
**Última intención registrada:** definir una metodología formal de ciclo de vida que permita gestionar y reconstruir la evolución técnica de 4-TERMX y hacer ese contexto consultable por una IA.
