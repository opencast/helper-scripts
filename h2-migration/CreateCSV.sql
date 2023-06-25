--TO MOVE DATA FROM oc_user_role TABLE  
--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_user_role_temp"(
    "user_id" BIGINT NOT NULL,
    "role_id" BIGINT NOT NULL
);         

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_user_role_temp" (user_id, role_id)
select user_id, role_id
FROM oc_user_role;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_user_role.csv', 'SELECT * FROM "public"."oc_user_role_temp"', 'charset=UTF-8  null=NULL');
--if the temp table exists, lets delete it
drop table "public"."oc_user_role_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_user_ref_role TABLE  
--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_user_ref_role_temp"(
    "user_id" BIGINT NOT NULL,
    "role_id" BIGINT NOT NULL
);         

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_user_ref_role_temp" (user_id, role_id)
select user_id, role_id
FROM oc_user_ref_role;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_user_ref_role.csv', 'SELECT * FROM "public"."oc_user_ref_role_temp"', 'charset=UTF-8  null=NULL');
--if the temp table exists, lets delete it
drop table "public"."oc_user_ref_role_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_user_ref TABLE  
--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_user_ref_temp"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(128),
    "last_login" TIMESTAMP,
    "email" VARCHAR,
    "name" VARCHAR,
    "login_mechanism" VARCHAR,
    "organization" VARCHAR(128)
);       

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_user_ref_temp" (id, username, last_login, email, name, login_mechanism, organization)
select id, username, last_login, email, name, login_mechanism, organization
FROM oc_user_ref;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_user_ref.csv', 'SELECT * FROM "public"."oc_user_ref_temp"', 'charset=UTF-8  null=NULL');
--if the temp table exists, lets delete it
drop table "public"."oc_user_ref_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_user TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_user_temp"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(128),
    "password" LONGVARCHAR,
    "name" VARCHAR,
    "email" VARCHAR,
    "organization" VARCHAR(128),
    "manageable" INTEGER
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_user_temp" (id, username, password, name, email, organization, manageable)
select id, username, password, name, email, organization, manageable
FROM oc_user;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_user.csv', 'SELECT * FROM "public"."oc_user_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_user_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_series_property TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_series_property_temp"(
    "organization" VARCHAR(128),
    "series" VARCHAR(128),
    "name" VARCHAR,
    "value" VARCHAR
);  

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_series_property_temp" (organization, series, name, value)
SELECT organization, series, name, value
FROM oc_series_property;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_series_property.csv', 'SELECT * FROM "public"."oc_series_property_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_series_property_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_series_elements TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_series_elements_temp"(
    "series" VARCHAR(128),
    "organization" VARCHAR(128), 
    "type" VARCHAR,
    "data" LONGVARBINARY
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_series_elements_temp" (series, organization, type, data)
SELECT series, organization, type, data
FROM oc_series_elements;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_series_elements.csv', 'SELECT * FROM "public"."oc_series_elements_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_series_elements_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_series TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_series_temp"(
    "id" VARCHAR(128) NOT NULL,
    "organization" VARCHAR(128) NOT NULL,
    "access_control" LONGVARCHAR,
    "dublin_core" LONGVARCHAR
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_series_temp" (id, organization, access_control, dublin_core)
SELECT id, organization, access_control, dublin_core
FROM oc_series;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_series.csv', 'SELECT * FROM "public"."oc_series_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_series_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_search TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_search_temp"(
    "id" VARCHAR(128) NOT NULL,
    "series_id" VARCHAR(128),
    "organization" VARCHAR(128),
    "deletion_date" TIMESTAMP,
    "access_control" LONGVARCHAR,
    "mediapackage_xml" LONGVARCHAR,
    "modification_date" TIMESTAMP
);   

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_search_temp" (id, series_id, organization, deletion_date, access_control, mediapackage_xml, modification_date)
SELECT id, series_id, organization, deletion_date, access_control, mediapackage_xml, modification_date
FROM oc_search;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_search.csv', 'SELECT * FROM "public"."oc_search_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_search_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_scheduled_last_modified TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_scheduled_last_modified_temp"(
    "capture_agent_id" VARCHAR(255) NOT NULL,
    "last_modified" TIMESTAMP
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_scheduled_last_modified_temp" (capture_agent_id, last_modified)
SELECT capture_agent_id, last_modified
FROM oc_scheduled_last_modified;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_scheduled_last_modified.csv', 'SELECT * FROM "public"."oc_scheduled_last_modified_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_scheduled_last_modified_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_scheduled_extended_event TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_scheduled_extended_event_temp"(
    "mediapackage_id" VARCHAR(128) NOT NULL,
    "organization" VARCHAR(128) NOT NULL,
    "capture_agent_id" VARCHAR(128),
    "start_date" TIMESTAMP,
    "end_date" TIMESTAMP,
    "source" VARCHAR,
    "recording_state" VARCHAR,
    "recording_last_heard" BIGINT,
    "presenters" VARCHAR,
    "last_modified_date" TIMESTAMP,
    "checksum" VARCHAR(64), 
    "capture_agent_properties" VARCHAR,
    "workflow_properties" VARCHAR
);

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_scheduled_extended_event_temp" (mediapackage_id, organization, capture_agent_id, start_date, end_date, source, recording_state, recording_last_heard, presenters, last_modified_date, checksum, capture_agent_properties, workflow_properties)
SELECT mediapackage_id, organization, capture_agent_id, start_date, end_date, source, recording_state, recording_last_heard, presenters, last_modified_date, checksum, capture_agent_properties, workflow_properties
FROM oc_scheduled_extended_event;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_scheduled_extended_event.csv', 'SELECT * FROM "public"."oc_scheduled_extended_event_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_scheduled_extended_event_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_organization_property TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_organization_property_tempp"(
    "organization" VARCHAR(128),
    "name" VARCHAR,
    "value" CLOB 
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_organization_property_tempp" (organization, name, value)
SELECT organization, name, value
FROM oc_organization_property;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_organization_property.csv', 'SELECT * FROM "public"."oc_organization_property_tempp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_organization_property_tempp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_organization_node TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_organization_node_temp"(
    "organization" VARCHAR(128),
    "port" INTEGER,
    "name" VARCHAR
);

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_organization_node_temp" (organization, port, name)
SELECT organization, port, name
FROM oc_organization_node;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_organization_node.csv', 'SELECT * FROM "public"."oc_organization_node_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_organization_node_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_incident_text TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_incident_text_temp"(
    "id" VARCHAR NOT NULL,
    "text" VARCHAR
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_incident_text_temp" (id, text)
SELECT id, text
FROM oc_incident_text;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_incident_text.csv', 'SELECT * FROM "public"."oc_incident_text_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_incident_text_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_incident TABLE  

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_incident_temp"(
    "id" BIGINT NOT NULL,
    "jobid" BIGINT,
    "timestamp" TIMESTAMP,
    "code" VARCHAR,
    "severity" INTEGER,
    "parameters" LONGVARCHAR,
    "details" LONGVARCHAR   
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_incident_temp" (id, jobid, timestamp, code, severity, parameters, details)
SELECT id, jobid, timestamp, code, severity, parameters, details
FROM oc_incident;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_incident.csv', 'SELECT * FROM "public"."oc_incident_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_incident_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_role TABLE  ---> Needed for oc_group_member

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_role_temp"(
    "id" BIGINT NOT NULL,
    "description" VARCHAR,
    "name" VARCHAR(128),
    "organization" VARCHAR(128)
);   
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_role_temp" (id, description, name, organization)
SELECT id, description, name, organization
FROM oc_role;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_role.csv', 'SELECT * FROM "public"."oc_role_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_role_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_group_member TABLE  ---> Needs oc_role

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_group_role_temp"(
    "group_id" BIGINT NOT NULL,
    "role_id" BIGINT NOT NULL
); 
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_group_role_temp" (group_id, role_id)
SELECT group_id, role_id
FROM oc_group_role;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_group_role.csv', 'SELECT * FROM "public"."oc_group_role_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_group_role_temp";
-------------------------------------------------------------------------------
--TO MOVE DATA FROM oc_group_member TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_group_member_temp"(
    "group_id" BIGINT,
    "member" VARCHAR
); 
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_group_member_temp" (id, group_id, description, role, name, organization)
SELECT id, group_id, description, role, name, organization
FROM oc_group_member;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_group_member.csv', 'SELECT * FROM "public"."oc_group_member_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_group_member_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_group TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_group_temp"(
    "id" BIGINT NOT NULL,
    "group_id" VARCHAR(128),
    "description" VARCHAR,
    "role" VARCHAR,
    "name" VARCHAR(128),
    "organization" VARCHAR(128)
); 
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_group_temp" (id, group_id, description, role, name, organization)
SELECT id, group_id, description, role, name, organization
FROM oc_group;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_group.csv', 'SELECT * FROM "public"."oc_group_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_group_temp";
-------------------------------------------------------------------------------
--TO MOVE DATA FROM oc_capture_agent_state TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_capture_agent_state_temp"(
    "id" VARCHAR(128) NOT NULL,
	"organization" VARCHAR(128) NOT NULL,
    "configuration" LONGVARCHAR,
    "state" LONGVARCHAR NOT NULL, 
    "last_heard_from" BIGINT NOT NULL,
    "url" LONGVARCHAR
);  
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_capture_agent_state_temp" (id, organization, configuration, state, last_heard_from, url)
SELECT id, organization, configuration, state, last_heard_from, url
FROM oc_capture_agent_state;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_capture_agent_state.csv', 'SELECT * FROM "public"."oc_capture_agent_state_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_capture_agent_state_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_capture_agent_role TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_capture_agent_role_temp"(
    "id" VARCHAR(128),
    "organization" VARCHAR(128),
    "role" VARCHAR
);   
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_capture_agent_role_temp" (id, organization, role)
SELECT id, organization, role
FROM oc_capture_agent_role;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_capture_agent_role.csv', 'SELECT * FROM "public"."oc_capture_agent_role_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_capture_agent_role_temp";
-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_bundleinfo TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_bundleinfo_temp"(
    "id" BIGINT NOT NULL,
    "bundle_name" VARCHAR(128) NOT NULL,
    "build_number" VARCHAR(128),
    "host" VARCHAR(128) NOT null,
    "bundle_id" BIGINT NOT NULL,
    "bundle_version" VARCHAR(128) NOT NULL,
    "db_schema_version" VARCHAR(128)
    
); 
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_bundleinfo_temp" (id, bundle_name, build_number, host, bundle_id, bundle_version, db_schema_version)
SELECT id, bundle_name, build_number, host, bundle_id, bundle_version, db_schema_version
FROM oc_bundleinfo;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_bundleinfo.csv', 'SELECT * FROM "public"."oc_bundleinfo_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_bundleinfo_temp";
-------------------------------------------------------------------------------
--TO MOVE DATA FROM oc_assets_version_claim TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_assets_version_claim_temp"(
    "mediapackage_id" VARCHAR(128) NOT NULL,
    "last_claimed" BIGINT NOT NULL
);  
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_assets_version_claim_temp" (mediapackage_id, last_claimed)
SELECT mediapackage_id, last_claimed
FROM oc_assets_version_claim;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_assets_version_claim.csv', 'SELECT * FROM "public"."oc_assets_version_claim_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_assets_version_claim_temp";
-------------------------------------------------------------------------------
--TO MOVE DATA FROM oc_assets_properties TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_assets_properties_temp"(
    "id" BIGINT NOT NULL,
    "val_bool" INTEGER,
    "val_date" TIMESTAMP,
    "val_long" BIGINT,
    "val_string" VARCHAR,
    "mediapackage_id" VARCHAR(128) NOT NULL,
    "namespace" VARCHAR(128) NOT NULL,
    "property_name" VARCHAR(128) NOT NULL
);   
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_assets_properties_temp" (id, val_bool, val_date, val_long, val_string, mediapackage_id, namespace, property_name)
SELECT id, val_bool, val_date, val_long, val_string, mediapackage_id, namespace, property_name
FROM oc_assets_properties;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_assets_properties.csv', 'SELECT * FROM "public"."oc_assets_properties_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_assets_properties_temp";

