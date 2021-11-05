
data "aws_ssm_parameter" "db_password" {
  name = "/ama-hoi/postgres-password"
}

resource "aws_rds_cluster" "rds_cluster" {
  cluster_identifier           = "ama-hoi-db"
  database_name                = "ama-hoi"
  master_username              = "postgres"
  master_password              = data.aws_ssm_parameter.db_password.value
  final_snapshot_identifier    = "ama-hoi-db-snapshot"
  preferred_backup_window      = "01:00-03:00"
  preferred_maintenance_window = "sun:04:00-sun:07:00"
  vpc_security_group_ids       = [module.security_group.security_group_id]
  db_subnet_group_name         = module.vpc.database_subnet_group_name
  engine_mode                  = "serverless"
  engine                       = "aurora-postgresql"
  scaling_configuration {
    min_capacity = 1
  }
}

resource "aws_ssm_parameter" "rds_endpoint" {
  name  = "/ama-hoi/rds-endpoint"
  type  = "String"
  value = aws_rds_cluster.rds_cluster.endpoint
}
