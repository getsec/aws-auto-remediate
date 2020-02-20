# aws-auto-remediate

This repo is used to deploy automatic remediations (controls) in your AWS account.

Hopefully we can make our environments a safer place, and stay out of the tabloids

[All Blog Posts](https://getsec.github.io)

## Whats Included

#### EC2 Security Groups
Automatically checks when the following API call is used, and replaces the bad SG with what we include in the whitelist


#### Public S3 Buckets
When a user creates a bucket, either through an ACL or bucket policy. This lambda will either update the principal to ONLY your account, or if its a ACL, it will remove any public ACLs

#### EC2 Tagging
This lambda will look for any instance events. If its RunInstance we will tag the instance with whoever created it. If its Reboot/Stop/Start instance, it will add a tag that informs you of who last changed the instance :)

