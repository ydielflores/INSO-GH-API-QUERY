import csv
import json
from datetime import datetime
from generateTeamMetrics import getTeamMetricsForMilestone
from getTeamMembers import get_team_members

from utils.models import MilestoneData


def write_milestone_data_to_csv(milestone_data: MilestoneData, csv_file_path: str):
    with open(csv_file_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Developer", "Points Closed", "Percent Contribution"])
        writer.writerow(["Total", milestone_data.totalPointsClosed, "100"])
        for developer, metrics in milestone_data.devMetrics.items():
            writer.writerow(
                [developer, metrics.pointsClosed, metrics.percentContribution]
            )


if __name__ == "__main__":
    import sys
    # if len(sys.argv) < 2:
    #     exit(0)
    # _, course_config_file, *_ = sys.argv
    # idk why this isn't working, so hardcode for now. Kinda had to anyway cuz managers are hard coded rn
    # teams = get_teams(org)
    with open("./data/courseConfig.json") as course_config:
        course_data = json.load(course_config)
    organization = course_data['data'][0]['organization']
    milestone = course_data['data'][0]['milestones'][0]['name']
    teams_and_managers = course_data['data'][0]['milestones'][0]['teams']
    startDate = datetime.fromisoformat(course_data['data'][0]['milestones'][0]['startDate'])
    endDate = datetime.fromisoformat(course_data['data'][0]['milestones'][0]['endDate'])
    print("Organization: ", organization)
    print("Milestone: ", milestone)

    team_metrics = {}
    for team, managers in teams_and_managers.items():
        print("Team: ", team)
        print("Managers: ", managers)
        members = get_team_members(organization, team)
        team_metrics[team] = getTeamMetricsForMilestone(
            org=organization,
            team=team,
            milestone=milestone,
            members=members,
            managers=managers,
            startDate=startDate,
            endDate=endDate,
        )
    for team, metrics in team_metrics.items():
        write_milestone_data_to_csv(metrics,
                                    f"{milestone}-{team}-{organization}.csv")
