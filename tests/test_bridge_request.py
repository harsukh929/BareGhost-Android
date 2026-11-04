import unittest
from integration.bridge_request import DownloadRequest, validate_request

class BridgeRequestTests(unittest.TestCase):
    def valid(self, **changes):
        values = {"page_url":"https://site.example/watch","media_url":"https://cdn.example/video.mp4"}
        values.update(changes)
        return DownloadRequest(**values)
    def test_accepts_basic_http_request(self):
        validate_request(self.valid())
    def test_rejects_non_http_urls(self):
        for field, value in (("page_url","file:///tmp/page"),("media_url","ftp://cdn.example/video")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_request(self.valid(**{field:value}))
    def test_rejects_missing_host(self):
        with self.assertRaises(ValueError):
            validate_request(self.valid(media_url="https:///missing-host"))
    def test_cookie_requires_permission(self):
        with self.assertRaises(ValueError):
            validate_request(self.valid(headers={"Cookie":"session=abc"}))
        validate_request(self.valid(headers={"Cookie":"session=abc"},allow_session_cookies=True))
    def test_incognito_never_forwards_cookies(self):
        with self.assertRaises(ValueError):
            validate_request(self.valid(is_incognito=True,allow_session_cookies=True))
    def test_rejects_header_injection(self):
        for headers in ({"X-Test":"ok\r\nInjected: yes"},{"Bad\nName":"value"}):
            with self.subTest(headers=headers), self.assertRaises(ValueError):
                validate_request(self.valid(headers=headers))
    def test_rejects_excessive_headers(self):
        with self.assertRaises(ValueError):
            validate_request(self.valid(headers={f"X-Test-{i}":"v" for i in range(65)}))
    def test_rejects_long_format_id(self):
        with self.assertRaises(ValueError):
            validate_request(self.valid(format_id="x"*129))

if __name__ == "__main__":
    unittest.main()
