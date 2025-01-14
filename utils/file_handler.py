import csv
import os

from core.profile import Profile
from utils.enum_constants import Placeholder


class FileHandler:
    @staticmethod
    def get_project_csv_path(project: str):
        filepath = os.path.join('projects', f'{project.lower()}', 'project_data', 'tasks_data.csv')
        return filepath

    @staticmethod
    def get_profile_ids(csv_filepath):
        profile_ids = []
        with open(csv_filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                profile_ids.append(row['PROFILE_ID'])
        return profile_ids

    @staticmethod
    def load_profiles_from_csv(csv_filepath) -> list[Profile]:
        profiles = []

        with open(csv_filepath, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)

            for row in csvreader:
                profile = Profile(
                    profile_number=row['PROFILE_NUMBER'],
                    profile_id=row['PROFILE_ID'],
                    wallet_pass=row['WALLET_PASS'],
                    pk=row['EVM_PK'],
                    evm_address=row['EVM_ADDRESS'],
                    sol_address=row['SOL_ADDRESS'],
                    email_address=row['EMAIL_ADDRESS'] if ['EMAIL_ADDRESS'] != Placeholder.email else None,
                    email_pass=row['EMAIL_PASS'],
                    proxy=row['PROXY'] if row['PROXY'] != Placeholder.proxy else None
                )
                profiles.append(profile)

        return profiles

    @staticmethod
    def load_task_results_from_csv(profile, csv_filepath, project, all_tasks: list[str]):
        with open(csv_filepath, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)

            for row in csvreader:
                if row['PROFILE_ID'] == profile.profile_id:
                    if project not in profile.task_results:
                        profile.task_results[project] = {}

                    for key, value in row.items():
                        if key == 'PROFILE_ID':
                            continue  # Skip the PROFILE_ID column

                        if f"{project} {key}" in all_tasks:
                            profile.task_results[project][key] = value == 'True'
                    break

