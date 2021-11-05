
resource "aws_iam_policy" "oma-hoi-policy" {
  name        = "oma-hoi-policy"
  description = "Policy for oma-hoi"
  policy      = data.aws_iam_policy_document.oma-hoi-policy.json
}


data "aws_iam_policy_document" "oma-hoi-policy" {
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:DeleteItem",
    ]

    resources = [
      aws_dynamodb_table.office_data.arn,
      "${aws_dynamodb_table.office_data.arn}/index/*",
    ]
  }
}