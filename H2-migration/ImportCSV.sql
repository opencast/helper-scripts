#Load oc_series_elements
LOAD DATA INFILE "oc_series_elements.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_series_elements  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_search  
LOAD DATA INFILE "oc_search.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_search  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_scheduled_last_modified  
LOAD DATA INFILE "oc_scheduled_last_modified.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_scheduled_last_modified  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


#---------OC_ORGANIZATION---------------------
#Load oc_organization  --> needed for oc_organization_node, oc_user, oc_series,  oc_organization_property and oc_scheduled_extended_event
LOAD DATA INFILoc_organization.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_organization  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_user_ref  -->needs oc_organization and is needed by oc_user_ref_role
LOAD DATA INFILE "oc_user_ref.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_user_ref  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_user  -->needs oc_organization  and is needed by oc_user_ref_role and oc_user_role
LOAD DATA INFILE "oc_user.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_user  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_role  --> needed for oc_group_role and for oc_user_role
LOAD DATA INFILE "/oc_role.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_role  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_user_role  --> needs oc_role and oc_user
LOAD DATA INFILE "oc_user_role.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_user_role  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;




#Load oc_user_ref_role  -->needs oc_user and oc_user_ref
LOAD DATA INFILE "oc_user_ref_role.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_user_ref_role  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


#Load oc_series  -->needs oc_organization
LOAD DATA INFILE "oc_series.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_series  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_series_property -->needs oc_series
LOAD DATA INFILE "oc_series_property.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_series_property  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_scheduled_extended_event  -->needs oc_organization
LOAD DATA INFILE "oc_scheduled_extended_event.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_scheduled_extended_event  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_organization_property  -->needs oc_organization
LOAD DATA INFILE "oc_organization_property.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_organization_property  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_organization_node  -->needs oc_organization
LOAD DATA INFILE "oc_organization_node.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_organization_node  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_incident_text 
LOAD DATA INFILE "oc_incident_text.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_incident_text  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_service_registration --> Needed for oc_job and oc_job_oc_service_registration
LOAD DATA INFILE "oc_service_registration.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_service_registration  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_job  --> Needs oc_service_registration
LOAD DATA INFILE "oc_job.csv" 
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_job  
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_incident 
LOAD DATA INFILE "oc_incident.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_incident  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;





#Load oc_group_role  --> needs oc_role
LOAD DATA INFILE "oc_group_role.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_group_role  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_group_member 
LOAD DATA INFILE "oc_group_member.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_group_member  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_group 
LOAD DATA INFILE "oc_group.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_group  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_capture_agent_state 
LOAD DATA INFILE "oc_capture_agent_state.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_capture_agent_state  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_capture_agent_role 
LOAD DATA INFILE "oc_capture_agent_role.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_capture_agent_role  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_bundleinfo 
LOAD DATA INFILE "oc_bundleinfo.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_bundleinfo  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_assets_version_claim 
LOAD DATA INFILE "oc_assets_version_claim.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_assets_version_claim  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_assets_properties 
LOAD DATA INFILE "oc_assets_properties.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_assets_properties  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_assets_snapshot --> Run before oc_assets_asset
LOAD DATA INFILE "oc_assets_snapshot.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_assets_snapshot  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_assets_asset --> Run after oc_assets_snapshot
LOAD DATA INFILE "oc_assets_asset.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_assets_asset  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_host_registration
LOAD DATA INFILE "oc_acl_managed_acl.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_acl_managed_acl  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

#Load oc_host_registration
LOAD DATA INFILE "oc_host_registration.csv"  
IGNORE #ignore fields with duplicated unique keys
INTO TABLE oc_host_registration  
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
