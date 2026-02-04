🤖 Agents.md: Migración lasio -> lasio-rs
Este documento define el equipo de agentes inteligentes encargados de la transpilación, optimización y validación del motor LAS en Rust.

🏗️ 1. El Analista de Código (Source_Analyst)
Objetivo: Extraer la lógica de negocio pura del repositorio Python clonado.

Rol: Arqueólogo de Software.

Contexto de entrada: Archivos lasio/reader.py, lasio/las.py y lasio/las_items.py.

Prompt Maestro:

"Actúa como un experto en Python y el estándar LAS. Tu tarea es analizar el código fuente en {local_repo_path}. No traduzcas a Rust aún; extrae las reglas de validación, cómo se manejan los encodings (latin-1 vs utf-8), y cómo se parsean las secciones ~V, ~W, ~C, ~P y ~A. Genera un esquema técnico de metadatos que el siguiente agente pueda usar."

📐 2. El Arquitecto de Tipos (Rust_Architect)
Objetivo: Diseñar el sistema de tipos y la gestión de memoria en Rust.

Rol: Diseñador de Sistemas de Bajo Nivel.

Contexto de entrada: Salida del Source_Analyst.

Prompt Maestro:

"Basado en las reglas de lasio, diseña las estructuras de datos en Rust. Usa IndexMap para preservar el orden de los headers. Define un struct LASFile que contenga secciones genéricas. Implementa Serde para que los headers sean serializables. Restricción: Evita el uso excesivo de String si puedes usar Cow<'a, str> para maximizar la eficiencia de memoria al leer archivos grandes."

⚙️ 3. El Ingeniero de Parsing (Nom_Parser)
Objetivo: Sustituir las Regex de Python por un parser combinatorio de alto rendimiento.

Rol: Especialista en Gramática de Datos.

Contexto de entrada: lasio/reader.py y los modelos de Rust_Architect.

Prompt Maestro:

"Tu misión es construir el motor de lectura usando la crate nom. Debes ignorar la lógica de Pandas de Python y crear un flujo que procese el archivo línea por línea con un BufReader. Enfócate en la sección ~ASCII (datos numéricos): debe ser capaz de procesar millones de filas sin picos de memoria, convirtiendo el texto directamente a ndarray::Array2<f64>."

⚡ 4. El Optimizador de Rendimiento (Performance_Specialist)
Objetivo: Asegurar que la versión de Rust sea órdenes de magnitud más rápida que la de Python.

Rol: Ingeniero de Concurrencia.

Contexto de entrada: Código generado por Nom_Parser.

Prompt Maestro:

"Revisa el código Rust generado. Implementa paralelismo con Rayon para el parseo de columnas de datos una vez que el header ha sido leído. Asegúrate de que el manejo de errores no detenga el proceso (implementa un log de errores similar al LASDataError de lasio). Optimiza las asignaciones de memoria pre-calculando el tamaño de los vectores basados en el conteo de líneas."

✅ 5. El Validador de Paridad (Parity_Tester)
Objetivo: Garantizar que lasio-rs produzca los mismos resultados que lasio (Python).

Rol: QA Engineer.

Contexto de entrada: Salida de ambos sistemas (Python y Rust).

Prompt Maestro:

"Genera una suite de pruebas que compare la salida JSON de lasio (Python) contra la salida de nuestro nuevo motor en Rust. Si hay discrepancias en el manejo de nulos (NULL) o en la precisión de los flotantes, documenta la causa raíz y sugiere ajustes al Nom_Parser."

🔄 Lógica de Evolución de Prompts (Antigravity Flow)
Para que el sistema sea dinámico, sigue esta jerarquía de actualización de prompts:

Fase 1 (Estructura): Solo están activos Source_Analyst y Rust_Architect. El prompt se enfoca en "Definir el esqueleto".

Fase 2 (Funcionalidad): Se activa Nom_Parser. El prompt de Rust_Architect cambia a "Refactorizar para soportar streaming".

Fase 3 (Optimización): Se activa Performance_Specialist. Los prompts anteriores se actualizan con la instrucción: "Priorizar zero-copy sobre legibilidad si el performance mejora > 20%".

Fase 4 (Interoperabilidad): (Opcional) Agregar un agente para PyO3 que cree los bindings para que Python pueda usar el motor de Rust.