-------------------------------------------------------------------------------
--TO MOVE DATA FROM oc_assets_snapshot TABLE --> Must be runned before oc_assets_asset

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_assets_snapshot_temp"(
    "id" BIGINT NOT NULL,
    "archival_date" TIMESTAMP NOT NULL,
    "availability" VARCHAR NOT NULL,
    "mediapackage_id" VARCHAR(128) NOT NULL,
    "mediapackage_xml" LONGVARCHAR NOT NULL,
    "series_id" VARCHAR(128),
    "organization_id" VARCHAR(128) NOT NULL,
    "owner" VARCHAR NOT NULL,
    "version" BIGINT NOT null,
    "storage_id" VARCHAR NOT NULL
);
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_assets_snapshot_temp" (id, archival_date, availability, mediapackage_id, mediapackage_xml, series_id, organization_id, owner, version, storage_id)
SELECT id, archival_date, availability, mediapackage_id, mediapackage_xml, series_id, organization_id, owner, version, storage_id
FROM oc_assets_snapshot;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_assets_snapshot.csv', 'SELECT * FROM "public"."oc_assets_snapshot_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_assets_snapshot_temp";

-------------------------------------------------------------------------------
--TO MOVE DATA FROM oc_assets_asset TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_assets_asset_temp"(
    "id" BIGINT NOT NULL,
    "snapshot_id" BIGINT NOT null,    
    "checksum" VARCHAR(64) NOT NULL,
    "mediapackage_element_id" VARCHAR(128) NOT NULL,
    "mime_type" VARCHAR(64),
    "size" BIGINT NOT NULL,
    "storage_id" VARCHAR NOT NULL
);  
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_assets_asset_temp" (id, snapshot_id, checksum, mediapackage_element_id, mime_type, size, storage_id)
SELECT id, snapshot_id, checksum, mediapackage_element_id, mime_type, size, storage_id
FROM oc_assets_asset;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_assets_asset.csv', 'SELECT * FROM "public"."oc_assets_asset_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_assets_asset_temp";

