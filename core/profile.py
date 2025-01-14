from loguru import logger

from utils.enum_constants import Colors


class Profile:
    def __init__(self,
                 profile_number: str,
                 profile_id: str,
                 wallet_pass: str,
                 pk: str,
                 evm_address: str,
                 sol_address: str,
                 email_address: str,
                 email_pass: str,
                 proxy: str):
        self.profile_number = profile_number
        self.profile_id = profile_id
        self.wallet_pass = wallet_pass
        self.pk = pk
        self.evm_address = evm_address
        self.sol_address = sol_address
        self.email_address = email_address
        self.email_pass = email_pass
        self.proxy = proxy
        self.task_results = {}


    def __str__(self) -> str:
        return f"PROFILE {self.profile_number} ({self.profile_id}):\n{self.task_results}\n"

    def set_task_result(self, project, task, result):
        if project not in self.task_results:
            self.task_results[project] = {}

        self.task_results[project][task] = result

    def get_task_result(self, task):
        project, task_name = task.split(maxsplit=1)

        return self.task_results.get(project, {}).get(task_name, None)

    def print_task_results(self, all_tasks: list[str]):
        bold = "\033[1m"
        final_msg = f"\n{Colors.BACKGROUND_WHITE}{Colors.BLACK}{bold} PROFILE {self.profile_number} ({self.profile_id}) {Colors.RESET}\n"

        if not self.task_results:
            return

        max_task_name_length = max((len(task.split()[1]) for task in all_tasks), default=0)

        for project, tasks in self.task_results.items():
            final_msg += f"  {bold}{Colors.BLUE}{project}{Colors.RESET}\n"
            for task_name, result in tasks.items():
                full_task_name = f"{project} {task_name}"
                if full_task_name in all_tasks:
                    status = f"{Colors.GREEN}SUCCESS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
                    final_msg += f"    {Colors.YELLOW}{bold}{task_name.ljust(max_task_name_length)}: {status}\n"

        logger.opt(raw=True).info(final_msg)
