provider "aws" {
  region = "us-west-2"  # Update as needed
}

# Create a security group that allows SSH access
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"
  
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Launch configuration for the notification service instances
resource "aws_launch_configuration" "notification_service" {
  name_prefix   = "notification-service-"
  image_id      = "ami-0c55b159cbfafe1f0"  # Replace with a valid AMI ID
  instance_type = "t2.micro"
  
  security_groups = [
    aws_security_group.allow_ssh.id
  ]
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto-scaling group for the notification service
resource "aws_autoscaling_group" "notification_service_group" {
  launch_configuration = aws_launch_configuration.notification_service.id
  desired_capacity     = 2
  max_size             = 3
  min_size             = 1
  
  # Replace with your own subnet ID(s)
  vpc_zone_identifier = ["subnet-0bb1c79de3EXAMPLE"]
  
  tag {
    key                 = "Name"
    value               = "NotificationServiceInstance"
    propagate_at_launch = true
  }
}
