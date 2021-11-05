resource "aws_dynamodb_table" "office_data" {
  name           = "office-data"
  hash_key       = "id"
  range_key      = "type"
  read_capacity  = 5
  write_capacity = 5

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "type"
    type = "S"
  }

  global_secondary_index {
    name            = "IdByTypeIndex"
    hash_key        = "type"
    range_key       = "id"
    write_capacity  = 5
    read_capacity   = 5
    projection_type = "ALL"
  }


  tags = {
    owner = "ama-hoi"
  }
}
