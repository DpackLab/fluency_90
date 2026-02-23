/*
  Auditoría canónica — Progress Guard
  Fuente de verdad: event_log
  Evento: progress_decision_evaluated

  Reglas:
  - Read-only
  - No gobierna runtime
  - Usable en psql / soporte / post-mortem
*/


-- 1) Últimas N decisiones de un usuario
-- Uso:
--   \set user_id 16
--   \set limit 20
SELECT
  occurred_at,
  event_type,
  meta->>'path'        AS endpoint_path,
  (meta->>'allowed')::boolean AS allowed,
  meta->>'reason'      AS reason,
  meta->'signals'      AS signals,
  meta->>'request_id'  AS request_id,
  meta->>'today'       AS decision_day,
  meta                 AS raw_meta
FROM event_log
WHERE event_type = 'progress_decision_evaluated'
  AND user_id = :user_id
ORDER BY occurred_at DESC
LIMIT :limit;


-- 2) Decisiones por día (auditoría diaria)
-- Uso:
--   \set user_id 16
--   \set day '2026-02-23'
SELECT
  occurred_at,
  meta->>'path'        AS endpoint_path,
  (meta->>'allowed')::boolean AS allowed,
  meta->>'reason'      AS reason,
  meta->'signals'      AS signals,
  meta->>'request_id'  AS request_id,
  meta->>'today'       AS decision_day
FROM event_log
WHERE event_type = 'progress_decision_evaluated'
  AND user_id = :user_id
  AND meta->>'today' = :day
ORDER BY occurred_at DESC;


-- 3) Correlación por request_id (cuando exista)
-- Uso:
--   \set req_id '7bacdec2-3c11-4ea5-a6ee-46eb3144bed4'
SELECT
  occurred_at,
  user_id,
  meta->>'path'        AS endpoint_path,
  (meta->>'allowed')::boolean AS allowed,
  meta->>'reason'      AS reason,
  meta->'signals'      AS signals,
  meta->>'today'       AS decision_day
FROM event_log
WHERE event_type = 'progress_decision_evaluated'
  AND meta->>'request_id' = :req_id
ORDER BY occurred_at ASC;


-- 4) Bloqueos efectivos (cuando aplicó enforcement)
SELECT
  occurred_at,
  user_id,
  meta->>'path'   AS endpoint_path,
  meta->'signals' AS signals
FROM event_log
WHERE event_type = 'users_blocked_without_output'
ORDER BY occurred_at DESC
LIMIT 50;
