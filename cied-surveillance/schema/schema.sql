-- DuckDB-oriented schema for CIED engineering surveillance.
-- This is a research schema, not a clinical production database.

CREATE TABLE IF NOT EXISTS source (
    source_id VARCHAR PRIMARY KEY,
    source_type VARCHAR NOT NULL,
    title VARCHAR,
    publisher VARCHAR,
    url VARCHAR,
    publication_date DATE,
    retrieval_date DATE,
    licence_or_terms VARCHAR,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS product (
    product_id VARCHAR PRIMARY KEY,
    manufacturer VARCHAR NOT NULL,
    brand VARCHAR,
    family VARCHAR,
    model VARCHAR,
    variant VARCHAR,
    device_class VARCHAR NOT NULL,
    introduced_year INTEGER,
    approval_date DATE,
    discontinued_date DATE,
    regulatory_identifier VARCHAR,
    parent_product_id VARCHAR,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS component (
    component_id VARCHAR PRIMARY KEY,
    component_type VARCHAR NOT NULL,
    supplier VARCHAR,
    manufacturer VARCHAR,
    model_or_family VARCHAR,
    material VARCHAR,
    chemistry VARCHAR,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS product_component (
    product_id VARCHAR NOT NULL,
    component_id VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    valid_from DATE,
    valid_to DATE,
    source_id VARCHAR NOT NULL,
    source_locator VARCHAR,
    evidence_level VARCHAR,
    confidence VARCHAR NOT NULL,
    notes VARCHAR,
    PRIMARY KEY (product_id, component_id, role, valid_from)
);

CREATE TABLE IF NOT EXISTS design_attribute (
    entity_id VARCHAR NOT NULL,
    entity_type VARCHAR NOT NULL,
    attribute_name VARCHAR NOT NULL,
    attribute_value VARCHAR,
    unit VARCHAR,
    valid_from DATE,
    valid_to DATE,
    source_id VARCHAR NOT NULL,
    source_locator VARCHAR,
    evidence_level VARCHAR,
    confidence VARCHAR NOT NULL,
    notes VARCHAR,
    PRIMARY KEY (entity_id, attribute_name, source_id, source_locator)
);

CREATE TABLE IF NOT EXISTS regulatory_event (
    regulatory_event_id VARCHAR PRIMARY KEY,
    product_id VARCHAR,
    event_type VARCHAR NOT NULL,
    jurisdiction VARCHAR,
    event_date DATE,
    title VARCHAR,
    description VARCHAR,
    source_id VARCHAR NOT NULL,
    source_locator VARCHAR,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS adverse_event (
    event_id VARCHAR PRIMARY KEY,
    source_system VARCHAR NOT NULL,
    source_record_id VARCHAR NOT NULL,
    product_id VARCHAR,
    manufacturer_reported VARCHAR,
    brand_reported VARCHAR,
    model_reported VARCHAR,
    event_date DATE,
    implant_date DATE,
    explant_date DATE,
    implant_age_days INTEGER,
    event_type_reported VARCHAR,
    device_problem_terms VARCHAR,
    patient_problem_terms VARCHAR,
    narrative_raw VARCHAR,
    manufacturer_narrative_raw VARCHAR,
    returned_product_available BOOLEAN,
    source_id VARCHAR NOT NULL,
    raw_record_hash VARCHAR,
    ingest_version VARCHAR
);

CREATE TABLE IF NOT EXISTS event_classification (
    event_id VARCHAR NOT NULL,
    classification_version VARCHAR NOT NULL,
    engineering_mechanism VARCHAR,
    failure_location VARCHAR,
    electrical_manifestation VARCHAR,
    detection_route VARCHAR,
    symptom_or_sign VARCHAR,
    clinical_consequence VARCHAR,
    intervention VARCHAR,
    manufacturer_finding VARCHAR,
    remote_detectability VARCHAR,
    adjudication_status VARCHAR,
    confidence VARCHAR,
    reviewer_notes VARCHAR,
    PRIMARY KEY (event_id, classification_version)
);

CREATE TABLE IF NOT EXISTS performance_observation (
    observation_id VARCHAR PRIMARY KEY,
    product_id VARCHAR NOT NULL,
    observation_date DATE,
    metric_name VARCHAR NOT NULL,
    metric_value DOUBLE,
    unit VARCHAR,
    denominator_description VARCHAR,
    implant_age_band VARCHAR,
    source_id VARCHAR NOT NULL,
    source_locator VARCHAR,
    notes VARCHAR
);

-- Suggested design_attribute names include:
-- connector_standard, seal_location, terminal_body_material,
-- connector_insulator_material, header_material, header_seal_design,
-- header_to_can_interface, feedthrough_design, feedthrough_insulator,
-- battery_supplier, battery_cell_model, battery_chemistry,
-- battery_capacity_mah, capacitor_system,
-- lead_architecture, stylet_driven, lumenless, coaxial, multilumen,
-- conductor_geometry, conductor_material, conductor_insulation,
-- outer_insulation, coil_construction, fixation, diameter_fr,
-- shock_coil_count, design_revision.
