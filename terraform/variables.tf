variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "ap-south-1"
}

variable "key_name" {
  description = "AWS key pair name"
  default     = "bhavesh-key"
}

variable "allowed_ssh_cidr" {
  description = "Your IP address for SSH (e.g. 1.2.3.4/32)"
  default     = "123.45.67.89/32" # Replace with your real IP
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.micro"
}

variable "db_instance_class" {
  description = "RDS instance class"
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Database name"
  default     = "devopsdb"
}

variable "db_user" {
  description = "Database username"
  default     = "admin"
}

variable "db_password" {
  description = "Database password"
  sensitive   = true
}
