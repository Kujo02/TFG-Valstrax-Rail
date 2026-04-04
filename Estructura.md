# 🚆 Proyecto Web App Gestión de Transporte Ferroviario

## 📌 Descripción General
Aplicación web para la gestión integral de transporte de mercancías mediante trenes.  
Permitirá a clientes reservar espacio (parcelas de 1m²) en vagones y a administradores gestionar trenes, viajes, pedidos y asignaciones.

---

# 🧩 Metodología de Desarrollo
- Desarrollo incremental por etapas
- Cada etapa debe ser **funcional e independiente**
- Revisión y actualización del modelo de datos (ER) en cada fase
- Preparación para escalabilidad futura

---

# 🏗️ ETAPA 1 — Autenticación y Base del Sistema

## 🎯 Objetivo
Crear una web app funcional con sistema de autenticación y control de acceso por roles.

## ⚙️ Funcionalidades
- Registro de usuarios (clientes)
- Login de usuarios
- Sistema de roles:
  - Cliente
  - Administrador/Trabajador
- Protección de rutas:
  - Página cliente (solo usuarios autenticados como cliente)
  - Página admin (solo administradores)
- Sistema de sesiones (JWT o cookies)

## 🗃️ Base de Datos (v1)
### Entidades:
- `users`
  - id
  - name
  - email
  - password
  - role (client/admin)
  - created_at

## 📐 Acciones
- Definir stack tecnológico (frontend + backend + DB)
- Configurar entorno de desarrollo
- Crear base de datos inicial
- Diseñar diagrama ER (v1)
- Implementar backend:
  - endpoints `/login`, `/register`
- Implementar frontend:
  - formularios login/register
  - redirecciones según rol
- Middleware de autenticación y autorización
- Testear flujo completo

---

# 🏗️ ETAPA 2 — Sistema de Reservas de Espacio

## 🎯 Objetivo
Permitir a usuarios reservar espacio en trenes (parcelas de 1m²).

## ⚙️ Funcionalidades
- Visualizar trenes disponibles
- Crear pedidos:
  - descripción
  - cantidad de parcelas
- Selección de comportamiento:
  - enviar parcialmente
  - esperar siguiente tren
- Usuarios no registrados pueden simular reserva (opcional)

## 🗃️ Base de Datos (v2)
### Nuevas entidades:
- `orders`
  - id
  - user_id
  - description
  - total_parcels
  - status
- `trains`
  - id
  - name
- `wagons`
  - id
  - train_id
  - capacity (en m²)

## 📐 Acciones
- Actualizar diagrama ER (v2)
- Crear endpoints:
  - `/trains`
  - `/orders`
- Lógica de creación de pedidos
- UI para reservas
- Validaciones de capacidad

---

# 🏗️ ETAPA 3 — Gestión de Viajes

## 🎯 Objetivo
Introducir el concepto de viajes y asignación de pedidos a trenes.

## ⚙️ Funcionalidades
- Crear viajes:
  - tren asignado
  - estaciones origen/destino
- Asociar pedidos a viajes
- Visualización de viajes disponibles

## 🗃️ Base de Datos (v3)
### Nuevas entidades:
- `trips`
  - id
  - train_id
  - origin
  - destination
  - departure_time
- Relación:
  - `trip_orders`

## 📐 Acciones
- Actualizar diagrama ER (v3)
- Implementar CRUD de viajes
- Asociar pedidos manualmente a viajes
- Mostrar viajes en frontend

---

# 🏗️ ETAPA 4 — Sistema de Parcelas (Core del Proyecto)

## 🎯 Objetivo
Representar los vagones como parcelas de 1m² y gestionar ocupación real.

## ⚙️ Funcionalidades
- División de vagones en parcelas
- Estado de cada parcela:
  - libre
  - ocupada
- Asignación manual de parcelas a pedidos

## 🗃️ Base de Datos (v4)
### Nuevas entidades:
- `parcels`
  - id
  - wagon_id
  - status
- `parcel_assignments`
  - id
  - parcel_id
  - order_id

## 📐 Acciones
- Actualizar diagrama ER (v4)
- Generar parcelas automáticamente por vagón
- UI visual tipo grid (muy importante)
- Sistema manual de asignación

---

# 🏗️ ETAPA 5 — Autoasignación Inteligente

## 🎯 Objetivo
Automatizar la asignación de mercancía a huecos disponibles.

## ⚙️ Funcionalidades
- Algoritmo de asignación automática
- Priorización:
  - pedidos más antiguos
  - pedidos más grandes/pequeños
- Gestión de falta de espacio:
  - parcial
  - siguiente tren

## 📐 Acciones
- Diseñar algoritmo (tipo bin packing simplificado)
- Implementar servicio de autoasignación
- Botón en panel admin
- Testeo con distintos escenarios

---

# 🏗️ ETAPA 6 — Panel de Administración Completo

## 🎯 Objetivo
Dar control total a administradores.

## ⚙️ Funcionalidades
- CRUD completo:
  - usuarios
  - trenes
  - vagones
  - viajes
  - pedidos
- Dashboard:
  - ocupación de trenes
  - pedidos pendientes
- Edición manual de asignaciones

## 📐 Acciones
- Diseño UI admin avanzado
- Implementar endpoints de administración
- Control de permisos granular

---

# 🏗️ ETAPA 7 — Optimización y Extras

## 🎯 Objetivo
Mejorar rendimiento y experiencia de usuario.

## ⚙️ Funcionalidades
- Notificaciones al usuario
- Historial de pedidos
- Sistema de estados:
  - pendiente
  - en tránsito
  - entregado
- Optimización de consultas DB
- Seguridad avanzada

## 📐 Acciones
- Refactor de código
- Indexación DB
- Tests automatizados
- Deploy

---

# 🧠 Consideraciones Técnicas

## 🔧 Stack sugerido
- Frontend: React / Next.js
- Backend: Node.js (Express)
- Base de datos: PostgreSQL
- ORM: Prisma / Sequelize

## 🔐 Seguridad
- Hash de contraseñas (bcrypt)
- JWT o sesiones
- Validación de inputs

## 📊 Escalabilidad
- Separación frontend/backend
- API REST bien estructurada
- Preparado para microservicios

---

# ✅ Resultado Final Esperado
Sistema completo donde:
- Clientes reservan espacio en trenes
- Administradores gestionan logística
- Parcelas representan físicamente la carga
- Asignación automática optimiza el espacio

---