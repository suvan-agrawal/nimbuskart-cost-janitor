output "vpc_id" {
  value = module.network.vpc_id
}

output "public_subnet_ids" {
  value = [
    module.network.public_subnet_1_id,
    module.network.public_subnet_2_id
  ]
}

output "s3_bucket_name" {
  value = aws_s3_bucket.logs.bucket
}