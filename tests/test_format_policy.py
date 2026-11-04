import unittest
from integration.format_policy import choices_from_extractor

class FormatPolicyTests(unittest.TestCase):
    def test_only_real_formats(self):
        r = choices_from_extractor({"formats": [{"format_id":"18","url":"https://cdn.test/a","height":360},{"format_id":"22","url":"https://cdn.test/b","height":720}]})
        self.assertEqual(r.state, "formats")
        self.assertEqual({x.height for x in r.choices}, {360, 720})
    def test_no_invented_quality(self):
        self.assertEqual(choices_from_extractor({"formats":[]}).state, "unavailable")
    def test_single_format(self):
        r = choices_from_extractor({"formats":[{"format_id":"x","url":"https://cdn.test/x","height":480}]})
        self.assertEqual(len(r.choices), 1)
    def test_generic_direct_url(self):
        self.assertEqual(choices_from_extractor({"url":"https://cdn.test/a"}).state, "generic")
    def test_no_url_unavailable(self):
        self.assertEqual(choices_from_extractor({"formats":[]}).state, "unavailable")
    def test_drm_blocked(self):
        self.assertEqual(choices_from_extractor({"has_drm":True,"url":"https://cdn.test/x"}).state, "unavailable")
    def test_deduplicate(self):
        r = choices_from_extractor({"formats":[{"format_id":"a","url":"https://cdn.test/1"},{"format_id":"a","url":"https://cdn.test/2"}]})
        self.assertEqual(len(r.choices), 1)

if __name__ == "__main__":
    unittest.main()
