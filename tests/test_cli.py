import json
from pathlib import Path

from click.testing import CliRunner
from pipdownload.cli import pipdownload
from pipdownload.settings import SETTINGS_FILE


def test_download_click_package(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["click==7.0", "-d", str(tmp_path)])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


# 这里的多余表示的是 requirement 文件包含了多余的换行符
# "redundant" means there are redundant blank lines in requirement file.
def test_download_from_requirement_file_redundant(
    requirement_file_redundant, tmp_path: Path
):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["-r", requirement_file_redundant, "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


def test_download_from_requirement_file_normal(requirement_file_normal, tmp_path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["-r", requirement_file_normal, "-d", tmp_path])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


def test_download_with_option_whl_suffixes(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["MarkupSafe==1.1.1", "--suffix", "win_amd64", "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    # TODO: This should be consider again!
    assert len(files) == 7


def test_download_with_option_python_versions(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["MarkupSafe==1.1.1", "-py", "cp27", "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 4


def test_download_when_dest_dir_does_not_exists(tmp_path: Path):
    runner = CliRunner()
    dir_name = "tmp"
    result = runner.invoke(pipdownload, ["click", "-d", str(tmp_path / dir_name)])
    assert result.exit_code == 0
    dirs = list(tmp_path.iterdir())
    assert len(dirs) == 1
    files = list((tmp_path / dir_name).iterdir())
    assert len(files) == 2


def test_option_platform_tag(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["MarkupSafe==1.1.1", "-p", "win_amd64", "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    # TODO: This should be consider again!
    assert len(files) == 7


def test_option_on_source(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["click==7.0", "--no-source", "-d", str(tmp_path)]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 1


def test_packege_with_egg_file(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["protobuf", "-d", str(tmp_path), "-py", "cp37"]
    )
    assert result.exit_code == 0
    # files = list(tmp_path.iterdir())
    # assert len(files) == 1


def test_download_with_config_file(tmp_path: Path):
    settings_dict = {
        "python-versions": ["cp37"],
        "platform-tags": ["win_amd64"]
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings_dict, f, indent=True)

    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["MarkupSafe==1.1.1", "-d", str(tmp_path)]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2
