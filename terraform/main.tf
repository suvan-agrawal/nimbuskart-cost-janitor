module "network" {
  source = "./modules/network"

  vpc_cidr             = "10.20.0.0/16"
  public_subnet_1_cidr = "10.20.1.0/24"
  public_subnet_2_cidr = "10.20.2.0/24"

  environment = var.environment
  project     = var.project
  owner       = var.owner
}
resource "aws_security_group" "web_sg" {
  name        = "${var.project}-${var.environment}-web-sg"
  description = "Security group for web tier"
  vpc_id      = module.network.vpc_id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project}-${var.environment}-web-sg"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "web_1" {
  ami                    = "ami-test"
  instance_type          = "t3.micro"
  subnet_id              = module.network.public_subnet_1_id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "${var.project}-web-1"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
    Tier        = "web"
  }
}

resource "aws_instance" "web_2" {
  ami                    = "ami-test"
  instance_type          = "t3.micro"
  subnet_id              = module.network.public_subnet_2_id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "${var.project}-web-2"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
    Tier        = "web"
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = "${lower(var.project)}-${var.environment}-logs"

  tags = {
    Name        = "${var.project}-${var.environment}-logs"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}
resource "aws_s3_bucket_versioning" "logs_versioning" {
  bucket = aws_s3_bucket.logs.id

  versioning_configuration {
    status = "Enabled"
  }
}
# NOTE:
# LocalStack has inconsistent support for S3 lifecycle configuration APIs.
# The lifecycle configuration is intentionally commented for local execution stability.
# This configuration works against real AWS environments with the standard AWS provider.
#resource "aws_s3_bucket_lifecycle_configuration" "logs_lifecycle" {
#  bucket = aws_s3_bucket.logs.id
#
#  rule {
#    id     = "expire-old-versions"
#    status = "Enabled"
#
#    filter {}
#
#    noncurrent_version_expiration {
#      noncurrent_days = 30
#    }
#  }
#}

resource "aws_ebs_volume" "orphan_volume" {
  availability_zone = "us-east-1a"
  size              = 8

  tags = {
    Name        = "${var.project}-orphan-volume"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}