-------------------------------------------------------------------------------
--TO MOVE DATA FROM oc_acl_managed_acl_temp TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_acl_managed_acl_temp"(
    "pk" BIGINT NOT NULL,
    "acl" LONGVARCHAR NOT NULL,
    "name" VARCHAR NOT NULL,
    "organization_id" VARCHAR NOT NULL
);
--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_acl_managed_acl_temp" (pk, acl, name, organization_id)
SELECT pk, acl, name, organization_id
FROM oc_acl_managed_acl;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_acl_managed_acl.csv', 'SELECT * FROM "public"."oc_acl_managed_acl_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_acl_managed_acl_temp";

-------------------------------------------------------------------------------

--TO MOVE DATA FROM oc_host_registration TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_host_registration_temp"(
    "id" BIGINT NOT NULL,
    "host" VARCHAR(255) NOT NULL,
    "node_name" VARCHAR(255),
    "address" VARCHAR(39) NOT NULL,
    "memory" BIGINT NOT NULL,
    "cores" INTEGER NOT NULL,
    "maintenance" INTEGER NOT NULL,
    "online" INTEGER NOT NULL, 
    "active" INTEGER NOT NULL,  
    "max_load" DOUBLE NOT NULL   
);    

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_host_registration_temp" (id, host, node_name, address, memory, cores, maintenance, online, active, max_load)
SELECT id, host, node_name, address, memory, cores, maintenance, online, active, max_load
FROM oc_host_registration;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_host_registration.csv', 'SELECT * FROM "public"."oc_host_registration_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_host_registration_temp";

