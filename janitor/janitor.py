import argparse
import boto3
import json
import sys
from datetime import datetime, timezone, timedelta

from constants import (
    EBS_GP3_PRICE_PER_GB,
    REQUIRED_TAGS
)

AWS_REGION = "us-east-1"

ec2 = boto3.client(
    "ec2",
    region_name=AWS_REGION,
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)


findings = []


def get_tag_dict(tags):
    if not tags:
        return {}

    return {tag["Key"]: tag["Value"] for tag in tags}


def check_missing_tags(resource_id, resource_type, tags):
    tag_dict = get_tag_dict(tags)

    missing = [
        tag for tag in REQUIRED_TAGS
        if tag not in tag_dict
    ]

    if missing:
        findings.append({
            "resource_id": resource_id,
            "resource_type": resource_type,
            "reason": f"missing_tags: {', '.join(missing)}",
            "age_days": 0,
            "estimated_monthly_cost_usd": 0,
            "tags": tag_dict,
            "suggested_action": "tag_resource",
            "safe_to_auto_delete": False
        })


def scan_ebs_volumes(delete_mode=False):
    response = ec2.describe_volumes()

    for volume in response["Volumes"]:
        tags = volume.get("Tags", [])

        check_missing_tags(
            volume["VolumeId"],
            "ebs_volume",
            tags
        )

        if volume["State"] == "available":

            size = volume["Size"]

            findings.append({
                "resource_id": volume["VolumeId"],
                "resource_type": "ebs_volume",
                "reason": "unattached",
                "age_days": 0,
                "estimated_monthly_cost_usd": round(
                    size * EBS_GP3_PRICE_PER_GB,
                    2
                ),
                "tags": get_tag_dict(tags),
                "suggested_action": "delete",
                "safe_to_auto_delete": True
            })

            tag_dict = get_tag_dict(tags)

            if (
                delete_mode and
                tag_dict.get("Protected") != "true"
            ):
                ec2.delete_volume(
                    VolumeId=volume["VolumeId"]
                )

def scan_stopped_instances(
    max_stopped_days=14,
    delete_mode=False
):
    response = ec2.describe_instances()

    reservations = response["Reservations"]

    for reservation in reservations:
        for instance in reservation["Instances"]:

            tags = instance.get("Tags", [])

            check_missing_tags(
                instance["InstanceId"],
                "ec2_instance",
                tags
            )

            state = instance["State"]["Name"]

            if state == "stopped":

                launch_time = instance.get(
                    "LaunchTime",
                    datetime.now(timezone.utc)
                )

                age_days = (
                    datetime.now(timezone.utc)
                    - launch_time
                ).days

                if age_days >= max_stopped_days:

                    findings.append({
                        "resource_id": instance["InstanceId"],
                        "resource_type": "ec2_instance",
                        "reason": "stopped_instance",
                        "age_days": age_days,
                        "estimated_monthly_cost_usd": 15,
                        "tags": get_tag_dict(tags),
                        "suggested_action": "terminate",
                        "safe_to_auto_delete": False
                    })

                    tag_dict = get_tag_dict(tags)

                    if (
                        delete_mode and
                        tag_dict.get("Protected") != "true"
                    ):
                        ec2.terminate_instances(
                            InstanceIds=[
                                instance["InstanceId"]
                            ]
                        )

def scan_unused_eips(delete_mode=False):
    response = ec2.describe_addresses()

    for address in response["Addresses"]:

        allocation_id = address.get(
            "AllocationId",
            "unknown"
        )

        association_id = address.get(
            "AssociationId"
        )

        tags = address.get("Tags", [])

        check_missing_tags(
            allocation_id,
            "elastic_ip",
            tags
        )

        if not association_id:

            findings.append({
                "resource_id": allocation_id,
                "resource_type": "elastic_ip",
                "reason": "unassociated_eip",
                "age_days": 0,
                "estimated_monthly_cost_usd": 3.5,
                "tags": get_tag_dict(tags),
                "suggested_action": "release",
                "safe_to_auto_delete": True
            })

            tag_dict = get_tag_dict(tags)

            if (
                delete_mode and
                tag_dict.get("Protected") != "true"
            ):
                ec2.release_address(
                    AllocationId=allocation_id
                )

def generate_report():
    total_waste = sum(
        item["estimated_monthly_cost_usd"]
        for item in findings
    )

    report = {
        "scan_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "account_id": "000000000000",
        "region": AWS_REGION,
        "summary": {
            "total_orphans": len(findings),
            "estimated_monthly_waste_usd": round(
                total_waste,
                2
            )
        },
        "findings": findings
    }

    with open("report.json", "w") as file:
        json.dump(report, file, indent=2)

    return report


def generate_markdown(report):
    lines = [
        "# Cost Janitor Report",
        "",
        f"Total Findings: {report['summary']['total_orphans']}",
        f"Estimated Monthly Waste: ${report['summary']['estimated_monthly_waste_usd']}",
        ""
    ]

    for finding in report["findings"]:
        lines.extend([
            f"## {finding['resource_id']}",
            f"- Type: {finding['resource_type']}",
            f"- Reason: {finding['reason']}",
            f"- Suggested Action: {finding['suggested_action']}",
            ""
        ])

    with open("report.md", "w") as file:
        file.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--delete",
        action="store_true"
    )

    parser.add_argument(
    "--max-stopped-days",
    type=int,
    default=14
)
    
    args = parser.parse_args()

    scan_ebs_volumes(
        delete_mode=args.delete
    )

    scan_stopped_instances(
        max_stopped_days=args.max_stopped_days,
        delete_mode=args.delete
    )

    scan_unused_eips(
        delete_mode=args.delete
    )

    report = generate_report()

    generate_markdown(report)

    if findings and not args.delete:
        sys.exit(1)


if __name__ == "__main__":
    main()