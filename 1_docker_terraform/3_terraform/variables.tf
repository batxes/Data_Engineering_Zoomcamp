variable "credentials" {
    description = "My Credentials"
    default = "./keys/terraform_creds.json"
}

variable "project" {
  description = "Project"
  default     = "sylvan-cirrus-448510-s0"
}

variable "region" {
  description = "Region"
  default     = "europe-west3"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "sylvan-cirrus-448510-s0-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

