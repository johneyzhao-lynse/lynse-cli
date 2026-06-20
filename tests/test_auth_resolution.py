"""Credential resolution tests.

Pins the API key/host precedence so a stale install ``.env`` can never silently
override the key a user saved via ``auth login`` into ``~/.lynse/config.json``.

Precedence (highest → lowest):
    explicit param  >  shell env var  >  user config (~/.lynse/config.json)  >  install .env
"""

import os
import tempfile
import unittest
from unittest import mock

from lynse import LynseAPI


_ENV_KEYS = (
    "LYNSE_API_KEY",
    "LYNSE_API_HOST",
    "LYNSE_OWNER_ID",
    "LYNSE_ACCESS_TOKEN",
)


class CredentialResolutionTests(unittest.TestCase):
    def setUp(self):
        # Snapshot and clear env so each test controls its own inputs. The
        # resolver loads the install .env into os.environ, so we must isolate.
        self._saved = {k: os.environ.get(k) for k in _ENV_KEYS}
        for k in _ENV_KEYS:
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)

    def _env_file(self, key, host="https://api.example.com"):
        f = tempfile.NamedTemporaryFile("w", suffix=".env", delete=False)
        f.write(f"LYNSE_API_KEY={key}\nLYNSE_API_HOST={host}\n")
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    @mock.patch("lynse._load_user_config")
    def test_user_config_key_wins_over_stale_env_file(self, m_ucfg):
        """The bug: stale install .env used to override the valid auth-login key."""
        m_ucfg.return_value = {
            "api_key": "dk_VALID_user_key_9999",
            "api_host": "https://api.example.com",
        }
        env_path = self._env_file("dk_STALE_install_key_0000")

        api = LynseAPI(config_file=env_path)

        self.assertEqual(api.api_key, "dk_VALID_user_key_9999")
        self.assertEqual(api.api_host, "https://api.example.com")

    @mock.patch("lynse._load_user_config")
    def test_explicit_param_wins_over_everything(self, m_ucfg):
        m_ucfg.return_value = {"api_key": "dk_VALID_user_key_9999"}
        env_path = self._env_file("dk_STALE_install_key_0000")

        api = LynseAPI(
            api_key="dk_PARAM_key_1234",
            api_host="https://api.example.com",
            config_file=env_path,
        )

        self.assertEqual(api.api_key, "dk_PARAM_key_1234")

    @mock.patch("lynse._load_user_config")
    def test_shell_env_wins_over_user_config_and_env_file(self, m_ucfg):
        """An explicit shell export is an intentional override and must win."""
        m_ucfg.return_value = {"api_key": "dk_VALID_user_key_9999"}
        env_path = self._env_file("dk_STALE_install_key_0000")
        os.environ["LYNSE_API_KEY"] = "dk_SHELL_key_5555"
        os.environ["LYNSE_API_HOST"] = "https://api.example.com"

        api = LynseAPI(config_file=env_path)

        self.assertEqual(api.api_key, "dk_SHELL_key_5555")

    @mock.patch("lynse._load_user_config")
    def test_install_env_used_when_no_user_config(self, m_ucfg):
        """Backward compat: install .env is still the default fallback."""
        m_ucfg.return_value = {}
        env_path = self._env_file("dk_ONLY_env_key_7777")

        api = LynseAPI(config_file=env_path)

        self.assertEqual(api.api_key, "dk_ONLY_env_key_7777")

    @mock.patch("lynse._load_user_config")
    def test_resolver_reports_config_source(self, m_ucfg):
        from lynse import _resolve_api_credentials  # added by the fix

        m_ucfg.return_value = {"api_key": "dk_VALID_user_key_9999"}
        env_path = self._env_file("dk_STALE_install_key_0000")

        _, key, source = _resolve_api_credentials(install_env_path=env_path)

        self.assertEqual(key, "dk_VALID_user_key_9999")
        self.assertEqual(source, "config")


if __name__ == "__main__":
    unittest.main()
