import logging
import re
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger()


def get_deleted_branches(branch_stdout: str) -> list[str]:
    deleted_branch_names = []
    eng_deleted_branch_pattern = re.compile(".*: gone].*")
    esp_deleted_branch_pattern = re.compile(".*: desaparecido].*")
    for line in branch_stdout.splitlines():
        logger.debug(f"Processing {line}")
        if eng_deleted_branch_pattern.match(line) or esp_deleted_branch_pattern.match(
            line
        ):
            branch_name = line.strip().split(" ")[0]
            if branch_name != "*":
                deleted_branch_names.append(branch_name)
                logger.debug(f"Branch will be deleted: {branch_name}")

    logger.info(f"Detected to delete: \n {deleted_branch_names}")
    return deleted_branch_names


def delete_old_branches(branches: list[str]):
    for branch in branches:
        delete_cmd = ["git", "branch", "-D", branch]
        delete_run = subprocess.run(delete_cmd, stdout=subprocess.PIPE)
        logger.info(delete_run.stdout.decode("utf-8"))


def main():
    fetch_deleted_branches_command = ["git", "fetch", "--prune"]
    branch_list_verbose = ["git", "branch", "-vv"]
    logger.info("Fetching deleted branches...")
    subprocess.run(fetch_deleted_branches_command, stdout=subprocess.PIPE)
    deleted_branches = subprocess.run(branch_list_verbose, stdout=subprocess.PIPE)
    logger.info(f"Deleted Branches: \n {deleted_branches.stdout.decode('utf-8')}")

    branches = get_deleted_branches(deleted_branches.stdout.decode("utf-8"))

    clean_remote_deleted_branches = ["git", "remote", "prune", "origin"]
    deleted_remote_branches = subprocess.run(
        clean_remote_deleted_branches, stdout=subprocess.PIPE
    )
    logger.info(
        f"Deleted Remote Branches: \n {deleted_remote_branches.stdout.decode('utf-8')}"
    )

    delete_old_branches(branches)


if __name__ == "__main__":
    main()