-------------------------------------------------------------------------------
--TO MOVE DATA FROM OC_SERVICE_REGISTRATION TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_service_registration_temp"(
    "id" BIGINT NOT NULL,
    "path" LONGVARCHAR NOT NULL,
    "job_producer" INTEGER NOT NULL,
    "service_type" VARCHAR(255) NOT NULL,
    "online" INTEGER NOT NULL,    
    "active" INTEGER NOT NULL,
    "online_from" TIMESTAMP,
    "service_state" INTEGER,
    "state_changed" TIMESTAMP,
    "warning_state_trigger" INTEGER,
    "error_state_trigger" INTEGER,  
    "host_registration" BIGINT
);

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_service_registration_temp" (id, path, job_producer, service_type, online, active, online_from, service_state, state_changed, warning_state_trigger, error_state_trigger, host_registration)
SELECT id, path, job_producer, service_type, online, active, online_from, service_state, state_changed, warning_state_trigger, error_state_trigger, host_registration
FROM oc_service_registration;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_service_registration.csv', 'SELECT * FROM "public"."oc_service_registration_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_service_registration_temp";

-------------------------------------------------------------------------------
--TO MOVE DATA FROM OC_ORGANIZATION TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_organization_temp"(
    "id" VARCHAR(128) NOT NULL,
    "anonymous_role" VARCHAR,
    "name" VARCHAR,
    "admin_role" VARCHAR   
);  

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_organization_temp" (id, anonymous_role, name, admin_role)
SELECT id, anonymous_role, name, admin_role
FROM oc_organization;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_organization.csv', 'SELECT * FROM "public"."oc_organization_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_organization_temp";

-------------------------------------------------------------------------------

--TO MOVE DATA FROM OC_JOB TABLE

--But first we need to reorginize columns to match mariaDB database, for that we create a temp table
CREATE CACHED TABLE "public"."oc_job_temp"(
    "id" BIGINT NOT NULL,
    "status" INTEGER,
    "payload" LONGVARCHAR,
    "date_started" TIMESTAMP,
	"run_time" BIGINT,    
    "creator" LONGVARCHAR NOT NULL,
    "instance_version" BIGINT,    
    "date_completed" TIMESTAMP,
    "operation" LONGVARCHAR,
    "dispatchable" INTEGER,
    "organization" LONGVARCHAR NOT NULL,    
    "date_created" TIMESTAMP,
    "queue_time" BIGINT,
    "creator_service" BIGINT,
    "processor_service" BIGINT,
    "parent" BIGINT,
    "root" BIGINT,
    "job_load" DOUBLE
); 

--Then we move the instances from our H2 relation to the recently created cache relation
INSERT INTO "public"."oc_job_temp" (id, status, payload, date_started,run_time,creator,instance_version,date_completed, operation, dispatchable, organization, date_created, queue_time, creator_service, processor_service, parent, root, job_load)
SELECT id, status, payload, date_started,run_time,creator,instance_version,date_completed, operation, dispatchable, organization, date_created, queue_time, creator_service, processor_service, parent, root, job_load
FROM oc_job;


--Now we move the instances to a CSV file that we will use later on
CALL CSVWRITE('oc_job.csv', 'SELECT * FROM "public"."oc_job_temp"', 'charset=UTF-8  null=NULL');

--if the temp table exists, lets delete it
drop table "public"."oc_job_temp";
