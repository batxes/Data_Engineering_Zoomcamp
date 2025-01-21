terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.16.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = "./keys/terraform_creds.json"
  project     = "sylvan-cirrus-448510-s0"
  region      = "europe-west3"
}


