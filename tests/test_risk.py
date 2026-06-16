from commandgraph.risk import check_command


def test_chmod_777_warns_high():
    review = check_command("chmod -R 777 .")
    assert review.decision == "warn"
    assert review.risk == "high"
    assert review.as_dict()["schema_version"] == "commandgraph.risk_review.v1"
    assert "chmod_recursive" in review.as_dict()["matched_rules"]


def test_root_delete_blocks():
    review = check_command("rm -rf /")
    assert review.decision == "block"
    assert review.risk == "critical"
    assert "root_filesystem_mutation" in review.as_dict()["risk_categories"]


def test_root_glob_delete_blocks():
    review = check_command("rm -rf /*")
    assert review.decision == "block"
    assert review.risk == "critical"


def test_readonly_command_allows():
    review = check_command("lsof -i :3000")
    assert review.decision == "allow"
    assert review.risk == "low"


def test_secret_file_warns():
    review = check_command("cat .env")
    assert review.decision == "warn"
    assert review.risk == "medium"
    assert "secret_exposure" in review.as_dict()["risk_categories"]


def test_empty_command_blocks():
    review = check_command("")
    assert review.decision == "block"
    assert review.risk == "critical"


def test_package_install_warns():
    review = check_command("python -m pip install requests")
    assert review.decision == "warn"
    assert "package_install" in review.as_dict()["risk_categories"]


def test_docker_prune_warns_high():
    review = check_command("docker system prune -a")
    assert review.decision == "warn"
    assert review.risk == "high"
