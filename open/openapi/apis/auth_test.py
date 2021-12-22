import pytest
from openapi import constants
from openapi import utils


class TestAuth:

    """Test cases for authorization in open-apis
    """
    @pytest.fixture(
        scope="function",
        params=utils.gen_invalid_pairs()
    )
    def get_invalid_pair(self, request):
        yield request.param

    def test_auth_with_invalid_pair(self, hc, get_invalid_pair):
        """Checking auth status if using the invalid format pair key.
        Expected: auth failed.
        """
        pair = get_invalid_pair
        with pytest.raises(Exception) as e: 
            hc._get_token(pair[0], pair[1])

    def test_auth_valid_one(self):
        """Checking auth status if using the only enabled pair key.
        Expected: auth success.
        """
        pass

    def test_auth_valid_two_pairs(self):
        """Checking auth status if using the parts of the enabled pair key.
        Expected: auth success.
        """
        pass

    def test_auth_invalid_status(self):
        """Checking auth status if using the disabled pair key.
        Expected: auth failed.
        """
        pass

    def test_auth_update_to_invalid_status(self):
        """Checking auth status if the pair key turned to invalid.
        Expected: auth failed.
        """
        pass

    def test_auth_update_to_valid_status(self):
        """Checking auth status if the pair key turned to valid.
        Expected: auth success.
        """
        pass

    def test_auth_delete_valid_pair(self):
        """Checking auth status if the pair key was deleted.
        Expected: auth failed.
        """
        pass


class TestAuthAdvanced:
    def test_auth_multi_threading(self):
        """Checking auth status if testing with multi-keys.
        Expected: All keys auth pass.
        """
        pass