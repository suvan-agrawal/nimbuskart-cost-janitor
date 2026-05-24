# Cost Janitor Report

Total Findings: 7
Estimated Monthly Waste: $19.54

## vol-920d6872
- Type: ebs_volume
- Reason: unattached
- Suggested Action: delete

## vol-7ca8b8ec
- Type: ebs_volume
- Reason: missing_tags: Project, Environment, Owner
- Suggested Action: tag_resource

## vol-b2008a94
- Type: ebs_volume
- Reason: missing_tags: Project, Environment, Owner
- Suggested Action: tag_resource

## vol-47e8b69b
- Type: ebs_volume
- Reason: missing_tags: Project, Environment, Owner
- Suggested Action: tag_resource

## vol-47e8b69b
- Type: ebs_volume
- Reason: unattached
- Suggested Action: delete

## i-1f4d351de8811f94d
- Type: ec2_instance
- Reason: stopped_instance
- Suggested Action: terminate

## eipalloc-5654f530
- Type: elastic_ip
- Reason: unassociated_eip
- Suggested Action: release
