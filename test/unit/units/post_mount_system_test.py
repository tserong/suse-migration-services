from unittest.mock import (
    patch, call
)

from suse_migration_services.units.post_mount_system import main
from suse_migration_services.defaults import Defaults


class TestPostMountSystem(object):
    @patch.object(Defaults, 'get_migration_config_file')
    @patch('suse_migration_services.logger.log.info')
    @patch('suse_migration_services.command.Command.run')
    @patch('suse_migration_services.defaults.Defaults.get_system_root_path')
    @patch('shutil.copy')
    def test_main(
        self, mock_shutil_copy, mock_get_system_root_path,
        mock_Command_run, mock_log_info, mock_get_migration_config_file
    ):
        mock_get_system_root_path.return_value = '../data'
        mock_get_migration_config_file.return_value = \
            '../data/migration-config.yml'
        main()
        assert mock_shutil_copy.call_args_list == [
            call('../data/etc/udev/rules.d/a.rules', '/etc/udev/rules.d'),
            call('../data/etc/udev/rules.d/b.rules', '/etc/udev/rules.d')
        ]
        assert mock_Command_run.call_args_list == [
            call(['udevadm', 'control', '--reload']),
            call(['udevadm', 'trigger', '--type=subsystems', '--action=add']),
            call(['udevadm', 'trigger', '--type=devices', '--action=add'])
        ]
