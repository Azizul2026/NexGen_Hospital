// ══════════════════════════════════════════════════════════════
//  NexGen Hospital — Neo4j Initialization Script
//  Run in Neo4j Browser or via cypher-shell before first startup
// ══════════════════════════════════════════════════════════════

// ── Constraints (uniqueness + existence) ────────────────────
CREATE CONSTRAINT user_username_unique   IF NOT EXISTS FOR (u:User)    REQUIRE u.username    IS UNIQUE;
CREATE CONSTRAINT patient_username_unique IF NOT EXISTS FOR (p:Patient) REQUIRE p.username    IS UNIQUE;
CREATE CONSTRAINT patient_id_unique       IF NOT EXISTS FOR (p:Patient) REQUIRE p.patientId   IS UNIQUE;
CREATE CONSTRAINT doctor_username_unique  IF NOT EXISTS FOR (d:Doctor)  REQUIRE d.username    IS UNIQUE;
CREATE CONSTRAINT appt_id_unique          IF NOT EXISTS FOR (a:Appointment) REQUIRE a.appointmentId IS UNIQUE;
CREATE CONSTRAINT record_id_unique        IF NOT EXISTS FOR (r:MedicalRecord) REQUIRE r.recordId IS UNIQUE;

// ── Indexes for fast lookups ─────────────────────────────────
CREATE INDEX user_role_idx          IF NOT EXISTS FOR (u:User)        ON (u.role);
CREATE INDEX patient_status_idx     IF NOT EXISTS FOR (p:Patient)     ON (p.status);
CREATE INDEX patient_doctor_idx     IF NOT EXISTS FOR (p:Patient)     ON (p.assignedDoctorUsername);
CREATE INDEX appt_patient_idx       IF NOT EXISTS FOR (a:Appointment) ON (a.patientUsername);
CREATE INDEX appt_doctor_idx        IF NOT EXISTS FOR (a:Appointment) ON (a.doctorUsername);
CREATE INDEX appt_date_idx          IF NOT EXISTS FOR (a:Appointment) ON (a.appointmentDate);
CREATE INDEX record_patient_idx     IF NOT EXISTS FOR (r:MedicalRecord) ON (r.patientUsername);
CREATE INDEX record_doctor_idx      IF NOT EXISTS FOR (r:MedicalRecord) ON (r.doctorUsername);

// ── Verify ───────────────────────────────────────────────────
SHOW CONSTRAINTS;
SHOW INDEXES;
