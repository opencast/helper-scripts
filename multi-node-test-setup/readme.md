Build and Setup Local Multi Node Cluster
========================================

This script build Opencast, extracts the admin, presentation and worker
distribution and configures all three to run on the same machine on different
ports as a local distributed setup for testing.

The setup requires ActiveMQ and a PostgreSQL database as provided by:

    docs/scripts/devel-dependency-containers/docker-compose-postgresql.yml
